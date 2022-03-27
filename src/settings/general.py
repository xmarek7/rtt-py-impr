import datetime
import os


class LoggerSettings:
    def __init__(self, dict_from: dict):
        self.dir_prefix = os.path.abspath(dict_from["dir-prefix"])
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
            setattr(self, key.replace('-', '_'),
                    os.path.join(self.dir_prefix, dict_from[key]))
        self.TIMESTAMP = datetime.datetime.now().isoformat()

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
            setattr(self, key.replace('-', '_'),
                    os.path.join(self.dir_prefix, dict_from[key]))

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


class GeneralSettings:
    def __init__(self,
                 logger_settings: LoggerSettings,
                 storage_settings: FileStorageSettings,
                 binaries_settings: BinariesSettings,
                 execution_settings: ExecutionSettings):
        self.logger = logger_settings
        self.storage = storage_settings
        self.binaries = binaries_settings
        self.execution = execution_settings


class GeneralSettingsFactory:
    def make_general_settings(toolkit_settings_json: str) -> GeneralSettings:
        """Takes json string containing app settings
        and parses it into classes representing general settings.

        Args:
            json_settings (str): JSON as string containing general settings
        """
        try:
            logger_settings = LoggerSettings(toolkit_settings_json["logger"])
        except Exception as err:
            print("Failed to parse LOGGER settings")
            raise err
        try:
            file_storage_settings = FileStorageSettings(
                toolkit_settings_json["result-storage"]["file"])
        except Exception as err:
            print("Failed to parse FILE_STORAGE settings")
            raise err
        try:
            binaries_settings = BinariesSettings(toolkit_settings_json["binaries"])
        except Exception as err:
            print("Failed to parse BINARIES settings")
            raise err
        try:
            execution_settings = ExecutionSettings(toolkit_settings_json["execution"])
        except Exception as err:
            print("Failed to parse EXECUTION settings")
            raise err

        return GeneralSettings(
            logger_settings,
            file_storage_settings,
            binaries_settings,
            execution_settings)
