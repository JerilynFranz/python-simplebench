"""Mapping containers for variation cols used in SimpleBench.

This is an immutable mapping of variation field names to their corresponding string cols
for a specific variation.
"""

from collections.abc import Iterator, Mapping

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError

from ._error_tags import _VariationColsErrorTag


class VariationCols(Mapping[str, str], Immutable):
    """Mapping container for variation cols used in SimpleBench.

    Maps variation field names to their corresponding string cols for a specific variation.

    Example:

    .. code-block:: python
        variation_cols = VariationCols({
            "input_size": "Input Size",
            "algorithm": "Algorithm",
        })

    """
    __slots__ = ("_cols",)

    def __init__(self, cols: Mapping[str, str] | None = None) -> None:
        """Construct a VariationCols instance.

        If cols is None, creates an empty VariationCols.

        :param cols: The mapping of variation field names to their Cols.
        :type cols: Mapping[str, str] | None
        :raises SimpleBenchTypeError: If the cols argument is not a mapping of strings to strings, or
            if any keys are not valid identifiers.
        """
        self._cols: dict[str, str] = {}
        if cols is None:
            return
        if not isinstance(cols, Mapping):
            raise SimpleBenchTypeError(
                f"Invalid cols: {cols}. Must be a mapping of strings to Cols.",
                tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE,
            )
        if not all(isinstance(key, str) for key in cols.keys()):
            raise SimpleBenchTypeError(
                "All keys in cols must be strings.",
                tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_TYPE,
            )
        if not all(key.isidentifier() for key in cols.keys()):
            raise SimpleBenchValueError(
                f"All keys in cols must be valid identifiers: {list(cols.keys())}",
                tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_VALUE,
            )
        if not all(isinstance(value, str) for value in cols.values()):
            raise SimpleBenchTypeError(
                "All values in cols must be of type str.",
                tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_VALUE_TYPE,
            )
        self._cols = dict(cols)

    def __getitem__(self, key: str) -> str:
        """Get the col for the given variation field name.

        :param key: The variation field name.
        :type key: str
        :returns: The corresponding col.
        :rtype: str
        :raises KeyError: If the key is not found.
        """
        try:
            return self._cols[key]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f"Variation field '{key}' not found in VariationCols.",
                tag=_VariationColsErrorTag.VARIATION_COLS_KEY_ERROR) from exc

    def __contains__(self, key: object) -> bool:
        """Check if the VariationCols contains the given key.

        :param key: The key to check.
        :type key: object
        :returns: True if the key is in the VariationCols, False otherwise.
        :rtype: bool
        """
        return key in self._cols

    def __setitem__(self, key: str, value: str) -> None:
        """Raise an error since VariationCols is immutable.

        :raises SimpleBenchTypeError: Always, since VariationCols is immutable.
        """
        raise SimpleBenchTypeError(
            "VariationCols is immutable and does not support item assignment.",
            tag=_VariationColsErrorTag.VARIATION_COLS_IMMUTABLE,
            )

    def __iter__(self) -> Iterator[str]:
        """Iterate over the variation field names.

        :returns Iterator[str]: An iterator over the variation field names.
        """
        return self._cols.__iter__()

    def __len__(self) -> int:
        """Get the number of variation fields.

        :returns int: The number of variation fields.
        """
        return len(self._cols)

    def __repr__(self) -> str:
        """Get the string representation of the VariationCols.

        :returns str: The string representation.
        """
        return f"VariationCols({dict(self._cols)!r})"

    def __hash__(self) -> int:
        """Get the hash of the VariationCols.

        :returns int: The hash value.
        """
        keys = sorted(list(self._cols.keys()))
        items = ((key, self._cols[key]) for key in keys)
        return hash(frozenset(items))

    def __eq__(self, other: object) -> bool:
        """Check equality with another VariationCols.

        :param object other: The other object to compare.
        :returns bool: True if equal, False otherwise.
        """
        if not isinstance(other, VariationCols):
            return False
        return dict(self._cols) == dict(other._cols)
