import unittest
import json


from settings.dieharder import DieharderSettingsFactory, DieharderSettings


DIEHARD_JSON = """
{
    "dieharder-settings": {
        "defaults": {
            "test-ids": ["0", "1", "200-204"],
            "psamples": 100
        },
        "test-specific-settings": [
            {
                "test-id": 0,
                "psamples": 65
            },
            {
                "test-id": 200,
                "variants": [
                    { "arguments": "-n 1", "psamples": 12 }
                ]
            }
        ]
    }
}
"""


class ParsingTest(unittest.TestCase):
    def test_initial(self):
        diehard_json = json.loads(DIEHARD_JSON)["dieharder-settings"]
        pass

if __name__ == "__main__":
    unittest.main()
