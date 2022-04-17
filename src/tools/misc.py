import os


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
                # the split of "1-5" is always of size 2
                assert len(_range) == 2
                for tid in range(int(_range[0]), int(_range[1]) + 1):
                    out.append(tid)
            else:  # id_or_range represents only a test id
                tid = int(id_or_range)
                out.append(tid)
    except:
        raise RuntimeError(
            "Check your batteries settings JSON file for default test-ids")
    return out


def nist_test_id_to_param(nist_test_id: int) -> str:
    """Takes one nist test-id and returns corresponding argument, i.e. 001000000000000

    Args:
        nist_test_id (list): NIST test-id in range from 1 to 15

    Returns:
        str: String to pass as a parameter for nist-battery executable, i.e. 100000000000000 (test with ID = 1 will be run)
    """
    out = '000000000000000'
    if nist_test_id > 15 or nist_test_id < 1:
        return None
    # out[nist_test_id - 1] = '1'
    replace_at = nist_test_id - 1
    out = out[:replace_at] + '1' + out[replace_at+1:]
    return out


def nist_get_specific_param(block_length: int, test_id: int) -> 'list[str]':
    """Takes NIST test id and returns special arguments for that particular test id.
    NIST battery allows its users to specify additional arguments for certain tests.
    For example, -blockfreqpar argument sets additional block length parameter for
    Block Frequency test.

    Args:
        block_length (int): Value of block length
        test_id (int): NIST test ID

    Returns:
        list[str]: Arguments for assess binary
    """
    retval = ["-defaultpar"]
    if block_length is None:
        return retval
    # BlockFrequency test
    if test_id == 2:
        retval.extend(["-blockfreqpar", str(block_length)])
    # NonOverlapping test
    elif test_id == 8:
        retval.extend(["-nonoverpar", str(block_length)])
    # Overlapping test
    elif test_id == 9:
        retval.extend(["-overpar", str(block_length)])
    # Approximate Entropy test
    elif test_id == 11:
        retval.extend(["-approxpar", str(block_length)])
    # Serial test
    elif test_id == 14:
        retval.extend(["-serialpar", str(block_length)])
    # Linear Complexity test
    elif test_id == 15:
        retval.extend(["-linearpar", str(block_length)])

    return retval


def gather_files(dir: str, extensions: list) -> list:
    """Given dir parameter, function takes all files in that directory
    and checks if their extensions are in 'extensions' list. These files
    are then returned in list.

    Args:
        dir (str): Directory to be searched
        extensions (list): File extensions we are interested in (like .rnd or .bin)

    Returns:
        list: List of files in 'dir' ending with extension in 'extensions' list
    """
    files = list()
    for file in os.listdir(dir):
        for ext in extensions:
            if file.endswith(ext):
                files.append(os.path.join(
                    dir, file))

    return files
