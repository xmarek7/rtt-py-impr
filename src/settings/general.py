import os

class LoggerSettings:
    def __init__(self, dict_from: dict):
        self.dir_prefix = dict_from["dir-prefix"]
        self.config_entries = [
            "run-log-dir",
            "dieharder-dir",
            "nist-sts-dir",
            "tu01-smallcrush-dir",
            "tu01-crush-dir",
            "tu01-bigcrush-dir",
            "tu01-rabbit-dir",
            "tu01-alphabit-dir",
            "tu01-blockalphabit-dir",
            "fips-dir",
            "bsi-dir",
        ]
        self.run_log_dir = None
        self.dieharder_dir = None
        self.nist_sts_dir = None
        self.tu01_smallcrush_dir = None
        self.tu01_crush_dir = None
        self.tu01_bigcrush_dir = None
        self.tu01_rabbit_dir = None
        self.tu01_alphabit_dir = None
        self.tu01_blockalphabit_dir = None
        self.fips_dir = None
        self.bsi_dir = None
        for key in self.config_entries:
            setattr(self, key.replace('-', '_'), os.path.join(self.dir_prefix, dict_from[key]))

    def __str__(self):
        __str = "# " + self.__class__.__name__ + " {\n"
        for key in self.config_entries:
            __attribute = key.replace('-', '_')
            __str += "\t" + __attribute + ": " + \
                getattr(self, __attribute) + "\n"
        __str += "}"
        return __str


class FileStorageSettings:
    def __init__(self, dict_from: dict):
        self.main_file = dict_from["main-file"]
        self.dir_prefix = dict_from["dir-prefix"]
        self.config_entries = [
            "dieharder-dir",
            "nist-sts-dir",
            "tu01-smallcrush-dir",
            "tu01-crush-dir",
            "tu01-bigcrush-dir",
            "tu01-rabbit-dir",
            "tu01-alphabit-dir",
            "tu01-blockalphabit-dir",
            "fips-dir",
            "bsi-dir",
        ]
        self.dieharder_dir = None
        self.nist_sts_dir = None
        self.tu01_smallcrush_dir = None
        self.tu01_crush_dir = None
        self.tu01_bigcrush_dir = None
        self.tu01_rabbit_dir = None
        self.tu01_alphabit_dir = None
        self.tu01_blockalphabit_dir = None
        self.fips_dir = None
        self.bsi_dir = None
        for key in self.config_entries:
            setattr(self, key.replace('-', '_'), os.path.join(self.dir_prefix, dict_from[key]))

    def __str__(self):
        __str = "# " + self.__class__.__name__ + " {\n"
        for key in self.config_entries:
            __attribute = key.replace('-', '_')
            __str += "\t" + __attribute + ": " + \
                str(getattr(self, __attribute)) + "\n"
        __str += "}"
        return __str


class BinariesSettings:
    def __init__(self, dict_from: dict):
        self.config_entries = [
            "nist-sts",
            "dieharder",
            "testu01",
            "fips",
            "bsi",
        ]
        self.nist_sts = None
        self.dieharder = None
        self.testu01 = None
        self.fips = None
        self.bsi = None
        for key in self.config_entries:
            setattr(self, key.replace('-', '_'), dict_from.get(key))

    def __str__(self):
        __str = "# " + self.__class__.__name__ + " {\n"
        for key in self.config_entries:
            __attribute = key.replace('-', '_')
            __str += "\t" + __attribute + ": " + \
                str(getattr(self, __attribute)) + "\n"
        __str += "}"
        return __str


class ExecutionSettings:
    def __init__(self, dict_from: dict):
        self.config_entries = [
            "max-parallel-tests",
            "test-timeout-seconds",
        ]
        self.max_parallel_tests = None
        self.test_timeout_seconds = None
        for key in self.config_entries:
            setattr(self, key.replace('-', '_'), dict_from.get(key))

    def __str__(self):
        __str = "# " + self.__class__.__name__ + " {\n"
        for key in self.config_entries:
            __attribute = key.replace('-', '_')
            __str += "\t" + __attribute + ": " + \
                str(getattr(self, __attribute)) + "\n"
        __str += "}"
        return __str
