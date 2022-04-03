import logging
from subprocess import Popen, PIPE
from settings.testu01 import TestU01Settings
from settings.general import GeneralSettings
from results.testu01 import TestU01Result, TestU01ResultFactory


class TestU01Execution:
    def __init__(self, testu01_settings: TestU01Settings,
                 general_settings: GeneralSettings):
        """Initialize a class responsible for execution of tests from TestU01 battery.
        This class is shared among [small, big]-crush, rabbit, (block)alphabit families of tests.

        Args:
            testu01_settings (TestU01Settings): Object containing TestU01-related settings
            general_settings (GeneralSettings): Object containing general settings
        """
        self.battery_settings = testu01_settings
        self.binaries_settings = general_settings.binaries
        self.execution_settings = general_settings.execution
        self.storage_settings = general_settings.storage
        self.logger_settings = general_settings.logger
        self.app_logger = logging.getLogger()
        self.log_prefix = f"[TestU01-{self.battery_settings.subbattery}]"

    # example commands:
    #   testu01 -m small_crush -t 2 -i bsi_input.rnd
    #   testu01 -m crush -t 8 -i bsi_input.rnd
    #   testu01 -m big_crush -t 8 -i bsi_input.rnd
    #   testu01 -m rabbit -t 1 -i bsi_input.rnd --bit_nb 10000000
    #   testu01 -m alphabit -t 8 -i bsi_input.rnd --bit_nb 10000000 --bit_r 0 --bit_s 32
    #   testu01 -m block_alphabit -t 9 -i bsi_input.rnd --bit_nb 10000000 --bit_r 0 --bit_s 32 --bit_w 8
    def execute_for_sequence(self, sequence_path: str) -> 'list[TestU01Result]':
        """Execute one TestU01 family of tests over a random sequence.

        Args:
            sequence_path (str): Path to a binary file containing random sequence

        Returns:
            list[TestU01Result]: Results of performed tests
        """
        execution_result: list[TestU01Result] = []
        for test in self.battery_settings.per_test_id_settings:
            for variant in test.variants:
                cli_args: list[str] = [
                    self.binaries_settings.testu01,
                    "-m", self.battery_settings.subbattery,
                    "-t", str(test.test_id),
                    "-r", str(variant.repetitions),
                    "-i", sequence_path]
                if variant.bit_nb is not None:
                    cli_args.extend(["--bit_nb", str(variant.bit_nb)])
                if variant.bit_r is not None:
                    cli_args.extend(["--bit_r", str(variant.bit_r)])
                if variant.bit_s is not None:
                    cli_args.extend(["--bit_s", str(variant.bit_s)])
                if variant.bit_w is not None:
                    cli_args.extend(["--bit_w", str(variant.bit_w)])
                self.app_logger.info(
                    f"{self.log_prefix} - Test execution arguments: {cli_args}")
                test_execution = Popen(cli_args, stdout=PIPE, stderr=PIPE)
                error_code = test_execution.wait(
                    timeout=self.execution_settings.test_timeout_seconds)
                stdout = test_execution.stdout.read().decode("utf-8")
                if error_code != 0:
                    stderr = test_execution.stderr.read().decode("utf-8")
                    self.app_logger.error(
                        f"{self.log_prefix} - Execution failed. Arguments were: {cli_args}\nSTDOUT:\n{stdout}"
                        f"\nSTDERR:\n{stderr}")
                else:
                    variant_result = TestU01ResultFactory.make_result(stdout)
                    if len(variant_result) > 0:
                        execution_result.extend(variant_result)
        return execution_result
