"""Module providing timing utilities."""
from __future__ import annotations

import importlib.util
import sys
import time
from functools import cache
from types import ModuleType
from typing import Callable

import numpy as np

from simplebench.exceptions import SimpleBenchImportError, SimpleBenchRuntimeError, SimpleBenchTypeError
from simplebench.validators import validate_positive_int

from .exceptions import _TimersErrorTag


def fake_timer() -> int:
    """A fake timer function that always returns zero.

    This is used for testing purposes and not for actual timing measurements.
    """
    return 0


_SUPPORTED_TIMERS: set[Callable[[], int]] = {
    time.monotonic_ns,
    time.perf_counter_ns,
    time.process_time_ns,
    time.thread_time_ns,
    fake_timer,
}

_BASE_TIMER_NAMES: dict[Callable[[], int], str] = {
    time.monotonic_ns: "time.monotonic_ns",
    time.perf_counter_ns: "time.perf_counter_ns",
    time.process_time_ns: "time.process_time_ns",
    time.thread_time_ns: "time.thread_time_ns",
    fake_timer: "fake_timer",
}


def timer_identifier(timer: Callable[[], int]) -> str:
    """Return a human-readable identifier for the given timer function.

    :param timer: The timer function to identify.
    :return: A string identifier for the timer.
    :rtype: str
    :raises SimpleBenchTypeError: If the provided timer is not supported.
    """
    if timer not in _BASE_TIMER_NAMES:
        raise SimpleBenchTypeError(
            f"The timer argument function '{str(timer)}' is not a supported timer function",
            tag=_TimersErrorTag.TIMER_IDENTIFIER_INVALID_TIMER_FUNCTION)
    return _BASE_TIMER_NAMES[timer]


def _create_timers_profiles_module() -> ModuleType:
    """Create a module to hold dynamically created timer profile functions.

    The module is created using :mod:`importlib` and added to :data:`sys.modules`
    under the name 'simplebench._timers_profiles'. If the module already exists
    in :data:`sys.modules`, it is returned as is.

    :return: The created or existing _timers_profiles module.
    :rtype: ModuleType
    :raises SimpleBenchImportError: If the module could not be created.
    """
    spec = importlib.util.spec_from_loader('simplebench._timers_profiles', loader=None)
    if spec is None:   # pragma: no cover   # Should not ever happen
        raise SimpleBenchImportError(  # pragma: no cover
            'Could not create spec for simplebench._timers_profiles module',
            tag=_TimersErrorTag.TIMERS_CREATE_TIMERS_PROFILES_MODULE_SPEC_FAILED)
    if 'simplebench._timers_profiles' in sys.modules:
        return sys.modules['simplebench._timers_profiles']  # Return existing module
    timers_module = importlib.util.module_from_spec(spec)
    sys.modules['simplebench._timers_profiles'] = timers_module
    return timers_module


_timers_profiles_module = _create_timers_profiles_module()  # Ensure the _timers_profiles module exists
"""A dynamically created module to hold generated timer profile functions."""


def _timer_collector_function(samples: int) -> Callable[[Callable[[], int]], tuple[int, ...]]:
    """Return a timer collector function.

    This function generates and compiles a new function that calls the provided
    timer `samples` times in a fully unrolled loop, returning all readings
    as a tuple. This minimizes Python overhead between calls, providing the
    cleanest possible data for precision analysis.

    The generated function is cached in the `simplebench._timers_profiles` module.

    :param samples: The number of samples to collect.
    :return: A function that takes a timer and returns a tuple of readings.
    """
    samples = validate_positive_int(
        samples, 'samples',
        _TimersErrorTag.TIMER_PROFILE_FUNCTION_INVALID_ROUNDS_TYPE,
        _TimersErrorTag.TIMER_PROFILE_FUNCTION_INVALID_ROUNDS_VALUE)

    collector_name = f'_timer_collector_function_{samples}'
    if not hasattr(_timers_profiles_module, collector_name):
        # Generate a function like: def collector(timer): return (timer(), timer(), timer(), ...)
        func_body = f'({", ".join(["timer()"] * samples)},)'
        func_code = f'def {collector_name}(timer: Callable[[], int]) -> tuple[int, ...]:\n    return {func_body}'
        exec(func_code, _timers_profiles_module.__dict__)  # pylint: disable=exec-used

    return getattr(_timers_profiles_module, collector_name)


def is_valid_timer(timer: Callable[[], float | int]) -> bool:
    """Checks if the provided timer is supported.

    :param timer: The timer function to check.
    :return: True if the timer is supported, False otherwise.
    :rtype: bool
    """
    return timer in _SUPPORTED_TIMERS


