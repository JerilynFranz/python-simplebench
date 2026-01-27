"""Error tags for kwargs variations validation."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _KWArgsVariationsErrorTag(ErrorTag):
    """Error tags for kwargs variations validation errors."""

    KWARGS_VARIATIONS_INVALID_ARG_TYPE = "KWARGS_VARIATIONS_INVALID_ARG_TYPE"
    """The kwargs_variations argument is not a mapping of strings to :class:`Sequence` of :class:`Mark`."""
    KWARGS_VARIATIONS_INVALID_ARG_KEY_TYPE = "KWARGS_VARIATIONS_INVALID_ARG_KEY_TYPE"
    """One or more keys in the kwargs_variations argument are not strings."""
    KWARGS_VARIATIONS_INVALID_ARG_KEY_VALUE = "KWARGS_VARIATIONS_INVALID_ARG_KEY_VALUE"
    """One or more keys in the kwargs_variations argument are not valid identifiers."""
    KWARGS_VARIATIONS_INVALID_ARG_VALUE_TYPE = "KWARGS_VARIATIONS_INVALID_ARG_VALUE_TYPE"
    """One or more values in the kwargs_variations argument are not a :class:`Sequence`."""
    KWARGS_VARIATIONS_INVALID_ARG_VALUE_ITEM_TYPE = "KWARGS_VARIATIONS_INVALID_ARG_VALUE_ITEM_TYPE"
    """One or more items in the sequences of the kwargs_variations argument are not of type :class:`Mark`."""
    KWARGS_VARIATIONS_IMMUTABLE = "KWARGS_VARIATIONS_IMMUTABLE"
    """Attempted to modify an immutable KWArgsVariations instance."""
    KWARGS_VARIATIONS_KEY_ERROR = "KWARGS_VARIATIONS_KEY_ERROR"
    """The specified key was not found in the KWArgsVariations instance."""
