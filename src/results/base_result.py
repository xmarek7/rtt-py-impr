from results.result_type import ResultType

class BaseResult:
    """Base class for derived battery result classes.
    This class just informs developers about the required fields
    that every battery result class must have.
    """
    def __init__(self) -> None:
        self.test_name = None
        self.result_value = None
        self.result_type = ResultType.UNKNOWN
