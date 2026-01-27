"""Variation marks for SimpleBench cases.

The marks defined here are used to indicate variations in benchmark cases that may affect
the performance measurements. These marks help in categorizing and analyzing benchmark results

The marks are 'shallow immutable' (only the top-level attributes are immutable
because values can be of any type) and hashable, and provide a clear
representation of the variations they signify.

They can be used in conjunction with benchmark cases to annotate specific variations that
may impact the results, allowing for more nuanced analysis and comparison of benchmark outcomes.

They are designed to be easily integrated into the SimpleBench framework, providing a standardized
way to represent and handle variations in benchmark cases in cases where the raw kwarg_variation
values are not suitable.

Because it defines a sorting behavior based on labels, it allows for consistent ordering
of marks when generating reports or analyzing results. It sorts marks with string labels
lexicographically and numeric labels in natural numeric order. When comparing marks with
different label types (string vs numeric), string labels are considered less than numeric labels
for sorting purposes (i.e., all string-labeled marks come before numeric-labeled marks).

It also provides equality comparison based on both label and value, ensuring
that marks can be accurately compared and managed within the SimpleBench framework.
"""

from typing import Any

from simplebench.exceptions import SimpleBenchValueError
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

    By using marks, users can annotate benchmark cases with specific variations
    even when the raw kwarg_variation values are not appropriate for direct use
    in reporting or analysis.

    :param label: The label of the mark.
    :type label: str | int | float
    :param value: The value associated with the mark.
    :type value: Any
    """

    __slots__ = ('_label', '_value', '_hash_cache', '_repr_cache')

    def __init__(self, label: str, value: Any) -> None:
        """Initialize a Mark instance.

        The label must be a number (int or float) or a non-empty, non-blank string.

        :param label: The label of the mark.
        :type label: str | int | float
        :param value: The value associated with the mark.
        :type value: Any
        :raises SimpleBenchTypeError: If `label` is not a non-empty string.
        """
        self._label: str | int | float
        if isinstance(label, (int, float)):
            if label != label:  # Check for NaN
                raise SimpleBenchValueError(
                    "Label cannot be a NaN.",
                    tag=_MarkErrorTag.LABEL_ARG_NAN)
            self._label = label
            return

        self._label = validate_string(
            label,
            'label',
            _MarkErrorTag.LABEL_ARG_TYPE,
            _MarkErrorTag.LABEL_ARG_EMPTY,
            allow_empty=False,
            strip=True,
            allow_blank=False,
        )
        self._value: Any = value  # No validation for value; can be any type
        self._hash_cache: int | None = None
        self._repr_cache: str | None = None

    @property
    def label(self) -> str | int | float:
        """Return the label of the mark.

        This is a non-empty string that identifies the mark in a human-readable way
        for reporting and analysis purposes.
        """
        return self._label

    @property
    def value(self) -> Any:
        """Return the value of the mark.

        This is the raw value associated with the mark, which can be of any type
        and is not restricted to strings.
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """Check equality between this Mark and another object.

        Two Mark instances are considered equal if both their labels
        and values are equal.

        If the labels are numeric types (int or float), a numeric comparison is performed.

        If the labels are strings, a straightforward string comparison is performed.

        If the labels are of different types (one string and one numeric), the marks are not equal.

        :param other: The object to compare with.
        :type other: object
        :return: True if both marks are equal, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Mark):
            return NotImplemented

        # Both labels are numeric types
        if isinstance(self.label, (float,  int)) and isinstance(other.label, (float, int)):
            return (self._label == other._label) and (self._value == other._value)

        # Both labels are strings
        if isinstance(self.label, str) and isinstance(other.label, str):
            return (self._label == other._label) and (self._value == other._value)

        # One label is string, the other is numeric
        return False

    def __lt__(self, other: object) -> bool:
        """Check if this Mark is less than another Mark based on label comparison.

        - If both labels are strings, lexicographical comparison is used.
        - If both labels are numeric types (int or float), numeric comparison is used.
        - If the labels are of different types (one string and one numeric),
          the string is always considered less than the numeric.

        :param other: The object to compare with.
        :type other: object
        :return: True if this Mark's label is less than the other's label, False otherwise.
        :rtype: bool
        :raises TypeError: If other is not a Mark or if labels are of incompatible types.
        """
        if not isinstance(other, Mark):
            return NotImplemented
        # two strings
        if isinstance(self.label, str) and isinstance(other.label, str):
            return self.label < other.label
        # two numbers
        if isinstance(self.label, (int, float)) and isinstance(other.label, (int, float)):
            return self.label < other.label
        # number and a string
        if isinstance(self.label, (int, float)) and isinstance(other.label, str):
            return False
        # string and a number
        return True

    def __hash__(self) -> int:
        """Return the hash of the Mark instance.

        The hash is computed based on both the label and value of the mark,
        ensuring that marks with the same label and value produce the same hash.

        If the value is unhashable, the hash is computed using the id of the value.
        """
        if self._hash_cache is None:
            try:
                self._hash_cache = hash((self._label, self._value))
            except Exception:
                self._hash_cache = hash((self._label, id(self._value)))
        return self._hash_cache

    def __repr__(self) -> str:
        """Return a string representation of the Mark instance.

        Not guaranteed to work for eval() or for all possible values.

        If the value's representation raises an exception, it will be shown as <unrepresentable>.
        """
        if self._repr_cache is None:
            try:
                self._repr_cache = f"Mark(label={self._label!r}, value={self._value!r})"
            except Exception:
                self._repr_cache = f"Mark(label={self._label!r}, value=<unrepresentable>)"
        return self._repr_cache
