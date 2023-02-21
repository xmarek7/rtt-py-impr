import logging
import os
from subprocess import Popen, PIPE
from settings.dieharder import DieharderSettings
from settings.general import GeneralSettings
from results.dieharder import DieharderResult


class DieharderExecution:
    def __init__(self, dieharder_settings: DieharderSettings,
                 general_settings: GeneralSettings):
        """Initialize a class responsible for executiion of tests from BSI battery

        Args:
            dieharder_settings (DieharderSettings): Object containing DieHarder-related settings
            general_settings (GeneralSettings): Object containing general settings
        """
        self.battery_settings = dieharder_settings
        self.binaries_settings = general_settings.binaries
        self.execution_settings = general_settings.execution
        self.storage_settings = general_settings.storage
        self.logger_settings = general_settings.logger
        self.app_logger = logging.getLogger()
        self.log_prefix = "[DieHarder]"

    # "dieharder -p 24 -d 101 -D 66047 -g 201
    #     -f bsi_input.rnd"
    def execute_for_sequence(self, sequence_path: str) -> 'list[DieharderResult]':
        """Execute DieHarder tests over a random sequence.

        Args:
            sequence_path (str): Path to a binary file containing random sequence

        Returns:
            list[DieharderResult]: Results of performed tests
        """
        self.prepare_output_dirs()
        execution_result: list[DieharderResult] = []
        for test in self.battery_settings.per_test_config:
            for variant in test.variants:
                cli_args = [
                    self.binaries_settings.dieharder,
                    # -D 33016 parameter causes dieharder to return results in the following format:
                    # test_name|ntuple|tsamples|psamples|p-value
                    # i.e.:
                    # diehard_operm5|0|1000000|1|0.59515332
                    "-D", "33016",
                    # 201 in dieharder means file_input_raw (for more info run ./dieharder -g 502)
                    "-g", "201",
                    # unique test id (see dieharder help for more info)
                    "-d", str(test.test_id),
                    # psamples parameter
                    "-p", str(variant.psamples),
                    # additional arguments if specified in .json file
                    *variant.arguments,
                    # file to be tested
                    "-f", sequence_path,
                    "-s", "1",
                    "-S", "0"
                ]
                self.app_logger.info(
                    f"{self.log_prefix} - Test execution arguments: {cli_args}")
                test_execution = Popen(
                    cli_args, stdout=PIPE, stderr=PIPE)
                error_code = test_execution.wait(
                    timeout=self.execution_settings.test_timeout_seconds)
                if error_code != 0:
                    self.app_logger.error(
                        f"{self.log_prefix} - Execution failed. Arguments were:\n{cli_args}.\nSTDOUT: \n{stdout}")
                else:
                    # some test results contain multiple p-values
                    # for example, the following output
                    # test_a|0|1|2|0.3
                    # test_a|1|2|3|0.4
                    # test_a|2|3|4|0.5
                    # will be parsed as:
                    # [ DieharderResult{name: test_a, ntuple: 0, tsamples: 1, psamples: 2, p-value: 0.3}
                    #   DieharderResult{name: test_a, ntuple: 1, tsamples: 2, psamples: 3, p-value: 0.4}
                    #   DieharderResult{name: test_a, ntuple: 2, tsamples: 3, psamples: 4, p-value: 0.5}]
                    stdout = test_execution.stdout.read().decode("utf-8")
                    output_lines = stdout.split("\n")
                    for output_line in output_lines:
                        # if you split one line, you get 2 strings.
                        # one of them is '', therefore the length check is here
                        if len(output_line) > 0:
                            line_split = output_line.split("|")
                            test_name = line_split[0]
                            ntuple = int(line_split[1])
                            tsamples = int(line_split[2])
                            psamples = int(line_split[3])
                            pvalue = float(line_split[4])
                            execution_result.append(
                                DieharderResult(test.test_id, test_name, ntuple, tsamples, psamples, pvalue))
        return execution_result

    def prepare_output_dirs(self):
        """Prepares a directory structure for run.
        """
        pass
