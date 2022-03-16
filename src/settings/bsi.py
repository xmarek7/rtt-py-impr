from tools.misc import parse_test_ids


class BsiSettings:
    def __init__(self, settings: dict):
        self.uniform_dist_K = None
        self.uniform_dist_N = None
        self.uniform_dist_A = None
        try:
            self.test_ids = parse_test_ids(settings["test-ids"])
            uniform_dist = settings.get("uniform-distribution")
            if uniform_dist is not None:
                self.uniform_dist_K = str(uniform_dist["K-param"])
                self.uniform_dist_N = str(uniform_dist["N-param"])
                self.uniform_dist_A = str(uniform_dist["A-param"])
        except:
            raise RuntimeError("BSI settings contain invalid values")
