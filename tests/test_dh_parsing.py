import pytest
import unittest
import json
from settings.dieharder import DieharderSettingsFactory, DieharderSettings, DieharderVariant


DIEHARD_JSON = """
{
    "dieharder-settings": {
        "defaults": {
            "test-ids": ["0", "1", "3-4"],
            "psamples": 100
        },
        "test-specific-settings": [
            {
                "test-id": 0,
                "psamples": 65
            },
            {
                "test-id": 4,
                "variants": [
                    { "arguments": "-n 1", "psamples": 12 }
                ]
            },
            {
                "test-id": 100,
                "psamples": 0
            }
        ]
    }
}
"""


def _get_dieharder_settings() -> DieharderSettings:
    return DieharderSettingsFactory.make_settings(
        json.loads(DIEHARD_JSON)["dieharder-settings"])


class TestDieharderParsing(unittest.TestCase):
    def test_correctness(self):
        dieharder_settings = _get_dieharder_settings()
        assert dieharder_settings.test_ids == [0, 1, 3, 4]
        assert dieharder_settings.default_psamples == 100
        assert len(dieharder_settings.per_test_config) == 4
        for test_cfg in dieharder_settings.per_test_config:
            assert test_cfg.test_id in dieharder_settings.test_ids

    def test_tid_4(self):
        test_id_4 = None
        for i in _get_dieharder_settings().per_test_config:
            if i.test_id == 4:
                test_id_4 = i
        assert len(test_id_4.variants) == 1
        assert type(test_id_4.variants[0]) == type(DieharderVariant("", 0))
        assert test_id_4.variants[0].arguments == ["-n", "1"]
        assert test_id_4.variants[0].psamples == 12

if __name__ == "__main__":
    unittest.main()
