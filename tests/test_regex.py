import unittest
import json
import re

from results.testu01 import EXTRACT_PVALUES_NEAR_0_REGEX, FIND_PVALUES_REGEX, TestU01ResultFactory, EXTRACT_PVALUES_REGEX, EXTRACT_PVALUES_NEAR_1_REGEX


tu01_pval_basic = "p-value of test                       :      0.1234"
tu01_pval_close_to_0 = "p-value of test                       :      8.9e-5    *****"
tu01_pval_close_to_1 = "p-value of test                       : 1 -  8.9e-5    *****"

tu01_result_example = f"""
{tu01_pval_basic}
{tu01_pval_close_to_0}
{tu01_pval_close_to_1}
"""

class TestRegexMatching(unittest.TestCase):
    def test_tu01_extract_pvalues_near_1(self):
        match = EXTRACT_PVALUES_NEAR_1_REGEX.match(tu01_pval_close_to_1)
        float_val = float(match.group(1))
        assert float_val == 8.9e-5
        
    def test_tu01_extract_pvalues_near_0(self):
        match = EXTRACT_PVALUES_NEAR_0_REGEX.match(tu01_pval_close_to_0)
        float_val = float(match.group(1))
        assert float_val == 8.9e-5
        
    def test_tu01_find_pvalues(self):
        result = FIND_PVALUES_REGEX.findall(tu01_result_example)
        assert len(result) == 3
        assert result[0] == "0.1234"
        assert result[1] == "8.9e-5    *****"
        assert result[2] == "1 -  8.9e-5    *****"

    def test_tu01_fallbacks(self):
        def _extract_pval(string):
            pval_match = EXTRACT_PVALUES_NEAR_1_REGEX.match(string)
            if pval_match:
                return 1 - float(pval_match.group(1))
            pval_match = EXTRACT_PVALUES_NEAR_0_REGEX.match(string)
            if pval_match:
                return float(pval_match.group(1))
            pval_match = EXTRACT_PVALUES_REGEX.match(string)
            if pval_match:
                return float(pval_match.group(1))
            return None
        for test in [[tu01_pval_basic, 0.1234], [tu01_pval_close_to_0, 8.9e-5], [tu01_pval_close_to_1, 1 - 8.9e-5]]:
            assert test[1] == _extract_pval(test[0])


if __name__ == "__main__":
    unittest.main()
