from conftest import (
    expected_breakdown_lines,
    expected_header_lines,
    expected_runtime_lines,
    expected_statistics_lines,
)


def test_default(pytester, sample_testfile):
    result = pytester.runpytest()
    result.assert_outcomes(passed=4)
    for line in [
        *expected_header_lines,
        *expected_runtime_lines,
        *expected_breakdown_lines,
        *expected_statistics_lines,
    ]:
        result.stdout.no_fnmatch_line(line)
