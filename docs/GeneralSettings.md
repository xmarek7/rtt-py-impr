# General settings
General settings are independent from test settings and they describe some properties
like path to a directory with logs/results, binaries and other properties that are common
for each of the supported batteries.\
It is required that the properties are under `toolkit-settings` object:
```json
{
  "toolkit-settings": {
    ...
  }
}
```
## Main Properties
- `logger` property
- `result-storage` property
- `binaries` property
- `execution` property

### Logger properties
- dir-prefix: directory path, other properties will start from this directory (can be absolute path)
- run-log-dir: directory path, toolkit will save logs to this directory (only relative path allowed)

### Result-storage properties
result-storage property currently supports only storing results to files, hence only one property is supported:
- file: specifies directories for storing output files of batteries (only batteries with file ouput are required)
List of properties required in `file` property:
- dir-prefix: base path for each following property
- bsi-dir: result files from BSI battery will be stored in this path (only relative path allowed)
- fips-dir: result files from FIPS battery will be stored in this path (only relative paths allowed) \
result-storage property example:
```json
{
  "toolkit-settings": {
    ...
    "result-storage": {
      "file": {
        "dir-prefix": "some/path",
        "bsi-dir": "some-dir-for-bsi-results",
        "fips-dir": "some-dir-for-fips-results"
      }
    },
    ...
  }
}
```

### Binaries property
As you already know, toolkit does not hold an implementation of statistical tests, executables do. The toolkit just executes binaries with implementation. This property sets paths to all supported batteries (to their binaries to be more precise).\
Required structure of the `binaries` property:
```json
{
  "toolkit-setings": {
    ...
    "binaries": {
      "nist-sts": "nist-exe",
      "dieharder": "dieharder-exe",
      "testu01": "testu01-exe",
      "bsi": "bsi-exe",
      "fips": "fips-exe"
    },
    ...
  }
}
```

### Execution property
Very simple and self-documenting property:
- max-parallel-tests: ! currently with no effect !
- test-timeout-seconds: how long can battery's executable run \
Structure:
```json
{
  "toolkit-setings": {
    ...
    "execution": {
      "max-parallel-tests": 1,
      "test-timeout-seconds": 120
    },
    ...
  }
}
```
