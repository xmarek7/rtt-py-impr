import json
import logging
import os
from subprocess import Popen, PIPE
from settings.fips import FipsSettings
from settings.general import GeneralSettings
from results.fips import FipsResult


class FipsExecution:
    def __init__(self, battery_settings: FipsSettings, general_settings: GeneralSettings):
        """Initialize a class responsible for execution of tests from FIPS battery.

        Args:
            general_settings (GeneralSettings): Object containing general settings
        """
        self.battery_settings = battery_settings
        self.binaries_settings = general_settings.binaries
        self.execution_settings = general_settings.execution
        self.storage_settings = general_settings.storage
        self.logger_settings = general_settings.logger
        self.app_logger = logging.getLogger()
        self.log_prefix = "[FIPS]"

    def execute_for_sequence(self, sequence_path: str) -> 'list[FipsResult]':
        """Execute BSI tests over a random sequence.

        Args:
            sequence_path (str): Path to a binary file containing random sequence

        Returns:
            list[FipsResult]: Results of performed tests
        """
        execution_result: list[FipsResult] = []
        test_execution = Popen([
            self.binaries_settings.fips,
            "--input_file",
            sequence_path,
            "--bytes_count",
            str(self.battery_settings.bytes_count)],
            stdout=PIPE,
            stderr=PIPE)
        exit_code = test_execution.wait(
            timeout=self.execution_settings.test_timeout_seconds)
        stdout = test_execution.stdout.read().decode("utf-8")
        if exit_code != 0:
            stderr = test_execution.stderr.read().decode("utf-8")
            self.app_logger.error(
                f"{self.log_prefix} - Execution for file {sequence_path} failed. STDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        else:
            output_as_json = json.loads(stdout)
            execution_accepted: bool = output_as_json["accepted"]
            for t in output_as_json["tests"]:
                test_name = t["name"]
                num_failures = t["num_failures"]
                num_runs = t["num_runs"]
                execution_result.append(FipsResult(
                    execution_accepted, test_name, num_failures, num_runs))
            self.app_logger.info(
                f"{self.log_prefix} - Execution for file {sequence_path} was successful.")
        return execution_result

    def prepare_output_dirs(self):
        pass
