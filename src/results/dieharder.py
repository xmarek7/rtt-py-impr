class DieharderResult:
    def __init__(self, test_id: int, test_name: str,
                 ntuples: int, tsamples: int, psamples: int,
                 pvalue: float):
        self.test_id = test_id
        self.test_name = test_name
        self.ntuples = ntuples
        self.tsamples = tsamples
        self.psamples = psamples
        self.pvalue = pvalue

    def __repr__(self):
        return "DieharderResult {\n" \
            f"\ttest_id: {self.test_id},\n" \
            f"\ttest_name: {self.test_name},\n" \
            f"\tntuples: {self.ntuples},\n" \
            f"\ttsamples: {self.tsamples},\n" \
            f"\tpsamples: {self.psamples},\n" \
            f"\tpvalue: {self.pvalue}\n" \
            "}"
