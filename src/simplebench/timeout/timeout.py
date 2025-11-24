"""
Raise asynchronous exceptions in other thread, control the timeout of blocks
or callables with a context manager

:param timeout_interval: ``float`` or ``int`` duration enabled to run the context manager block
"""
import ctypes
import threading
from contextlib import AbstractContextManager
from types import TracebackType

from ..exceptions import SimpleBenchRuntimeError, SimpleBenchTypeError, SimpleBenchValueError
from .enums import TimeoutState
from .exceptions import TimeoutErrorTag
from .thread_id import ThreadId

# Create a thread-local storage for the timeout token.
_thread_local = threading.local()


class _NotSet:
    """Sentinel class for unset attributes."""


class Timeout(AbstractContextManager):
    """Context manager for limiting in the time the execution of a block
    using asynchronous threads launching exception.
    """

    def __init__(self, *, timeout_interval: float):
        """Initialize the Timeout context manager.

        :param timeout_interval: ``float`` or ``int`` duration enabled to run the context manager block
        """
        self._target_thread_id = threading.current_thread().ident
        self._set_timeout_interval(timeout_interval)
        self._set_state(TimeoutState.EXECUTED)
        self._lock = threading.Lock()

    @property
    def _target_thread_id(self) -> ThreadId | None:
        """The target thread identifier.

        :raises SimpleBenchRuntimeError: If an attempt to read the value is made
        before it has been set.
        """
        thread_id: ThreadId | None | _NotSet = getattr(self, "_private_target_thread_id", _NotSet())
        if thread_id is None or isinstance(thread_id, ThreadId):
            return thread_id
        raise SimpleBenchRuntimeError(
            "target_thread_id has not been set",
            tag=TimeoutErrorTag.TARGET_THREAD_ID_NOT_SET)

    @_target_thread_id.setter
    def _target_thread_id(self, value: ThreadId | int | None):
        """Set the target thread identifier.

        :param value: Target thread identifier.
        :raises SimpleBenchTypeError: If the value is not a ThreadId, int, or None.
        :raises SimpleBenchValueError: If the value is an int less than 1.
        """
        if isinstance(value, int):
            value = ThreadId(value)
        if not isinstance(value, (ThreadId, type(None))):
            raise SimpleBenchTypeError(
                "target_thread_id must be a ThreadId or None",
                tag=TimeoutErrorTag.INVALID_THREAD_ID_TYPE)
        setattr(self, "_private_target_thread_id", value)

    @property
    def _timer(self) -> threading.Timer:
        """Get the timer thread."""
        timer: threading.Timer | _NotSet = getattr(self, "_private_timer", _NotSet())
        if isinstance(timer, threading.Timer):
            return timer
        raise SimpleBenchRuntimeError(
            "timer has not been set",
            tag=TimeoutErrorTag.TIMER_NOT_SET)

    @_timer.setter
    def _timer(self, value: threading.Timer):
        """Set the timer thread."""
        if not isinstance(value, threading.Timer):
            raise SimpleBenchTypeError(
                "timer must be a threading.Timer instance",
                tag=TimeoutErrorTag.INVALID_TIMER_TYPE)
        setattr(self, "_private_timer", value)

    @property
    def timeout_interval(self) -> float:
        """Get the timeout interval in seconds."""
        interval: float | _NotSet = getattr(self, "_private_timeout_interval", _NotSet())
        if isinstance(interval, float):
            return interval
        raise SimpleBenchRuntimeError(
            "timeout_interval has not been set",
            tag=TimeoutErrorTag.TIMEOUT_INTERVAL_NOT_SET)

    def _set_timeout_interval(self, value: float | int):
        """Set the timeout interval in seconds."""
        if not isinstance(value, (float, int)):
            raise SimpleBenchTypeError(
                "timeout_interval must be a float or int",
                tag=TimeoutErrorTag.INVALID_TIMEOUT_INTERVAL_TYPE)
        if value <= 0:
            raise SimpleBenchValueError(
                "timeout_interval must be greater than zero",
                tag=TimeoutErrorTag.INVALID_TIMEOUT_INTERVAL_VALUE)
        setattr(self, "_private_timeout_interval", float(value))

    @property
    def state(self) -> TimeoutState:
        """Get the current state of the timeout context manager."""
        state: TimeoutState | _NotSet = getattr(self, "_private_state", _NotSet())
        if isinstance(state, TimeoutState):
            return state
        raise SimpleBenchRuntimeError(
            "state has not been set",
            tag=TimeoutErrorTag.STATE_NOT_SET)

    def _set_state(self, value: TimeoutState):
        """Set the current state of the timeout context manager."""
        if not isinstance(value, TimeoutState):
            raise SimpleBenchTypeError(
                "state must be a TimeoutState",
                tag=TimeoutErrorTag.INVALID_STATE_TYPE)
        setattr(self, "_private_state", value)

    def _stop(self):
        """Called by timer thread at timeout."""
        should_raise = False
        with self._lock:
            # Atomically check and set the state.
            if self.state == TimeoutState.EXECUTING:
                self._set_state(TimeoutState.TIMED_OUT)
                should_raise = True

        if should_raise:
            thread_id = self._target_thread_id
            if thread_id is not None:
                self._raise_timeout_error(thread_id)

    def _setup_interrupt_timer(self):
        """Setting up the resource that interrupts the block"""
        self._timer = threading.Timer(self.timeout_interval, self._stop)
        self._timer.start()

    def _suppress_interrupt_timer(self):
        """Removing the resource that interrupts the block"""
        self._timer.cancel()

    def __bool__(self) -> bool:
        """Boolean evaluation of the context manager state"""
        return self.state in (
            TimeoutState.EXECUTED,
            TimeoutState.EXECUTING,
            TimeoutState.CANCELED,
        )

    def __enter__(self):
        # Set the initial state for this run.
        self._set_state(TimeoutState.EXECUTING)
        self._setup_interrupt_timer()
        return self

    def __exit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> bool:
        # Immediately request timer cancellation.
        self._suppress_interrupt_timer()

        # Check the thread-local storage to see if our _stop method was the source.
        is_our_timeout = hasattr(_thread_local, 'source') and _thread_local.source is self

        # Clear the thread-local token after reading it.
        if hasattr(_thread_local, 'source'):
            del _thread_local.source

        with self._lock:
            if is_our_timeout:
                self._set_state(TimeoutState.TIMED_OUT)
            elif exc_type is None:
                if self.state != TimeoutState.CANCELED:
                    self._set_state(TimeoutState.EXECUTED)
            elif issubclass(exc_type, TimeoutError):
                self._set_state(TimeoutState.INTERRUPTED)
            else:
                self._set_state(TimeoutState.FAILED)

        # Never swallow the exception. Always return False.
        return False

    def cancel(self):
        """In case inside the block you realize you don't need the time limit"""
        with self._lock:
            # Set the state to CANCELED within the lock.
            self._set_state(TimeoutState.CANCELED)
        self._suppress_interrupt_timer()

    def _raise_timeout_error(self, thread_id: ThreadId):
        """Raise a Timeout exception in a different thread."""
        if not isinstance(thread_id, ThreadId):
            raise SimpleBenchTypeError(f"thread_id must be a ThreadId, not {type(thread_id)}",
                                       tag=TimeoutErrorTag.INVALID_THREAD_ID_TYPE)

        # Set the thread-local token to our instance identity BEFORE raising.
        _thread_local.source = self

        c_thread_id = ctypes.c_ulong(thread_id)
        # Pass the exception TYPE, not an instance.
        states_modified: int = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            c_thread_id, ctypes.py_object(TimeoutError)
        )
        if states_modified == 0:
            error_message = f"Invalid thread ID {thread_id}"
            raise SimpleBenchValueError(
                error_message, tag=TimeoutErrorTag.INVALID_THREAD_ID_VALUE)
        elif states_modified > 1:
            # This part is tricky. If we modified more than one state, we should
            # probably try to clear the exception from the thread.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(c_thread_id, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
