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
                assert len(_range) == 2 # the split of "1-5" is always of size 2
                for tid in range(int(_range[0]), int(_range[1]) + 1):
                    out.append(tid)
            else: # id_or_range represents only a test id
                tid = int(id_or_range)
                out.append(tid)
    except:
        raise RuntimeError(
            "Check your batteries settings JSON file for default test-ids")
    return out


def nist_test_ids_to_param(nist_test_ids: list) -> str:
    """Takes list of test-ids from 1-15 and returns a corresponding parameter of a nist-sts executable

    Args:
        nist_test_ids (list): List of unique test ids from 1-15

    Returns:
        str: String to pass as a parameter for nist-battery executable, i.e. 111111111111111 (all tests enabled)
    """
    out = ''
    for i in range(15):
        if i + 1 in nist_test_ids:
            out += '1'
        else:
            out += '0'
    return out


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
