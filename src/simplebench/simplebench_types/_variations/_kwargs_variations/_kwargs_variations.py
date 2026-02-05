"""Mapping containers for collections of variation marks used in SimpleBench.

This is an immutable mapping of variation field names to their corresponding collections of Marks
defining multiple variations.
"""

from collections.abc import Iterator, Mapping

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import ElementCollection, Mark, is_element_collection

from ._error_tags import _KWArgsVariationsErrorTag


class KWArgsVariations(Mapping[str, ElementCollection[Mark]], Immutable):
    """Mapping container for ElementCollections of variation marks used in SimpleBench.

    Maps variation field names to their corresponding collections of Marks for a specific variation.

    Example:

    .. code-block:: python
        variation_kwarg_variations = KWArgsVariations({
            "input_size": [Mark(label="Large", value=1000000), Mark(label="Small", value=1000)],
            "algorithm": [Mark(label="QuickSort", value="quicksort"), Mark(label="MergeSort", value="mergesort")],
        })

    """
    __slots__ = ("_kwarg_variations",)

    def __init__(self, marks: Mapping[str, ElementCollection[Mark]] | None = None) -> None:
        """Construct a KWArgsVariations instance.

        :param marks: The mapping of variation field names to their Mark collections.
        :type marks: Mapping[str, ElementCollection[Mark]] | None
        :raises SimpleBenchTypeError: If the marks argument is not a mapping of strings
            to :class:`ElementCollection` of :class:`Mark`
        :raises SimpleBenchValueError: If any keys are not valid identifiers.
        """
        self._kwarg_variations: dict[str, tuple[Mark, ...]] = {}
        if marks is None:
            return

        if not isinstance(marks, Mapping):
            raise SimpleBenchTypeError(
                f"Invalid marks: {marks}. Must be a mapping of strings to ElementCollection of Mark.",
                tag=_KWArgsVariationsErrorTag.KWARGS_VARIATIONS_INVALID_ARG_TYPE,
            )
        if not all(isinstance(key, str) for key in marks.keys()):
            raise SimpleBenchTypeError(
                "All keys in marks must be strings.",
                tag=_KWArgsVariationsErrorTag.KWARGS_VARIATIONS_INVALID_ARG_KEY_TYPE,
            )
        if not all(key.isidentifier() for key in marks.keys()):
            raise SimpleBenchValueError(
                f"All keys in marks must be valid identifiers: {list(marks.keys())}",
                tag=_KWArgsVariationsErrorTag.KWARGS_VARIATIONS_INVALID_ARG_KEY_VALUE,
            )
        if not all(is_element_collection(value) for value in marks.values()):
            raise SimpleBenchTypeError(
                "All values in marks must be ElementCollection of Mark.",
                tag=_KWArgsVariationsErrorTag.KWARGS_VARIATIONS_INVALID_ARG_VALUE_TYPE,
            )
        for value in marks.values():
            if not all(isinstance(item, Mark) for item in value):
                raise SimpleBenchTypeError(
                    "All items in the ElementCollection of marks must be of type Mark.",
                    tag=_KWArgsVariationsErrorTag.KWARGS_VARIATIONS_INVALID_ARG_VALUE_ITEM_TYPE,
                )
        self._kwarg_variations = {k: tuple(sorted(v)) for k, v in marks.items()}

    def __getitem__(self, key: str) -> tuple[Mark, ...]:
        """Get the mark for the given variation field name.

        :param key: The variation field name.
        :type key: str
        :returns: The corresponding tuple of Marks.
        :rtype: tuple[Mark, ...]
        :raises KeyError: If the key is not found.
        """
        try:
            return self._kwarg_variations[key]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f"Variation field '{key}' not found in KWArgsVariations.",
                tag=_KWArgsVariationsErrorTag.KWARGS_VARIATIONS_KEY_ERROR) from exc

    def __contains__(self, key: object) -> bool:
        """Check if the KWArgsVariations contains the given key.

        :param key: The key to check.
        :type key: object
        :returns: True if the key is in the KWArgsVariations, False otherwise.
        :rtype: bool
        """
        return key in self._kwarg_variations

    def __setitem__(self, key: str, value: tuple[Mark, ...]) -> None:
        """Raise an error since KWArgsVariations is immutable.

        :raises SimpleBenchTypeError: Always, since KWArgsVariations is immutable.
        """
        raise SimpleBenchTypeError(
            "KWArgsVariations is immutable and does not support item assignment.",
            tag=_KWArgsVariationsErrorTag.KWARGS_VARIATIONS_IMMUTABLE,
            )

    def __iter__(self) -> Iterator[str]:
        """Iterate over the variation field names.

        :returns Iterator[str]: An iterator over the variation field names.
        """
        return self._kwarg_variations.__iter__()

    def __len__(self) -> int:
        """Get the number of variation fields.

        :returns int: The number of variation fields.
        """
        return len(self._kwarg_variations)

    def __repr__(self) -> str:
        """Get the string representation of the KWArgsVariations.

        :returns str: The string representation.
        """
        return f"KWArgsVariations({dict(self._kwarg_variations)!r})"

    def __hash__(self) -> int:
        """Get the hash of the KWArgsVariations.

        :returns int: The hash value.
        """
        keys = sorted(list(self._kwarg_variations.keys()))
        items = ((key, self._kwarg_variations[key]) for key in keys)
        return hash(frozenset(items))

    def __eq__(self, other: object) -> bool:
        """Check equality with another KWArgsVariations.

        :param object other: The other object to compare.
        :returns bool: True if equal, False otherwise.
        """
        if not isinstance(other, KWArgsVariations):
            return False
        return dict(self._kwarg_variations) == dict(other._kwarg_variations)
