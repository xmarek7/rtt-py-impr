import unittest

from results.nist import NistResultFactory, NistResult
from assets.test_variables import NIST_FINAL_ANALYSIS_REPORT_PARSED

# !!!! CHANGES CAN CAUSE TEST FAILURES !!!!
FINAL_ANALYSIS_EXAMPLE = """
------------------------------------------------------------------------------
 C1  C2  C3  C4  C5  C6  C7  C8  C9 C10  P-VALUE  PROPORTION  STATISTICAL TEST
------------------------------------------------------------------------------
  3  14  10  11   5   9   6   9   6   7  0.227773   1.0000    Frequency
 14   7   4  11   4  11   6   7  10   6  0.186566   0.3001    Runs
  7  10   4  12  10   7   9   9   5   7  0.663130   0.8000    FFT
"""

EXPECTED_NIST_RESULTS = [
    NistResult("Frequency", 0.227773, 1.0000),
    NistResult("Runs", 0.186566, 0.3001),
    NistResult("FFT", 0.663130,  0.8000),
]


class TestNistResultParsing(unittest.TestCase):
    def test_parse_example(self):
        result = NistResultFactory.make(FINAL_ANALYSIS_EXAMPLE)
        assert len(result) == 3
        assert result[0] == EXPECTED_NIST_RESULTS[0]
        assert result[1] == EXPECTED_NIST_RESULTS[1]
        assert result[2] == EXPECTED_NIST_RESULTS[2]

    def test_parse_from_file(self):
        with open("tests/assets/test_results/nist_finalAnalysisReport.txt", "r") as final_analysis:
            content = final_analysis.read()
            result = NistResultFactory.make(content)
            for i in range(len(result)):
                assert result[i] == NIST_FINAL_ANALYSIS_REPORT_PARSED[i]

if __name__ == "__main__":
    unittest.main()
