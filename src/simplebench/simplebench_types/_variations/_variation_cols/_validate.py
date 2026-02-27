"""Validators for variation cols data structures."""
from collections.abc import Mapping
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError

from ._error_tags import _VariationColsErrorTag


def data(value: Any) -> dict[str, str]:
    """Validate that the input value is a mapping of strings to strings
    where all keys are valid identifiers and value are non-blank strings,
    and return it as a dict.

    :param Any value: The value to validate.
    :returns dict[str, str]: The validated mapping of strings to strings.
    :raises SimpleBenchTypeError: If the input value is not a mapping of strings to strings.
    :raises SimpleBenchValueError: If any keys in the mapping are not valid identifiers.
    """
    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            'VariationCols value must be a Mapping',
            tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE)
    if not all(isinstance(k, str) for k in value.keys()):
        raise SimpleBenchTypeError(
            'VariationCols keys must be strings.',
            tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE)
    if not all(k.isidentifier() for k in value.keys()):
        raise SimpleBenchTypeError(
            'VariationCols keys must be valid identifiers.',
            tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_VALUE)
    if not all(isinstance(v, str) for v in value.values()):
        raise SimpleBenchTypeError(
            'VariationCols values must be strings.',
            tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE)
    if not all(v.strip() for v in value.values()):
        raise SimpleBenchTypeError(
            'VariationCols values must be non-blank strings.',
            tag=_VariationColsErrorTag.VARIATION_COLS_INVALID_ARG_VALUE_TYPE)
    return dict(value)
