from tools.misc import parse_test_ids


class BsiSettings:
    """Object for storing BSI settings provided in JSON file
    """
    def __init__(self, test_settings_json: dict):
        """Initialize BsiSettings class

        Args:
            test_settings_json (dict): Parsed test config JSON file

        Raises:
            RuntimeError: Throws when some invalid or incomplete settings were found
        """
        settings = test_settings_json.get("bsi-settings")
        if not settings:
            raise RuntimeError("Configuration 'bsi-settings' was not specified")
        self.uniform_dist_K = None
        self.uniform_dist_N = None
        self.uniform_dist_A = None
        try:
            self.test_ids = parse_test_ids(settings["defaults"]["test-ids"])
            self.bytes_count = settings["defaults"]["bytes-count"]
            uniform_dist = settings["defaults"].get("uniform-distribution")
            if uniform_dist is not None:
                self.uniform_dist_K = str(uniform_dist["K-param"])
                self.uniform_dist_N = str(uniform_dist["N-param"])
                self.uniform_dist_A = str(uniform_dist["A-param"])
        except:
            raise RuntimeError("BSI settings contain invalid values")
