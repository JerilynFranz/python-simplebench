"""Execution environment exception ErrorTags"""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ExecutionEnvironmentErrorTag(ErrorTag):
    """Error tags for execution environment exceptions."""

    INVALID_ENVIRONMENT_NAME_TYPE = 'INVALID_ENVIRONMENT_NAME_TYPE'
    """An environment name provided to the execution environment is not a string."""
    INVALID_ENVIRONMENT_NAME_VALUE = 'INVALID_ENVIRONMENT_NAME_VALUE'
    """An environment name provided to the execution environment is not valid."""
    BAD_KNOWN_ENVIRONMENT_TYPE = 'BAD_KNOWN_ENVIRONMENT_TYPE'
    """A known environment provided to the execution environment was not of type
    :class:`~simplebench.report.base.Environment`."""
    NO_ENVIRONMENTS_PROVIDED = 'NO_ENVIRONMENTS_PROVIDED'
    """No execution environments were provided."""
    INVALID_ENVIRONMENTS_TYPE = 'INVALID_ENVIRONMENTS_TYPE'
    """The execution environments provided to the execution environment validator was not a Mapping"""
    INVALID_ENVIRONMENT_TYPE = 'INVALID_ENVIRONMENT_TYPE'
    """An environment provided to the execution environment is of an invalid type."""
    INVALID_VERSION_TYPE = 'INVALID_VERSION_TYPE'
    """The version provided to the execution environment is of an invalid type."""
    UNSUPPORTED_VERSION = 'UNSUPPORTED_VERSION'
    """The version provided to the execution environment is not supported."""
    INVALID_DATA_ARG_TYPE = 'INVALID_DATA_ARG_TYPE'
    """The data argument provided to the execution environment is of an invalid type."""
    INVALID_DATA_ARG_EXTRA_KEYS = 'INVALID_DATA_ARG_EXTRA_KEYS'
    """The data argument provided to the execution environment contains extra keys that are not allowed."""
    INVALID_DATA_ARG_VALUE_TYPE = 'INVALID_DATA_ARG_VALUE_TYPE'
    """A value in the data argument provided to the execution environment is of an invalid type."""
    INVALID_PYTHON_PROPERTY_TYPE = 'INVALID_PYTHON_PROPERTY_TYPE'
    """The Python property provided to the execution environment is of an invalid type."""
    MISSING_PYTHON_PROPERTY = 'MISSING_PYTHON_PROPERTY'
    """The required Python property is missing from the execution environment data."""
