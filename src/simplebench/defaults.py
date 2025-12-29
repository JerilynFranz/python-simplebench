"""Defaults for SimpleBench."""
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simplebench.benchmark_runner import BenchmarkRunner

# Note: The following constants are defined here for easy access and modification.
# They are used throughout the SimpleBench framework.

_DEFAULT_RUNNERS: list[type["BenchmarkRunner"]] = []


class _NoDefault:
    """A class to represent a no default value."""


_NO_DEFAULT = _NoDefault()


def default_runners(
        runners: list[type["BenchmarkRunner"]] | _NoDefault | None = _NO_DEFAULT) -> list[type["BenchmarkRunner"]]:
    """Default list of runner classes to use for benchmarking.

    This function allows you to set or get the default list of runner classes
    used for benchmarking.

    - If no argument is provided, the function returns the current default list of runners.
    - If a list of runner classes is provided, the function sets the default list of runners
        and returns the updated list.
    - If `None` is provided, the function resets the default list of runners
        to the default value and returns the updated list.

    :param runners: List of runner classes to use for benchmarking.
    :return: List of runner classes to use for benchmarking.

    Currently, the default runners list is `[SimpleRunner]`."""
    is_first_call = not _DEFAULT_RUNNERS and runners is _NO_DEFAULT
    is_reset_call = runners is None

    # THIS IS WHERE THE BASE DEFAULT RUNNERS ARE SET
    if is_first_call or is_reset_call:
        from simplebench.benchmark_runner import SimpleRunner  # pylint: disable=import-outside-toplevel
        _DEFAULT_RUNNERS.clear()
        _DEFAULT_RUNNERS.append(SimpleRunner)
        return _DEFAULT_RUNNERS

    if isinstance(runners, list):
        if not all(issubclass(runner, BenchmarkRunner) for runner in runners):
            raise TypeError("All items in runners must be subclasses of BenchmarkRunner")
        _DEFAULT_RUNNERS.clear()
        _DEFAULT_RUNNERS.extend(runners)  # Mutate in-place
        return _DEFAULT_RUNNERS

    if runners is _NO_DEFAULT:
        return _DEFAULT_RUNNERS

    # If we get here, the input was invalid
    raise TypeError(f"runners must be a list of BenchmarkRunner subclasses or None, not {type(runners)}")


DEFAULT_TIMEOUT_GRACE_PERIOD: float = 10.0
"""Grace period to wait after timeout before forcefully terminating (in seconds)."""

MIN_MEASURED_ITERATIONS: int = 3
"""Minimum number of iterations for statistical analysis."""

DEFAULT_ITERATIONS: int = 20
"""Default number of iterations for benchmarking."""

DEFAULT_WARMUP_ITERATIONS: int = 100
"""Default number of warmup iterations before benchmarking."""

DEFAULT_TIMER = time.perf_counter_ns
"""Default timer function for benchmarking."""

DEFAULT_CPU_TIMER = time.process_time_ns
"""Default CPU timer function for benchmarking."""

DEFAULT_MIN_TIME: float = 5.0
"""Default minimum time for a benchmark run (in seconds)."""

DEFAULT_MAX_TIME: float = 20.0
"""Default maximum time for a benchmark run (in seconds)."""

DEFAULT_INTERVAL_SCALE: float = 1e-9
"""Default scaling factor for time intervals (nanoseconds -> seconds)."""

DEFAULT_INTERVAL_UNIT: str = 'ns'
"""Default unit for time intervals (nanoseconds)."""

BASE_INTERVAL_UNIT: str = 's'
"""Base unit for time intervals."""

DEFAULT_OPS_PER_INTERVAL_SCALE: float = 1.0
"""Default scaling factor for operations per interval (1.0 -> 1.0)."""

DEFAULT_OPS_PER_INTERVAL_UNIT: str = 'Ops/s'
"""Default unit for operations per interval (operations per second)."""

BASE_OPS_PER_INTERVAL_UNIT: str = 'Ops/s'
"""Base unit for operations per interval."""

DEFAULT_MEMORY_SCALE: float = 1.0
"""Default scaling factor for memory usage (1.0 -> 1.0)."""

DEFAULT_MEMORY_UNIT: str = 'bytes'
"""Default unit for memory usage (bytes)."""

BASE_MEMORY_UNIT: str = 'bytes'
"""Base unit for memory usage."""

DEFAULT_SIGNIFICANT_FIGURES: int = 3
"""Default number of significant figures for output values (3 significant figures)."""

DEFAULT_MAX_CORE_DATA_DEPTH: int = 10
"""Default maximum depth for core data structures (10 levels)."""
