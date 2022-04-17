import unittest
import json
from settings.nist import NistSettingsFactory, NistSettings
from tools.misc import nist_get_specific_param, nist_test_id_to_param


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

NIST_WITH_VARIANTS_JSON = """
{
    "nist-sts-settings": {
        "defaults": {
            "test-ids": ["1", "2"],
            "block-length": 30,
            "stream-size": "1000000",
            "stream-count": "80"
        },
        "test-specific-settings": [
            {
                "test-id": 1,
                "block-length": 32,
                "stream-size": 128000,
                "stream-count": 64
            },
            {
                "test-id": 2,
                "variants": [
                    {"block-length": 32, "stream-size": 12800, "stream-count": 0},
                    {"block-length": 18, "stream-size": 10000, "stream-count": 1},
                    {"block-length": 12, "stream-size": 98765, "stream-count": 3},
                    {"block-length": 51, "stream-size": 12345, "stream-count": 5}
                ]
            }
        ]
    }
}
"""


def _get_nist_settings() -> NistSettings:
    return NistSettingsFactory.make_settings(
        json.loads(NIST_JSON))


def _get_nist_with_variants_settings() -> NistSettings:
    return NistSettingsFactory.make_settings(
        json.loads(NIST_WITH_VARIANTS_JSON))


class TestNistParsing(unittest.TestCase):
    def test_correctness(self):
        nist_settings = _get_nist_settings()
        assert nist_settings.test_ids == [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        for test_config in nist_settings.per_test_config:
            for variant in test_config.variants:
                assert variant.stream_size == 1000000
                assert variant.stream_count == 80

    def test_variants(self):
        nist_settings = _get_nist_with_variants_settings()
        for test_config in nist_settings.per_test_config:
            if test_config.test_id == 1:
                assert test_config.variants[0].block_length == 32
                assert test_config.variants[0].stream_size == 128000
                assert test_config.variants[0].stream_count == 64
            if test_config.test_id == 2:
                assert test_config.variants[0].block_length == 32
                assert test_config.variants[1].block_length == 18
                assert test_config.variants[2].block_length == 12
                assert test_config.variants[3].block_length == 51
                assert test_config.variants[0].stream_size == 12800
                assert test_config.variants[1].stream_size == 10000
                assert test_config.variants[2].stream_size == 98765
                assert test_config.variants[3].stream_size == 12345
                assert test_config.variants[0].stream_count == 0
                assert test_config.variants[1].stream_count == 1
                assert test_config.variants[2].stream_count == 3
                assert test_config.variants[3].stream_count == 5

    def test_nist_ids_to_params(self):
        assert nist_test_id_to_param(1) == "100000000000000"
        assert nist_test_id_to_param(2) == "010000000000000"
        assert nist_test_id_to_param(3) == "001000000000000"
        assert nist_test_id_to_param(4) == "000100000000000"
        assert nist_test_id_to_param(5) == "000010000000000"
        assert nist_test_id_to_param(6) == "000001000000000"
        assert nist_test_id_to_param(7) == "000000100000000"
        assert nist_test_id_to_param(8) == "000000010000000"
        assert nist_test_id_to_param(9) == "000000001000000"
        assert nist_test_id_to_param(10) == "000000000100000"
        assert nist_test_id_to_param(11) == "000000000010000"
        assert nist_test_id_to_param(12) == "000000000001000"
        assert nist_test_id_to_param(13) == "000000000000100"
        assert nist_test_id_to_param(14) == "000000000000010"
        assert nist_test_id_to_param(15) == "000000000000001"

    def test_nist_get_specific_param(self):
        assert nist_get_specific_param(
            1, 2) == ["-defaultpar", "-blockfreqpar", "1"]
        assert nist_get_specific_param(
            1, 8) == ["-defaultpar", "-nonoverpar", "1"]
        assert nist_get_specific_param(
            1, 9) == ["-defaultpar", "-overpar", "1"]
        assert nist_get_specific_param(
            1, 11) == ["-defaultpar", "-approxpar", "1"]
        assert nist_get_specific_param(
            1, 14) == ["-defaultpar", "-serialpar", "1"]
        assert nist_get_specific_param(
            1, 15) == ["-defaultpar", "-linearpar", "1"]


if __name__ == "__main__":
    unittest.main()
