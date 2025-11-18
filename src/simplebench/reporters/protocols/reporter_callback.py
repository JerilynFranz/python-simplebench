""""Protocols for reporters stuff."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

# Disconnects any possible circular imports
if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.enums import Format, Section


@runtime_checkable
class ReporterCallback(Protocol):
    """A protocol for callback functions used by Case and Reporters.

    Defines a method signature for a reporter callback function.

    The method's signature must match the following:

    .. code-block:: python

        def method_name(self, *, case: Case, section: Section, output_format: Format, output: Any) -> None:
    """
    def __call__(self, *, case: Case, section: Section, output_format: Format, output: Any) -> None:
        """A callback function to handle benchmark results from a Reporter.

        This function is called with the results of a benchmark run, and is responsible for
        processing the output in some way, such as logging it, storing it, or displaying it.

        The ``output`` parameter can be of any type, depending on the context in which the
        callback is used. The ``output_format`` parameter indicates the format of the
        output, which can be used to determine how to process or display the output or
        infer its type in a general way.

        One way to implement this is to examine the ``output_format`` and type of the
        ``output`` instance to handle it appropriately:

        .. code-block:: python

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

        :param case: The :class:`~simplebench.case.Case` instance.
        :param section: The section of the report (e.g.,
            :attr:`~simplebench.enums.Section.OPS`,
            :attr:`~simplebench.enums.Section.TIMING`, etc).
        :param output_format: The format of the output (e.g.,
            :attr:`~simplebench.enums.Format.TEXT`,
            :attr:`~simplebench.enums.Format.RICH_TEXT`, etc).
        :param output: The content to be handled by the callback. This can be of any type,
            depending on the context in which the callback is used.
        """
