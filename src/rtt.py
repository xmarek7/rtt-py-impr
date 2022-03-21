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

from shutil import copytree
from tools.html_reports import generate_html_with_results


# TODO: implement
def generate_summary_report():
    pass


# TODO: better name
class SummaryPerBat:
    def __init__(self, html_path, tested_file):
        self.html_path = html_path
        self.tested_file = tested_file


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
    general_config = "/ws/rtt-py/tests/assets/configs/rtt-settings.json"
    test_spec = "/ws/rtt-py/tests/assets/configs/10MB.json"
    # general settings
    rtt_json = json.loads(
        open(general_config).read())["toolkit-settings"]
    logger_settings = LoggerSettings(rtt_json["logger"])
    binaries_settings = BinariesSettings(rtt_json["binaries"])
    execution_settings = ExecutionSettings(rtt_json["execution"])
    file_storage_settings = FileStorageSettings(
        rtt_json["result-storage"]["file"])

    init_logging(logger_settings, EXECUTION_TIMESTAMP)

    # battery settings
    bat_json = json.loads(open(
        test_spec).read())["randomness-testing-toolkit"]
    bsi_settings = BsiSettings(bat_json["bsi-settings"])
    nist_settings = NistSettingsFactory.make_settings(
        bat_json["nist-sts-settings"])
    dieharder_settings = DieharderSettingsFactory.make_settings(
        bat_json["dieharder-settings"])
    tu01_rabbit_settings = TestU01SettingsFactory.make_settings(
        bat_json["tu01-rabbit-settings"], "rabbit")
    tu01_alphabit_settings = TestU01SettingsFactory.make_settings(
        bat_json["tu01-alphabit-settings"], "alphabit")
    tu01_block_alphabit_settings = TestU01SettingsFactory.make_settings(
        bat_json["tu01-blockalphabit-settings"], "block_alphabit")

    # execution initialization
    bsi_execution = BsiExecution(bsi_settings, binaries_settings, execution_settings,
                                 file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    fips_execution = FipsExecution(binaries_settings, execution_settings,
                                   file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    nist_execution = NistExecution(nist_settings, binaries_settings, execution_settings,
                                   file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    dieharder_execution = DieharderExecution(
        dieharder_settings, binaries_settings, execution_settings, file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    tu01_rabbit_execution = TestU01Execution(
        tu01_rabbit_settings, binaries_settings, execution_settings, file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    tu01_alphabit_execution = TestU01Execution(
        tu01_alphabit_settings, binaries_settings, execution_settings, file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)
    tu01_block_alphabit_execution = TestU01Execution(
        tu01_block_alphabit_settings, binaries_settings, execution_settings, file_storage_settings, logger_settings, EXECUTION_TIMESTAMP)

    execution_html_dir = os.path.join(
        file_storage_settings.dir_prefix, "html", EXECUTION_TIMESTAMP)
    os.makedirs(execution_html_dir, exist_ok=True)
    # just to have fancy html
    copytree("jinja_templates/css", os.path.join(execution_html_dir, "css"))

    configured_batteries = ["bsi", "fips", "nist",
                            "dieharder", "rabbit", "alphabit", "block_alphabit"]
    for per_battery_dir in configured_batteries:
        os.mkdir(os.path.join(execution_html_dir, per_battery_dir))

    bsi_report_files: list[SummaryPerBat] = []
    fips_report_files: list[SummaryPerBat] = []
    nist_report_files: list[SummaryPerBat] = []
    dh_report_files: list[SummaryPerBat] = []
    rabbit_report_files: list[SummaryPerBat] = []
    alphabit_report_files: list[SummaryPerBat] = []
    block_alphabit_report_files: list[SummaryPerBat] = []

    input_files = [
        "/ws/rtt-py/tests/assets/rnd/10MB.rnd",
        "/ws/rtt-statistical-batteries/bsi-src/assets/bsi_input.rnd",
    ]
    for f in input_files:
        input_file_basename = os.path.basename(f)
        html_result_file = input_file_basename + ".html"
        # bsi exec
        bsi_results = bsi_execution.execute_for_sequence(f)
        bsi_report_file = os.path.join(
            execution_html_dir, "bsi", html_result_file)
        generate_html_with_results(
            "jinja_templates/bsi_template.html.j2",
            {"tested_file": f, "list_of_results": bsi_results},
            bsi_report_file)
        bsi_report_files.append(SummaryPerBat(
            bsi_report_file.replace(execution_html_dir + "/", ""), f))
        # fips exec
        fips_results = fips_execution.execute_for_sequence(f)
        fips_bat_accepted = fips_results[0].battery_accepted if len(
            fips_results) > 0 else False
        fips_report_file = os.path.join(
            execution_html_dir, "fips", html_result_file)
        generate_html_with_results(
            "jinja_templates/fips_template.html.j2",
            {"tested_file": f, "battery_accepted": fips_bat_accepted,
                "list_of_results": fips_results},
            fips_report_file)
        fips_report_files.append(SummaryPerBat(
            fips_report_file.replace(execution_html_dir + "/", ""), f))
        # nist exec
        nist_results = nist_execution.execute_for_sequence(f)
        nist_report_file = os.path.join(
            execution_html_dir, "nist", html_result_file)
        generate_html_with_results(
            "jinja_templates/nist_template.html.j2",
            {"tested_file": f, "list_of_results": nist_results},
            nist_report_file)
        nist_report_files.append(SummaryPerBat(
            nist_report_file.replace(execution_html_dir + "/", ""), f))
        # dieharder exec
        dh_results = dieharder_execution.execute_for_sequence(f)
        dh_report_file = os.path.join(
            execution_html_dir, "dieharder", html_result_file)
        generate_html_with_results(
            "jinja_templates/dieharder_template.html.j2",
            {"tested_file": f, "list_of_results": dh_results},
            dh_report_file)
        dh_report_files.append(SummaryPerBat(
            dh_report_file.replace(execution_html_dir + "/", ""), f))
        # rabbit exec
        rabbit_results = tu01_rabbit_execution.execute_for_sequence(f)
        rabbit_report_file = os.path.join(
            execution_html_dir, "rabbit", html_result_file)
        generate_html_with_results(
            "jinja_templates/testu01_template.html.j2",
            {"tested_file": f, "list_of_results": rabbit_results,
                "subbattery": "rabbit"},
            rabbit_report_file)
        rabbit_report_files.append(SummaryPerBat(
            rabbit_report_file.replace(execution_html_dir + "/", ""), f))
        # alphabit exec
        alphabit_results = tu01_alphabit_execution.execute_for_sequence(f)
        alphabit_report_file = os.path.join(
            execution_html_dir, "alphabit", html_result_file)
        generate_html_with_results(
            "jinja_templates/testu01_template.html.j2",
            {"tested_file": f, "list_of_results": alphabit_results,
                "subbattery": "alphabit"},
            alphabit_report_file)
        alphabit_report_files.append(SummaryPerBat(
            alphabit_report_file.replace(execution_html_dir + "/", ""), f))
        # block_alphabit exec
        block_alphabit_results = tu01_block_alphabit_execution.execute_for_sequence(
            f)
        block_alphabit_report_file = os.path.join(
            execution_html_dir, "block_alphabit", html_result_file)
        generate_html_with_results(
            "jinja_templates/testu01_template.html.j2",
            {"tested_file": f, "list_of_results": block_alphabit_results,
                "subbattery": "block_alphabit"},
            block_alphabit_report_file)
        block_alphabit_report_files.append(
            SummaryPerBat(block_alphabit_report_file.replace(execution_html_dir + "/", ""), f))

    generate_html_with_results("jinja_templates/index.html.j2",
                               {"bsi_files_list": bsi_report_files,
                                "fips_files_list": fips_report_files,
                                "nist_files_list": nist_report_files,
                                "dieharder_files_list": dh_report_files,
                                "rabbit_files_list": rabbit_report_files,
                                "alphabit_files_list": alphabit_report_files,
                                "block_alphabit_files_list": block_alphabit_report_files,
                                },
                               os.path.join(execution_html_dir, "index.html"))
    generate_summary_report()


if __name__ == "__main__":
    main()
