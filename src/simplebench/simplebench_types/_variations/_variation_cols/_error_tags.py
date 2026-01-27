"""Error tags for variation cols validation."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VariationColsErrorTag(ErrorTag):
    """Error tags for variation cols validation errors."""

    VARIATION_COLS_INVALID_ARG_TYPE = "VARIATION_COLS_INVALID_ARG_TYPE"
    """The variation_cols argument is not a mapping of strings to :class:`str`."""
    VARIATION_COLS_INVALID_ARG_KEY_TYPE = "VARIATION_COLS_INVALID_ARG_KEY_TYPE"
    """One or more keys in the variation_cols argument are not strings."""
    VARIATION_COLS_INVALID_ARG_KEY_VALUE = "VARIATION_COLS_INVALID_ARG_KEY_VALUE"
    """One or more keys in the variation_cols argument are not valid identifiers."""
    VARIATION_COLS_INVALID_ARG_VALUE_TYPE = "VARIATION_COLS_INVALID_ARG_VALUE_TYPE"
    """One or more values in the variation_cols argument are not of type :class:`str`."""
    VARIATION_COLS_IMMUTABLE = "VARIATION_COLS_IMMUTABLE"
    """Attempted to modify an immutable VariationCols instance."""
    VARIATION_COLS_KEY_ERROR = "VARIATION_COLS_KEY_ERROR"
    """The specified key was not found in the VariationCols instance."""
