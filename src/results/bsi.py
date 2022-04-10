from results.result_type import ResultType


class BsiResult:
    """Wrap result of single BSI test into a class.
        Each BSI test has a result that says if there was an error
        and if not, number of all runs and number of failed runs are returned
        by the battery.
    """
    def __init__(self, test_name: str, has_error: bool, num_runs: int, num_failures: int):
        """Initialize BsiResult class

        Args:
            test_name (str): Name of a test
            has_error (bool): If True, test result is not valid.
            num_runs (int): Number of runs made on a sequence
            num_failures (int): Number of failed runs.
        """
        self.test_name = test_name
        self.has_error = has_error
        self.num_runs = num_runs
        self.num_failures = num_failures
        self.result_type = ResultType.NUM_FAILURES

    def __repr__(self):
        return "BsiResult {\n" \
            f"\ttest_name: {self.test_name},\n" \
            f"\thas_error: {self.has_error},\n" \
            f"\tnum_runs: {self.num_runs},\n" \
            f"\tnum_failures: {self.num_failures}\n" \
            "}"
