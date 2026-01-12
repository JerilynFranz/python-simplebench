"""Error tags for CPU information retrieval issues."""

# ruff: noqa: F401
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__ = []


@enum_docstrings
class _CPUInfoErrorTag(ErrorTag):
    """Error tags for CPU information retrieval issues."""

    INVALID_CACHE_KEY_PARAM_TYPE = 'INVALID_CACHE_KEY_PARAM_TYPE'
    """The 'cache_key' argument is not of type 'str'."""
    INVALID_CACHE_KEY_PARAM_VALUE = 'INVALID_CACHE_KEY_PARAM_VALUE'
    """The 'cache_key' argument is a blank or empty string."""
    INVALID_NAME_PARAM_TYPE = 'INVALID_NAME_PARAM_TYPE'
    """The 'name' argument is not of type 'str'."""
    INVALID_NAME_PARAM_VALUE = 'INVALID_NAME_PARAM_VALUE'
    """The 'name' argument is a blank or empty string."""
    INVALID_USE_CACHE_TYPE = 'INVALID_USE_CACHE_TYPE'
    """The `use_cache` parameter is not a boolean value."""
    INVALID_DETACHED_TYPE = 'INVALID_DETACHED_TYPE'
    """The `detached` parameter is not a boolean value."""
    INVALID_USE_CACHE_AND_DETACHED_COMBINATION = 'INVALID_USE_CACHE_AND_DETACHED_COMBINATION'
    """The `use_cache` and `detached` parameters cannot both be `False`."""
    INVALID_DATA_PARAM_TYPE = 'INVALID_DATA_PARAM_TYPE'
    """The 'data' argument is not of type 'dict'."""
    INVALID_DATA_PARAM_NESTING_DEPTH = 'INVALID_DATA_PARAM_NESTING_DEPTH'
    """The 'data' argument is nested too deeply."""
    INVALID_DATA_PARAM_CYCLIC_REFERENCE = 'INVALID_DATA_PARAM_CYCLIC_REFERENCE'
    """The 'data' argument contains cyclic references."""
    INVALID_DATA_PARAM_NON_FINITE_FLOAT = 'INVALID_DATA_PARAM_NON_FINITE_FLOAT'
    """The 'data' argument contains non-finite float values (NaN, Infinity)."""
    INVALID_DATA_PARAM_KEYS_TYPE = 'INVALID_DATA_PARAM_KEYS_TYPE'
    """One or more keys in the 'data' argument are not of type 'str'"""
    INVALID_DATA_PARAM_KEYS_VALUE = 'INVALID_DATA_PARAM_KEYS_VALUE'
    """One or more keys in the 'data' argument are blank strings."""
