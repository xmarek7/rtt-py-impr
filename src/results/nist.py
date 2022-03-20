import re

# assess produces finalAnalysisReport.txt file from each execution
# one line looks like this:
#   3  14  10  11   5   9   6   9   6   7  0.227773   1.0000    Frequency
# and it has the following header:
#  C1  C2  C3  C4  C5  C6  C7  C8  C9 C10  P-VALUE  PROPORTION  STATISTICAL TEST
# putting this together, we get
# C1  C2  C3  C4  C5  C6  C7  C8  C9 C10  P-VALUE  PROPORTION  STATISTICAL TEST
# -----------------------------------------------------------------------------
#  3  14  10  11   5   9   6   9   6   7  0.227773 1.0000      Frequency

# this regex helps to extract all the lines form finalAnalysisReport.txt
FIND_FINAL_TABLE = re.compile(r"[^\s]*\d\.\d+\s+\d\.\d+\s+\w+\b")

#                                (P-VALUE)(PROPORTION)(TESTNAME)
#                                    |           |         |
#                                    V           V         V
EXTRACT_ONE_LINE = re.compile(r"^(\d\.\d+)\s+(\d\.\d+)\s+(\S+)\b")


class NistResult:
    def __init__(self, test_name: str, p_value: float, proportion: float):
        self.test_name = test_name
        self.p_value = p_value
        self.proportion = proportion

    def __repr__(self):
        return "NistResult {" \
            f"\ttest_name: {self.test_name},\n" \
            f"\tp_value: {self.p_value},\n" \
            f"\tproportion: {self.proportion},\n" \
            "}"
            
    def __eq__(self, other: 'NistResult'):
        if type(self) != type(other):
            return False
        return self.test_name == other.test_name and \
            self.p_value == other.p_value and \
            self.proportion == other.proportion


class NistResultFactory:
    def make(final_analysis_content: str) -> 'list[NistResult]':
        execution_result: list[NistResult] = []
        final_analysis_lines = FIND_FINAL_TABLE.findall(final_analysis_content)
        if len(final_analysis_lines) > 0:  # we have at least 1 result
            for line in final_analysis_lines:
                # let's extract p-value, proportion, test name
                match = EXTRACT_ONE_LINE.match(line)
                if match:
                    p_value = float(match.group(1))
                    proportion = float(match.group(2))
                    test_name = match.group(3)
                    execution_result.append(
                        NistResult(test_name, p_value, proportion))
        return execution_result
