"""Variation marks for SimpleBench cases.


The marks defined here are used to indicate variations in benchmark cases that may affect
the performance measurements. These marks help in categorizing and analyzing benchmark results

The marks are immutable and hashable, and provide a clear representation of the variations they signify.

They can be used in conjunction with benchmark cases to annotate specific variations that
may impact the results, allowing for more nuanced analysis and comparison of benchmark outcomes.

They are designed to be easily integrated into the SimpleBench framework, providing a standardized
way to represent and handle variations in benchmark cases in cases where the raw kwarg_variation
values are not suitable.
"""

from typing import Any

from simplebench.validators import validate_string

from ._error_tags import _MarkErrorTag


class Mark:
    """Base class for variation marks in SimpleBench cases.

    Marks are used to indicate variations in benchmark cases that may affect
    the performance measurements.

    Because kwarg_variations values may not always be suitable for marking variations
    (for example, if they contain sensitive information, or cannot be easily
    represented as strings), the Mark class provides a way to create standardized
    marks that can be used to represent these variations in results and reports.

    :ivar name: The name of the mark.
    :vartype name: str
    :ivar value: The value associated with the mark.
    :vartype value: Any
    """
    __slots__ = ('_name', '_value')

    def __init__(self, name: str, value: Any) -> None:
        """Initialize a Mark instance.

        :param name: The name of the mark.
        :param value: The value associated with the mark.
        :raises SimpleBenchTypeError: If `name` is not a non-empty string.
        """
        self._name: str = validate_string(
            name, 'name',
            _MarkErrorTag.NAME_ARG_TYPE,
            _MarkErrorTag.NAME_ARG_EMPTY,
            allow_empty=False, strip=True, allow_blank=False)
        self._value: Any = value

    @property
    def name(self) -> str:
        """Return the name of the mark."""
        return self._name

    @property
    def value(self) -> Any:
        """Return the value of the mark."""
        return self._value

    def __repr__(self) -> str:
        """Return a string representation of the Mark instance."""
        return f"Mark(name='{self._name}, value={repr(self._value)})"
