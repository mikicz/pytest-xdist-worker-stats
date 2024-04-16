# pytest-xdist-worker-stats

A pytest plugin to list worker statistics after a xdist run.

## Installation

```shell
$ pip install pytest-xdist-worker-stats
```

## Usage

All that is needed is to have xdist installed & enabled, and to run tests in multiple workers.

### Default mode

```shell
pytest {all_your_options}
```

```text
============================= test session starts ==============================
platform linux -- Python 3.10.7, pytest-8.1.1, pluggy-1.4.0
plugins: xdist-worker-stats-0.1.7, xdist-3.5.0
created: 2/2 workers
2 workers [4 items]

....                                                                     [100%]
============================== Worker statistics ===============================
worker gw0  :    2 tests       0.00s runtime
worker gw1  :    2 tests       0.00s runtime

Tests   : min        2, max        2, average 2.0
Runtime : min    0.00s, max    0.00s, average 0.00s
============================== 4 passed in 1.82s ===============================
```

### Summary mode

```shell
pytest {all_your_options} --no-xdist-runtimes
```

```text
============================= test session starts ==============================
platform linux -- Python 3.10.7, pytest-8.1.1, pluggy-1.4.0
plugins: xdist-worker-stats-0.1.7, xdist-3.5.0
created: 2/2 workers
2 workers [4 items]

....                                                                     [100%]
============================== Worker statistics ===============================
Tests   : min        2, max        2, average 2.0
Runtime : min    0.00s, max    0.00s, average 0.00s
============================== 4 passed in 1.82s ===============================
```

### Breakdown mode

```shell
pytest {all_your_options} --xdist-breakdown
```

```text
============================= test session starts ==============================
platform linux -- Python 3.10.7, pytest-8.1.1, pluggy-1.4.0
plugins: xdist-worker-stats-0.1.7, xdist-3.5.0
created: 2/2 workers
2 workers [4 items]

....                                                                     [100%]
============================== Worker statistics ===============================
worker gw0  :    2 tests       0.00s runtime
    test_plugin.py::test_bar[1]
    test_plugin.py::test_foo
worker gw1  :    2 tests       0.00s runtime
    test_plugin.py::test_bar[2]
    test_plugin.py::test_bar[3]

Tests   : min        2, max        2, average 2.0
Runtime : min    0.00s, max    0.00s, average 0.00s
============================== 4 passed in 1.82s ===============================
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
