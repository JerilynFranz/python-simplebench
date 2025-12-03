"""
A pytest plugin to provide a similar interface to `pytest-benchmark`
powered by the simplebench framework.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional

import pytest
from rich.console import Console

import simplebench.defaults as defaults
from simplebench.case import Case
from simplebench.reporters._pytest.reporter.reporter import PytestReporter
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import ReporterOptions
from simplebench.results import Results
from simplebench.runners import SimpleRunner
from simplebench.session import Session
from simplebench.vcs import GitInfo

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser
    from _pytest.nodes import Item

# Phase 1: Setup and Configuration
# ---------------------------------


def pytest_addoption(parser: Parser) -> None:
    """Add simplebench-specific command-line options to pytest.

    :param parser: The pytest command-line parser.
    """
    group = parser.getgroup("simplebench", "simplebench: benchmark framework")
    group.addoption(
        "--sb-enable",
        action="store_true",
        default=False,
        help="Enable simplebench benchmarking (disables pytest-benchmark if installed)."
    )
    # Example of adding a simplebench config option
    group.addoption(
        "--sb-iterations",
        type=int,
        default=None,
        help="Number of iterations per benchmark. Overrides simplebench defaults."
    )


def pytest_configure(config: Config) -> None:
    """
    Called after command-line options are parsed.
    We use this to create and configure our simplebench Session.

    :param config: The pytest Config object.
    """
    log.debug("pytest_configure hook called.")
    config.addinivalue_line("markers", "benchmark: mark a test for simplebench benchmarking.")

    if not config.getoption("--sb-enable"):
        log.debug("simplebench not enabled, skipping configuration.")
        return

    # Create a simplebench Session instance and configure it to use the PytestReporter.
    # 1. Create the Session
    sb_session = Session()
    reporter_manager = sb_session.reporter_manager
    reporter_manager.unregister_all_reporters()
    pytest_reporter = PytestReporter()
    reporter_manager.register(pytest_reporter)

    sb_session.parse_args(['--pytest'])

    config._simplebench_session = sb_session  # type: ignore[reportAttributeAccessIssue]
    config._simplebench_pytest_reporter = pytest_reporter  # type: ignore[reportAttributeAccessIssue]
    log.debug("simplebench configured with session %r and reporter %r", sb_session, pytest_reporter)


# Phase 2: The Fixture (Test Case Collection)
# -------------------------------------------

class BenchmarkRegistrar:
    """
    A callable object provided by the `benchmark` fixture to register a benchmark case.
    """
    def __init__(self, sb_session: Session, pytest_node: Item):
        self._session = sb_session
        self._pytest_node = pytest_node

    def __call__(
            self,
            action: Callable[..., Any],
            *,
            benchmark_id: Optional[str] = None,
            git_info: Optional[GitInfo] = None,
            group: str = 'default',
            title: Optional[str] = None,
            description: Optional[str] = None,
            iterations: int = defaults.DEFAULT_ITERATIONS,
            warmup_iterations: int = defaults.DEFAULT_WARMUP_ITERATIONS,
            rounds: int | None = None,
            timer: Callable[[], int] | None = None,
            min_time: float = defaults.DEFAULT_MIN_TIME,
            max_time: float = defaults.DEFAULT_MAX_TIME,
            timeout: float | int | None = None,
            variation_cols: Optional[dict[str, str]] = None,
            kwargs_variations: Optional[dict[str, list[Any]]] = None,
            runner: Optional[type[SimpleRunner]] = None,
            callback: Optional[ReporterCallback] = None,
            options: Optional[Iterable[ReporterOptions]] = None) -> None:
        """
        This is called by the user (`benchmark(...)`). Its signature mirrors the
        `simplebench.Case` constructor to provide IDE autocompletion and static
        type checking. It creates a Case and registers it with the session.
        """
        # The full name of the test, including parameterization, is a good default title.
        default_title = self._pytest_node.nodeid

        # This is the wrapper that conforms to the ActionRunner protocol.
        # It closes over the user's `action`.
        def benchmark_action_wrapper(_bench: SimpleRunner, **kwargs: Any) -> Results:
            """The benchmark action wrapper."""
            # The `kwargs` here are the per-variation kwargs from the Case.
            return _bench.run(action=action, n=1, kwargs=kwargs)

        # Create a simplebench Case, passing the explicit arguments from the signature.
        case = Case(
            action=benchmark_action_wrapper,
            benchmark_id=benchmark_id,
            git_info=git_info,
            group=group,
            title=title or default_title,
            description=description,
            iterations=iterations,
            warmup_iterations=warmup_iterations,
            rounds=rounds,
            timer=timer,
            min_time=min_time,
            max_time=max_time,
            timeout=timeout,
            variation_cols=variation_cols,
            kwargs_variations=kwargs_variations,
            runner=runner,
            callback=callback,
            options=options
        )

        # Register the case with the session
        self._session.add_case(case)


@pytest.fixture
def benchmark(request: pytest.FixtureRequest) -> BenchmarkRegistrar:
    """
    The simplebench-powered benchmark fixture.

    It retrieves the session and provides a callable object to register
    a benchmark case for the current test node.

    :param request: The pytest FixtureRequest object.
    :return: A BenchmarkRegistrar instance to register benchmark cases.
    """
    if not request.config.getoption("--sb-enable"):
        pytest.skip("SimpleBench is not enabled. Use --sb-enable to run benchmarks.")

    # Retrieve the session object we created in pytest_configure
    sb_session = getattr(request.config, "_simplebench_session", None)
    if sb_session is None:
        # This should not happen if --sb-enable is used, but it's a good safeguard.
        pytest.fail("SimpleBench session not initialized.", pytrace=False)

    # Provide the registrar object to the test function.
    # The user's call will be forwarded to BenchmarkRegistrar.__call__
    return BenchmarkRegistrar(sb_session, request.node)


# Phase 3: Execution and Reporting
# --------------------------------

def pytest_sessionfinish(session: pytest.Session) -> None:
    """
    Called after the whole test session finishes.
    We now run the simplebench session and let it handle reporting.

    :param session: The pytest Session object.
    """
    log.debug("pytest_sessionfinish hook called.")
    sb_session: Session = getattr(session.config, "_simplebench_session", None)  # type: ignore[reportAssigmentType]

    if not sb_session or not sb_session.cases:
        log.debug("No simplebench cases found, skipping run.")
        return

    log.info("Calling sb_session.run() for %d cases", len(sb_session.cases))
    sb_session.run()
    sb_session.report()


def pytest_terminal_summary(terminalreporter: Any, config: Config) -> None:
    """
    Add the captured benchmark results to the pytest terminal summary.

    :param terminalreporter: The pytest terminal reporter object.
    :param config: The pytest Config object.
    """
    log.debug("pytest_terminal_summary hook called.")
    pytest_reporter: PytestReporter = getattr(config, "_simplebench_pytest_reporter", None)  # type: ignore[reportAssignmentType]  # noqa: E501
    if not pytest_reporter or not pytest_reporter.rendered_tables:
        log.debug("No rendered tables found in PytestReporter, skipping summary.")
        return

    log.info("Found %d rendered tables to print in summary.", len(pytest_reporter.rendered_tables))
    # Get the real terminal writer from pytest
    writer = terminalreporter._tw  # pylint: disable=protected-access
    writer.sep("=", "simplebench results", blue=True)

    # Use a Rich Console to print the captured tables to pytest's writer
    console = Console(file=writer, force_terminal=True)
    for table in pytest_reporter.rendered_tables:
        console.print(table)
