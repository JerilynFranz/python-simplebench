"""Tests for the pytest simplebench plugin."""
from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simplebench import BenchmarkRegistrar


def test_sleep(benchmark: BenchmarkRegistrar) -> None:
    """Test that the pytest simplebench plugin can benchmark a sleep action."""
    def sleep_action(duration: float) -> None:
        time.sleep(duration)

    benchmark(action=sleep_action, benchmark_id="sleep_0.01", iterations=5, kwargs_variations={'duration': [0.01]})
