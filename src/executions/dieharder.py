import logging
import os
from subprocess import Popen, PIPE
from settings.dieharder import DieharderSettings
from settings.general import BinariesSettings, ExecutionSettings, FileStorageSettings, LoggerSettings
from results.dieharder import DieharderResult


class DieharderExecution:
    def __init__(self, dieharder_settings: DieharderSettings,
                 binaries_settings: BinariesSettings,
                 execution_settings: ExecutionSettings,
                 storage_settings: FileStorageSettings,
                 logger_settings: LoggerSettings,
                 timestamp: str):
        self.battery_settings = dieharder_settings
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings
        self.timestamp = timestamp
        self.app_logger = logging.getLogger()

    # "dieharder -p 24 -d 101 -D 66047 -g 201
    #     -f bsi_input.rnd"
    def execute_for_sequence(self, sequence_path: str) -> 'list[DieharderResult]':
        self.prepare_output_dirs()
        result_for_sequence: list[DieharderResult] = []
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
                    "-f", sequence_path
                ]
                test_execution = Popen(
                    cli_args, stdout=PIPE, stderr=PIPE)
                error_code = test_execution.wait(
                    timeout=self.execution_settings.test_timeout_seconds)
                # some test results contain multiple p-values
                # for example, the following output
                # test_a|0|1|2|0.3
                # test_a|1|2|3|0.4
                # test_a|2|3|4|0.5
                # will be parsed as:
                # [ DieharderResult{name: test_a, ntuple: 0, tsamples: 1, psamples: 2, p-value: 0.3}
                #   DieharderResult{name: test_a, ntuple: 1, tsamples: 2, psamples: 3, p-value: 0.4}
                #   DieharderResult{name: test_a, ntuple: 2, tsamples: 3, psamples: 4, p-value: 0.5}]
                output_lines = test_execution.stdout.read().decode("utf-8").split("\n")
                # iterate through all the output lines
                for output_line in output_lines:
                    # if you split one line, you get 2 strings.
                    # one of them is '', therefore the check is here
                    if len(output_line) > 0:
                        line_split = output_line.split("|")
                        test_name = line_split[0]
                        ntuple = line_split[1]
                        tsamples = line_split[2]
                        psamples = line_split[3]
                        pvalues = line_split[4]
                        result_for_sequence.append(
                            DieharderResult(test.test_id, test_name, ntuple, tsamples, psamples, pvalues))
                if error_code != 0:
                    self.app_logger.error(f"Dieharder execution failed. Args: {cli_args}. STDOUT: \n{stdout}")
        return result_for_sequence

    def prepare_output_dirs(self):
        os.makedirs(self.storage_settings.dieharder_dir, exist_ok=True)
