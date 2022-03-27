from tools.misc import parse_test_ids


class DieharderVariant:
    def __init__(self, arguments: 'list[str]', psamples):
        self.arguments = arguments
        self.psamples = psamples
        # incremented by execution class:
        self.passed_variants = 0
        self.executed_variants = 0


class DieharderTestIdSetting:
    def __init__(self, test_id: int, variants: 'list[DieharderVariant]'):
        self.test_id: int = test_id
        self.variants = variants


class DieharderSettings:
    def __init__(self, test_ids: list, default_psamples, test_configs: 'list[DieharderTestIdSetting]'):
        self.test_ids: list[int] = test_ids
        self.default_psamples = default_psamples
        self.per_test_config = test_configs

    def __str__(self):
        __out = "# " + str(self.__class__.__name__) + " {\n"
        __out += "\tTest IDs: " + ", ".join(str(x) for x in self.test_ids)
        return __out


class DieharderSettingsFactory:
    def make_settings(dict_from: dict) -> DieharderSettings:
        dieharder_settings = None
        try:
            defaults = dict_from["defaults"]
            default_test_ids = parse_test_ids(defaults["test-ids"])
            default_psamples = defaults["psamples"]
            per_tid_settings = list()
            for tid in default_test_ids:  # fill per_tid_settings array with default settings, override later
                per_tid_settings.append(DieharderTestIdSetting(
                    int(tid), [DieharderVariant([], default_psamples)]))  # defaults for each test id
            specific_settings_raw = dict_from["test-specific-settings"]
            for specs in specific_settings_raw:
                tid = int(specs["test-id"])
                variants = list()
                variants_raw = specs.get("variants")
                if variants_raw:
                    for variant in variants_raw:
                        variants.append(DieharderVariant(
                            variant["arguments"].split(" "), variant["psamples"]))
                else:
                    psamples = specs["psamples"]
                    variants.append(DieharderVariant("", psamples))
                for i in range(len(per_tid_settings)):
                    if per_tid_settings[i].test_id == tid:
                        per_tid_settings[i].variants = variants
                        break
            dieharder_settings = DieharderSettings(
                default_test_ids, default_psamples, per_tid_settings)
        except:
            raise RuntimeError(
                "Dieharder settings don't contain required fields")
        return dieharder_settings
