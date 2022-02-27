import tools


class NistSettings:
    def __init__(self, test_ids: list, stream_size, stream_count):
        self.test_ids = test_ids
        self.stream_size = stream_size
        self.stream_count = stream_count


class NistSettingsFactory:
    """Parses JSON battery config and creates NistSettings object"""
    def make_settings(dict_from: dict) -> NistSettings:
        nist_settings = None
        try:
            defaults = dict_from["defaults"]
            test_ids = tools.misc.parse_test_ids(defaults["test-ids"])
            stream_size = int(defaults["stream-size"])
            stream_count = int(defaults["strea-count"])
            nist_settings = NistSettings(test_ids, stream_size, stream_count)
        except:
            raise RuntimeError("Nist settings don't contain required fields")
        return nist_settings
