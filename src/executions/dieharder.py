from ast import List
from subprocess import Popen, PIPE
from multiprocessing import Process
from settings.dieharder import DieharderSettings
from settings.general import BinariesSettings, ExecutionSettings, FileStorageSettings, LoggerSettings


class DieharderExecution:
    def __init__(self, dieharder_settings: DieharderSettings, binaries_settings: BinariesSettings, execution_settings: ExecutionSettings, storage_settings: FileStorageSettings, logger_settings: LoggerSettings):
        self.battery_settings = dieharder_settings
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.storage_settings = storage_settings
        self.logger_settings = logger_settings

    # "dieharder -p 24 -d 101 -D 66047 -g 201
    #     -f bsi_input.rnd"
    def execute_for_sequence(self, sequence_path: str):
        for test in self.battery_settings.per_test_config:
            for variant in test.variants:
                test_execution = Popen(
                    ["-D", "66047",  # 65536+256+128+64+32+16+8+4+2+1 (for more info run ./dieharder -F)
                     # 201 in dieharder means file_input_raw (for more info run ./dieharder -g 502)
                     "-g", "201",
                     "-d", test.test_id, "-p", variant.psamples, *variant.arguments, "-f", sequence_path],
                    executable=self.binaries_settings.nist_sts)
                test_execution.wait(
                    timeout=self.execution_settings.test_timeout_seconds)
