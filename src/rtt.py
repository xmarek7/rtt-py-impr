import os
import json
import logging
from shutil import copytree

from settings.bsi import BsiSettings
from settings.nist import NistSettingsFactory
from settings.testu01 import TestU01SettingsFactory
from settings.dieharder import DieharderSettingsFactory
from settings.general import GeneralSettingsFactory, LoggerSettings

from executions.bsi import BsiExecution
from executions.fips import FipsExecution
from executions.nist import NistExecution
from executions.testu01 import TestU01Execution
from executions.dieharder import DieharderExecution

from tools.html_reports import generate_html_with_results, get_html_template_name
from tools.final_reports import finalize_bsi_fips_results, finalize_nist_results, finalize_dieharder_results


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
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    general_config = "/ws/rtt-py/tests/assets/configs/rtt-settings.json"
    test_spec = "/ws/rtt-py/tests/assets/configs/10MB.json"
    for file in [general_config, test_spec]:
        if not os.path.isfile(file):
            print(f"[ERROR] - File {file} does not exist")

    input_files = [
        "/ws/rtt-py/tests/assets/rnd/10MB.rnd",
        "/ws/rtt-statistical-batteries/bsi-src/assets/bsi_input.rnd",
    ]

    # general settings
    try:
        rtt_json = json.loads(
            open(general_config).read())["toolkit-settings"]
    except Exception as err:
        print(f"[ERROR] - Loading {general_config} failed. Reason:\n{err}")
        exit(1)
    general_settings = GeneralSettingsFactory.make_general_settings(rtt_json)

    # html reports
    html_root_dir = os.path.join(
        general_settings.storage.dir_prefix, "html", general_settings.logger.TIMESTAMP)
    os.makedirs(html_root_dir, exist_ok=True)
    # copy css files
    copytree("jinja_templates/css", os.path.join(html_root_dir, "css"))

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

    run_instance = dict()
    configured_batteries = ["fips"]
    # execution initialization
    # FIPS does not require any settings
    fips_execution = FipsExecution(general_settings)
    run_instance.update({
        "fips": {
            "execution_class": FipsExecution(general_settings),
            "results": list(),
            "html_summary": list(),
        }
    })
    if bsi_settings:
        run_instance.update({
            "bsi": {
                "execution_class": BsiExecution(bsi_settings, general_settings),
                "results": list(),
                "html_summary": list(),
            }
        })
        configured_batteries.append("bsi")

    if nist_settings:
        run_instance.update({
            "nist": {
                "execution_class": NistExecution(nist_settings, general_settings),
                "results": list(),
                "html_summary": list(),
            }
        })
        configured_batteries.append("nist")

    if dieharder_settings:
        run_instance.update({
            "dieharder": {
                "execution_class": DieharderExecution(dieharder_settings, general_settings),
                "results": list(),
                "html_summary": list(),
            }
        })
        configured_batteries.append("dieharder")

    if tu01_rabbit_settings:
        run_instance.update({
            "rabbit": {
                "execution_class": TestU01Execution(tu01_rabbit_settings, general_settings),
                "results": list(),
                "html_summary": list(),
            }
        })
        configured_batteries.append("rabbit")

    if tu01_alphabit_settings:
        run_instance.update({
            "alphabit": {
                "execution_class": TestU01Execution(tu01_alphabit_settings, general_settings),
                "results": list(),
                "html_summary": list(),
            }
        })
        configured_batteries.append("alphabit")

    if tu01_block_alphabit_settings:
        run_instance.update({
            "block_alphabit": {
                "execution_class": TestU01Execution(tu01_block_alphabit_settings, general_settings),
                "results": list(),
                "html_summary": list(),
            }
        })
        configured_batteries.append("block_alphabit")

    for per_battery_dir in configured_batteries:
        os.mkdir(os.path.join(html_root_dir, per_battery_dir))

    for input_file in input_files:
        input_file_basename = os.path.basename(input_file)
        html_result_file = input_file_basename + ".html"
        # generic exec
        for battery in configured_batteries:
            results = run_instance[battery]["execution_class"].execute_for_sequence(
                input_file)
            run_instance[battery]["results"].append(results)
            html_file = os.path.join(
                html_root_dir, battery, html_result_file)
            html_template = os.path.join(
                THIS_DIR, "..", "jinja_templates", get_html_template_name(battery))
            generate_html_with_results(
                # html_template,
                get_html_template_name(battery),
                {"tested_file": input_file,
                    "list_of_results": results, "battery": battery},
                html_file)
            run_instance[battery]["html_summary"].append(HtmlSummary(
                html_file.replace(html_root_dir + os.path.sep, ""), input_file))

    index_html_value_dict = dict()
    for battery in configured_batteries:
        index_html_value_dict.update(
            {f"{battery}_files_list": run_instance[battery]["html_summary"]})

    generate_html_with_results("index.html.j2",
                               index_html_value_dict,
                               os.path.join(html_root_dir, "index.html"))

    failure_percentage = []
    if "bsi" in configured_batteries:
        failure_percentage.extend(
            finalize_bsi_fips_results(run_instance["bsi"]["results"]))
    if "nist" in configured_batteries:
        failure_percentage.extend(
            finalize_nist_results(run_instance["nist"]["results"]))
    if "dieharder" in configured_batteries:
        failure_percentage.extend(
            finalize_dieharder_results(dieharder_settings))
    for percentage in failure_percentage:
        if percentage > 0.04:
            print("Generator failed")
            return
    print("Generator passed")


if __name__ == "__main__":
    main()
