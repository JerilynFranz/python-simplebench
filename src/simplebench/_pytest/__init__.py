"""
A pytest plugin to provide a similar interface to `pytest-benchmark`
powered by the simplebench framework.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional

import pytest
from rich.console import Console

from simplebench import defaults
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

    config._simplebench_session = sb_session  # pylint: disable=protected-access,line-too-long  # type: ignore[reportAttributeAccessIssue]  # noqa: E501
    config._simplebench_pytest_reporter = pytest_reporter  # pylint: disable=protected-access,line-too-long  # type: ignore[reportAttributeAccessIssue]  # noqa: E501
    log.debug("simplebench configured with session %r and reporter %r", sb_session, pytest_reporter)


# Phase 2: The Fixture (Test Case Collection)
# -------------------------------------------

class BenchmarkRegistrar:
    """
    A callable object provided by the `benchmark` fixture to register a benchmark case.

    The only REQUIRED parameter is `action`.

    :param benchmark_id: An optional unique identifier for the benchmark case.

        If None, a transient ID is assigned. This is meant to provide a stable identifier for the
        benchmark case across multiple runs for tracking purposes. If not provided,
        an attempt will be made to generate a stable ID based on the the action function
        name, signature, and group. If that is not possible, a transient ID based
        on the instance's id() will be used. If a transient ID is used, it will differ
        between runs and cannot be used to correlate results across multiple runs.

        Benchmark ids must be unique within a benchmarking session and stable across runs
        or they cannot be used for tracking benchmark results over time.
    :param git_info: An optional GitInfo instance representing the state of the Git repository.

        If not provided, the GitInfo will be automatically retrieved from the current
        context of the caller if the code is part of a Git repository.
    :param action: The function to perform the benchmark.

        This function must accept a `bench` instance of type SimpleRunner and
        arbitrary keyword arguments ('**kwargs'). See the ``ActionRunner``
        protocol for the exact signature required. It must return a `Results` object.
    :param group: The benchmark reporting group to which the benchmark case belongs.

        Benchmarks with the same group can be selected for execution without running
        other benchmarks. If not specified, the default group 'default' is used.
    :param title: The title of the benchmark case.

        If None, the name of the action function will be used. Cannot be blank.
    :param description: A brief description of the benchmark case.

        If None, the docstring of the action function will be used, or
        '(no description)' if no docstring is available. Cannot be blank.
    :param iterations: The minimum number of iterations to run for the benchmark.
    :param warmup_iterations: The number of warmup iterations to run before the benchmark.
    :param rounds: The number of rounds to run for the benchmark.

        Rounds are multiple runs of calls to the action within an iteration to mitigate timer
        quantization, loop overhead, and other measurement effects for very fast actions. Setup and teardown
        functions are called only once per iteration (all rounds in the same iteration share the same
        setup/teardown context).

        If None, rounds will be auto-calibrated based on the precision and overhead of the timer function
        and the expected execution time of the action. If the action is very fast (e.g., under
        10 microseconds), rounds will be set to a higher value to improve measurement accuracy
        with the goal of reducing timer quantization errors. If the action is slower, rounds
        will be set lower values.

        If specified, it must be a positive integer.
    :param timer: The timer function to use for the benchmark. If None, the default timer
        from the Session() (if set) or from `simplebench.defaults.DEFAULT_TIMER` ({DEFAULT_TIMER})
        is used by benchmark runners that require a timer.

        The timer function should be a callable that returns a float or int representing the current time.
    :param min_time: The minimum time for the benchmark to run in seconds. Its reference depends on the timer used,
        but by default it is wall-clock time.
    :param max_time: The maximum time for the benchmark run in seconds. Its reference depends on the timer used,
        but by default it is wall-clock time.
    :param timeout: How long to wait before timing out a benchmark run (in seconds). It is
        measured as wall-clock time.

        If None, it waits the full duration of ``max_time`` plus the default timeout grace period
        ({DEFAULT_TIMEOUT_GRACE_PERIOD} seconds). It must be a positive float or int that is greater
        than ``max_time`` if provided. This is a safety mechanism to prevent runaway benchmarks.

        If the timeout is reached during a run, a :class:`~simplebench.exceptions.SimpleBenchTimeoutError``
        will be raised, and the benchmark case's state will be set to TIMED_OUT.
    :param variation_cols: kwargs to be used for cols to denote kwarg variations.

        Each key is a keyword argument name, and the value is the column label to use for that
        argument. Only keywords that are also in `kwargs_variations` can be used here. These
        fields will be added to the output of reporters that support them as columns of data
        with the specified labels.

        If None, an empty dict is used.
    :param kwargs_variations: A map of keyword argument names to a list of possible values for that argument.

        Default is {}. When tests are run, the benchmark
        will be executed for each combination of the specified keyword argument variations. The action
        function will be called with a `bench` parameter that is an instance of the runner and the
        keyword arguments for the current variation.
        If None, an empty dict is used.
    :param runner: A custom runner class for the benchmark.

        Any custom runner classes must be a subclass of SimpleRunner and must have a method
        named `run` that accepts the same parameters as SimpleRunner.run and returns a Results object.
        The action function will be called with a `bench` parameter that is an instance of the
        custom runner.
        It may also accept additional parameters to the run method as needed. If additional
        parameters are needed for the custom runner, they will need to be passed to the run
        method as keyword arguments.
        No support is provided for passing additional parameters to a custom runner from the @benchmark
        decorator.
    :param callback: A callback function for additional processing of the report.

        The function should must four arguments: the Case instance, the Section,
        the Format, and the generated report data.

        - case (Case): The `Case` instance processed for the report.
        - section (Section): The `Section` of the report.
        - output_format (Format): The `Format` of the report.
        - output (Any): The generated report data. Note that the actual type of this data will
            depend on the Format specified for the report and the type generated by the
            reporter for that Format

        Omit if no callback is needed by a reporter.
    :param options: A list of additional options for the benchmark case.

        Each option is an instance of ReporterOption or a subclass of ReporterOption.
        Reporter options can be used to customize the output of the benchmark reports for
        specific reporters. Reporters are responsible for extracting applicable ReporterOptions
        from the list of options themselves.
        If None, an empty list is used.
    :raises SimpleBenchTypeError: If any parameter is of incorrect type.
    :raises SimpleBenchValueError: If any parameter has an invalid value.
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
    pytest_reporter: PytestReporter = getattr(config, "_simplebench_pytest_reporter", None)  # pylint: disable=line-too-long  # type: ignore[reportAssignmentType]  # noqa: E501
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
