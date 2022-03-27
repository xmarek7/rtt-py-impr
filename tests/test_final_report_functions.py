import unittest
from results.nist import NistResult

from tools.final_reports import finalize_nist_results


NIST_RESULTS_FOR_MULTIPLE_FILES = [
    [
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Monobit", 0.003, 0.1),
        NistResult("Overlapping", 0.004, 0.1),
        NistResult("NonOverlapping", 0.9, 0.1),
        NistResult("NonOverlapping", 0.4, 0.1),
        NistResult("NonOverlapping", 0.005, 0.1),
        NistResult("Maurer", 0.6, 0.1),
        NistResult("Maurer2", 0.5, 0.1),
    ],
    [
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Monobit", 0.03, 0.1),
    ],
    [
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Monobit", 0.03, 0.1),
        NistResult("Overlapping", 0.04, 0.1),
    ],
    [
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Frequency", 0.02, 0.1),
        NistResult("Monobit", 0.03, 0.1),
        NistResult("Overlapping", 0.04, 0.1),
        NistResult("Maurer", 0.6, 0.1),
        NistResult("Maurer", 0.8, 0.1),
        NistResult("Maurer", 0.68, 0.1),
        NistResult("Maurer", 0.86, 0.1),
        NistResult("Maurer", 0.8866, 0.1),
    ],
]


class TestFinalReportFunctionality(unittest.TestCase):
    def test_finalize_nist(self):
        res = finalize_nist_results(NIST_RESULTS_FOR_MULTIPLE_FILES)
        assert len(res) == 15
        res = sorted(res, key=float)
        assert res == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                              0.0, 0.0, 0.0, 0.0, 0.25, 0.33333333333333337, 1.0]


if __name__ == "__main__":
    unittest.main()
