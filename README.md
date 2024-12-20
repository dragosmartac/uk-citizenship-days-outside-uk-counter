# Python Counter for Days Outside UK

## What is this for?

The UK Citizenship application has a number of [requirements that need to be fulfilled](https://www.gov.uk/apply-citizenship-indefinite-leave-to-remain) in order to be eligible to apply

The UK Citizenship application has several eligibility requirements that must be met. To qualify, applicants must fulfill the necessary conditions outlined on the [UK Government's website](https://www.gov.uk/apply-citizenship-indefinite-leave-to-remain). Among these, two are relevant for this script:

- spent more than 450 days outside the UK during the 5 years before your application
- spent more than 90 days outside the UK in the last 12 months

*These have been taken from the webside linked above on Fri 20 Dec 2024. Please do check them in the official source.*


## Usage

```
python3 src.py -f example/data.txt
```

ALL DATES:
=======================================================

| Start Date  | End Date    | Total Days Outside UK | Full Days Outside UK |
| 12 Dec 2023 | 14 Dec 2023 |                     3 |                    1 |
| 27 Dec 2023 | 11 Jan 2024 |                    16 |                   14 |
| 22 Feb 2024 | 24 Feb 2024 |                     3 |                    1 |
| 24 Feb 2024 | 27 Feb 2024 |                     4 |                    2 |

Total Days Outside UK: 26
Full Days Outside UK: 18

=======================================================

PAST YEAR DATES:
=======================================================

| Start Date  | End Date    | Total Days Outside UK | Full Days Outside UK |
| 27 Dec 2023 | 11 Jan 2024 |                    16 |                   14 |
| 22 Feb 2024 | 24 Feb 2024 |                     3 |                    1 |
| 24 Feb 2024 | 27 Feb 2024 |                     4 |                    2 |

Total Days Outside UK: 23
Full Days Outside UK: 17

=======================================================

*Note: the day one year ago is computed by substracting from the current date 365 days*

## Tests

```
python3 test_src.py
```

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.004s

OK
```
