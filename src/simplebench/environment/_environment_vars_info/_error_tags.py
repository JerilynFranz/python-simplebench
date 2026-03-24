"""Error tags for Environment Variables information retrieval issues."""

# ruff: noqa: F401
from enum import auto

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _EnvironmentVarsInfoErrorTag(ErrorTag):
    """Error tags for Environment Variables information retrieval issues."""
    INVALID_ENV_VARS_INFO_TYPE_STR_OR_BYTES = auto()
    """The provided environment variables information is of an invalid type.
    Expected a set, sequence, or iterable of strings, but got a string or bytes object."""
    INVALID_ENV_VARS_INFO_TYPE = auto()
    """The provided environment variables information is of an invalid type.
    Expected a mapping of strings to strings."""
    INVALID_ENV_VARS_INFO_KEY_TYPE = auto()
    """One or more keys in the environment variables information are of an invalid type.
    All keys must be strings."""
