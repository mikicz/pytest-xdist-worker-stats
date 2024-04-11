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
12 workers [359 items]
.............................................................................................. [ 25%]
.............................................................................................. [ 52%]
.............................................................................................. [ 78%]
.............................................................................                  [100%]
========================================= Worker statistics ==========================================
worker gw0  :   15 tests      12.25s runtime
worker gw1  :   14 tests      12.00s runtime
worker gw2  :   27 tests      11.66s runtime
worker gw3  :   13 tests      12.08s runtime
worker gw4  :   14 tests      12.59s runtime
worker gw5  :   27 tests      12.13s runtime
worker gw6  :   18 tests      12.22s runtime
worker gw7  :   78 tests      12.04s runtime
worker gw8  :   21 tests      12.01s runtime
worker gw9  :   59 tests      12.36s runtime
worker gw10 :   20 tests      11.79s runtime
worker gw11 :   53 tests      12.09s runtime

Tests   : min       13, max       78, average 29.9
Runtime : min   11.66s, max   12.59s, average 12.10s
======================================== 359 passed in 21.52s ========================================
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

### 0.1.4 (Aug 8, 2023)

* Summarize statistics

### 0.1.3 (Aug 8, 2023)

* Add CI

### 0.1.2 (Jun 19, 2023)

* Fix several issues

### 0.1.1 (Jun 15, 2023)

* First Release
