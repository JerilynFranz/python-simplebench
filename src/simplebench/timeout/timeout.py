"""
Raise asynchronous exceptions in other thread, control the timeout of blocks
or callables with a context manager

:param timeout_interval: ``float`` or ``int`` duration enabled to run the context manager block
:param swallow_exception: Whether to swallow the SimpleBenchTimeoutError exception or not.
    - ``False`` if you want to manage the ``SimpleBenchTimeoutError`` (or any other) in an
      outer ``try ... except`` structure.
    - ``True`` (default) if you just want to check the execution of
      the block with the ``state`` attribute of the context manager.

"""
import ctypes
import threading
from contextlib import AbstractContextManager
from types import TracebackType

from ..exceptions import SimpleBenchRuntimeError, SimpleBenchTimeoutError, SimpleBenchTypeError, SimpleBenchValueError
from .enums import TimeoutState
from .exceptions import TimeoutErrorTag
from .thread_id import ThreadId

# Create a thread-local storage object at the module level.
_thread_local = threading.local()
"""Thread-local storage for timeout context managers."""


class _NotSet:
    """Sentinel class for unset attributes."""


class Timeout(AbstractContextManager):
    """Context manager for limiting in the time the execution of a block
    using asynchronous threads launching exception.
    """

    def __init__(self, *, timeout_interval: float, swallow_exception: bool = True):
        """Initialize the Timeout context manager.

        :param timeout_interval: ``float`` or ``int`` duration enabled to run the context manager block
        :param swallow_exception: Whether to swallow the ``SimpleBenchTimeoutError`` exception or not.
        - ``False`` if you want to manage any exceptions in an outer ``try ... except`` structure.
        - ``True`` (default) if you just want to check the execution of
            the block with the ``state`` attribute of the context manager.
        """
        self._target_thread_id = threading.current_thread().ident
        self._set_timeout_interval(timeout_interval)
        self._set_swallow_exception(swallow_exception)
        self._set_state(TimeoutState.EXECUTED)
        self._is_timeout_source = False
        # 1. Add a lock to protect shared state.
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
            raise SimpleBenchTimeoutError(
                "timeout_interval must be a float or int",
                tag=TimeoutErrorTag.INVALID_TIMEOUT_INTERVAL_TYPE)
        if value <= 0:
            raise SimpleBenchValueError(
                "timeout_interval must be greater than zero",
                tag=TimeoutErrorTag.INVALID_TIMEOUT_INTERVAL_VALUE)
        setattr(self, "_private_timeout_interval", float(value))

    @property
    def swallow_exception(self) -> bool:
        """Get whether to swallow the Timeout exception."""
        swallow: bool | _NotSet = getattr(self, "_private_swallow_exception", _NotSet())
        if isinstance(swallow, bool):
            return swallow
        raise SimpleBenchRuntimeError(
            "swallow_exception has not been set",
            tag=TimeoutErrorTag.SWALLOW_EXCEPTION_NOT_SET)

    def _set_swallow_exception(self, value: bool):
        """Set whether to swallow the Timeout exception."""
        if not isinstance(value, bool):
            raise SimpleBenchTypeError(
                "swallow_exception must be a boolean",
                tag=TimeoutErrorTag.INVALID_SWALLOW_EXCEPTION_TYPE)
        setattr(self, "_private_swallow_exception", value)

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
        with self._lock:
            # If __exit__ or cancel() has already run, the state will not be EXECUTING.
            if self.state != TimeoutState.EXECUTING:
                return
            self._is_timeout_source = True

        # Now, raise the exception in the main thread. This call will block.
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
        # Reset the flag for this instance.
        self._is_timeout_source = False
        self._set_state(TimeoutState.EXECUTING)
        self._setup_interrupt_timer()
        return self

    def __exit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> bool:
        with self._lock:
            # By acquiring the lock, we prevent the _stop method from changing
            # _is_timeout_source while we are in this critical section.
            self._suppress_interrupt_timer()

            is_our_timeout = self._is_timeout_source

            if is_our_timeout:
                self._set_state(TimeoutState.TIMED_OUT)
                return exc_type is TimeoutError and self.swallow_exception

            # If we are here, our timer did not fire.
            if exc_type is None:
                if self.state != TimeoutState.CANCELED:
                    self._set_state(TimeoutState.EXECUTED)
            elif exc_type is TimeoutError:
                self._set_state(TimeoutState.INTERRUPTED)
            else:
                self._set_state(TimeoutState.FAILED)

            return False

    def cancel(self):
        """In case inside the block you realize you don't need the time limit"""
        self._set_state(TimeoutState.CANCELED)
        self._suppress_interrupt_timer()

    def _raise_timeout_error(self, thread_id: ThreadId):
        """Raise a Timeout exception in a different thread.
        Read https://docs.python.org/c-api/init.html#PyThreadState_SetAsyncExc
        for further enlightenments.

        :param thread_id: target thread identifier
        """
        if not isinstance(thread_id, ThreadId):
            raise SimpleBenchTypeError(f"thread_id must be a ThreadId, not {type(thread_id)}",
                                       tag=TimeoutErrorTag.INVALID_THREAD_ID_TYPE)

        c_thread_id = ctypes.c_ulong(thread_id)
        # gil_state = ctypes.pythonapi.PyGILState_Ensure()
        states_modified: int = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            c_thread_id, ctypes.py_object(TimeoutError)
        )
        # ctypes.pythonapi.PyGILState_Release(gil_state)
        if states_modified == 0:
            error_message = f"Invalid thread ID {thread_id}"
            raise SimpleBenchValueError(
                error_message, tag=TimeoutErrorTag.INVALID_THREAD_ID_VALUE)
        elif states_modified > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(c_thread_id, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
