import pandas as pd

from results.bsi import BsiResult
from results.fips import FipsResult


def generate_csv_report(tested_files: list, batteries: list, report: dict) -> pd.DataFrame:
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
                    df.at[f"{test_result.test_name}_{test_result_idx} ({battery.upper()})", file] = extract_value_from_result(
                        test_result)
                    test_result_idx += 1

    return df


def get_test_list_of_battery(tested_files: list, battery: str, report: dict) -> set:
    tests = set()
    for file in tested_files:
        for result in report[file][battery]:
            tests.add(result.test_name)

    return tests


def find_test_results_for_file(tested_file: str, test_name: str, report: dict) -> list:
    test_result = list()
    for battery in report[tested_file].keys():
        for result in report[tested_file][battery]:
            if test_name == result.test_name:
                test_result.append(result)

    return test_result


def extract_value_from_result(result):
    # FIPS and BSI results are represented as number of failures
    if isinstance(result, BsiResult) or isinstance(result, FipsResult):
        return result.num_failures
    # rest of the batteries have p-value results
    else:
        return result.p_value
