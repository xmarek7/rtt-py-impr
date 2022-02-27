from tools.misc import parse_test_ids


class BsiSettings:
    def __init__(self, settings: dict):
        try:
            self.test_ids = parse_test_ids(settings["test-ids"])
            uniform_dist = settings["uniform-distribution"]
            self.uniform_dist_K = int(uniform_dist["K-param"])
            self.uniform_dist_N = int(uniform_dist["N-param"])
            self.uniform_dist_A = int(uniform_dist["A-param"])
        except:
            raise RuntimeError("BSI settings contain invalid values")
