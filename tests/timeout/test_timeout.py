"""Tests for the Timeout runner."""

import threading
import time

import pytest

from simplebench.exceptions import SimpleBenchValueError
from simplebench.timeout import Timeout
from simplebench.timeout.enums import TimeoutState

# A small delay that is long enough for context switches but short enough for tests.
SHORT_WAIT = 0.05
# A longer delay guaranteed to trigger a timeout in tests.
LONG_WAIT = 0.5


class TestTimeout:
    """Test suite for the Timeout runner."""

    def test_callable_completes_successfully(self):
        """Test that a callable shorter than the timeout completes successfully."""
        timeout = Timeout(timeout_interval=LONG_WAIT)
        result = timeout.run(time.sleep, SHORT_WAIT)
        assert timeout.state == TimeoutState.EXECUTED
        assert result is None  # time.sleep returns None

    def test_callable_times_out_and_raises_exception(self):
        """Test that a timeout raises TimeoutError."""
        timeout = Timeout(timeout_interval=SHORT_WAIT)
        with pytest.raises(TimeoutError):
            timeout.run(time.sleep, LONG_WAIT)
        assert timeout.state == TimeoutState.TIMED_OUT

    def test_other_exception_is_propagated(self):
        """Test that an unrelated exception inside the callable is always propagated."""
        def func_that_raises():
            raise ValueError("test error")

        timeout = Timeout(timeout_interval=LONG_WAIT)
        with pytest.raises(ValueError, match="test error"):
            timeout.run(func_that_raises)
        assert timeout.state == TimeoutState.FAILED

    def test_invalid_timeout_interval_raises_error(self):
        """Test that a negative timeout interval raises a ValueError."""
        with pytest.raises(SimpleBenchValueError):
            Timeout(timeout_interval=-1)

    def test_nested_timeouts_inner_fires(self):
        """Test that an inner timeout's exception propagates correctly."""
        def inner_task():
            # This inner timeout is short and will fire
            inner_timeout = Timeout(timeout_interval=SHORT_WAIT)
            inner_timeout.run(time.sleep, LONG_WAIT)

        # The outer timeout is long and will not fire
        outer_timeout = Timeout(timeout_interval=LONG_WAIT)
        with pytest.raises(TimeoutError):
            outer_timeout.run(inner_task)
        # The outer timeout itself failed because its task raised an exception
        assert outer_timeout.state == TimeoutState.FAILED

    def test_nested_timeouts_outer_fires(self):
        """Test that an outer timeout correctly interrupts a block with an inner timeout."""
        def inner_task_long():
            # Inner timeout is long and will be interrupted by the outer timeout
            inner_timeout = Timeout(timeout_interval=LONG_WAIT)
            inner_timeout.run(time.sleep, LONG_WAIT)

        # Outer timeout is short and will fire
        outer_timeout = Timeout(timeout_interval=SHORT_WAIT)
        with pytest.raises(TimeoutError):
            outer_timeout.run(inner_task_long)
        assert outer_timeout.state == TimeoutState.TIMED_OUT

    def test_concurrent_threads_do_not_interfere(self):
        """
        Test that two concurrent Timeout instances in different threads do not interfere.
        """
        results = {}
        barrier = threading.Barrier(2)

        def thread_a_target():
            """This thread should time out."""
            try:
                timeout_a = Timeout(timeout_interval=SHORT_WAIT)

                def task_a():
                    barrier.wait()  # Sync with thread B
                    time.sleep(LONG_WAIT)
                timeout_a.run(task_a)
                results['a'] = 'completed'  # Should not be reached
            except TimeoutError:
                results['a'] = 'timed_out'
            except Exception as e:  # pylint: disable=broad-exception-caught
                results['a'] = e

        def thread_b_target():
            """This thread should complete successfully."""
            try:
                timeout_b = Timeout(timeout_interval=LONG_WAIT)

                def task_b():
                    barrier.wait()  # Sync with thread A
                    time.sleep(SHORT_WAIT)
                timeout_b.run(task_b)
                results['b'] = 'completed'
            except Exception as e:  # pylint: disable=broad-exception-caught
                results['b'] = e

        thread_a = threading.Thread(target=thread_a_target)
        thread_b = threading.Thread(target=thread_b_target)

        thread_a.start()
        thread_b.start()

        thread_a.join(timeout=2)
        thread_b.join(timeout=2)

        assert results.get('a') == 'timed_out'
        assert results.get('b') == 'completed'
