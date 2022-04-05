# Randomness Testing Toolkit (RTT) in python

Revolution in testing Random Number Generators.

## Supported batteries
- FIPS
- BSI
- NIST
- DieHarder
- TestU01

## Basic idea
Inspiration for this solution was found in [randomness-testing-toolkit repo](https://github.com/crocs-muni/randomness-testing-toolkit).
Each supported battery has its own executable. Executables are implemented in C++ and
it's up to a user to build them. They are located in [this repo](https://github.com/pvavercak/rtt-statistical-batteries).\
The toolkit serves like a script that executes the binaries, parses their output and collects results
into a CSV file and also as HTML report.\
`It is highly recommended to study individual batteries first, you'll have better understanding
of the code in this repository.`

## Project structure
- settings [src/settings](https://github.com/pvavercak/rtt-py/tree/master/src/settings)
- executions [src/executions](https://github.com/pvavercak/rtt-py/tree/master/src/executions)
- results [src/results](https://github.com/pvavercak/rtt-py/tree/master/src/results)
- tools [src/tools](https://github.com/pvavercak/rtt-py/tree/master/src/tools)
- main application [rtt.py](https://github.com/pvavercak/rtt-py/tree/master/src/)
### Settings
Responsibility for parsing JSON configuration files. \
You can read more about various settings here:
- [general-settings](https://github.com/pvavercak/rtt-py/tree/master/docs/GeneralSettings.md)
- [test-settings](https://github.com/pvavercak/rtt-py/tree/master/docs/TestSettings.md)
### Executions
Execution of binaries of the supported batteries is happening here. Each one of the batteries has its dedicated class.
### Results
As the name suggests, this subfolder holds classes responsible for parsing and storing results. Metrics like `p-value` or `number of failed tests` are then exported to HTML files for easier result analysis.
### Tools
Small section of the code base that holds some useful utilities like HTML file generation, directory search, CSV construction, etc.
### Main application
This is the place where all the subfolders are becoming useful. User-specified program arguments from CLI are parsed here, all the user settings/parameters are evaluated and then the test execution is triggered.

## Development
### Quick install
```bash
pip3 install -e .
```
### Development extras
```bash
pip3 install -e .[dev]
```