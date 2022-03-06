import os
from subprocess import Popen, PIPE
from settings.bsi import BsiSettings
from settings.general import ExecutionSettings, BinariesSettings, FileStorageSettings, LoggerSettings


class BsiExecution:
    def __init__(self, bsi_settings: BsiSettings, binaries_settings: BinariesSettings, execution_settings: ExecutionSettings, storage_settings: FileStorageSettings, logger_settings: LoggerSettings):
        self.battery_settings = bsi_settings
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings

    def execute_for_sequence(self, sequence_path):
        out_file = os.path.splitext(os.path.basename(sequence_path))[0]
        process_args = ["--input_file",
                        sequence_path, "--output_file", out_file]
        process_args.extend(self.get_skip_test_args())
        if self.battery_settings.uniform_dist_K is not None:
            process_args.extend(["-K", self.battery_settings.uniform_dist_K])
        if self.battery_settings.uniform_dist_N is not None:
            process_args.extend(["-N", self.battery_settings.uniform_dist_N])
        if self.battery_settings.uniform_dist_A is not None:
            process_args.extend(["-A", self.battery_settings.uniform_dist_A])
        test_execution = Popen(
            process_args,
            executable=self.binaries_settings.bsi
        )
        exit_code = test_execution.wait(
            timeout=self.execution_settings.test_timeout_seconds)
        # TODO: error handling & logging
        # TODO: test results handling

    def get_skip_test_args(self) -> list:
        skip_args = list()
        ids = self.battery_settings.test_ids
        if "0" not in ids:
            skip_args.append("--skip_words_test")
        if "1" not in ids:
            skip_args.append("--skip_monobit_test")
        if "2" not in ids:
            skip_args.append("--skip_poker_test")
        if "3" not in ids:
            skip_args.append("--skip_runs_test")
        if "4" not in ids:
            skip_args.append("--skip_long_run_test")
        if "5" not in ids:
            skip_args.append("--skip_autocorrelation_test")
        if "6" not in ids:
            skip_args.append("--skip_uniform_test")
        if "7" not in ids:
            skip_args.append("--skip_homogenity_test")
        if "8" not in ids:
            skip_args.append("--skip_entropy_test")
        return skip_args
