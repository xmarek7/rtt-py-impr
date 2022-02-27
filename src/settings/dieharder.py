from tools.misc import parse_test_ids


class DieharderVariant:
    def __init__(self, arguments, psamples):
        self.arguments = arguments
        self.psamples = psamples


class DieharderSpecificSettings:
    def __init__(self, test_id, variants: list):
        self.test_id = test_id
        self.variants = variants


class DieharderSettings:
    def __init__(self, test_ids: list, default_psamples, variants: list):
        self.test_ids = test_ids
        self.default_psamples = default_psamples
        self.variants = variants
        
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
            specific_settings = list()
            for tid in default_test_ids:  # fill specific_settings array with default settings, override later
                specific_settings.append(DieharderSpecificSettings(
                    tid, [DieharderVariant("", default_psamples)]))
            specific_settings_raw = dict_from["test-specific-settings"]
            for specs in specific_settings_raw:
                tid = int(specs["test-id"])
                variants = list()
                variants_raw = specs.get("variants")
                if variants_raw:
                    for variant in variants_raw:
                        variants.append(DieharderVariant(
                            variant["arguments"], variant["psamples"]))
                else:
                    psamples = specs["psamples"]
                    variants.append(DieharderVariant("", psamples))
                for i in range(len(specific_settings)):
                    if specific_settings[i] == tid:
                        specific_settings[i].variants = variants
                        break
            dieharder_settings = DieharderSettings(
                default_test_ids, default_psamples, specific_settings)
        except:
            raise RuntimeError(
                "Dieharder settings don't contain required fields")
        return dieharder_settings