@cache
def timer_precision_ns(timer: Callable[[], int]) -> float:
    """Returns the precison of the passed timer in nanoseconds.

    The precision of the timer is the smallest possible difference between
    two consecutive calls to the timer function. It is determined by calling
    the timer in a tight loop and analyzing the non-zero differences between
    consecutive readings using a Fourier Transform on a histogram of these
    differences.

    This reflects the fundamental resolution of the timer on the current system.

    :param timer: The timer function to analyze.
    :return: The precision of the timer in nanoseconds.
    :raises SimpleBenchTypeError: If the provided timer is not supported.
    :raises SimpleBenchRuntimeError: If the timer does not advance during profiling.
    """
    if not is_valid_timer(timer):
        raise SimpleBenchTypeError(
            f"The timer argument function '{str(timer)}' is not a supported timer function",
            tag=_TimersErrorTag.TIMER_PRECISION_NS_INVALID_TIMER_FUNCTION,
        )

    # 1. WARM-UP & DATA COLLECTION
    # Warm-up to get CPU caches hot and stabilize system state
    for _ in range(10000):
        _ = timer()

    # Use a dynamically generated, unrolled function to collect readings
    # with minimal overhead between calls.
    num_samples = 50000
    collector = _timer_collector_function(num_samples)
    _ = np.array(collector(timer), dtype=np.int64)
    readings = np.array(collector(timer), dtype=np.int64)

    # 2. CALCULATE DIFFERENCES
    # The precision is the smallest step the timer can take. We find this by
    # looking at the differences between consecutive readings.
    diffs = np.diff(readings)

    # Filter out zero-diffs, which happen when two calls are faster than the timer's tick.
    # The non-zero diffs will be multiples of the timer's fundamental precision.
    non_zero_diffs = diffs[diffs > 0]

    if non_zero_diffs.size == 0:
        timer_name = _BASE_TIMER_NAMES[timer]
        raise SimpleBenchRuntimeError(
            f"The timer function '{timer_name}' did not advance during profiling; "
            "it may be on a system with very low resolution. This timer cannot be used.",
            tag=_TimersErrorTag.TIMER_PRECISION_NS_UNUSABLE_TIMER,
        )

    # 3. CREATE A HISTOGRAM OF DIFFERENCES
    min_diff = np.min(non_zero_diffs)
    max_diff = np.max(non_zero_diffs)

    # We only need to analyze a small range of the smallest differences
    # to find the fundamental unit. Cap the histogram range to avoid noise.
    hist_max = min(min_diff * 10, max_diff)
    bins = np.arange(0, hist_max + 2)
    histogram, _ = np.histogram(non_zero_diffs, bins=bins)

    # 4. PERFORM THE FOURIER TRANSFORM
    fft_result = np.abs(np.fft.rfft(histogram))
    fft_result[0] = 0  # Ignore the DC component

    # 5. FIND THE DOMINANT FREQUENCY
    peaks = _find_peaks_numpy(fft_result, height=np.max(fft_result) * 0.1)
    if not peaks.any():
        # If FFT fails (e.g., too much noise), fall back to the most direct method:
        # the smallest observed non-zero difference.
        return float(min_diff)

    dominant_peak_index = peaks[np.argmax(fft_result[peaks])]

    # 6. CONVERT FREQUENCY TO PRECISION
    n: int = len(histogram)
    dominant_frequency = dominant_peak_index / n
    precision = 1.0 / dominant_frequency

    return precision


def _find_peaks_numpy(x: np.ndarray, height: float) -> np.ndarray:
    """A lightweight, numpy-based implementation to find peaks in a 1D array.

    This function is a replacement for scipy.signal.find_peaks to avoid the
    heavy dependency. It finds local maxima that are greater than their
    immediate neighbors and meet a minimum height requirement.

    :param x: The input array.
    :param height: The minimum height for a peak to be considered.
    :return: An array of indices of the found peaks.
    """
    # A point is a peak if it is greater than its two neighbors
    # Compare element to its left neighbor and its right neighbor
    peaks_bool = np.logical_and(x[1:-1] > x[:-2], x[1:-1] > x[2:])

    # Get the indices of the peaks. Add 1 to account for the slicing.
    peak_indices = np.where(peaks_bool)[0] + 1

    # Filter peaks by the minimum height requirement
    high_peaks_indices = peak_indices[x[peak_indices] > height]

    return high_peaks_indices


@cache
def timer_overhead_ns(timer: Callable[[], int], samples: int = 50000) -> float:
    """Estimate the overhead of calling the timer function.

    This function measures the average time taken to call the provided
    timer function by collecting a large number of consecutive readings and
    analyzing the distribution of the differences. This provides a more
    accurate measurement than a simple bulk average.

    The overhead is returned in nanoseconds and represents the mean time taken
    for a single call to the timer function.

    The results are cached because the overhead of a timer function is expected
    to be fairly constant for a given system and timer on short timescales
    while computing it is expensive.

    :param timer: The timer function to measure.
    :param samples: The number of samples to collect for the analysis.
    :return: The mean overhead of calling the timer in nanoseconds.
    :raises SimpleBenchTypeError: If the provided timer is not supported.
    """
    if not is_valid_timer(timer):
        raise SimpleBenchTypeError(
            f"The timer argument function '{str(timer)}' is not a supported timer function",
            tag=_TimersErrorTag.TIMER_OVERHEAD_NS_INVALID_TIMER_FUNCTION,
        )

    # Use the unrolled collector to get clean readings
    collector = _timer_collector_function(samples)

    # Perform a warm-up run to stabilize CPU state
    _ = collector(timer)

    start = timer()

    # Perform the measurement run
    readings = np.array(collector(timer), dtype=np.int64)

    end = timer()

    # Check if the timer advanced at all during the profiling run
    if end - start == 0:
        timer_name = _BASE_TIMER_NAMES[timer]
        raise SimpleBenchRuntimeError(
            f"The timer function '{timer_name}' did not advance during profiling; "
            "it may be on a system with very low resolution. This timer cannot be used.",
            tag=_TimersErrorTag.TIMER_OVERHEAD_NS_UNUSABLE_TIMER,
        )

    # The differences between consecutive readings represent the overhead
    # of a single timer() call.
    diffs = np.diff(readings)

    # Return the mean of the observed overheads.
    return float(np.mean(diffs))
