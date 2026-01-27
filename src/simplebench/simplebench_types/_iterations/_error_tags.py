"""Error tags for Iterations validation."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _IterationsErrorTag(ErrorTag):
    """Error tags for iterations validation errors."""

    ITERATIONS_INVALID_ARG_TYPE = "ITERATIONS_INVALID_ARG_TYPE"
    """The iterations argument is not a mapping of Metrics to :class:`Values`."""
    ITERATIONS_INVALID_ARG_KEY_TYPE = "ITERATIONS_INVALID_ARG_KEY_TYPE"
    """One or more keys in the iterations argument are not Metrics."""
    ITERATIONS_INVALID_ARG_KEY_VALUE = "ITERATIONS_INVALID_ARG_KEY_VALUE"
    """One or more keys in the iterations argument are not valid Metrics."""
    ITERATIONS_INVALID_ARG_VALUE_TYPE = "ITERATIONS_INVALID_ARG_VALUE_TYPE"
    """One or more values in the iterations argument are not a :class:`Values`."""
    ITERATIONS_IMMUTABLE = "ITERATIONS_IMMUTABLE"
    """Attempted to modify an immutable Iterations instance."""
    ITERATIONS_KEY_ERROR = "ITERATIONS_KEY_ERROR"
    """The specified key was not found in the Iterations instance."""
