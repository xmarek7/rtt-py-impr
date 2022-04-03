import json
import os
import logging
from subprocess import Popen, PIPE
from settings.bsi import BsiSettings
from settings.general import GeneralSettings
from results.bsi import BsiResult


class BsiExecution:
    def __init__(self, bsi_settings: BsiSettings, general_settings: GeneralSettings):
        """Initialize a class responsible for execution of tests from BSI battery

        Args:
            bsi_settings (BsiSettings): Object containing BSI-related settings
            general_settings (GeneralSettings): Object containing general settings
        """
        self.battery_settings = bsi_settings
        self.binaries_settings = general_settings.binaries
        self.execution_settings = general_settings.execution
        self.storage_settings = general_settings.storage
        self.logger_settings = general_settings.logger
        self.app_logger = logging.getLogger()
        self.log_prefix = "[BSI]"

    def execute_for_sequence(self, sequence_path: str) -> 'list[BsiResult]':
        """Execute BSI tests over a random sequence.

        Args:
            sequence_path (str): Path to a binary file containing random sequence

        Returns:
            list[BsiResult]: Results of performed tests
        """
        self.prepare_output_dirs()
        execution_result: list[BsiResult] = []
        output_filename = str(self.logger_settings.TIMESTAMP) + "_" + \
            os.path.splitext(os.path.basename(sequence_path))[0] + ".json"
        out_file = os.path.join(self.storage_settings.bsi_dir, output_filename)
        self.app_logger.info(
            f"{self.log_prefix} - Results will be saved to {out_file}")
        process_args = [self.binaries_settings.bsi, "--input_file",
                        sequence_path, "--output_file", out_file]
        process_args.extend(self.get_skip_test_args())

        if self.battery_settings.uniform_dist_K is not None:
            process_args.extend(["-K", self.battery_settings.uniform_dist_K])
        if self.battery_settings.uniform_dist_N is not None:
            process_args.extend(["-N", self.battery_settings.uniform_dist_N])
        if self.battery_settings.uniform_dist_A is not None:
            process_args.extend(["-A", self.battery_settings.uniform_dist_A])

        test_execution = Popen(process_args, stdout=PIPE, stderr=PIPE)
        exit_code = test_execution.wait(
            timeout=self.execution_settings.test_timeout_seconds)
        stdout = test_execution.stdout.read().decode("utf-8")
        if exit_code != 0:
            stderr = test_execution.stderr.read().decode("utf-8")
            self.app_logger.info(
                f"{self.log_prefix} - Execution for file {sequence_path} failed. STDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        else:
            output_as_json = json.loads(stdout)
            for test_result in output_as_json["tests"]:
                execution_result.append(BsiResult(
                    test_result["name"],
                    test_result["error"],
                    test_result.get("num_runs"),
                    test_result.get("num_failures")))
            self.app_logger.info(
                f"{self.log_prefix} - Execution for file {sequence_path} was successful.")
        return execution_result

    def get_skip_test_args(self) -> list:
        """Analyze configured test IDs and return list of arguments
        that are going to make BSI binary skip tests that were not included in IDs

        Returns:
            list: '--skip-{test}'-like arguments
        """
        skip_args = list()
        ids = self.battery_settings.test_ids
        if 0 not in ids:
            skip_args.append("--skip_words_test")
        if 1 not in ids:
            skip_args.append("--skip_monobit_test")
        if 2 not in ids:
            skip_args.append("--skip_poker_test")
        if 3 not in ids:
            skip_args.append("--skip_runs_test")
        if 4 not in ids:
            skip_args.append("--skip_long_run_test")
        if 5 not in ids:
            skip_args.append("--skip_autocorrelation_test")
        if 6 not in ids:
            skip_args.append("--skip_uniform_test")
        if 7 not in ids:
            skip_args.append("--skip_homogenity_test")
        if 8 not in ids:
            skip_args.append("--skip_entropy_test")
        return skip_args

    def prepare_output_dirs(self):
        """Prepares a directory structure for run.
        """
        res_dir = self.storage_settings.bsi_dir
        if not os.path.isdir(res_dir):
            self.app_logger.info(
                f"{self.log_prefix} - Creating output directory {res_dir}.")
            os.makedirs(res_dir)
