from results.result_type import ResultType
from results.base_result import BaseResult


class FipsResult(BaseResult):
    """Wrap result of single FIPS test into a class.
    Since FIPS is a very small battery and is extremely simple,
    it produces only a number of failures and a number of runs
    on a particular sequence.
    """
    def __init__(self, battery_accepted: bool, test_name: str,
                 num_failures: int, num_runs: int):
        """Initialize FipsResult class

        Args:
            battery_accepted (bool): Information about acceptance of a generator by FIPS battery
            test_name (str): Name of a test
            num_failures (int): Number of failed runs
            num_runs (int): Number of runs
        """
        self.battery_accepted = battery_accepted
        self.test_name = test_name
        self.result_value = num_failures
        self.num_runs = num_runs
        self.result_type = ResultType.NUM_FAILURES

    def __repr__(self):
        return "FipsResult {\n" \
            f"\tbattery_accepted: {self.battery_accepted},\n" \
            f"\ttest_name: {self.test_name},\n" \
            f"\tnum_failures: {self.result_value},\n" \
            f"\tnum_runs: {self.num_runs}\n" \
            "}"
