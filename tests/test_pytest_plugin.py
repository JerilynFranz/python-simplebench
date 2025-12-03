"""Tests for the pytest simplebench plugin."""
import time


def test_sleep(benchmark):
    """Test that the pytest simplebench plugin can benchmark a sleep action."""
    def sleep_action(duration: float):
        time.sleep(duration)

    benchmark(sleep_action, kwargs_variations={'duration': [0.01]})
