"""Error tags for variation marks validation."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VariationMarksErrorTag(ErrorTag):
    """Error tags for variation marks validation errors."""

    VARIATION_MARKS_INVALID_ARG_TYPE = "VARIATION_MARKS_INVALID_ARG_TYPE"
    """The variation_marks argument is not a mapping of strings to :class:`Mark`."""
    VARIATION_MARKS_INVALID_ARG_KEY_TYPE = "VARIATION_MARKS_INVALID_ARG_KEY_TYPE"
    """One or more keys in the variation_marks argument are not strings."""
    VARIATION_MARKS_INVALID_ARG_KEY_VALUE = "VARIATION_MARKS_INVALID_ARG_KEY_VALUE"
    """One or more keys in the variation_marks argument are not valid identifiers."""
    VARIATION_MARKS_INVALID_ARG_VALUE_TYPE = "VARIATION_MARKS_INVALID_ARG_VALUE_TYPE"
    """One or more values in the variation_marks argument are not of type :class:`Mark`."""
    VARIATION_MARKS_IMMUTABLE = "VARIATION_MARKS_IMMUTABLE"
    """Attempted to modify an immutable VariationMarks instance."""
    VARIATION_MARKS_KEY_ERROR = "VARIATION_MARKS_KEY_ERROR"
    """The specified key was not found in the VariationMarks instance."""
