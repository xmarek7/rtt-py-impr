import pytest
import unittest
import json
from settings.nist import NistSettingsFactory, NistSettings


NIST_JSON = """
{
    "nist-sts-settings": {
        "defaults": {
            "test-ids": ["1-15"],
            "stream-size": "1000000",
            "stream-count": "80"
        },
        "test-specific-settings": []
    }
}
"""


def _get_nist_settings() -> NistSettings:
    return NistSettingsFactory.make_settings(
        json.loads(NIST_JSON)["nist-sts-settings"])


class TestNistParsing(unittest.TestCase):
    def test_correctness(self):
        nist_settings = _get_nist_settings()
        assert nist_settings.test_ids == [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        assert nist_settings.stream_size == 1000000
        assert nist_settings.stream_count == 80


if __name__ == "__main__":
    unittest.main()
