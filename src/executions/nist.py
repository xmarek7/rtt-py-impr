import logging
import os
import tempfile

from subprocess import Popen, PIPE
from results.nist import NistResult, NistResultFactory
from tools.misc import nist_test_ids_to_param
from settings.nist import NistSettings
from settings.general import BinariesSettings, ExecutionSettings, FileStorageSettings, LoggerSettings


class NistExecution:
    def __init__(self, nist_settings: NistSettings,
                 binaries_settings: BinariesSettings,
                 execution_settings: ExecutionSettings,
                 storage_settings: FileStorageSettings,
                 logger_settings: LoggerSettings,
                 timestamp: str):
        self.battery_settings = nist_settings
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings
        self.test_ids_param = nist_test_ids_to_param(
            self.battery_settings.test_ids)
        self.app_logger = logging.getLogger()
        self.timestamp = timestamp
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
        # stepping into temp directory to ensure no data race
        # among multiple executions (i.e. async execution)
        execution_result = []
        with tempfile.TemporaryDirectory(prefix="rtt_py_nist_") as temp_cwd:
            self.prepare_output_dirs(temp_cwd)
            test_execution = Popen([
                os.path.abspath(self.binaries_settings.nist_sts),
                str(self.battery_settings.stream_size),
                "-fast",
                "-defaultpar",
                "--file",
                os.path.abspath(sequence_path),
                "-binary",
                "-tests",
                self.test_ids_param,
                "--streams",
                str(self.battery_settings.stream_count),
                "-templatesdir",
                os.path.abspath(self.nist_templates_dir)],
                stdout=PIPE,
                stderr=PIPE,
                cwd=temp_cwd)
            error_code = test_execution.wait(
                timeout=self.execution_settings.test_timeout_seconds)
            stdout = test_execution.stdout.read()
            if error_code != 1:  # assess returns 1 on success
                self.app_logger.error(
                    f"NIST-STS execution for file {sequence_path} failed."
                    f" STDOUT:\n{str(stdout)}\n")
            else:
                final_analysis_location = os.path.join(
                    temp_cwd, "experiments", "AlgorithmTesting",
                    "finalAnalysisReport.txt")
                with open(final_analysis_location, "r") as final_analysis:
                    execution_result = NistResultFactory.make(final_analysis.read())
        return execution_result

    def prepare_output_dirs(self, temp_dir: str):
        log_dir = self.logger_settings.nist_sts_dir
        if not os.path.isdir(log_dir):
            self.app_logger.info(
                f"Logging directory {log_dir} does not exist. Creating ...")
            os.makedirs(log_dir)
        res_dir = self.storage_settings.nist_sts_dir
        if not os.path.isdir(res_dir):
            self.app_logger.info(
                f"Output directory {res_dir} does not exist. Creating ...")
            os.makedirs(res_dir)
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
            dir_path = os.path.join(
                temp_dir,
                "experiments", "AlgorithmTesting", test_result_dir)
            self.app_logger.info(
                f"NIST-STS creating result directory {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
