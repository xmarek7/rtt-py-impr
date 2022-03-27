import os
import json
import logging
from shutil import copytree
from results.bsi import BsiResult
from results.fips import FipsResult
from results.nist import NistResult

from settings.bsi import BsiSettings
from settings.nist import NistSettingsFactory
from settings.testu01 import TestU01SettingsFactory
from settings.dieharder import DieharderSettingsFactory
from settings.general import FileStorageSettings, BinariesSettings, GeneralSettingsFactory, LoggerSettings, ExecutionSettings

from executions.bsi import BsiExecution
from executions.fips import FipsExecution
from executions.nist import NistExecution
from executions.testu01 import TestU01Execution
from executions.dieharder import DieharderExecution

from tools.html_reports import generate_html_with_results
from tools.final_reports import finalize_bsi_fips_results, finalize_nist_results, finalize_dieharder_results


# TODO: better name
class HtmlSummary:
    def __init__(self, html_path, tested_file):
        self.html_path = html_path
        self.tested_file = tested_file


def init_logging(settings: LoggerSettings) -> logging.Logger:
    base_dir = settings.dir_prefix
    os.makedirs(base_dir, exist_ok=True)
    run_log_dir = settings.run_log_dir
    os.makedirs(run_log_dir, exist_ok=True)
    run_log_filename = settings.TIMESTAMP + "_run.log"
    run_log_file = os.path.join(run_log_dir, run_log_filename)
    main_logger = logging.getLogger()
    default_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s - %(message)s \n")
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(default_formatter)
    stdout_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(filename=run_log_file, mode="w")
    file_handler.setFormatter(default_formatter)
    file_handler.setLevel(logging.DEBUG)
    main_logger.addHandler(stdout_handler)
    main_logger.addHandler(file_handler)
    main_logger.setLevel(logging.DEBUG)
    return main_logger


