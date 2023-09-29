import pytest


@pytest.fixture
def sample_testfile(pytester):
    code = """
def test_foo():
    pass
def test_bar():
    pass
    """
    pytester.makepyfile(code)


def test_default(pytester, sample_testfile):
    result = pytester.runpytest("-n", "2")
    result.assert_outcomes(passed=2)
    result.stdout.fnmatch_lines(
        [
            "*Worker statistics*",
            "worker gw0  :    1 tests       0.00s runtime",
            "worker gw1  :    1 tests       0.00s runtime",
        ],
        consecutive=True,
    )

    result.stdout.fnmatch_lines(
        [
            "Tests   : min        1, max        1, average 1.0",
            "Runtime : min    0.00s, max    0.00s, average 0.00s",
        ],
        consecutive=True,
    )
