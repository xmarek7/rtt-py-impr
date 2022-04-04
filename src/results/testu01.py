import re

# this constant splits multiple repetitions into a list.
# if we look at some example results that TestU01 battery prints out
# we can see that if repetitions parameter is > 1, there are multiple results
# and this line separates them consistently across all the subbatteries
# (i.e. alphabit, rabbit, crush, etc.)
SPLIT_MULTIPLE_REPETITIONS = "\nGenerator providing data from binary file.\n"


# next thing we want is to take a statistical part of the results and save them as strings
# from this string we later extract p-values.
EXTRACT_STATISTICS_REGEX = re.compile(
    r".* test:\n-{47}\n[\s\S\n]+?-{47}\nCPU time used")

# this only finds all the lines containing p-values
# lines with p-values look like this:
# p-value of test<23 spaces(that's why \s{23})>:<some spaces for alignment>0.123
# or (pvalue close to 1)
# p-value of test<23 spaces(that's why \s{23})>:<some spaces for alignment>1 - 8.9e-5
# or (pvalue close to 0)
# p-value of test<23 spaces(that's why \s{23})>:<some spaces for alignment>8.9e-5
FIND_PVALUES_REGEX = re.compile(r"p-value of test\s{23}:\s+\d.*")

# after collecting lines containing p-values
# we must parse float number representing p-value:
EXTRACT_PVALUES_REGEX = re.compile(r"p-value of test\s{23}:\s+(\d+\.\d+)")

# sometimes there is a p-value that's really close to 1
# and once that happens, TestU01 battery interprets the p-value
# in the following format:
# 0.999911 -> 1 - 8.9e-5
# so we need to check if the first regular expression fails
# and if it does we have to extract the value using this fallback regex:
EXTRACT_PVALUES_NEAR_1_REGEX = re.compile(
    r"p-value of test\s{23}:\s+1\s+-\s+(\d+.\d+e-\d+)\s+")

# similarly, if the p-value is close to 0,
# the same problem happens
# another fallback regex should handle that for us
EXTRACT_PVALUES_NEAR_0_REGEX = re.compile(
    r"p-value of test\s{23}:\s+(\d+.\d+e-\d+)\s+")

# test name is typically followed by 'test:' + 'newline' + 47 dashes '-'
EXTRACT_TEST_NAME = re.compile(r"(^.*) test:\n-{47}")


class TestU01Result:
    """Wraps result of one of the TestU01 battery tests.
    """
    def __init__(self, test_name, statistics: str, p_value: float):
        """Initialize TestU01Result class

        Args:
            test_name (_type_): Name of a test
            statistics (str): Statistics printed to STDOUT by TestU01 battery
            p_value (float): Parsed p-value from statistics
        """
        self.test_name = test_name
        self.statistics = statistics
        self.p_value = p_value

    def __repr__(self):
        return "TestU01Result {\n" \
            f"\tstatistics: {self.statistics},\n" \
            f"\tp-value: {self.p_value},\n" \
            "}"


class TestU01ResultFactory:
    def make_result(standard_output: str) -> 'list[TestU01Result]':
        """Factory method responsible for parsing STDOUT of TestU01 battery.

        Args:
            standard_output (str): STDOUT of testU01 battery

        Returns:
            list[TestU01Result]: Parsed list of test results.
            Length of list should be the same as repetitions parameter.
            Empty on error.
        """
        results: list[TestU01Result] = []
        # split the output in case of the repetitions parameter > 1
        results_split = standard_output.split(SPLIT_MULTIPLE_REPETITIONS)
        if len(results_split) > 1:
            # drop garbage before the first result output
            results_split = results_split[1:]
            for result in results_split:
                # match statistics of each result output
                match = EXTRACT_STATISTICS_REGEX.search(result)
                if match:
                    # save statistics printed to STDOUT
                    statistics = match.group(0).replace("CPU time used", "")
                    # parse test name from stdout
                    test_name = EXTRACT_TEST_NAME.match(statistics)
                    if test_name:
                        test_name = test_name.group(1)
                    else: # some exceptional output was produced
                        test_name = "TU01 UNKNOWN TEST"
                    # collect all the lines containing pvals to a list
                    # TODO: decide what to do with other pvalues
                    pval_line = FIND_PVALUES_REGEX.findall(
                        statistics)[-1]  # take last

                    numeric_pval = None
                    # do not change order of regexes!!!
                    # try matching the p-value that is close to 1
                    pval_match = EXTRACT_PVALUES_NEAR_1_REGEX.match(pval_line)
                    if pval_match:
                        # if pvalue is close to 1, we parse only second part of a number:
                        # for example: 1 - 8.9e-5
                        # will be parsed only as 8.9e-5
                        numeric_pval = 1 - float(pval_match.group(1))
                    else: # p-value was not close to 1
                        for regex in [EXTRACT_PVALUES_NEAR_0_REGEX, EXTRACT_PVALUES_REGEX]:
                            # try matching p-value that is close to 0
                            # and also a normal p-value, i.e. 0.123
                            pval_match = regex.match(pval_line)
                            if pval_match:
                                numeric_pval = float(pval_match.group(1))
                                break

                    if numeric_pval:  # no error, appending to return variable
                        results.append(TestU01Result(
                            test_name, statistics, numeric_pval))
        return results
