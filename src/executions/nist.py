from subprocess import Popen, PIPE
from tools.misc import nist_test_ids_to_param
from settings.nist import NistSettings
from settings.general import BinariesSettings, ExecutionSettings


class NistExecution:
    def __init__(self, nist_settings: NistSettings, binaries_settings: BinariesSettings, execution_settings: ExecutionSettings):
        self.battery_settings = nist_settings
        self.binaries_settings = binaries_settings
        self.execution_settings = execution_settings
        self.test_ids_param = nist_test_ids_to_param(self.battery_settings.test_ids)

    # assess 1000000 -fast --file test_sequences/10MB.rnd --tests 1111111111111111 --streams 80 --defaultpar --binary
    def execute_for_sequence(self, sequence_path: str):
        test_execution = Popen(
            [str(self.battery_settings.stream_size), "-fast", "-defaultpar",
             "--file", sequence_path, "-binary", "-tests", self.test_ids_param,
             "--streams", self.battery_settings.stream_count],
            executable=self.binaries_settings.nist_sts)
        test_execution.wait(timeout=self.execution_settings.test_timeout_seconds)
