"""Mapping containers for variation marks used in SimpleBench.

This is an immutable mapping of variation field names to their corresponding string marks
for a specific variation.
"""

from collections.abc import Iterator, Mapping

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import Mark

from ._error_tags import _VariationMarksErrorTag


class VariationMarks(Mapping[str, Mark], Immutable):
    """Mapping container for variation marks used in SimpleBench.

    Maps variation field names to their corresponding string marks for a specific variation.

    Example:

    .. code-block:: python
        variation_marks = VariationMarks({
            "input_size": Mark(label="Large", value=1000000),
            "algorithm": Mark(label="QuickSort", value="quicksort"),
        })

    """
    __slots__ = ("_marks",)

    def __init__(self, marks: Mapping[str, Mark ]) -> None:
        """Construct a VariationMarks instance.

        :param Mapping[str, Mark] marks: The mapping of variation field names to their Marks.
        :raises SimpleBenchTypeError: If the marks argument is not a mapping of strings to strings, or
            if any keys are not valid identifiers.
        """
        if not isinstance(marks, Mapping):
            raise SimpleBenchTypeError(
                f"Invalid marks: {marks}. Must be a mapping of strings to Marks.",
                tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE,
            )
        if not all(isinstance(key, str) for key in marks.keys()):
            raise SimpleBenchTypeError(
                "All keys in marks must be strings.",
                tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_TYPE,
            )
        if not all(key.isidentifier() for key in marks.keys()):
            raise SimpleBenchValueError(
                f"All keys in marks must be valid identifiers: {list(marks.keys())}",
                tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_VALUE,
            )
        if not all(isinstance(value, Mark) for value in marks.values()):
            raise SimpleBenchTypeError(
                "All values in marks must be of type Mark.",
                tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_VALUE_TYPE,
            )
        self._marks: dict[str, Mark] = dict(marks)

    def __getitem__(self, key: str) -> Mark:
        """Get the mark for the given variation field name.

        :param key: The variation field name.
        :type key: str
        :returns: The corresponding mark.
        :rtype: Mark
        :raises KeyError: If the key is not found.
        """
        try:
            return self._marks[key]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f"Variation field '{key}' not found in VariationMarks.",
                tag=_VariationMarksErrorTag.VARIATION_MARKS_KEY_ERROR) from exc

    def __contains__(self, key: object) -> bool:
        """Check if the VariationMarks contains the given key.

        :param key: The key to check.
        :type key: object
        :returns: True if the key is in the VariationMarks, False otherwise.
        :rtype: bool
        """
        return key in self._marks

    def __setitem__(self, key: str, value: Mark) -> None:
        """Raise an error since VariationMarks is immutable.

        :raises SimpleBenchTypeError: Always, since VariationMarks is immutable.
        """
        raise SimpleBenchTypeError(
            "VariationMarks is immutable and does not support item assignment.",
            tag=_VariationMarksErrorTag.VARIATION_MARKS_IMMUTABLE,
            )

    def __iter__(self) -> Iterator[str]:
        """Iterate over the variation field names.

        :returns Iterator[str]: An iterator over the variation field names.
        """
        return self._marks.__iter__()

    def __len__(self) -> int:
        """Get the number of variation fields.

        :returns int: The number of variation fields.
        """
        return len(self._marks)

    def __repr__(self) -> str:
        """Get the string representation of the VariationMarks.

        :returns str: The string representation.
        """
        return f"VariationMarks({dict(self._marks)!r})"

    def __hash__(self) -> int:
        """Get the hash of the VariationMarks.

        :returns int: The hash value.
        """
        keys = sorted(list(self._marks.keys()))
        items = ((key, self._marks[key]) for key in keys)
        return hash(frozenset(items))

    def __eq__(self, other: object) -> bool:
        """Check equality with another VariationMarks.

        :param object other: The other object to compare.
        :returns bool: True if equal, False otherwise.
        """
        if not isinstance(other, VariationMarks):
            return False
        return dict(self._marks) == dict(other._marks)
