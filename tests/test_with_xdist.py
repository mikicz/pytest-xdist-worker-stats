from conftest import (
    expected_breakdown_lines,
    expected_header_lines,
    expected_runtime_lines,
    expected_statistics_lines,
)


def test_default(pytester, sample_testfile):
    result = pytester.runpytest("-n", "2")
    result.assert_outcomes(passed=4)
    result.stdout.fnmatch_lines(
        [
            *expected_header_lines,
            *expected_runtime_lines,
            "",
            *expected_statistics_lines,
        ],
        consecutive=True,
    )


def test_no_runtimes(pytester, sample_testfile):
    result = pytester.runpytest("-n", "2", "--no-xdist-runtimes")
    result.assert_outcomes(passed=4)
    result.stdout.fnmatch_lines(
        [
            *expected_header_lines,
            *expected_statistics_lines,
        ],
        consecutive=True,
    )
    for line in expected_runtime_lines:
        result.stdout.no_fnmatch_line(line)


def test_breakdown(pytester, sample_testfile):
    result = pytester.runpytest("-n", "2", "--xdist-breakdown")
    result.assert_outcomes(passed=4)
    result.stdout.fnmatch_lines(
        [
            *expected_header_lines,
            *expected_breakdown_lines,
            "",
            *expected_statistics_lines,
        ],
        consecutive=True,
    )
