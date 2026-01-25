"""Base TestSpec class"""
import inspect
from abc import ABC, abstractmethod
from types import TracebackType


class TestSpec(ABC):
    """Base class for test specifications."""
    # Prevent pytest from trying to collect this class as a test case
    __test__ = False

    _creation_traceback: TracebackType | None = None
    """The traceback at the point where the TestSpec was created."""

    @abstractmethod
    def run(self) -> None:
        """Run the test based on the provided TestSpec entry.

        This function is intended to be overridden by subclasses to implement
        specific test execution logic.
        """
        raise NotImplementedError("Subclasses must implement the run method.")

    def __post_init__(self) -> None:
        """Capture the traceback at the point of creation."""
        # Don't capture the traceback if this is a subclass, as it will be captured by the parent
        current_frame = inspect.currentframe()
        if current_frame is None:
            # This should not be able to happen in CPython, but it's better to be safe.
            raise RuntimeError("Could not get current frame.") from None

        try:
            while current_frame is not None:
                module = inspect.getmodule(current_frame)
                if module is None or module.__name__.startswith('testspec'):
                    current_frame = current_frame.f_back
                    continue

                # We've found the first frame outside the testspec package.
                self._creation_traceback = TracebackType(
                    None, current_frame, current_frame.f_lasti, current_frame.f_lineno
                )
                return
        finally:
            # As per the inspect module documentation, we need to delete the frame reference
            # when we are done with it to avoid reference cycles.
            del current_frame

        raise RuntimeError("Could not find creation traceback.") from None

    def _fail(self, message: str) -> None:
        """Raise a test failure, attaching the creation traceback if available."""
        __tracebackhide__ = True  # pylint: disable=unused-variable
        exc = AssertionError(message)
        if self._creation_traceback:
            raise exc.with_traceback(self._creation_traceback) from None
        # If we failed to get a traceback, raise the assertion as-is.
        raise exc
