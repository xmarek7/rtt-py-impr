import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Python implementation of Randomness Testing Toolkit"
    )
    parser.add_argument("--general-settings", "-g",
                        help="Path to a JSON file containing general settings",
                        type=str,
                        required=True)
    parser.add_argument("--test-settings", "-t",
                        help="Path to a JSON file containing settings related to batteries of tests",
                        type=str,
                        required=True)
    parser.add_argument("--extensions", "-e",
                        help="Extension of input files from inputs-dir to test",
                        type=str,
                        nargs="+",
                        default=".rnd")
    parser.add_argument("-af", "--allowed-failure",
                        help="Failure percentage of a test. Failure percentage calculation: 1 - passed_tests_count / executed_tests",
                        type=float,
                        default=0.04)
    parser.add_argument("--alpha",
                        help="Value of alpha to be used for evaluation: test p_value > alpha -> test passed",
                        type=float,
                        default=0.01)

    # mutually exclusive arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inputs-dir", "-d",
                       help="Directory containing input files. Specify either 'inputs-dir' or 'file'",
                       type=str)
    group.add_argument("--input-file", "-f",
                       help="Path to a single input file to test. Specify either 'file' or 'inputs-dir'",
                       type=str)

    # optional battery skip
    bats = ["bsi", "fips", "nist", "dieharder", "tu01", "tu01-smallcrust", "tu01-crush",
            "tu01-bigcrush", "tu01-rabbit", "tu01-alphabit", "tu01-blockalphabit"]
    for bat in bats:
        parser.add_argument(f"--no-{bat}",
                            help=f"Skip tests from {bat.upper()} battery",
                            action="store_true")

    return parser.parse_args()
