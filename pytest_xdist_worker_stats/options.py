import pytest


def pytest_addoption(parser: pytest.Parser):
    from pytest_xdist_worker_stats.plugin import (
        ARGPARSE_PARSER_GROUP,
        ARGPARSE_REPORT_TEST_BREAKDOWN_OPTION_NAME,
        ARGPARSE_REPORT_WORKER_RUNTIMES_OPTION_NAME,
    )

    group = parser.getgroup(ARGPARSE_PARSER_GROUP)
    group.addoption(
        "--no-xdist-runtimes",
        action="store_false",
        default=True,
        dest=ARGPARSE_REPORT_WORKER_RUNTIMES_OPTION_NAME,
        help="Do not report runtimes per 'xdist' worker.",
    )
    group.addoption(
        "--xdist-breakdown",
        action="store_true",
        dest=ARGPARSE_REPORT_TEST_BREAKDOWN_OPTION_NAME,
        help="Display test breakdown per 'xdist' worker.",
    )


def pytest_configure(config: pytest.Config):
    pluginmanager = config.pluginmanager
    if pluginmanager.hasplugin("xdist"):
        from pytest_xdist_worker_stats.plugin import XdistWorkerStatsPlugin

        pluginmanager.register(XdistWorkerStatsPlugin(config))
