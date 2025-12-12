"""Execution environment exception ErrorTags"""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ExecutionEnvironmentErrorTag(ErrorTag):
    """Error tags for execution environment exceptions."""
    INVALID_DATA_ARG_TYPE = "Invalid data argument type"
    """The data argument provided to the execution environment is of an invalid type."""
    INVALID_DATA_ARG_EXTRA_KEYS = "Invalid data argument extra keys"
    """The data argument provided to the execution environment contains extra keys that are not allowed."""
    INVALID_DATA_ARG_VALUE_TYPE = "Invalid data argument value type"
    """A value in the data argument provided to the execution environment is of an invalid type."""
    INVALID_PYTHON_PROPERTY_TYPE = "Invalid Python property type"
    """The Python property provided to the execution environment is of an invalid type."""