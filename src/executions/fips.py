import os
from subprocess import Popen, PIPE
from settings.general import ExecutionSettings, BinariesSettings, FileStorageSettings, LoggerSettings


class FipsExecution:
    def __init__(self, binaries_settings: BinariesSettings, execution_settings: ExecutionSettings, storage_settings: FileStorageSettings, logger_settings: LoggerSettings):
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings

    def execute_for_sequence(self, sequence_path):
        out_file = os.path.splitext(os.path.basename(sequence_path))[0]
        test_execution = Popen(
            ["--input_file",
             sequence_path, "--output_file", out_file],
            executable=self.binaries_settings.bsi
        )
        exit_code = test_execution.wait(
            timeout=self.execution_settings.test_timeout_seconds)
        # TODO: error handling & logging
        # TODO: test results handling
