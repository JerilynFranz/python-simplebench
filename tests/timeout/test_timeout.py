"""Tests for the Timeout runner."""

import threading
import time

import pytest

from simplebench.exceptions import SimpleBenchTimeoutError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.timeout import Timeout, TimeoutErrorTag, TimeoutState

# A small delay that is long enough for context switches but short enough for tests.
SHORT_WAIT = 0.05
# A longer delay guaranteed to trigger a timeout in tests.
LONG_WAIT = 0.5


class TestTimeout:
    """Test suite for the Timeout runner."""

    def test_timeout_initial_state(self):
        """Test that the initial state of Timeout is PENDING."""
        timeout = Timeout(timeout_interval=SHORT_WAIT)
        assert timeout.state == TimeoutState.PENDING, f"Initial state should be PENDING not {timeout.state}"

    def test_callable_completes_successfully(self):
        """Test that a callable shorter than the timeout completes successfully."""
        timeout = Timeout(timeout_interval=LONG_WAIT)
        result = timeout.run(time.sleep, SHORT_WAIT)
        assert timeout.state == TimeoutState.FINISHED, f"State should be FINISHED not {timeout.state}"
        assert result is None  # time.sleep returns None

    def test_callable_times_out_and_raises_exception(self):
        """Test that a timeout raises SimpleBenchTimeoutError."""
        timeout = Timeout(timeout_interval=SHORT_WAIT)
        errors = []
        successfully_failed = False
        try:
            timeout.run(time.sleep, LONG_WAIT)
        except SimpleBenchTimeoutError as e:
            successfully_failed = True
            if not e.func_name == "sleep":
                errors.append(f"Function name in exception should be 'sleep', got '{e.func_name}'")
            if timeout.state != TimeoutState.TIMED_OUT:
                errors.append(f"State should be TIMED_OUT not {timeout.state}")
        except BaseException as e:  # pylint: disable=broad-exception-caught
            errors.append(f"Expected SimpleBenchTimeoutError was not raised, {e} was raised instead.")
        if not successfully_failed:
            pytest.fail("The timeout did not raise SimpleBenchTimeoutError as expected.")
        if errors:
            pytest.fail(" ; ".join(errors))

    def test_raises_timeout_exception_with_correct_function_name(self):
        """Test that a timeout raises SimpleBenchTimeoutError."""
        timeout = Timeout(timeout_interval=SHORT_WAIT)
        errors = []

        def long_running_function():
            time.sleep(LONG_WAIT)

        expected_func_name = "TestTimeout.test_raises_timeout_exception_with_correct_function_name.<locals>.long_running_function"  # pylint: disable=line-too-long  # noqa: E501
        successfully_failed = False
        try:
            timeout.run(long_running_function)
        except SimpleBenchTimeoutError as e:
            successfully_failed = True
            if e.func_name != expected_func_name:
                errors.append(f"Function name in exception should be '{expected_func_name}', got '{e.func_name}'")
            if timeout.state != TimeoutState.TIMED_OUT:
                errors.append(f"State should be TIMED_OUT not {timeout.state}")
        except BaseException as e:  # pylint: disable=broad-exception-caught
            errors.append(f"Expected SimpleBenchTimeoutError was not raised, {e} was raised instead.")
        if not successfully_failed:
            pytest.fail("The timeout did not raise SimpleBenchTimeoutError as expected.")
        if errors:
            pytest.fail(" ; ".join(errors))

    def test_other_exception_is_propagated(self):
        """Test that an unrelated exception inside the callable is always propagated."""
        def func_that_raises():
            raise ValueError("test error")

        timeout = Timeout(timeout_interval=LONG_WAIT)
        with pytest.raises(ValueError, match="test error"):
            timeout.run(func_that_raises)
        assert timeout.state == TimeoutState.FAILED, f"State should be FAILED not {timeout.state}"

    def test_invalid_timeout_interval_raises_correct_error(self):
        """Test that a timeout interval of zero or negative raises a SimpleBenchValueError."""
        successfully_failed = False
        try:
            Timeout(timeout_interval=0)
        except SimpleBenchValueError as e:
            if e.tag_code != TimeoutErrorTag.INVALID_TIMEOUT_INTERVAL_VALUE:
                pytest.fail(f"Exception tag should be INVALID_TIMEOUT_INTERVAL, got {e.tag_code}")
            successfully_failed = True
        if not successfully_failed:
            pytest.fail("Expected SimpleBenchValueError was not raised for zero timeout interval.")

        successfully_failed = False
        try:
            Timeout(timeout_interval="-1")  # type: ignore[arg-type]
        except SimpleBenchTypeError as e:
            if e.tag_code != TimeoutErrorTag.INVALID_TIMEOUT_INTERVAL_TYPE:
                pytest.fail(f"Exception tag should be INVALID_TIMEOUT_INTERVAL_TYPE, got {e.tag_code}")
            successfully_failed = True
        if not successfully_failed:
            pytest.fail("Expected SimpleBenchTypeError was not raised for string timeout interval.")
        if not successfully_failed:
            pytest.fail("Expected SimpleBenchValueError was not raised for negative timeout interval.")

    def test_non_callable_raises_type_error(self):
        """Test that passing a non-callable to run raises SimpleBenchTypeError."""
        timeout = Timeout(timeout_interval=SHORT_WAIT)
        successfully_failed = False
        try:
            timeout.run("not_a_function")  # type: ignore[arg-type]
        except SimpleBenchTypeError as e:
            if e.tag_code != TimeoutErrorTag.NON_CALLABLE_FUNCTION_ARGUMENT:
                pytest.fail(f"Exception tag should be NON_CALLABLE_FUNCTION_ARGUMENT, got {e.tag_code}")
            successfully_failed = True
        if not successfully_failed:
            pytest.fail("Expected SimpleBenchTypeError was not raised for non-callable argument.")

    def test_nested_timeouts_inner_fires(self):
        """Test that an inner timeout's exception propagates correctly."""
        def inner_task():
            # This inner timeout is short and will fire
            inner_timeout = Timeout(timeout_interval=SHORT_WAIT)
            inner_timeout.run(time.sleep, LONG_WAIT)

        # The outer timeout is long and will not fire
        outer_timeout = Timeout(timeout_interval=LONG_WAIT)
        with pytest.raises(SimpleBenchTimeoutError):
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
        with pytest.raises(SimpleBenchTimeoutError):
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
            except SimpleBenchTimeoutError:
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
