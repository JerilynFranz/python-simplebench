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
    def __call__(self, *, case: Case, section: Section, output_format: Format, output: Any) -> None:
        """A callback function to handle benchmark results from a Reporter.

        This function is called with the results of a benchmark run, and is responsible for
        processing the output in some way, such as logging it, storing it, or displaying it.

        The output parameter can be of any type, depending on the context in which the callback is used.
        The output_format parameter indicates the format of the output, which can be used to
        determine how to process or display the output or infer its type in a general way.

        One way to implement this is to examine the output_format and type of the output instance to
        handle it appropriately:

            def my_callback(*,
                            case: Case,
                            section: Section,
                            output_format: Format,
                            output: Any) -> None:
                # Handle the output based on its type and format
                match output_format:
                    case Format.TEXT:
                        print(f"String output: {output}")
                    case Format.RICH_TEXT:
                        if isinstance(output, dict):
                            print(f"Dictionary output: {output}")
                        elif isinstance(output, bytes):
                            print(f"Bytes output: {output}")
                    case Format.GRAPH:
                        if isinstance(output, bytes):
                            print(f"Binary output: {output}")
                        elif isinstance(output, dict):
                            print(f"Graph data: {output}")
                        elif isinstance(output, str):
                            print(f"Graph path: {output}")
                    case _:
                        print(f"Unknown output type: {type(output)}")

        Args:
            case (Case): The Case instance.
            section (Section): The section of the report (e.g., Section.OPS, Section.TIMING, etc).
            output_format (Format): The format of the output (e.g., Format.TEXT, Format.RICH_TEXT, etc).
            output (Any): The content to be handled by the callback. This can be of any type,
                          depending on the context in which the callback is used.
        """
