from tools.misc import parse_test_ids


class NistVariant:
    """Each NIST test with unique test ID can have multiple configurations.
    A user is allowed to request the same test to be executed with different parameters.
    Supported custom parameters are ['block-length', 'stream-size', 'stream-count'] 'block-length' affects only these tests:
    ["BlockFrequency", "NonOverlappingTemplate", "OverlappingTemplate" ,"ApproximateEntropy"
        "Serial", "LinearComplexity"]
    Arguments are passed directly as program options to nist binary.
    """

    def __init__(self, block_length: int, stream_size: int, stream_count: int):
        self.block_length = block_length
        self.stream_size = stream_size
        self.stream_count = stream_count


class NistTestIdSetting:
    """This class holds configured variants for one particular NIST test ID.
    """

    def __init__(self, test_id: int, variants: 'list[NistVariant]'):
        self.test_id: int = test_id
        self.variants: list[NistVariant] = variants


class NistSettings:
    """User-defined nist settings are stored here. Unlike TU01 or DieHarder,
    NIST settings are very simple and currently don't support test variants.
    """

    def __init__(self, test_ids: list, test_configs: 'list[NistTestIdSetting]'):
        self.test_ids: list[int] = test_ids
        self.per_test_config = test_configs


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
            default_test_ids = parse_test_ids(defaults["test-ids"])
            default_block_length = defaults.get("block-length")
            if default_block_length:
                default_block_length = int(default_block_length)
            default_stream_size = int(defaults["stream-size"])
            default_stream_count = int(defaults["stream-count"])
            per_tid_settings = list()
            for tid in default_test_ids:
                per_tid_settings.append(NistTestIdSetting(
                    int(tid), [NistVariant(default_block_length, default_stream_size, default_stream_count)]))
            specific_settings_raw = settings["test-specific-settings"]
            for specs in specific_settings_raw:
                tid = int(specs["test-id"])
                variants = list()
                variants_raw = specs.get("variants")
                if variants_raw:
                    for variant in variants_raw:
                        bl = variant.get("block-length")
                        ss = variant.get("stream-size")
                        sc = variant.get("stream-count")
                        if bl is None:
                            bl = default_block_length
                        if ss is None:
                            ss = default_stream_size
                        if sc is None:
                            sc = default_stream_count
                        variants.append(NistVariant(bl, ss, sc))
                else:
                    bl = specs.get("block-length")
                    ss = specs.get("stream-size")
                    sc = specs.get("stream-count")
                    if bl is None:
                        bl = default_block_length
                    if ss is None:
                        ss = default_stream_size
                    if sc is None:
                        sc = default_stream_count
                    variants.append(NistVariant(bl, ss, sc))
                for i in range(len(per_tid_settings)):
                    if per_tid_settings[i].test_id == tid:
                        per_tid_settings[i].variants = variants
                        break
            nist_settings = NistSettings(
                default_test_ids, per_tid_settings)
        except:
            raise RuntimeError("Nist settings don't contain required fields")
        return nist_settings
