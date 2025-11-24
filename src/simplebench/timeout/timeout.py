"""
Run a callable with a timeout, ensuring safe termination.
"""
import threading
from typing import Any, Callable, Generic, ParamSpec, TypeVar, cast

from ..exceptions import SimpleBenchTimeoutError, SimpleBenchTypeError, SimpleBenchValueError
from .enums import TimeoutState
from .exceptions import TimeoutErrorTag

# Define a TypeVar for the class instance. This is not used by run.
_T = TypeVar("_T")
# Define a ParamSpec for the arguments of the callable passed to run.
_P = ParamSpec("_P")
# Define a TypeVar specifically for the return type of the run method.
_RT = TypeVar("_RT")


class Timeout(Generic[_T]):
    """
    Executes a callable in a separate daemon thread and enforces a timeout.

    This implementation avoids the risks of raising asynchronous exceptions by
    running the target function in a worker thread and using `thread.join()`
    with a timeout. If the worker thread is still alive after the timeout,
    it is considered to have timed out. Because the worker is a daemon thread,
    the main program can exit without needing to forcefully terminate it.

    .. warning:: After a timeout, it is recommended to exit the program cleanly rather than continuing execution.

        The worker thread may still be running in the background and this can lead to
        undefined behavior. This design ensures that the main thread remains responsive
        and avoids the complexities of forcibly terminating threads.

    .. code-block:: python3
      :linenos:
      :caption: Example of using the new Timeout class.

        def my_long_running_task():
            time.sleep(10)
            return "done"

        timeout = Timeout(5.0)
        try:
            result = timeout.run(my_long_running_task)
            print(f"Task finished with result: {result}")
        except SimpleBenchTimeoutError as e:
            print(f"Task {e.func_name} timed out. Final state: {timeout.state}")
            sys.exit(1)
    """
    def __init__(self, timeout_interval: float | int):
        """Initialize the Timeout runner.

        :param timeout_interval: ``float`` or ``int`` duration to wait for the callable to complete.
        """
        self._set_timeout_interval(timeout_interval)
        self._worker_thread: threading.Thread | None = None
        # The internal result is Any because a single instance can run functions with different return types.
        self._result: Any = None
        self._exception: BaseException | None = None
        self._set_state(TimeoutState.PENDING)

    @property
    def timeout_interval(self) -> float:
        """Get the timeout interval in seconds."""
        return getattr(self, "_private_timeout_interval")

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
        """Get the final state of the timeout execution."""
        return getattr(self, "_private_state")

    def _set_state(self, value: TimeoutState):
        """Set the current state of the timeout context manager."""
        if not isinstance(value, TimeoutState):
            raise SimpleBenchTypeError(
                "state must be a TimeoutState",
                tag=TimeoutErrorTag.INVALID_STATE_TYPE)
        setattr(self, "_private_state", value)

    def _target_wrapper(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        """
        Internal wrapper to run in the worker thread.
        It captures the result or any exception that occurs.
        """
        try:
            self._result = func(*args, **kwargs)
        except BaseException as e:  # pylint: disable=broad-exception-caught
            self._exception = e

    def run(self, _calling_func: Callable[_P, _RT], *args: _P.args, **kwargs: _P.kwargs) -> _RT:
        """
        Runs the given callable in a worker thread with a timeout.

        :param _calling_func: The callable to execute.
        :param args: Positional arguments to pass to the callable.
        :param kwargs: Keyword arguments to pass to the callable.
        :raises SimpleBenchTimeoutError: If the callable does not complete within the specified timeout.
        :raises BaseException: Any exception raised by the callable will be re-raised in the main thread.
        :return: The return value of the callable if it completes successfully.
        """
        # Reset state for this run to ensure instance reusability.
        self._result = None
        self._exception = None

        func_name = getattr(_calling_func, "__qualname__",
                            getattr(_calling_func, "__name__", repr(_calling_func)))
        if not callable(_calling_func):
            raise SimpleBenchTypeError(
                f"The provided _calling_func '{func_name}' is not callable",
                tag=TimeoutErrorTag.NON_CALLABLE_FUNCTION_ARGUMENT)
        self._worker_thread = threading.Thread(
            target=self._target_wrapper,
            args=(_calling_func,) + args,
            kwargs=kwargs,
            name=f"TimeoutWorker-{func_name}",
            daemon=True  # Crucial: Allows the main thread to exit even if this thread is blocked.
        )

        self._set_state(TimeoutState.RUNNING)
        self._worker_thread.start()
        self._worker_thread.join(timeout=self.timeout_interval)

        if self._worker_thread.is_alive():
            # The thread is still running, so it has timed out.
            self._set_state(TimeoutState.TIMED_OUT)
            raise SimpleBenchTimeoutError(
                f"Execution of '{func_name}' timed out after {self.timeout_interval} seconds",
                tag=TimeoutErrorTag.TIMED_OUT,
                func_name=func_name
                )

        # If we get here, the thread has finished.
        if self._exception:
            # An exception occurred inside the thread.
            self._set_state(TimeoutState.FAILED)
            raise self._exception

        # The thread completed successfully.
        self._set_state(TimeoutState.FINISHED)
        # We cast here to assure the type checker that if the thread has finished
        # and no exception was raised, _result must have been assigned a value of type _RT.
        return cast(_RT, self._result)
