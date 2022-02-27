import unittest
import json

from settings.testu01 import AlphabitSettings, BlockAlphabitSettingsFactory, BlockAlphabitSettings, RabbitSettings, TestU01SettingsFactory


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


def _get_rabbit() -> RabbitSettings:
    return TestU01SettingsFactory.make_settings(
        json.loads(RABBIT_JSON)["tu01-rabbit-settings"], "Rabbit")


def _get_alphabit() -> AlphabitSettings:
    return TestU01SettingsFactory.make_settings(
        json.loads(ALPHABIT_JSON)["tu01-alphabit-settings"], "Alphabit")


def _get_blockalphabit() -> BlockAlphabitSettings:
    return TestU01SettingsFactory.make_settings(
        json.loads(BLOCKALPHABIT_JSON)["tu01-blockalphabit-settings"], "BlockAlphabit")


class TestU01Parsing(unittest.TestCase):
    def test_correctness_rabbit(self):
        rabbit = _get_rabbit()
        assert rabbit.test_ids == [1, 2]
        assert rabbit.bit_nb == 10000000
        assert not rabbit.bit_r
        assert not rabbit.bit_s

    def test_correctness_blockalphabit(self):
        blockalpha = _get_blockalphabit()
        assert blockalpha.test_ids == [1, 2, 3, 4]
        assert len(blockalpha.per_test_config) == 4
        for per_test_config in blockalpha.per_test_config:
            for blockalpha_variant in per_test_config.variants:
                assert blockalpha_variant.repetitions == 1
                assert blockalpha_variant.bit_nb == 10000000
                assert blockalpha_variant.bit_r == 0
                assert blockalpha_variant.bit_s == 32
                if per_test_config.test_id == 1:
                    assert blockalpha_variant.bit_w == 1 or blockalpha_variant.bit_w == 2

    def test_correctness_alphabit(self):
        alpha = _get_alphabit()
        assert alpha.test_ids == [1, 2, 3]
        assert alpha.repetitions == 1
        assert alpha.bit_nb == 10000000
        assert alpha.bit_r == 0
        assert alpha.bit_s == 32


if __name__ == "__main__":
    unittest.main()
