import os
import time
from typing import NamedTuple

import pytest

SHARED_WORKER_INFO = "worker_info"


class RunStatistics(NamedTuple):
    mininum_tests: int
    maximum_tests: int
    average_tests: float
    mininum_runtime: float
    maximum_runtime: float
    average_runtime: float


class XdistWorkerStatsPlugin:
    def __init__(self, config):
        self.config = config
        self.test_stats = {}
        self.worker_test_times = {}

    def add(self, name):
        self.test_stats[name] = self.test_stats.get(name) or {}
        return self.test_stats[name]

    def pytest_runtest_setup(self, item):
        self.add(item.nodeid)["start"] = time.time()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):
        yield
        end = time.time()
        self.add(item.nodeid)["diff"] = end - self.add(item.nodeid)["start"]

        if (worker := os.environ.get("PYTEST_XDIST_WORKER", "primary")) not in self.worker_test_times:
            self.worker_test_times[worker] = []

        self.worker_test_times[worker].append(self.add(item.nodeid)["diff"])

    def get_statistics(self) -> RunStatistics:
        workers = self.worker_test_times.keys()
        tests = [len(self.worker_test_times[worker]) for worker in workers]
        runtimes = [sum(self.worker_test_times[worker]) for worker in workers]

        return RunStatistics(
            mininum_tests=min(tests),
            maximum_tests=max(tests),
            average_tests=sum(tests) / len(tests),
            mininum_runtime=min(runtimes),
            maximum_runtime=max(runtimes),
            average_runtime=sum(runtimes) / len(runtimes),
        )

    def pytest_terminal_summary(self, terminalreporter):
        """
        If there's multiple workers, report on number of tests and total runtime.
        """
        tr = terminalreporter
        if self.worker_test_times and len(self.worker_test_times) > 1:
            tr._tw.sep("=", "Worker statistics", yellow=True)
            workers = sorted(self.worker_test_times.keys(), key=lambda x: int(x.lstrip("gw")))
            statistics = self.get_statistics()

            for worker in workers:
                worker_times = self.worker_test_times[worker]
                tr._tw.line(f"worker {worker: <5}: {len(worker_times): >4} tests {sum(worker_times):10.2f}s runtime")

            tr._tw.line("")
            tr._tw.line(
                f"Tests   : min {statistics.mininum_tests: >8}, "
                f"max {statistics.maximum_tests: >8}, "
                f"average {statistics.average_tests:.1f}"
            )
            tr._tw.line(
                f"Runtime : min {statistics.mininum_runtime:7.2f}s, "
                f"max {statistics.maximum_runtime:7.2f}s, "
                f"average {statistics.average_runtime:.2f}s"
            )

    def pytest_testnodedown(self, node, error):
        """
        Get statistic about worker usage for test cases from xdist nodes and merge to primary stats.
        """
        if (
            hasattr(node, "workeroutput")
            and (node_worker_stats := node.workeroutput.get(SHARED_WORKER_INFO)) is not None
        ):
            self.worker_test_times.update(dict(node_worker_stats))

    @pytest.hookimpl(hookwrapper=True, trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        """
        Dump worker usage statistics to `workeroutput`.
        Executed once per node if with xdist and will gen from primary node.
        """
        yield
        if hasattr(self.config, "workeroutput"):
            self.config.workeroutput[SHARED_WORKER_INFO] = self.worker_test_times
