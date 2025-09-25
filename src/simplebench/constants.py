# -*- coding: utf-8 -*-
"""constants for simplebenchmark."""
import time

# Note: The following constants are defined here for easy access and modification.
# They are used throughout the SimpleBench framework.

MIN_MEASURED_ITERATIONS: int = 3
"""Minimum number of iterations for statistical analysis."""

DEFAULT_ITERATIONS: int = 20
"""Default number of iterations for benchmarking."""

DEFAULT_WARMUP_ITERATIONS: int = 10
"""Default number of warmup iterations before benchmarking."""

DEFAULT_TIMER = time.perf_counter_ns
"""Default timer function for benchmarking."""

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

DEFAULT_CUSTOM_METRICS_UNIT: str = 'units'
"""Default unit for custom metrics."""

DEFAULT_CUSTOM_METRICS_SCALE: float = 1.0
"""Default scaling factor for custom metrics (1.0 -> 1.0)."""

BASE_MEMORY_UNIT: str = 'bytes'
"""Base unit for memory usage."""

DEFAULT_SIGNIFICANT_FIGURES: int = 3
"""Default number of significant figures for output values (3 significant figures)."""
