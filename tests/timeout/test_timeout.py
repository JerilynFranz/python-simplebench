"""Tests for the Timeout context manager."""

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
    """Test suite for the Timeout context manager."""

    def test_block_completes_successfully(self):
        """Test that a block shorter than the timeout completes successfully."""
        with Timeout(timeout_interval=LONG_WAIT) as timeout:
            time.sleep(SHORT_WAIT)
        assert timeout.state == TimeoutState.EXECUTED

    def test_block_times_out_with_swallowed_exception(self):
        """Test that a timeout with exception swallowing works as expected."""
        try:
            with Timeout(timeout_interval=SHORT_WAIT, swallow_exception=True) as timeout:
                time.sleep(LONG_WAIT)
        except TimeoutError as e:
            pytest.fail(f"TimeoutError was not swallowed: {e}")
        except Exception as e:  # pylint: disable=broad-exception-caught
            pytest.fail(f"Unexpected exception raised: {e}")
        assert timeout.state == TimeoutState.TIMED_OUT, f"Expected TIMED_OUT but got {timeout.state}"

    def test_block_times_out_and_raises_exception(self):
        """Test that a timeout raises TimeoutError when not swallowed."""
        with pytest.raises(TimeoutError):
            with Timeout(timeout_interval=SHORT_WAIT, swallow_exception=False):
                time.sleep(LONG_WAIT)

    def test_other_exception_is_propagated(self):
        """Test that an unrelated exception inside the block is always propagated."""
        with pytest.raises(ValueError, match="test error"):
            with Timeout(timeout_interval=LONG_WAIT) as timeout:
                raise ValueError("test error")
        assert timeout.state == TimeoutState.FAILED  # type: ignore[reportPossiblyUnboundVariable]

    def test_cancel_method_prevents_timeout(self):
        """Test that calling cancel() prevents the timeout from firing."""
        with Timeout(timeout_interval=SHORT_WAIT) as timeout:
            timeout.cancel()
            time.sleep(LONG_WAIT)  # Sleep past the original timeout
        assert timeout.state == TimeoutState.CANCELED, f"Expected CANCELED but got {timeout.state}"

    def test_invalid_timeout_interval_raises_error(self):
        """Test that a negative timeout interval raises a ValueError."""
        with pytest.raises(SimpleBenchValueError):
            Timeout(timeout_interval=-1)

    def test_nested_timeouts_inner_fires(self):
        """Test that an inner timeout firing is handled correctly and not swallowed by the outer."""
        with pytest.raises(TimeoutError):
            # Outer timeout is long
            with Timeout(timeout_interval=LONG_WAIT, swallow_exception=True):
                # Inner timeout is short and will fire, but is not swallowed
                with Timeout(timeout_interval=SHORT_WAIT, swallow_exception=False):
                    time.sleep(LONG_WAIT)

    def test_nested_timeouts_outer_fires(self):
        """Test that an outer timeout correctly interrupts a block with an inner timeout."""
        with pytest.raises(TimeoutError):
            # Outer timeout is short and will fire
            with Timeout(timeout_interval=SHORT_WAIT, swallow_exception=False):
                # Inner timeout is long and will be interrupted
                with Timeout(timeout_interval=LONG_WAIT, swallow_exception=True):
                    time.sleep(LONG_WAIT)

    def test_concurrent_threads_do_not_interfere(self):
        """
        Test that two concurrent Timeout instances in different threads do not interfere,
        validating the use of instance-specific thread IPC mechanisms.
        """
        results = {}
        barrier = threading.Barrier(2)

        def thread_a_target():
            """This thread should time out."""
            try:
                with Timeout(timeout_interval=SHORT_WAIT, swallow_exception=False):
                    barrier.wait()  # Sync with thread B
                    time.sleep(LONG_WAIT)
                results['a'] = 'completed'  # Should not be reached
            except TimeoutError:
                results['a'] = 'timed_out'
            except Exception as e:  # pylint: disable=broad-exception-caught
                results['a'] = e

        def thread_b_target():
            """This thread should complete successfully."""
            try:
                with Timeout(timeout_interval=LONG_WAIT, swallow_exception=False):
                    barrier.wait()  # Sync with thread A
                    time.sleep(SHORT_WAIT)
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
