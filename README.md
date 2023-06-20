# pytest-xdist-worker-stats

A pytest plugin to list worker statistics after a xdist run.

## Installation

```shell
$ pip install pytest-xdist-worker-stats
```

## Usage

All that is needed is to have xdist installed & enabled, and to run tests in multiple workers.

## Example output

```text
platform linux -- Python 3.10.11, pytest-7.3.2, pluggy-1.0.0
plugins: xdist-3.3.1, xdist-worker-stats-0.1.0
12 workers [318 items]
............................................................................................................... [ 34%]
............................................................................................................... [ 69%]
................................................................................................                [100%]
================================================= Worker statistics ==================================================
worker gw0  :   11 tests       5.75s runtime
worker gw1  :   10 tests       6.17s runtime
worker gw2  :    8 tests       5.80s runtime
worker gw3  :   21 tests       5.70s runtime
worker gw4  :   16 tests       5.73s runtime
worker gw5  :    9 tests       5.76s runtime
worker gw6  :   12 tests      19.21s runtime
worker gw7  :   48 tests       5.58s runtime
worker gw8  :   17 tests       5.70s runtime
worker gw9  :   78 tests       5.50s runtime
worker gw10 :   41 tests       5.60s runtime
worker gw11 :   47 tests       5.59s runtime
================================================ 318 passed in 26.66s ================================================
```

## Development

[Poetry](https://python-poetry.org/) (dependencies) and [pre-commit](https://pre-commit.com/) (coding standards) are required for development.

```shell
$ poetry install
$ pre-commit install
```

## Thanks

Many thanks to [Denys Korytkin](https://github.com/DKorytkin) for the article [How to get data from pytest-xdist nodes](https://korytkin.medium.com/how-to-get-data-from-pytest-xdist-nodes-2fbf2f0fe957).

## Changelog

### 0.1.1 (Jun 15, 2023)

* First Release
