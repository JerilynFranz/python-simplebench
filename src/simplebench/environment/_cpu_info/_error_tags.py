"""Error tags for CPU information retrieval issues."""

# ruff: noqa: F401
from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _CPUInfoErrorTag(ErrorTag):
    """Error tags for CPU information retrieval issues."""

    INVALID_CPUINFO_DATA = auto()
    """The CPU information data is invalid or malformed."""
    INVALID_CACHE_KEY_PARAM_TYPE = auto()
    """The 'cache_key' argument is not of type 'str'."""
    INVALID_CACHE_KEY_PARAM_VALUE = auto()
    """The 'cache_key' argument is a blank or empty string."""
    INVALID_NAME_PARAM_TYPE = auto()
    """The 'name' argument is not of type 'str'."""
    INVALID_NAME_PARAM_VALUE = auto()
    """The 'name' argument is a blank or empty string."""
    INVALID_USE_CACHE_TYPE = auto()
    """The `use_cache` parameter is not a boolean value."""
    INVALID_DETACHED_TYPE = auto()
    """The `detached` parameter is not a boolean value."""
    INVALID_USE_CACHE_AND_DETACHED_COMBINATION = auto()
    """The `use_cache` and `detached` parameters cannot both be `False`."""
    INVALID_DATA_PARAM_TYPE = auto()
    """The 'data' argument is not of type 'dict'."""
    INVALID_DATA_PARAM_NESTING_DEPTH = auto()
    """The 'data' argument is nested too deeply."""
    INVALID_DATA_PARAM_CYCLIC_REFERENCE = auto()
    """The 'data' argument contains cyclic references."""
    INVALID_DATA_PARAM_NON_FINITE_FLOAT = auto()
    """The 'data' argument contains non-finite float values (NaN, Infinity)."""
    INVALID_DATA_PARAM_KEYS_TYPE = auto()
    """One or more keys in the 'data' argument are not of type 'str'"""
    INVALID_DATA_PARAM_KEYS_VALUE = auto()
    """One or more keys in the 'data' argument are blank strings."""
