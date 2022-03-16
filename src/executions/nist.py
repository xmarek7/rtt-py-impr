import logging
import os

from subprocess import Popen, PIPE
from tools.misc import nist_test_ids_to_param
from settings.nist import NistSettings
from settings.general import BinariesSettings, ExecutionSettings, FileStorageSettings, LoggerSettings


class NistExecution:
    def __init__(self, nist_settings: NistSettings, binaries_settings: BinariesSettings, execution_settings: ExecutionSettings, storage_settings: FileStorageSettings, logger_settings: LoggerSettings, timestamp: str):
        self.battery_settings = nist_settings
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings
        self.test_ids_param = nist_test_ids_to_param(
            self.battery_settings.test_ids)
        self.app_logger = logging.getLogger()
        self.timestamp = timestamp

    # nonoverlappingtest check templates
    # assess 1000000 -fast --file test_sequences/10MB.rnd --tests 1111111111111111 --streams 80 --defaultpar --binary
    def execute_for_sequence(self, sequence_path: str):
        self.prepare_output_dirs()
        test_execution = Popen([
            self.binaries_settings.nist_sts,
            str(self.battery_settings.stream_size), "-fast", "-defaultpar",
            "--file", sequence_path, "-binary", "-tests", self.test_ids_param,
            "--streams", str(self.battery_settings.stream_count)],
            stdout=PIPE,
            stderr=PIPE,
            cwd=self.storage_settings.nist_sts_dir)
        error_code = test_execution.wait(
            timeout=self.execution_settings.test_timeout_seconds)
        stdout = test_execution.stdout.read()
        stderr = test_execution.stderr.read()
        if error_code != 0:
            self.app_logger.error(
                f"NIST-STS execution for file {sequence_path} failed. STDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        else:
            if len(stdout) > 0:
                self.app_logger.info(f"NIST-STS execution STDOUT:\n{stdout}")
            if len(stderr) > 0:
                self.app_logger.warning(
                    f"NIST-STS execution ended with non-empty STDERR:\n{stderr}")

    def prepare_output_dirs(self):
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
                self.storage_settings.nist_sts_dir, "experiments", "AlgorithmTesting", test_result_dir)
            self.app_logger.info(
                f"NIST-STS creating result directory {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
