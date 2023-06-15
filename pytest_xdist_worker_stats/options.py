from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from _pytest.config import Config, PytestPluginManager
    from _pytest.config.argparsing import Parser


def pytest_addoption(parser: "Parser", pluginmanager: "PytestPluginManager") -> NoReturn:
    group = parser.getgroup("pytest-unused-fixtures")
    group.addoption("--unused-fixtures", action="store_true", default=False, help="Try to identify unused fixtures.")
    group.addoption(
        "--unused-fixtures-ignore-path",
        metavar="PATH",
        type=str,
        default=None,
        action="append",
        help="Ignore fixtures in PATHs from unused fixtures report.",
    )


def pytest_configure(config: "Config") -> NoReturn:
    pluginmanager = config.pluginmanager
    if pluginmanager.hasplugin("xdist"):
        from pytest_xdist_worker_stats.plugin import XdistWorkerStatsPlugin

        pluginmanager.register(XdistWorkerStatsPlugin(config))
