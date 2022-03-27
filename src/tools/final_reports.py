from cmath import sqrt
from results.bsi import BsiResult
from results.fips import FipsResult
from results.dieharder import DieharderResult
from results.nist import NistResult
from results.testu01 import TestU01Result

ALPHA = 0.01


def finalize_nist_results_for_one_test(nist_results: 'list[list[NistResult]]', test_name: str, max_instances: int) -> 'list[float]':
    num_passed = [0] * max_instances
    num_interpretable = [0] * max_instances
    for file_results in nist_results:
        relevant_tests: list[NistResult] = []
        for test_result in file_results:
            if test_name == test_result.test_name:
                relevant_tests.append(test_result)
        for i in range(len(relevant_tests)):
            pval = relevant_tests[i].p_value
            if pval > ALPHA:
                num_passed[i] += 1
            num_interpretable[i] += 1
    results = []
    for i in range(len(num_passed)):
        rejected_percentage = 1 - num_passed[i] / num_interpretable[i]
        results.append(rejected_percentage)

    return results


def finalize_nist_results(nist_results: 'list[list[NistResult]]') -> 'list[float]':
    max_num_results = 0
    for file_results in nist_results:
        if len(file_results) > max_num_results:
            max_num_results = len(file_results)
    # get unique test names
    unique_test_names = set()
    for file_results in nist_results:
        for test_result in file_results:
            unique_test_names.add(test_result.test_name)

    max_instances_per_test = dict()
    for test_name in unique_test_names:
        max_results = 0
        for file_results in nist_results:
            num_results = 0
            for test_result in file_results:
                if test_result.test_name == test_name:
                    num_results += 1
            if num_results > max_results:
                max_results = num_results
        max_instances_per_test.update({test_name: max_results})

    rejection_percentage = list()
    for test_name in unique_test_names:
        percentage_for_test = finalize_nist_results_for_one_test(nist_results, test_name, max_instances_per_test[test_name])
        rejection_percentage.extend(percentage_for_test)

    return rejection_percentage
