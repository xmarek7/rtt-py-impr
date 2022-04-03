import json
import logging
import os
from subprocess import Popen, PIPE
from settings.general import GeneralSettings
from results.fips import FipsResult


class FipsExecution:
    def __init__(self, general_settings: GeneralSettings):
        """Initialize a class responsible for execution of tests from FIPS battery.
        Unlike other classes, this class does not require object containing battery-related settings.
        FIPS does not offer much to configure.

        Args:
            general_settings (GeneralSettings): Object containing general settings
        """
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
        self.prepare_output_dirs()
        execution_result: list[FipsResult] = []
        output_filename = self.logger_settings.TIMESTAMP + "_" + \
            os.path.splitext(
                os.path.basename(sequence_path))[0] + ".json"
        out_file = os.path.join(
            self.storage_settings.fips_dir, output_filename)
        self.app_logger.info(
            f"{self.log_prefix} - Results will be saved to {out_file}")
        test_execution = Popen([
            self.binaries_settings.fips,
            "--input_file",
            sequence_path,
            "--output_file",
            out_file],
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
        """Prepares a directory structure for run.
        """
        res_dir = self.storage_settings.fips_dir
        if not os.path.isdir(res_dir):
            self.app_logger.info(
                f"{self.log_prefix} - Creating output directory {res_dir}.")
            os.makedirs(res_dir)
