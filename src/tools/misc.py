def parse_test_ids(test_ids: list) -> list:
    """Helper function for parsing test-ids from JSON

    Args:
        test_ids (list): a list containing ids or ranges of ids, i.e. ["1", "4-8"]

    Raises:
        RuntimeError: In case of invalid elements in test_ids array, i.e. ["a", "one", "1->4"]

    Returns:
        list: contains parsed test ids
    """
    out = list()
    try:
        for id_or_range in test_ids:
            if '-' in id_or_range:  # user provided a range
                _range = id_or_range.split('-')
                assert len(_range) == 2 # the split of "1-5" is always of size 2
                for tid in range(int(_range[0]), int(_range[1]) + 1):
                    out.append(tid)
            else: # id_or_range represents only a test id
                tid = int(id_or_range)
                out.append(tid)
    except:
        raise RuntimeError(
            "Check your batteries settings JSON file for default Dieharder test-ids")
    return out
