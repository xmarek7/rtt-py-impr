import unittest

from results.testu01 import TestU01ResultFactory, TestU01Result


# !!!! CHANGES CAN CAUSE TEST FAILURES !!!!
STDOUT_STR_2_REPS = """
Generator providing data from binary file.
smultin_MultinomialBitsOver test:
-----------------------------------------------

       Sparse =  FALSE

       Number of bits = n = 10000000
-----------------------------------------------
some stat value                       :    0.29
p-value of test                       :    0.87


-----------------------------------------------
CPU time used                    :  00:00:00.01

Generator providing data from binary file.


smultin_MultinomialBitsOver test:
-----------------------------------------------
   <someline>
<someline>
                <someline>
p-value of test                       :    0.77

-----------------------------------------------
CPU time used                    :  00:00:00.01
"""

# !!!! DO NOT FORMAT THIS ARRAY !!!!
STDOUT_2_REPS_STATS = [
    """smultin_MultinomialBitsOver test:
-----------------------------------------------

       Sparse =  FALSE

       Number of bits = n = 10000000
-----------------------------------------------
some stat value                       :    0.29
p-value of test                       :    0.87


-----------------------------------------------
""",
    """smultin_MultinomialBitsOver test:
-----------------------------------------------
   <someline>
<someline>
                <someline>
p-value of test                       :    0.77

-----------------------------------------------
""",
]


STDOUT_STR_1_REP = """
Generator providing data from binary file.
smultin_MultinomialBitsOver test:
-----------------------------------------------

       Sparse =  FALSE

       Number of bits = n = 10000000
-----------------------------------------------
some stat value                       :    0.29
p-value of test                       :    0.87


-----------------------------------------------
CPU time used                    :  00:00:00.01
"""

class TestTestU01StdoutParsing(unittest.TestCase):
    def test_parse_block_alphabit_from_file(self):
        with open(
            "tests/assets/test_results/testu01_logs_example_alphabit.txt", "r") as stdout:
            results = TestU01ResultFactory.make_result(stdout.read())
            # print(results)

    def test_parse_stdout(self):
        results = TestU01ResultFactory.make_result(STDOUT_STR_2_REPS)
        # print(results)

    def test_parse_and_check_pvals(self):
        results = TestU01ResultFactory.make_result(STDOUT_STR_2_REPS)
        assert len(results) == 2
        assert results[0].result_value == 0.87
        assert results[1].result_value == 0.77

    def test_parse_and_check_statistics_exact(self):
        results = TestU01ResultFactory.make_result(STDOUT_STR_2_REPS)
        assert len(results) == 2
        assert results[0].statistics == STDOUT_2_REPS_STATS[0]
        assert results[1].statistics == STDOUT_2_REPS_STATS[1]

    def test_parse_one_rep_stdout(self):
        results = TestU01ResultFactory.make_result(STDOUT_STR_1_REP)
        assert len(results) == 1
        assert results[0].statistics == STDOUT_2_REPS_STATS[0]
        assert results[0].result_value == 0.87

if __name__ == "__main__":
    unittest.main()
