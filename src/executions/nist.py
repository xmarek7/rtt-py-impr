import logging
import os
import tempfile

from subprocess import Popen, PIPE
from results.nist import NistResult, NistResultFactory
from tools.misc import nist_test_id_to_param, nist_get_specific_param
from settings.nist import NistSettings
from settings.general import GeneralSettings


class NistExecution:
    def __init__(self, nist_settings: NistSettings,
                 general_settings: GeneralSettings):
        """Initialize a class responsible for execution of tests from BSI battery

        Args:
            nist_settings (NistSettings): Object containing NIST-related settings
            general_settings (GeneralSettings): Object containing general settings
        """
        self.battery_settings = nist_settings
        self.binaries_settings = general_settings.binaries
        self.execution_settings = general_settings.execution
        self.storage_settings = general_settings.storage
        self.logger_settings = general_settings.logger
        self.app_logger = logging.getLogger()
        self.log_prefix = "[NIST STS]"
        # some tests require templates (see src/nist_templates directory)
        # therefore we need to provide a full path to those templates
        # this full path is then passed as '-templatesdir' argument to assess
        self.nist_templates_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "nist_templates")

    # assess 1000000
    #   -fast
    #   --file test_sequences/10MB.rnd
    #   --tests 1111111111111111
    #   --templatesdir templates
    #   --streams 80
    #   --defaultpar
    #   --binary
    def execute_for_sequence(self, sequence_path: str) -> 'list[NistResult]':
        """Execute NIST tests over a random sequence.

        Args:
            sequence_path (str): Path to a binary file containing random sequence

        Returns:
            list[NistResult]: Results of performed tests
        """
        # stepping into temp directory to ensure no data race
        # among multiple executions (i.e. async execution)
        execution_result = []
        with tempfile.TemporaryDirectory(prefix="rtt_py_nist_") as temp_cwd:
            self.prepare_output_dirs(temp_cwd)
            for test in self.battery_settings.per_test_config:
                for variant in test.variants:
                    one_test_param = nist_test_id_to_param(test.test_id)
                    cli_args = [
                        os.path.abspath(self.binaries_settings.nist_sts),
                        str(variant.stream_size),
                        "-fast",
                        "-file",
                        os.path.abspath(sequence_path),
                        "-binary",
                        "-tests",
                        one_test_param,
                        "--streams",
                        str(variant.stream_count),
                        "-templatesdir",
                        os.path.abspath(self.nist_templates_dir)
                    ]
                    test_specific_param = nist_get_specific_param(
                        variant.block_length, test.test_id)
                    cli_args.extend(test_specific_param)
                    self.app_logger.info(
                        f"{self.log_prefix} - Test execution arguments: {cli_args}")
                    test_execution = Popen(cli_args,
                                           stdout=PIPE,
                                           stderr=PIPE,
                                           cwd=temp_cwd)
                    error_code = test_execution.wait(
                        timeout=self.execution_settings.test_timeout_seconds)
                    stdout = test_execution.stdout.read().decode("utf-8")
                    if error_code != 1:  # assess returns 1 on success
                        self.app_logger.error(
                            f"{self.log_prefix} - Execution for file {sequence_path} failed."
                            f" STDOUT:\n{stdout}")
                    else:
                        final_analysis_file = os.path.join(
                            temp_cwd, "experiments", "AlgorithmTesting",
                            "finalAnalysisReport.txt")
                        with open(final_analysis_file, "r") as final_analysis:
                            # x = final_analysis.read()
                            # print(x)
                            execution_result.extend(NistResultFactory.make(
                                final_analysis.read()))
        return execution_result

    def prepare_output_dirs(self, temp_dir: str):
        """Prepares a directory structure for run.
        We need to specify the 'temp_dir' parameter since NIST battery
        writes all of its results into files. The files are being saved in certain
        directory structure so for each execution we create a temporary directory,
        create the desired directory structure and after the execution is done,
        the temp directory is deleted.

        Args:
            temp_dir (str): Path to a temp directory in which NIST will be executed
        """
        # list of all tests, they must have own subdirectory
        test_result_dirs = [
            "Frequency",
            "BlockFrequency",
            "Runs",
            "LongestRun",
            "Rank",
            "FFT",
            "NonOverlappingTemplate",
            "OverlappingTemplate",
            "Universal",
            "LinearComplexity",
            "Serial",
            "ApproximateEntropy",
            "CumulativeSums",
            "RandomExcursions",
            "RandomExcursionsVariant",
        ]
        for test_result_dir in test_result_dirs:
            # AlgorithmTesting - this directory name is used when testing a binary file
            dir_path = os.path.join(
                temp_dir,
                "experiments", "AlgorithmTesting", test_result_dir)
            os.makedirs(dir_path)
