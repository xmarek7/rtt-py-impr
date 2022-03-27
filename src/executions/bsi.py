import json
import os
import logging
from subprocess import Popen, PIPE
from settings.bsi import BsiSettings
from settings.general import ExecutionSettings, BinariesSettings, FileStorageSettings, LoggerSettings
from results.bsi import BsiResult


class BsiExecution:
    def __init__(self, bsi_settings: BsiSettings,
                 binaries_settings: BinariesSettings,
                 execution_settings: ExecutionSettings,
                 storage_settings: FileStorageSettings,
                 logger_settings: LoggerSettings):
        self.battery_settings = bsi_settings
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings
        self.app_logger = logging.getLogger()

    def execute_for_sequence(self, sequence_path) -> 'list[BsiResult]':
        self.prepare_output_dirs()
        execution_result: list[BsiResult] = []
        output_filename = str(self.logger_settings.TIMESTAMP) + "_" + \
            os.path.splitext(os.path.basename(sequence_path))[0] + ".json"
        out_file = os.path.join(self.storage_settings.bsi_dir, output_filename)
        self.app_logger.info(f"BSI results will be saved to {out_file}")
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
                f"BSI execution for file {sequence_path} failed. STDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        else:
            output_as_json = json.loads(stdout)
            for test_result in output_as_json["tests"]:
                execution_result.append(BsiResult(
                    test_result["name"],
                    test_result["error"],
                    test_result.get("num_runs"),
                    test_result.get("num_failures")))
        return execution_result

    def get_skip_test_args(self) -> list:
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
        log_dir = self.logger_settings.bsi_dir
        if not os.path.isdir(self.logger_settings.bsi_dir):
            self.app_logger.info(
                f"Logging directory {log_dir} does not exist. Creating ...")
            os.makedirs(log_dir)
        res_dir = self.storage_settings.bsi_dir
        if not os.path.isdir(res_dir):
            self.app_logger.info(
                f"Output directory {res_dir} does not exist. Creating ...")
            os.makedirs(res_dir)
