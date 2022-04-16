import unittest
import pytest
import json

from settings.bsi import BsiSettings

BSI_JSON = """
{
    "bsi-settings": {
        "defaults": {
            "test-ids": ["0-8"],
            "uniform-distribution": {
                "K-param": 123,
                "N-param": 456,
                "A-param": 789
            }
        }
    }
}
"""

NO_UNIFORM_JSON = """
{
    "bsi-settings": {
        "defaults": {
            "test-ids": ["0-5"],
            "not-a-uniform-distribution": {
                "K-param": 123
            }
        }
    }
}
"""

BAD_UNIFORM_PARAM_JSON = """
{
    "bsi-settings": {
        "defaults": {
            "test-ids": ["0-5"],
            "uniform-distribution": {
                "NOT-a-param": 123
            }
        }
    }
}
"""


def _get_bsi() -> BsiSettings:
    return BsiSettings(json.loads(BSI_JSON))


class TestBsiParsing(unittest.TestCase):
    def test_correctness(self):
        bsi = _get_bsi()
        assert bsi.test_ids == [0, 1, 2, 3, 4, 5, 6, 7, 8]
        assert bsi.uniform_dist_K == '123'
        assert bsi.uniform_dist_N == '456'
        assert bsi.uniform_dist_A == '789'


class TestBsiError(unittest.TestCase):
    def test_expect_uniform_none(self):
        bsi = BsiSettings(json.loads(NO_UNIFORM_JSON))
        assert not bsi.uniform_dist_K
        assert not bsi.uniform_dist_N
        assert not bsi.uniform_dist_A

    def test_expect_error_uniform_param(self):
        with pytest.raises(RuntimeError):
            BsiSettings(json.loads(BAD_UNIFORM_PARAM_JSON))
