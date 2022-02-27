from modulefinder import STORE_GLOBAL
import unittest
import json

from settings.general import ExecutionSettings, LoggerSettings, BinariesSettings, FileStorageSettings

LOGGER_JSON = """
{
    "logger": {
        "dir-prefix": "results/logs",
        "run-log-dir": "run-logs",
        "dieharder-dir": "dieharder",
        "nist-sts-dir": "niststs",
        "tu01-smallcrush-dir": "testu01/smallcrush",
        "tu01-crush-dir": "testu01/crush",
        "tu01-bigcrush-dir": "testu01/bigcrush",
        "tu01-rabbit-dir": "testu01/rabbit",
        "tu01-alphabit-dir": "testu01/alphabit",
        "tu01-blockalphabit-dir": "testu01/blockalphabit",
        "fips-dir": "fips",
        "bsi-dir": "bsi"
    }
}
"""

RESULT_STORAGE_JSON = """
{
    "result-storage": {
        "file": {
            "main-file": "results/testbed-table.txt",
            "dir-prefix": "results/reports",
            "dieharder-dir": "dieharder",
            "nist-sts-dir": "niststs",
            "tu01-smallcrush-dir": "testu01/smallcrush",
            "tu01-crush-dir": "testu01/crush",
            "tu01-bigcrush-dir": "testu01/bigcrush",
            "tu01-rabbit-dir": "testu01/rabbit",
            "tu01-alphabit-dir": "testu01/alphabit",
            "tu01-blockalphabit-dir": "testu01/blockalphabit",
            "fips-dir": "fips",
            "bsi-dir": "bsi"
        }
    }
}
"""

BINARIES_JSON = """
{
    "binaries": {
        "nist-sts": "nist-sts",
        "dieharder": "dieharder",
        "testu01": "testu01",
        "fips": "fips_battery",
        "bsi": "bsi_battery"
    }
}
"""

EXECUTION_JSON = """
{
    "execution": {
        "max-parallel-tests": 8,
        "test-timeout-seconds": 3600
    }
}
"""

# TODO: More sophisticated tests
class TestGeneralSettings(unittest.TestCase):
    def test_filestorage(self):
        FileStorageSettings(json.loads(RESULT_STORAGE_JSON)["result-storage"]["file"])

    def test_execution(self):
        ExecutionSettings(json.loads(EXECUTION_JSON)["execution"])

    def test_binaries(self):
        binaries = BinariesSettings(json.loads(BINARIES_JSON)["binaries"])
        assert binaries.dieharder == "dieharder"
        assert binaries.nist_sts == "nist-sts"
        assert binaries.testu01 == "testu01"
        assert binaries.fips == "fips_battery"
        assert binaries.bsi == "bsi_battery"

    def test_logger(self):
        LoggerSettings(json.loads(LOGGER_JSON)["logger"])
