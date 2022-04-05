# Test Settings
IMPORTANT: \
`If you don't know anything about supported batteries, read their documentation first.`

It is possible to handle behavior of batteries via test settings JSON file. Information about its structure and required/optional properties can be found here. \
Each battery configuration should be a subproperty of `randomness-testing-toolkit` object:
```json
{
  "randomness-testing-toolkit": {
    ...
  }
}
```
If you want to fully understand what some parameters mean and how they can affect results, you should read documentation of a battery you're interested in.

## Main properties
- `bsi-settings` property
- `fips-settings` property
- `dieharder-settings` property
- `nist-sts-settings` property
- `tu01-rabbit-settings` property
- `tu01-alphabit-settings` property
- `tu01-blockalphabit-settings` property

### Bsi-settings property
BSI battery has 9 tests and their test IDs go from 0 to 8. Uniform distribution test can be configured with K, N and A parameters. If they are not provided, battery's default values are used
- test-ids: list of test IDs, ranges (i.e. "0-8" are supported
- uniform-distribution: contains K-param, N-param, A-param properties \
Example:
```json
{
  "randomness-testing-toolkit": {
    "bsi-settings": {
      "test-ids": ["0", "1", "2-5", "8"],
      "uniform-distribution": {
        "K-param": 1,
        "N-param": 2,
        "A-param": 3
      }
    },
    ...
  }
}
```

### Fips-settings property
They can be null:
```json
{
  "fips-settings": null
}
```
This property is there for future improvements but currently, FIPS binary does not support any additional arguments except the basic ones (input file, output file)

### Dieharder-settings property
User provides defaults: test-ids and psamples properties. Then some test-specific-settings can be configured.
- defaults: test-ids and psamples parameters
```json
{
  ...
  "defaults": {
    "test-ids": ["0", "5-10", "100"],
    "psamples": 100
  }
}
```
- test-specific-settings: array
```json
{
  "test-specific-settings": [
    { // change just psamples
      "test-id": 0,
      "psamples": 65 // overrides default psamples
    },
    { // invalid test id
      "test-id": 1, // test id not in defaults->test-ids, no effect
      "psamples": 77
    },
    { // change psamples and add some variants
      "test-id": 100,
      "variants": [
        {
          "arguments": "-some-argument", // passed directly to dieharder-exe
          "psamples": 1 // overrides default psamples
        },
        {
          "arguments": "-another-argument", // passed directly to dieharder-exe
          "psamples": 2 // overrides default psamples
        }
      ]
    }
  ]
}
```

### Nist-sts-settings
Currently, just `defaults` are supported:
- defaults:
```json
{
  "defaults": {
    "test-ids": ["1", "3", "6-8", "15"], // test ids like in other battery configurations
    "stream-size": "123456", // size of bytes to be taken from input file
    "stream-count": "80" // stream-count parameter
  }
}
```
- `test-specific-settings`: array, not supported

### Tu01-[rabbit, alphabit, blockalphabit]-settings
Similar structure for all subbatteries.
- defaults
- test-specific-settings
```json
{
  "tu01-***-settings": {
    "defaults": { // default configuration
      "test-ids": ["0", "1", "4-5"], // test IDs you want to run
      "repetitions": 1, // reps parameter
      "bit-nb": "123456",
      "bit-r": "0",
      "bit-s": "64"
    },
    "test-specific-settings": [
      {// test-id not present in defaults->test-ids is omitted
        "test-id": 100,
        ...
      },
      {
        "test-id": 1,
        "variants": [
          {"bit-s": "46"}
        ]
      }
    ]
  }
}
```
