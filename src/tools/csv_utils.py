import logging
import re
import pandas as pd

from results.bsi import BsiResult
from results.fips import FipsResult
from results.result_type import ResultType


def generate_csv_report(tested_files: list, batteries: list, report: dict, alpha: float = 0.01, rejection_threshold: float = 0.04) -> pd.DataFrame:
    """Generate CSV report from main run report.

    Args:
        tested_files (list): List of files tested in the run
        batteries (list): List of configured batteries
        report (dict): Full report containing test results of all configured batteries
        alpha (float, optional): Alpha value for p-value threshold. Defaults to 0.01.
        rejection_threshold (float, optional): If failure percentage is above the threshold, reject generator. Defaults to 0.04.

    Returns:
        pd.DataFrame: dataframe containing all results and failure percentage of each test
    """
    df = pd.DataFrame()

    # initialize columns from list of tested files
    for file in tested_files:
        df[file] = []

    for battery in batteries:
        performed_tests = get_test_list_of_battery(
            tested_files, battery, report)
        for test in performed_tests:
            for file in tested_files:
                test_results = find_test_results_for_file(file, test, report)
                test_result_idx = 0  # needed to have unique indexes
                for test_result in test_results:
                    # indexing: rows are test names and cols are files
                    df.at[f"{test_result.test_name}_{test_result_idx} ({battery.upper()})",
                          file] = test_result.result_value
                    test_result_idx += 1

    rejection_column = "Failure rate"
    df.insert(0, rejection_column, None)
    for i in range(len(df)):
        test_name = str(df.iloc[i].name)
        result_type = get_result_type_by_test_name(test_name)
        if result_type == ResultType.NUM_FAILURES:
            df.at[test_name, rejection_column] = 1 - \
                (df.iloc[i, 1:] == 0).sum() / df.iloc[i, 1:].count()
        elif result_type == ResultType.P_VALUE:
            df.at[test_name, rejection_column] = 1 - \
                (df.iloc[i, 1:] > alpha).sum() / df.iloc[i, 1:].count()

    main_logger = logging.getLogger()
    above_rejection_th = (df[rejection_column] > rejection_threshold).sum()
    if above_rejection_th > 0:
        main_logger.error(f"[RESULT] - Generator was rejected")
    else:
        main_logger.error(f"[RESULT] - Generator was accepted")

    return df


def get_test_list_of_battery(tested_files: list, battery: str, report: dict) -> set:
    """For given battery, get all tests that were executed in a run.

    Args:
        tested_files (list): List of tested files
        battery (str): Battery name
        report (dict): Full run report

    Returns:
        set: Unique test names executed by battery
    """
    tests = set()
    for file in tested_files:
        for result in report[file][battery]:
            tests.add(result.test_name)

    return tests


def find_test_results_for_file(tested_file: str, test_name: str, report: dict) -> list:
    """Given test name, this function returns all the test instances of 'test_name' test
    that were executed for given 'tested_file'

    Args:
        tested_file (str): File for which tests should be searched
        test_name (str): Name of a test
        report (dict): Full run report

    Returns:
        list: All results of test with name 'test_name' executed for file 'tested_file'
    """
    test_result = list()
    for battery in report[tested_file].keys():
        for result in report[tested_file][battery]:
            if test_name == result.test_name:
                test_result.append(result)

    return test_result


def get_result_type_by_test_name(test_name: str) -> ResultType:
    """Extract battery name from test_name and return its ResultType enum value.
    Test names in DataFrame are stored as "{test_name} (battery_name)" so it's easy to extract
    battery name from test_name with regex.

    Args:
        test_name (str): Name of a test from dataframe

    Returns:
        str: Battery name
    """
    rgx = re.compile(r".* \((.*)\)$")
    match = rgx.match(test_name)
    if match:
        battery_name = match.group(1)
        if battery_name in ["FIPS", "BSI"]:
            return ResultType.NUM_FAILURES
        elif battery_name in ["NIST", "DIEHARDER", "RABBIT", "ALPHABIT", "BLOCK_ALPHABIT"]:
            return ResultType.P_VALUE
    return ResultType.UNKNOWN
