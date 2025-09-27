"""Protocols for SimpleBench."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Protocol

from .enums import Format, Section
from .results import Results
from .runners import SimpleRunner

if TYPE_CHECKING:
    from .case import Case


class ActionRunner(Protocol):
    """A protocol for benchmark action functions used by Case.

    The action function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter.
    The 'bench' parameter is an instance of SimpleRunner, and '**kwargs' allows for additional
    keyword arguments to be passed to the function being benchmarked.

    Example action function signature:

        def my_action(bench: SimpleRunner, **kwargs) -> Results:
            # Benchmark logic here
            def some_function_to_benchmark():
                pass
            return bench.run(action=some_function_to_benchmark, **kwargs)
    """
    def __call__(self, bench: SimpleRunner, **kwargs) -> Results:  # type: ignore[reportReturnType]
        """Run the benchmark action.

        Args:
            bench: The SimpleRunner instance.
            **kwargs: Additional keyword arguments for the action.

        Returns:
            Results: The results of the benchmark action.
        """


class ReporterCallback(Protocol):
    """A protocol for callback functions used by Case and Reporters."""
    def __call__(self, case: Case, section: Section, output_format: Format, output: Any) -> None:
        """A callback function to handle benchmark results from a Reporter.

        Args:
            case (Case): The Case instance.
            section (Section): The section of the report (e.g., Section.OPS, Section.TIMING, etc).
            output_format (Format): The format of the output (e.g., Format.TEXT, Format.RICH_TEXT, etc).
            output (Any): The content to be handled by the callback.
        """
