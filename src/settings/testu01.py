from tools.misc import parse_test_ids


class TestU01Settings:
    def __init__(self, test_ids: list, repetitions, bit_nb, bit_r=None, bit_s=None):
        self.test_ids = test_ids
        self.repetitions = repetitions
        self.bit_nb = bit_nb
        self.bit_r = bit_r
        self.bit_s = bit_s


class RabbitSettings:
    def __init__(self, test_ids: list, repetitions, bit_nb, bit_r=None, bit_s=None):
        self.test_ids = test_ids
        self.repetitions = repetitions
        self.bit_nb = bit_nb
        self.bit_r = bit_r
        self.bit_s = bit_s


class AlphabitSettings:
    def __init__(self, test_ids: list, repetitions, bit_nb, bit_r, bit_s):
        self.test_ids = test_ids
        self.repetitions = repetitions
        self.bit_nb = bit_nb
        self.bit_r = bit_r
        self.bit_s = bit_s


class BlockAlphabitVariant:
    def __init__(self, repetitions, bit_nb, bit_r, bit_s, bit_w=None):
        self.repetitions = repetitions
        self.bit_nb = bit_nb
        self.bit_r = bit_r
        self.bit_s = bit_s
        self.bit_w = bit_w


class BlockAlphabitTestIdSettings:
    def __init__(self, test_id, variants: list):
        self.test_id = test_id
        self.variants = variants


class BlockAlphabitSettings:
    def __init__(self, test_ids: list, test_config: list):
        self.test_ids = test_ids
        self.per_test_config = test_config


class BlockAlphabitSettingsFactory:
    def make_settings(specific_settings_raw: list, test_ids: list, repetitions, bit_nb, bit_r, bit_s) -> BlockAlphabitSettings:
        per_tid_settings = list()
        for test_id in test_ids:
            per_tid_settings.append(BlockAlphabitTestIdSettings(
                test_id, [BlockAlphabitVariant(repetitions, bit_nb, bit_r, bit_s)]))
        for specs in specific_settings_raw:
            tid = int(specs["test-id"])
            variants = list()
            variants_raw = specs.get("variants")
            if variants_raw:
                for variant in variants_raw:
                    b_w = None if not variant.get(
                        "bit-w") else int(variant["bit-w"])
                    variants.append(BlockAlphabitVariant(
                        variant.get("repetitions", repetitions),
                        variant.get("bit-nb", bit_nb),
                        variant.get("bit-r", bit_r),
                        variant.get("bit-s", bit_s),
                        b_w))
            else:
                variants.append(BlockAlphabitVariant(
                    repetitions, bit_nb, bit_r, bit_s, None))
            for i in range(len(per_tid_settings)):
                if per_tid_settings[i].test_id == tid:
                    per_tid_settings[i].variants = variants
                    break
        return BlockAlphabitSettings(test_ids, per_tid_settings)


class TestU01SettingsFactory:
    def make_settings(dict_from: dict, test_kind: str):
        try:
            defaults = dict_from["defaults"]
            tids = parse_test_ids(defaults["test-ids"])
            reps = int(defaults["repetitions"])
            bit_nb = int(defaults["bit-nb"])
            bit_r = None if not defaults.get(
                "bit-r") else int(defaults["bit-r"])
            bit_s = None if not defaults.get(
                "bit-s") else int(defaults["bit-s"])
            if test_kind == "Rabbit":
                return RabbitSettings(tids, reps, bit_nb, bit_r, bit_s)
            elif test_kind == "Alphabit":
                return AlphabitSettings(tids, reps, bit_nb, bit_r, bit_s)
            elif test_kind == "BlockAlphabit":
                specific_settings_raw = dict_from["test-specific-settings"]
                return BlockAlphabitSettingsFactory.make_settings(specific_settings_raw, tids, reps, bit_nb, bit_r, bit_s)
        except:
            raise RuntimeError(
                "TestU01 settings don't contain required fields")
