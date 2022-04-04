class DieharderResult:
    def __init__(self, test_id: int, test_name: str,
                 ntuples: int, tsamples: int, psamples: int,
                 pvalue: float):
        """Wrap result of single DieHarder test into a class.
        The most important attribute is p_value because it is
        used for overall evaluation and has impact on final decision
        if generator was accepted or rejected.

        Args:
            test_id (int): Internal DieHarder test ID, not used by this codebase
            test_name (str): Name of a test
            ntuples (int): Number of tuples the test was configured with (see DieHarder docs)
            tsamples (int): Number of test samples (see DieHarder docs)
            psamples (int): Number of p-value samples used in test (see DieHarder docs)
            pvalue (float): P-value of a test (most important)
        """
        self.test_id = test_id
        self.test_name = test_name
        self.ntuples = ntuples
        self.tsamples = tsamples
        self.psamples = psamples
        self.p_value = pvalue

    def __repr__(self):
        return "DieharderResult {\n" \
            f"\ttest_id: {self.test_id},\n" \
            f"\ttest_name: {self.test_name},\n" \
            f"\tntuples: {self.ntuples},\n" \
            f"\ttsamples: {self.tsamples},\n" \
            f"\tpsamples: {self.psamples},\n" \
            f"\tpvalue: {self.p_value}\n" \
            "}"
