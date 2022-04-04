import tools


class NistSettings:
    """User-defined nist settings are stored here. Unlike TU01 or DieHarder,
    NIST settings are very simple and currently don't support test variants.
    """
    def __init__(self, test_ids: list, stream_size, stream_count):
        self.test_ids = test_ids
        self.stream_size = stream_size
        self.stream_count = stream_count


class NistSettingsFactory:
    """Parses JSON battery config and creates NistSettings object"""
    def make_settings(test_settings_json: dict) -> NistSettings:
        settings = test_settings_json.get("nist-sts-settings")
        if not settings:
            raise Exception(
                "Configuration 'nist-sts-settings' was not specified")
        nist_settings = None
        try:
            defaults = settings["defaults"]
            test_ids = tools.misc.parse_test_ids(defaults["test-ids"])
            stream_size = int(defaults["stream-size"])
            stream_count = int(defaults["stream-count"])
            nist_settings = NistSettings(test_ids, stream_size, stream_count)
        except:
            raise RuntimeError("Nist settings don't contain required fields")
        return nist_settings
