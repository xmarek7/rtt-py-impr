from subprocess import Popen, PIPE
import json
import subprocess
from settings import general, dieharder, nist


if __name__ == "__main__":
    json_file = "tests/assets/configs/rtt-settings.json"
    toolkit_settings = None
    with open(json_file, "r") as _f:
        toolkit_settings = json.loads(_f.read())["toolkit-settings"]

    logger = general.LoggerSettings(toolkit_settings["logger"])
    result_storage = general.FileStorageSettings(
        toolkit_settings["result-storage"])
    binaries = general.BinariesSettings(toolkit_settings["binaries"])
    execution = general.ExecutionSettings(toolkit_settings["execution"])
    json_file = "tests/assets/configs/10MB.json"
    bat_settings = None
    with open(json_file, "r") as _f:
        bat_settings = json.loads(
            _f.read())["randomness-testing-toolkit"]
    dieharder_settings = dieharder.DieharderSettingsFactory.make_settings(
        bat_settings["dieharder-settings"])
    # nist_settings = nist.NistSettingsFactory.make_settings(
    #     bat_settings["nist-sts-settings"])
    
    print(dieharder_settings)

    # s = subprocess.Popen(
    #     [binaries.nist_sts,
    #      "1000000",
    #      "-fast",
    #      "--file",
    #      "tests/assets/rnd/10MB.rnd",
    #      "--tests",
    #      "1111111111111111",
    #      "--streams",
    #      "80",
    #      "--defaultpar"])
    # s.wait()