def main():
    general_config = "/ws/rtt-py/tests/assets/configs/rtt-settings.json"
    test_spec = "/ws/rtt-py/tests/assets/configs/10MB.json"
    for file in [general_config, test_spec]:
        if not os.path.isfile(file):
            print(f"[ERROR] - File {file} does not exist")

    # general settings
    try:
        rtt_json = json.loads(
            open(general_config).read())["toolkit-settings"]
    except Exception as err:
        print(f"[ERROR] - Loading {general_config} failed. Reason:\n{err}")
        exit(1)
    general_settings = GeneralSettingsFactory.make_general_settings(rtt_json)

    main_logger = init_logging(general_settings.logger)

    # test settings
    try:
        test_settings = json.loads(open(
            test_spec).read())
        test_settings = test_settings.get("randomness-testing-toolkit")
        if not test_settings:
            raise Exception(
                f"File {test_spec} does not contain 'randomness-testing-toolkit' config entry")
    except Exception as err:
        main_logger.error(
            f"Loading {test_spec} failed. Reason:\n{err}")
        exit(1)

    # bsi test settings
    try:
        bsi_settings = BsiSettings(test_settings)
    except Exception as err:
        main_logger.warn(
            f"Settings for BSI battery provided in file {test_spec} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from BSI battery will not be executed")
        bsi_settings = None

    # nist test settings
    try:
        nist_settings = NistSettingsFactory.make_settings(
            test_settings)
    except Exception as err:
        main_logger.warn(
            f"Settings for NIST battery provided in file {test_spec} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from NIST battery will not be executed")
        nist_settings = None

    # DieHarder test settings
    try:
        dieharder_settings = DieharderSettingsFactory.make_settings(
            test_settings)
    except Exception as err:
        main_logger.warn(
            f"Settings for DieHarder battery provided in file {test_spec} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from DieHarder battery will not be executed")
        dieharder_settings = None

    # TestU01 rabbit test settings
    try:
        tu01_rabbit_settings = TestU01SettingsFactory.make_settings(
            test_settings, "rabbit")
    except Exception as err:
        main_logger.warn(
            f"Settings for TU01-Rabbit battery provided in file {test_spec} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from TU01-Rabbit battery will not be executed")
        tu01_rabbit_settings = None

    # TestU01 alphabit test settings
    try:
        tu01_alphabit_settings = TestU01SettingsFactory.make_settings(
            test_settings, "alphabit")
    except Exception as err:
        main_logger.warn(
            f"Settings for TU01-Alphabit battery provided in file {test_spec} are not valid. Reason:\n{err}")
        main_logger.warn(
            "Tests from TU01-Alphabit battery will not be executed")
        tu01_alphabit_settings = None

    # TestU01 block-alphabit test settings
    try:
        tu01_block_alphabit_settings = TestU01SettingsFactory.make_settings(
            test_settings, "block_alphabit")
    except Exception as err:
        main_logger.warn(
            f"Settings for TU01-Block-Alphabit battery provided in file {test_spec} are not valid. Reason:\n{err}")
        main_logger.warn(
            "Tests from TU01-Block-Alphabit battery will not be executed")
        tu01_block_alphabit_settings = None

    # execution initialization
    bsi_execution = BsiExecution(bsi_settings, general_settings)
    fips_execution = FipsExecution(general_settings)
    nist_execution = NistExecution(nist_settings, general_settings)
    dieharder_execution = DieharderExecution(
        dieharder_settings, general_settings)
    tu01_rabbit_execution = TestU01Execution(
        tu01_rabbit_settings, general_settings)
    tu01_alphabit_execution = TestU01Execution(
        tu01_alphabit_settings, general_settings)
    tu01_block_alphabit_execution = TestU01Execution(
        tu01_block_alphabit_settings, general_settings)

    execution_html_dir = os.path.join(
        general_settings.storage.dir_prefix, "html", general_settings.logger.TIMESTAMP)
    os.makedirs(execution_html_dir, exist_ok=True)
    # just to have fancy html
    copytree("jinja_templates/css", os.path.join(execution_html_dir, "css"))

    configured_batteries = ["bsi", "fips", "nist",
                            "dieharder", "rabbit", "alphabit", "block_alphabit"]
    for per_battery_dir in configured_batteries:
        os.mkdir(os.path.join(execution_html_dir, per_battery_dir))

    bsi_report_files: list[HtmlSummary] = []
    fips_report_files: list[HtmlSummary] = []
    nist_report_files: list[HtmlSummary] = []
    dh_report_files: list[HtmlSummary] = []
    rabbit_report_files: list[HtmlSummary] = []
    alphabit_report_files: list[HtmlSummary] = []
    block_alphabit_report_files: list[HtmlSummary] = []

    all_bsi_results: list[list[BsiResult]] = []
    all_fips_results: list[list[FipsResult]] = []
    all_nist_results: list[list[NistResult]] = []

    input_files = [
        "/ws/rtt-py/tests/assets/rnd/10MB.rnd",
        "/ws/rtt-statistical-batteries/bsi-src/assets/bsi_input.rnd",
    ]
    for input_file in input_files:
        input_file_basename = os.path.basename(input_file)
        html_result_file = input_file_basename + ".html"
        # bsi exec
        bsi_results = bsi_execution.execute_for_sequence(input_file)
        all_bsi_results.append(bsi_results)
        bsi_report_file = os.path.join(
            execution_html_dir, "bsi", html_result_file)
        generate_html_with_results(
            "jinja_templates/bsi_template.html.j2",
            {"tested_file": input_file, "list_of_results": bsi_results},
            bsi_report_file)
        bsi_report_files.append(HtmlSummary(
            bsi_report_file.replace(execution_html_dir + "/", ""), input_file))
        # fips exec
        fips_results = fips_execution.execute_for_sequence(input_file)
        all_fips_results.append(fips_results)
        fips_bat_accepted = fips_results[0].battery_accepted if len(
            fips_results) > 0 else False
        fips_report_file = os.path.join(
            execution_html_dir, "fips", html_result_file)
        generate_html_with_results(
            "jinja_templates/fips_template.html.j2",
            {"tested_file": input_file, "battery_accepted": fips_bat_accepted,
                "list_of_results": fips_results},
            fips_report_file)
        fips_report_files.append(HtmlSummary(
            fips_report_file.replace(execution_html_dir + "/", ""), input_file))
        # nist exec
        nist_results = nist_execution.execute_for_sequence(input_file)
        all_nist_results.append(nist_results)
        nist_report_file = os.path.join(
            execution_html_dir, "nist", html_result_file)
        generate_html_with_results(
            "jinja_templates/nist_template.html.j2",
            {"tested_file": input_file, "list_of_results": nist_results},
            nist_report_file)
        nist_report_files.append(HtmlSummary(
            nist_report_file.replace(execution_html_dir + "/", ""), input_file))
        # dieharder exec
        dh_results = dieharder_execution.execute_for_sequence(input_file)
        dh_report_file = os.path.join(
            execution_html_dir, "dieharder", html_result_file)
        generate_html_with_results(
            "jinja_templates/dieharder_template.html.j2",
            {"tested_file": input_file, "list_of_results": dh_results},
            dh_report_file)
        dh_report_files.append(HtmlSummary(
            dh_report_file.replace(execution_html_dir + "/", ""), input_file))
        # rabbit exec
        rabbit_results = tu01_rabbit_execution.execute_for_sequence(input_file)
        rabbit_report_file = os.path.join(
            execution_html_dir, "rabbit", html_result_file)
        generate_html_with_results(
            "jinja_templates/testu01_template.html.j2",
            {"tested_file": input_file, "list_of_results": rabbit_results,
                "subbattery": "rabbit"},
            rabbit_report_file)
        rabbit_report_files.append(HtmlSummary(
            rabbit_report_file.replace(execution_html_dir + "/", ""), input_file))
        # alphabit exec
        alphabit_results = tu01_alphabit_execution.execute_for_sequence(
            input_file)
        alphabit_report_file = os.path.join(
            execution_html_dir, "alphabit", html_result_file)
        generate_html_with_results(
            "jinja_templates/testu01_template.html.j2",
            {"tested_file": input_file, "list_of_results": alphabit_results,
                "subbattery": "alphabit"},
            alphabit_report_file)
        alphabit_report_files.append(HtmlSummary(
            alphabit_report_file.replace(execution_html_dir + "/", ""), input_file))
        # block_alphabit exec
        block_alphabit_results = tu01_block_alphabit_execution.execute_for_sequence(
            input_file)
        block_alphabit_report_file = os.path.join(
            execution_html_dir, "block_alphabit", html_result_file)
        generate_html_with_results(
            "jinja_templates/testu01_template.html.j2",
            {"tested_file": input_file, "list_of_results": block_alphabit_results,
                "subbattery": "block_alphabit"},
            block_alphabit_report_file)
        block_alphabit_report_files.append(
            HtmlSummary(block_alphabit_report_file.replace(execution_html_dir + "/", ""), input_file))

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
    nist_failure_percentage = finalize_nist_results(all_nist_results)
    dh_failure_percentage = finalize_dieharder_results(
        dieharder_settings)
    bsi_failure_percentage = finalize_bsi_fips_results(all_bsi_results)
    fips_failure_percentage = finalize_bsi_fips_results(all_fips_results)
    failure_percentage = [
        *bsi_failure_percentage,
        *fips_failure_percentage,
        *nist_failure_percentage,
        *dh_failure_percentage
    ]
    for percentage in failure_percentage:
        if percentage > 0.04:
            print("Generator failed")
            return
    print("Generator passed")


if __name__ == "__main__":
    main()
