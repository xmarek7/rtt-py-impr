class LoggerSettings:
    def __init__(self, dict_from: dict):
        self.config_entries = [
            "dir-prefix",
            "run-log-dir",
            "dieharder-dir",
            "nist-sts-dir",
            "tu01-smallcrush-dir",
            "tu01-crush-dir",
            "tu01-bigcrush-dir",
            "tu01-rabbit-dir",
            "tu01-alphabit-dir",
            "tu01-blockalphabit-dir",
        ]
        self.dir_prefix = None
        self.run_log_dir = None
        self.dieharder_dir = None
        self.nist_sts_dir = None
        self.tu01_smallcrush_dir = None
        self.tu01_crush_dir = None
        self.tu01_bigcrush_dir = None
        self.tu01_rabbit_dir = None
        self.tu01_alphabit_dir = None
        self.tu01_blockalphabit_dir = None
        for key in self.config_entries:
            setattr(self, key.replace('-', '_'), dict_from.get(key))

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
        self.config_entries = [
            "main-file",
            "dir-prefix",
            "dieharder-dir",
            "nist-sts-dir",
            "tu01-smallcrush-dir",
            "tu01-crush-dir",
            "tu01-bigcrush-dir",
            "tu01-rabbit-dir",
            "tu01-alphabit-dir",
            "tu01-blockalphabit-dir",
        ]
        self.main_file = None
        self.dir_prefix = None
        self.dieharder_dir = None
        self.nist_sts_dir = None
        self.tu01_smallcrush_dir = None
        self.tu01_crush_dir = None
        self.tu01_bigcrush_dir = None
        self.tu01_rabbit_dir = None
        self.tu01_alphabit_dir = None
        self.tu01_blockalphabit_dir = None
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


class BinariesSettings:
    def __init__(self, dict_from: dict):
        self.config_entries = [
            "nist-sts",
            "dieharder",
            "testu01",
        ]
        self.nist_sts = None
        self.dieharder = None
        self.testu01 = None
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
