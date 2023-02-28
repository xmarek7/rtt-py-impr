import argparse
import os
import sys
import json
import logging
from shutil import copytree

from settings.bsi import BsiSettings
from settings.fips import FipsSettings
from settings.nist import NistSettingsFactory
from settings.testu01 import TestU01SettingsFactory
from settings.dieharder import DieharderSettingsFactory
from settings.general import GeneralSettingsFactory, LoggerSettings

from executions.bsi import BsiExecution
from executions.fips import FipsExecution
from executions.nist import NistExecution
from executions.testu01 import TestU01Execution
from executions.dieharder import DieharderExecution

from tools.csv_utils import generate_csv_report
from tools.html_reports import generate_html_with_results, get_html_template_name
from tools.misc import gather_files
from program_arguments import parse_arguments


class HtmlSummary:
    def __init__(self, html_path, tested_file):
        self.html_path = html_path
        self.tested_file = tested_file


def init_logging(settings: LoggerSettings) -> logging.Logger:
    base_dir = settings.dir_prefix
    run_log_dir = settings.run_log_dir
    try:
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(run_log_dir, exist_ok=True)
    except Exception as err:
        print(f"Unable to create directories for logging. Reason {err}")
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


def main(args: argparse.Namespace):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    allowed_failure = args.allowed_failure
    alpha = args.alpha

    general_settings = args.general_settings
    test_settings = args.test_settings
    for file in [general_settings, test_settings]:
        if not os.path.isfile(file):
            print(f"[ERROR] - File {file} does not exist")

    # general settings
    try:
        rtt_json = json.loads(
            open(general_settings).read())["toolkit-settings"]
    except Exception as err:
        print(f"[ERROR] - Loading {general_settings} failed. Reason:\n{err}")
        exit(1)
    general_settings = GeneralSettingsFactory.make_general_settings(rtt_json)

    main_logger = init_logging(general_settings.logger)

    input_files = []
    if args.inputs_dir:
        if not os.path.isdir(args.inputs_dir):
            main_logger.error(f"Inputs dir {args.inputs_dir} does not exist")
        else:
            input_files.extend(
                gather_files(args.inputs_dir, args.extensions))
            main_logger.info(f"Batch-processing directory: {args.inputs_dir}")
    else:
        if not os.path.isfile(args.input_file):
            main_logger.error(f"Input file {args.input_file} does not exist")
        else:
            input_files.append(args.input_file)
            main_logger.info(f"Processing single file: {args.input_file}")

    if len(input_files) == 0:
        main_logger.error("No input files were provided")
        sys.exit(1)

    # html reports
    html_root_dir = os.path.join(
        general_settings.storage.dir_prefix, "html", general_settings.logger.TIMESTAMP)
    os.makedirs(html_root_dir, exist_ok=True)
    html_result_table_filename = "results.html"
    html_result_table_file = os.path.join(
        html_root_dir, html_result_table_filename)
    # copy css files
    copytree(os.path.join(THIS_DIR, "..", "jinja_templates", "css"),
             os.path.join(html_root_dir, "css"))

    # test settings
    try:
        test_settings = json.loads(open(
            test_settings).read())
        test_settings = test_settings.get("randomness-testing-toolkit")
        if not test_settings:
            raise Exception(
                f"File {test_settings} does not contain 'randomness-testing-toolkit' config entry")
    except Exception as err:
        main_logger.error(
            f"Loading {test_settings} failed. Reason:\n{err}")
        exit(1)

    # bsi test settings
    bsi_settings = None
    try:
        if not args.no_bsi:
            bsi_settings = BsiSettings(test_settings)
        else:
            main_logger.info("BSI battery was omitted by user")
    except Exception as err:
        main_logger.warn(
            f"Settings for BSI battery provided in file {test_settings} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from BSI battery will not be executed")

    # fips test settings
    fips_settings = None
    try:
        if not args.no_fips:
            fips_settings = FipsSettings(test_settings)
        else:
            main_logger.info("FIPS battery was omitted by user")
    except Exception as err:
        main_logger.warn(
            f"Settings for FIPS battery provided in file {test_settings} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from FIPS battery will not be executed")

    # nist test settings
    nist_settings = None
    try:
        if not args.no_nist:
            nist_settings = NistSettingsFactory.make_settings(
                test_settings)
        else:
            main_logger.info("NIST battery was omitted by user")
    except Exception as err:
        main_logger.warn(
            f"Settings for NIST battery provided in file {test_settings} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from NIST battery will not be executed")

    # DieHarder test settings
    dieharder_settings = None
    try:
        if not args.no_dieharder:
            dieharder_settings = DieharderSettingsFactory.make_settings(
                test_settings)
        else:
            main_logger.info("DieHarder battery was omitted by user")
    except Exception as err:
        main_logger.warn(
            f"Settings for DieHarder battery provided in file {test_settings} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from DieHarder battery will not be executed")

    # TestU01 rabbit test settings
    tu01_rabbit_settings = None
    try:
        if not args.no_tu01_rabbit and not args.no_tu01:
            tu01_rabbit_settings = TestU01SettingsFactory.make_settings(
                test_settings, "rabbit")
        else:
            main_logger.info("TU01-Rabbit battery was omitted by user")
    except Exception as err:
        main_logger.warn(
            f"Settings for TU01-Rabbit battery provided in file {test_settings} are not valid. Reason:\n{err}")
        main_logger.warn("Tests from TU01-Rabbit battery will not be executed")

    # TestU01 alphabit test settings
    tu01_alphabit_settings = None
    try:
        if not args.no_tu01_alphabit and not args.no_tu01:
            tu01_alphabit_settings = TestU01SettingsFactory.make_settings(
                test_settings, "alphabit")
        else:
            main_logger.info("TU01-Alphabit battery was omitted by user")
    except Exception as err:
        main_logger.warn(
            f"Settings for TU01-Alphabit battery provided in file {test_settings} are not valid. Reason:\n{err}")
        main_logger.warn(
            "Tests from TU01-Alphabit battery will not be executed")

    # TestU01 block-alphabit test settings
    tu01_block_alphabit_settings = None
    try:
        if not args.no_tu01_blockalphabit and not args.no_tu01:
            tu01_block_alphabit_settings = TestU01SettingsFactory.make_settings(
                test_settings, "block_alphabit")
        else:
            main_logger.info("TU01-Block-Alphabit battery was omitted by user")
    except Exception as err:
        main_logger.warn(
            f"Settings for TU01-Block-Alphabit battery provided in file {test_settings} are not valid. Reason:\n{err}")
        main_logger.warn(
            "Tests from TU01-Block-Alphabit battery will not be executed")

    # execution initialization
    run_instance = dict()
    configured_batteries = list()
    if not args.no_fips:
        run_instance.update({
            "fips": {
                "execution_class": FipsExecution(fips_settings, general_settings),
                "results": list(),
                "html_summary": list(),
            }
        })
        configured_batteries.append("fips")
    else:
        main_logger.info("FIPS battery was omitted by user")
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

    full_report = dict()
    for input_file in input_files:
        main_logger.info(f"Current file being processed: {input_file}")
        html_result_file = os.path.basename(input_file) + ".html"

        for battery in configured_batteries:
            results = run_instance[battery]["execution_class"].execute_for_sequence(
                input_file)
            run_instance[battery]["results"].append(results)
            if input_file in full_report:
                full_report[input_file].update({battery: results})
            else:
                full_report[input_file] = {battery: results}
            html_file = os.path.join(
                html_root_dir, battery, html_result_file)
            generate_html_with_results(
                get_html_template_name(battery),
                {"tested_file": input_file,
                    "list_of_results": results, "battery": battery},
                html_file)
            run_instance[battery]["html_summary"].append(HtmlSummary(
                html_file.replace(html_root_dir + os.path.sep, ""), input_file))
        main_logger.info(f"Done processing file: {input_file}")

    index_html_value_dict = {"results_html_file": html_result_table_filename}
    for battery in configured_batteries:
        index_html_value_dict.update(
            {f"{battery}_files_list": run_instance[battery]["html_summary"]})

    generate_html_with_results("index.html.j2",
                               index_html_value_dict,
                               os.path.join(html_root_dir, "index.html"))

    # save csv to file
    csv_file = os.path.join(
        general_settings.storage.dir_prefix, "csv", general_settings.logger.TIMESTAMP, "report.csv")
    os.makedirs(os.path.dirname(csv_file))

    # generate csv
    try:
        df = generate_csv_report(
            input_files, configured_batteries, full_report, alpha, allowed_failure)
        df.to_csv(csv_file, float_format="{:.8f}".format)
        main_logger.info(f"Saving CSV report into: {csv_file}")
    except Exception as err:
        main_logger.error(f"Failed to generate CSV report. Reason: {err}")
        sys.exit(1)

    # save csv as html
    try:
        html_results_table = df.to_html()
        generate_html_with_results("results.html.j2",
                                   {"results_table": html_results_table},
                                   html_result_table_file)
    except Exception as err:
        main_logger.error(
            f"Failed to generate HTML from DataFrame. Reason: {err}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
    sys.exit(0)
