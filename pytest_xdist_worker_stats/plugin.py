import os
import time
from typing import NamedTuple

import pytest
from _pytest.terminal import TerminalReporter

ARGPARSE_PARSER_GROUP = "pytest-xdist-worker-stats"
ARGPARSE_REPORT_WORKER_RUNTIMES_OPTION_NAME = "pytest_xdist_worker_stats_report_worker_runtimes"
ARGPARSE_REPORT_TEST_BREAKDOWN_OPTION_NAME = "pytest_xdist_worker_stats_report_test_breakdown"

SHARED_WORKER_INFO = "worker_info"


class RuntimeStats(NamedTuple):
    mininum_tests: int
    maximum_tests: int
    average_tests: float
    mininum_runtime: float
    maximum_runtime: float
    average_runtime: float


class XdistWorkerStatsPlugin:
    def __init__(self, config: pytest.Config):
        self.config = config
        self.test_stats = {}
        self.worker_stats = {}
        self.report_worker_runtimes = config.getoption(ARGPARSE_REPORT_WORKER_RUNTIMES_OPTION_NAME, False)
        self.report_test_breakdown = config.getoption(ARGPARSE_REPORT_TEST_BREAKDOWN_OPTION_NAME, False)

    def add(self, name):
        self.test_stats[name] = self.test_stats.get(name) or {}
        return self.test_stats[name]

    def pytest_runtest_setup(self, item):
        self.add(item.nodeid)["start"] = time.time()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):
        yield
        runtime = time.time() - self.add(item.nodeid)["start"]
        self.add(item.nodeid)["runtime"] = runtime

        if (worker := os.environ.get("PYTEST_XDIST_WORKER", "primary")) not in self.worker_stats:
            self.worker_stats[worker] = {}

        self.worker_stats[worker][item.nodeid] = runtime

    def get_runtime_stats(self) -> RuntimeStats:
        test_counts = [len(stats) for stats in self.worker_stats.values()]
        test_runtimes = [sum(stats.values()) for stats in self.worker_stats.values()]

        return RuntimeStats(
            mininum_tests=min(test_counts),
            maximum_tests=max(test_counts),
            average_tests=sum(test_counts) / len(test_counts),
            mininum_runtime=min(test_runtimes),
            maximum_runtime=max(test_runtimes),
            average_runtime=sum(test_runtimes) / len(test_runtimes),
        )

    def pytest_terminal_summary(self, terminalreporter: TerminalReporter):
        """
        If there's multiple workers, report on number of tests and total runtime.
        """
        tr = terminalreporter
        if self.worker_stats and len(self.worker_stats) > 1:
            tr._tw.sep("=", "Worker statistics", yellow=True)
            worker_columns = len(max(self.worker_stats.keys(), key=len)) + 2

            if self.report_worker_runtimes:
                for worker, stats in sorted(self.worker_stats.items()):
                    runtimes = stats.values()
                    tr._tw.line(
                        f"worker {worker: <{worker_columns}}: {len(runtimes): >4} tests {sum(runtimes):10.2f}s runtime"
                    )
                    if self.report_test_breakdown:
                        for nodeid in sorted(stats.keys()):
                            tr._tw.line(f"    {nodeid}")
                tr._tw.line("")

            runtime_stats = self.get_runtime_stats()
            tr._tw.line(
                f"Tests   : min {runtime_stats.mininum_tests: >8}, "
                f"max {runtime_stats.maximum_tests: >8}, "
                f"average {runtime_stats.average_tests:.1f}"
            )
            tr._tw.line(
                f"Runtime : min {runtime_stats.mininum_runtime:7.2f}s, "
                f"max {runtime_stats.maximum_runtime:7.2f}s, "
                f"average {runtime_stats.average_runtime:.2f}s"
            )

    def pytest_testnodedown(self, node, error):
        """
        Get statistic about worker usage for test cases from xdist nodes and merge to primary stats.
        """
        if (
            hasattr(node, "workeroutput")
            and (node_worker_stats := node.workeroutput.get(SHARED_WORKER_INFO)) is not None
        ):
            self.worker_stats.update(dict(node_worker_stats))

    @pytest.hookimpl(hookwrapper=True, trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        """
        Dump worker usage statistics to `workeroutput`.
        Executed once per node if with xdist and will gen from primary node.
        """
        yield
        if hasattr(self.config, "workeroutput"):
            self.config.workeroutput[SHARED_WORKER_INFO] = self.worker_stats
