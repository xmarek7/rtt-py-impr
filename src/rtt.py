import os
import json
import time
import logging

from settings.bsi import BsiSettings
from settings.nist import NistSettingsFactory
from settings.testu01 import TestU01SettingsFactory
from settings.dieharder import DieharderSettingsFactory
from settings.general import FileStorageSettings, BinariesSettings, LoggerSettings, ExecutionSettings

from executions.bsi import BsiExecution
from executions.fips import FipsExecution
from executions.nist import NistExecution
from executions.testu01 import TestU01Execution
from executions.dieharder import DieharderExecution


def init_logging(settings: LoggerSettings, timestamp: str):
    base_dir = settings.dir_prefix
    os.makedirs(base_dir, exist_ok=True)
    run_log_dir = settings.run_log_dir
    os.makedirs(run_log_dir, exist_ok=True)
    run_log_filename = timestamp + "_run.log"
    run_log_file = os.path.join(run_log_dir, run_log_filename)
    root_logger = logging.getLogger()
    default_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s - %(message)s \n")
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(default_formatter)
    stdout_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(filename=run_log_file, mode="w")
    file_handler.setFormatter(default_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)


def main():
    # will be used as part of each output file's name
    EXECUTION_TIMESTAMP = str(time.time())
    f = "/ws/rtt-py/tests/assets/rnd/10MB.rnd"
    # general settings
    rtt_json = json.loads(
        open("/ws/rtt-py/tests/assets/configs/rtt-settings.json").read())["toolkit-settings"]
    logger_settings = LoggerSettings(rtt_json["logger"])
    binaries_settings = BinariesSettings(rtt_json["binaries"])
    execution_settings = ExecutionSettings(rtt_json["execution"])
    file_storage_settings = FileStorageSettings(
        rtt_json["result-storage"]["file"])

    init_logging(logger_settings, EXECUTION_TIMESTAMP)

    rl = logging.getLogger()

    # battery settings
    bat_json = json.loads(open(
        "/ws/rtt-py/tests/assets/configs/10MB.json").read())["randomness-testing-toolkit"]
    bsi_settings = BsiSettings(bat_json["bsi-settings"])
    dieharder_settings = DieharderSettingsFactory.make_settings(
        bat_json["dieharder-settings"])
    testu01_settings = TestU01SettingsFactory.make_settings(
        bat_json["tu01-rabbit-settings"], "rabbit")
    nist_settings = NistSettingsFactory.make_settings(
        bat_json["nist-sts-settings"])

    # execution
    bsi_execution = BsiExecution(bsi_settings, binaries_settings, execution_settings,
                                 file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    fips_execution = FipsExecution(binaries_settings, execution_settings,
                                   file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    nist_execution = NistExecution(nist_settings, binaries_settings, execution_settings,
                                   file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    dieharder_execution = DieharderExecution(
        dieharder_settings, binaries_settings, execution_settings, file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    testu01_execution = TestU01Execution(
        testu01_settings, binaries_settings, execution_settings, file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)

    bsi_execution.execute_for_sequence(f)
    fips_execution.execute_for_sequence(f)
    nist_execution.execute_for_sequence(f)
    dieharder_execution.execute_for_sequence(f)
    testu01_execution.execute_for_sequence(f)


if __name__ == "__main__":
    main()
