import pytest


@pytest.fixture
def sample_testfile(pytester):
    code = """
def test_foo():
    pass
    """
    pytester.makepyfile(code)


def test_default(pytester, sample_testfile):
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    result.stdout.no_fnmatch_line("*Worker statistics*")
