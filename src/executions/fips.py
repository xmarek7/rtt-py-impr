import logging
import os
from subprocess import Popen, PIPE
from settings.general import ExecutionSettings, BinariesSettings, FileStorageSettings, LoggerSettings


class FipsExecution:
    def __init__(self, binaries_settings: BinariesSettings, execution_settings: ExecutionSettings, storage_settings: FileStorageSettings, logger_settings: LoggerSettings, timestamp: str):
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings
        self.timestamp = timestamp
        self.app_logger = logging.getLogger()

    def execute_for_sequence(self, sequence_path):
        self.prepare_output_dirs()
        output_filename = self.timestamp + "_" + os.path.splitext(os.path.basename(sequence_path))[0] + ".json"
        out_file = os.path.join(self.storage_settings.fips_dir, output_filename)
        self.app_logger.info(f"FIPS results will be saved to {out_file}")
        test_execution = Popen(
            [self.binaries_settings.fips, "--input_file",
             sequence_path, "--output_file", out_file], stdout=PIPE, stderr=PIPE)
        exit_code = test_execution.wait(
            timeout=self.execution_settings.test_timeout_seconds)
        stdout = test_execution.stdout.read()
        stderr = test_execution.stderr.read()
        if exit_code != 0:
            self.app_logger.error(f"FIPS execution for file {sequence_path} failed. STDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        else:
            if len(stdout) > 0:
                self.app_logger.info(f"FIPS execution STDOUT:\n{stdout}")
            if len(stderr) > 0:
                self.app_logger.warning(
                    f"FIPS execution ended with non-empty STDERR:\n{stderr}")
        # TODO: error handling & logging
        # TODO: test results handling
        
    def prepare_output_dirs(self):
        log_dir = self.logger_settings.fips_dir
        if not os.path.isdir(log_dir):
            self.app_logger.info(
                f"Logging directory {log_dir} does not exist. Creating ...")
            os.makedirs(log_dir)
        res_dir = self.storage_settings.fips_dir
        if not os.path.isdir(res_dir):
            self.app_logger.info(
                f"Output directory {res_dir} does not exist. Creating ...")
            os.makedirs(res_dir)
