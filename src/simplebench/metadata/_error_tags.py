"""ErrorTags for Metadata validation errors."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetadataErrorTag(ErrorTag):
    """Error tags for Metadata validation errors."""

    INVALID_VERSION_TYPE = auto()
    """The version provided is not an integer."""
    UNSUPPORTED_VERSION = auto()
    """The version provided is not supported."""
    INVALID_FILEPATH_ARG_TYPE = auto()
    """The filepath argument provided to Metadata.__init__() is not a Path instance."""
    INVALID_TIMESTAMP_ARG_TYPE = auto()
    """The timestamp argument provided to Metadata.__init__() is not a float."""
    INVALID_REPORTS_LOG_PATH_ARG_TYPE = auto()
    """The reports_log_path argument provided to Metadata.__init__() is not a Path instance."""
    INVALID_CASE_ARG_TYPE = auto()
    """The case argument provided to Metadata.__init__() is not a Case instance."""
    INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument provided to Metadata.__init__() is not a Choice instance."""
    REPORTS_LOG_PATH_NOT_SET = auto()
    """The reports_log_path is not set when attempting to access it."""
