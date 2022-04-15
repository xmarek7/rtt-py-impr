import unittest
import json

from settings.testu01 import TestU01Settings as TU01Settings, TestU01SettingsFactory as TU01SettingsFactory


RABBIT_JSON = """
{
    "tu01-rabbit-settings": {
        "defaults": {
            "test-ids": ["1-2"],
            "repetitions": 1,
            "bit-nb": "10000000"
        }
    }
}
"""

ALPHABIT_JSON = """
{
    "tu01-alphabit-settings": {
        "defaults": {
            "test-ids": ["1-3"],
            "repetitions": 1,
            "bit-nb": "10000000",
            "bit-r": "0",
            "bit-s": "32"
        }
    }
}
"""

BLOCKALPHABIT_JSON = """
{
    "tu01-blockalphabit-settings": {
        "defaults": {
            "test-ids": ["1-4"],
            "repetitions": 1,
            "bit-nb": "10000000",
            "bit-r": "0",
            "bit-s": "32"
        },
        "test-specific-settings": [
            {
                "test-id": 1, "variants": [{ "bit-w": "1" }, { "bit-w": "2" }]
            }
        ]
    }
}
"""


SAMPLE_JSON = """
{
    "tu01-smallcrush-settings": {
        "defaults": {
            "test-ids": ["1-2"],
            "repetitions": 1
        },
        "test-specific-settings": [
            {
                "test-id": 2,
                "repetitions": 6
            }
        ]
    },
    "tu01-crush-settings": {
        "defaults": {
            "test-ids": ["1-2"],
            "repetitions": 1
        },
        "test-specific-settings": [
            {
                "test-id": 2,
                "repetitions": 6
            }
        ]
    },
    "tu01-bigcrush-settings": {
        "defaults": {
            "test-ids": ["1-2"],
            "repetitions": 1
        },
        "test-specific-settings": [
            {
                "test-id": 2,
                "repetitions": 6
            }
        ]
    },
    "tu01-rabbit-settings": {
        "defaults": {
            "test-ids": ["1-2"],
            "repetitions": 1,
            "bit-nb": "10000000"
        },
        "test-specific-settings": [
            {
                "test-id": 2,
                "repetitions": 6
            }
        ]
    },
    "tu01-alphabit-settings": {
        "defaults": {
            "test-ids": ["1"],
            "repetitions": 2,
            "bit-nb": 10000000
        },
        "test-specific-settings": [
            {
                "test-id": 1,
                "variants": [
                    {
                        "bit-r": "128",
                        "bit-s": "64"
                    },
                    {
                        "bit-r": "16"
                    }
                ]
            }
        ]
    },
    "tu01-blockalphabit-settings": {
        "defaults": {
            "test-ids": ["1-4"],
            "repetitions": 1,
            "bit-nb": "10000000",
            "bit-r": "0",
            "bit-s": "32",
            "bit-w": "32"
        },
        "test-specific-settings": [
            {
                "test-id": 1,
                "variants": [
                    { "bit-w": "128" },
                    { "bit-w": "16" }
                ]
            }
        ]
    }
}
"""


def _get_rabbit() -> TU01Settings:
    return TU01SettingsFactory.make_settings(
        json.loads(RABBIT_JSON), "rabbit")


def _get_alphabit() -> TU01Settings:
    return TU01SettingsFactory.make_settings(
        json.loads(ALPHABIT_JSON), "alphabit")


def _get_blockalphabit() -> TU01Settings:
    return TU01SettingsFactory.make_settings(
        json.loads(BLOCKALPHABIT_JSON), "block_alphabit")


class TU01Parsing(unittest.TestCase):
    def test_correctness_rabbit(self):
        rabbit = _get_rabbit()
        assert rabbit.test_ids == [1, 2]
        assert rabbit.subbattery == "rabbit"
        for tid_settings in rabbit.per_test_id_settings:
            assert tid_settings.test_id in [1, 2]
            for var in tid_settings.variants:
                assert var.bit_nb == 10000000
                assert var.bit_r == None
                assert var.bit_s == None
                assert var.bit_w == None

    def test_correctness_blockalphabit(self):
        blockalpha = _get_blockalphabit()
        assert blockalpha.test_ids == [1, 2, 3, 4]
        assert len(blockalpha.per_test_id_settings) == 4
        assert blockalpha.subbattery == "block_alphabit"
        for per_test_id_settings in blockalpha.per_test_id_settings:
            for blockalpha_variant in per_test_id_settings.variants:
                assert blockalpha_variant.repetitions == 1
                assert blockalpha_variant.bit_nb == 10000000
                assert blockalpha_variant.bit_r == 0
                assert blockalpha_variant.bit_s == 32
                if per_test_id_settings.test_id == 1:
                    assert blockalpha_variant.bit_w == 1 or blockalpha_variant.bit_w == 2

    def test_correctness_alphabit(self):
        alpha = _get_alphabit()
        assert alpha.test_ids == [1, 2, 3]
        assert alpha.subbattery == "alphabit"
        for tid_settings in alpha.per_test_id_settings:
            assert tid_settings.test_id in [1, 2, 3]
            for var in tid_settings.variants:
                assert var.repetitions == 1
                assert var.bit_nb == 10000000
                assert var.bit_r == 0
                assert var.bit_s == 32


if __name__ == "__main__":
    unittest.main()
