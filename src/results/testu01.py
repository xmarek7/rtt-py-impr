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
FIND_PVALUES_REGEX = re.compile(r"p-value of test\s{23}:\s+\d+\.\d+")

# after collecting lines containing p-values
# we must parse float number representing p-value:
EXTRACT_PVALUES_REGEX = re.compile(r"p-value of test\s{23}:\s+(\d+\.\d+)")


class TestU01Result:
    def __init__(self, statistics: str, p_value: float):
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
                    statistics = match.group(0).replace("CPU time used", "")
                    # collect all the lines containing pvals to a list
                    pvals = FIND_PVALUES_REGEX.findall(statistics)
                    for pval_str in pvals:
                        # extract the float from string
                        pval_match = EXTRACT_PVALUES_REGEX.match(pval_str)
                        pval = pval_match.group(1) if pval_match else None
                        if pval:  # no error, appending to return variable
                            results.append(TestU01Result(
                                statistics, float(pval)))
        return results
