"""Factories for creating Results, Iteration, and Stats test objects."""
from __future__ import annotations

from typing import Any, Sequence

from simplebench.iteration import Iteration
from simplebench.stats import MemoryUsage, OperationsPerInterval, OperationTimings, PeakMemoryUsage

from ..kwargs import ResultsKWArgs
from ._primitives import (
    case_group_factory,
    description_factory,
    interval_scale_factory,
    interval_unit_factory,
    memory_scale_factory,
    memory_unit_factory,
    n_factory,
    ops_per_interval_scale_factory,
    ops_per_interval_unit_factory,
    rounds_factory,
    title_factory,
    total_elapsed_factory,
    variation_cols_factory,
    variation_marks_factory,
)


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
    :ivar total_elapsed: The total elapsed time.
    :vartype total_elapsed: float
    :ivar iterations: A sequence of Iteration instances.
    :vartype iterations: Sequence[Iteration]
    :ivar variation_cols: The variation columns.
    :vartype variation_cols: Sequence[str]
    :ivar variation_marks: The variation marks.
    :vartype variation_marks: Sequence[str]
    :ivar interval_unit: The interval unit.
    :vartype interval_unit: str
    :ivar interval_scale: The interval scale.
    :vartype interval_scale: float
    :ivar ops_per_interval_unit: The ops per interval unit.
    :vartype ops_per_interval_unit: str
    :ivar ops_per_interval_scale: The ops per interval scale.
    :vartype ops_per_interval_scale: float
    :ivar memory_unit: The memory unit.
    :vartype memory_unit: str
    :ivar memory_scale: The memory scale.
    :vartype memory_scale: float
    :ivar ops_per_second: The ops per second.
    :vartype ops_per_second: OperationsPerInterval
    :ivar per_round_timings: The per-round timings.
    :vartype per_round_timings: OperationTimings
    :ivar memory: The memory usage.
    :vartype memory: MemoryUsage
    :ivar peak_memory: The peak memory usage.
    :vartype peak_memory: PeakMemoryUsage
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
                         total_elapsed=total_elapsed_factory(),
                         iterations=iterations_sequence_factory(),
                         variation_cols=variation_cols_factory(),
                         variation_marks=variation_marks_factory(),
                         interval_unit=interval_unit_factory(),
                         interval_scale=interval_scale_factory(),
                         ops_per_interval_unit=ops_per_interval_unit_factory(),
                         ops_per_interval_scale=ops_per_interval_scale_factory(),
                         memory_unit=memory_unit_factory(),
                         memory_scale=memory_scale_factory(),
                         ops_per_second=ops_per_interval_factory(),
                         per_round_timings=per_round_timings_factory(),
                         memory=memory_factory(),
                         peak_memory=peak_memory_factory(),
                         extra_info=results_extra_info_factory())


def results_extra_info_factory() -> dict[str, Any]:
    """Return a default dictionary of extra info for testing purposes.

    :return: A dictionary with extra info.
    :rtype: dict[str, Any]
    """
    return {'info_key': 'info_value'}


def iterations_sequence_factory() -> Sequence[Iteration]:
    """Return a default sequence of Iteration instances for testing purposes.

    :return: A sequence containing a single Iteration instance.
    :rtype: Sequence[Iteration]
    """
    return [
        Iteration(
            n=n_factory(),
            rounds=rounds_factory(),
            elapsed=total_elapsed_factory(),
            scale=interval_scale_factory(),
            unit=interval_unit_factory(),
            memory=1400,
            peak_memory=2400,
        )
    ]


def peak_memory_factory() -> PeakMemoryUsage:
    """Return a default PeakMemoryUsage instance for testing purposes.

    :return: Container for peak memory usage data.
    :rtype: PeakMemoryUsage
    """
    return PeakMemoryUsage(
        unit=memory_unit_factory(),
        scale=memory_scale_factory(),
        data=[2200, 2250, 2150, 2300, 2100],
        iterations=[
            Iteration(n=n_factory(),
                      rounds=rounds_factory(),
                      elapsed=total_elapsed_factory(),
                      scale=memory_scale_factory(),
                      unit=memory_unit_factory(),
                      memory=1300,
                      peak_memory=2300)
        ],
    )


def memory_factory() -> MemoryUsage:
    """Return a default MemoryUsage instance for testing purposes.

    :return: Container for memory usage data.
    :rtype: MemoryUsage
    """
    return MemoryUsage(
        unit=memory_unit_factory(),
        scale=memory_scale_factory(),
        data=[1200, 1300, 1100, 1250, 1150],
        iterations=[
            Iteration(n=n_factory(),
                      rounds=rounds_factory(),
                      elapsed=total_elapsed_factory(),
                      scale=memory_scale_factory(),
                      unit=memory_unit_factory(),
                      memory=1200,
                      peak_memory=2200)
        ],
    )


def per_round_timings_factory() -> OperationTimings:
    """Return a default OperationTimings instance for testing purposes.

    :return: Container for per-round timing data.
    :rtype: OperationTimings
    """
    return OperationTimings(
        unit=interval_unit_factory(),
        scale=interval_scale_factory(),
        data=[0.05, 0.06, 0.04, 0.07, 0.05],
        iterations=[
            Iteration(n=n_factory(),
                      rounds=rounds_factory(),
                      elapsed=total_elapsed_factory(),
                      scale=interval_scale_factory(),
                      unit=interval_unit_factory(),
                      memory=1500,
                      peak_memory=2500)
        ],
    )


def ops_per_interval_factory() -> OperationsPerInterval:
    """Return a default ops per second value for testing purposes.

    :return: Container for ops per interval data.
    :rtype: OperationsPerInterval
    """
    return OperationsPerInterval(
        unit=ops_per_interval_unit_factory(),
        scale=ops_per_interval_scale_factory(),
        data=[100, 110, 90, 105, 95],
        iterations=[
            Iteration(n=n_factory(),
                      rounds=rounds_factory(),
                      elapsed=total_elapsed_factory(),
                      scale=ops_per_interval_scale_factory(),
                      unit=ops_per_interval_unit_factory(),
                      memory=2000,
                      peak_memory=3000)
        ],
    )
