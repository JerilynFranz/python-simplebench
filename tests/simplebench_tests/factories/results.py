"""Factories for creating Results, Iteration, and Stats test objects."""

from simplebench.case import Results
from simplebench.metrics import metrics_registry
from simplebench.simplebench_types import Extras, Iterations, MetricsTimers, Values
from simplebench_tests.kwargs import ResultsKWArgs

from ._primitives import (
    case_group_factory,
    description_factory,
    n_factory,
    rounds_factory,
    title_factory,
    variation_marks_factory,
)

def results_factory() -> Results:
    """Return a default Results instance for testing purposes.

    It creates a Results instance with default test parameters by calling the
    results_kwargs_factory to get the necessary keyword arguments.

    :return: A Results instance with default test parameters.
    :rtype: Results
    """
    return Results(**results_kwargs_factory())

def results_kwargs_factory() -> ResultsKWArgs:
    """Returns a configured ResultsKWArgs instance for testing purposes.

    It creates a ResultsKWArgs instance with default test parameters by calling
    the various factory functions for each parameter.

    :ivar group: The case group.
    :vartype group: str
    :ivar title: The title of the results.
    :vartype title: str
    :ivar description: The description of the results.
    :vartype description: str
    :ivar n: The number of iterations.
    :vartype n: int
    :ivar rounds: The number of rounds.
    :vartype rounds: int
    :ivar iterations: An Iterations instance containing the metrics and their corresponding values.
    :vartype iterations: Iterations
    :ivar metrics_timers: A mapping of Metrics to their timing information.
    :vartype metrics_timers: MetricsTimers
    :ivar variation_marks: The variation marks.
    :vartype variation_marks: VariationMarks

    :ivar extra_info: Extra information.
    :vartype extra_info: dict[str, Any]
    :return: A ResultsKWArgs instance with default test parameters.
    :rtype: ResultsKWArgs
    """
    return ResultsKWArgs(group=case_group_factory(),
                         title=title_factory(),
                         description=description_factory(),
                         n=n_factory(),
                         rounds=rounds_factory(),
                         iterations=iterations_factory(),
                         metrics_timers=metrics_timers_factory(),
                         variation_marks=variation_marks_factory(),
                         extra_info=results_extra_info_factory())


def results_extra_info_factory() -> Extras:
    """Return a default dictionary of extra info for testing purposes.

    :return: A dictionary with extra info.
    :rtype: dict[str, Any]
    """
    return Extras()


def iterations_factory() -> Iterations:
    """Return a default sequence of Iteration instances for testing purposes.

    It creates an Iterations instance with default test parameters by using the
    metrics_registry to get the standard timing and operations stats metrics, and
    assigning them Values instances with a range of values.

    - `STD_TIMING_STATS` :class:`Metric` is assigned :class:`Values` with integers from 1 to 9.
    - `STD_OPS_STATS` :class:`Metric` is assigned :class:`Values` with the reciprocals of integers from 1 to 9.

    :return: An Iterations instance with default test parameters.
    :rtype: Iterations
    """

    timing_stats_metric = metrics_registry['STD_TIMING_STATS']
    timing_stats_values = Values(tuple(value for value in range(1,10)))
    ops_stats_metric = metrics_registry['STD_OPS_STATS']
    ops_stats_values = Values(tuple(1/value for value in range(1,10)))
    return Iterations({
        timing_stats_metric: timing_stats_values,
        ops_stats_metric: ops_stats_values,
    })

def metrics_timers_factory() -> MetricsTimers:
    """Return a default MetricsTimers instance for testing purposes.

    It creates a MetricsTimers instance with default test parameters by using the
    metrics_registry to get the standard timing and operations stats metrics, and
    assigning them string timer names.

    - `STD_TIMING_STATS` :class:`Metric` is assigned the timer name "timing.perf_counter_ns".
    - `STD_OPS_STATS` :class:`Metric` is assigned the timer name "timing.perf_counter_ns".

    :return: A MetricsTimers instance with default test parameters.
    :rtype: MetricsTimers
    """
    timing_stats_metric = metrics_registry['STD_TIMING_STATS']
    timing_name = 'timing.perf_counter_ns'
    ops_stats_metric = metrics_registry['STD_OPS_STATS']
    ops_name = 'timing.perf_counter_ns'
    return MetricsTimers({
        timing_stats_metric: timing_name,
        ops_stats_metric: ops_name,
    })
