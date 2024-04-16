import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def sample_testfile(pytester: pytest.Pytester):
    code = """
import pytest

def test_foo():
    pass

@pytest.mark.parametrize("fix1", (1, 2, 3))
def test_bar(fix1):
    pass
    """
    pytester.makepyfile(test_plugin=code)


expected_header_lines = [
    "*Worker statistics*",
]

expected_statistics_lines = [
    "Tests   : min        2, max        2, average 2.0",
    "Runtime : min    0.00s, max    0.00s, average 0.00s",
]

expected_runtime_lines = [
    "worker gw0  :    2 tests       0.00s runtime",
    "worker gw1  :    2 tests       0.00s runtime",
]

expected_breakdown_lines = [
    "worker gw0  :    2 tests       0.00s runtime",
    "    test_plugin.py::test_bar[1]",
    "    test_plugin.py::test_foo",
    "worker gw1  :    2 tests       0.00s runtime",
    "    test_plugin.py::test_bar[2]",
    "    test_plugin.py::test_bar[3]",
]
