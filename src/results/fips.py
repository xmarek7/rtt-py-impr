class FipsResult:
    def __init__(self, battery_accepted: bool, test_name: str,
                 num_failures: int, num_runs: int):
        self.battery_accepted = battery_accepted
        self.test_name = test_name
        self.num_failures = num_failures
        self.num_runs = num_runs

    def __repr__(self):
        return "FipsResult {\n" \
            f"\tbattery_accepted: {self.battery_accepted},\n" \
            f"\ttest_name: {self.test_name},\n" \
            f"\tnum_failures: {self.num_failures},\n" \
            f"\tnum_runs: {self.num_runs}\n" \
            "}"
