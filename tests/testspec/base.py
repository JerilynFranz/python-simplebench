"""Base TestSpec class"""
from abc import abstractmethod, ABC


class TestSpec(ABC):
    """Base class for test specifications."""
    # Prevent pytest from trying to collect this class as a test case
    __test__ = False

    @abstractmethod
    def run(self) -> None:
        """Run the test based on the provided TestSpec entry.

        This function is intended to be overridden by subclasses to implement
        specific test execution logic.
        """
        raise NotImplementedError("Subclasses must implement the run method.")
