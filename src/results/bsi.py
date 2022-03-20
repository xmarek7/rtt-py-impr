class BsiResult:
    def __init__(self, test_name: str, has_error: bool, num_runs: int, num_failures: int):
        self.test_name = test_name
        self.has_error = has_error
        self.num_runs = num_runs
        self.num_failures = num_failures

    def __repr__(self):
        return "BsiResult {\n" \
            f"\ttest_name: {self.test_name},\n" \
            f"\thas_error: {self.has_error},\n" \
            f"\tnum_runs: {self.num_runs},\n" \
            f"\tnum_failures: {self.num_failures}\n" \
            "}"
