"""ErrorTags for Metadata validation errors."""

from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetadataErrorTag(ErrorTag):
    """Error tags for Metadata validation errors."""
    INVALID_VERSION_TYPE = "INVALID_VERSION_TYPE"
    """The version provided is not an integer."""
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    """The version provided is not supported."""
    INVALID_FILEPATH_ARG_TYPE = "INVALID_FILEPATH_ARG_TYPE"
    """The filepath argument provided to ReportMetadata.__init__() is not a Path instance."""
    INVALID_TIMESTAMP_ARG_TYPE = "INVALID_TIMESTAMP_ARG_TYPE"
    """The timestamp argument provided to ReportMetadata.__init__() is not a float."""
    INVALID_REPORTS_LOG_PATH_ARG_TYPE = "INVALID_REPORTS_LOG_PATH_ARG_TYPE"
    """The reports_log_path argument provided to ReportMetadata.__init__() is not a Path instance."""
    INVALID_CASE_ARG_TYPE = "INVALID_CASE_ARG_TYPE"
    """The case argument provided to ReportMetadata.__init__() is not a Case instance."""
    INVALID_CHOICE_ARG_TYPE = "INVALID_CHOICE_ARG_TYPE"
    """The choice argument provided to ReportMetadata.__init__() is not a Choice instance."""
    REPORTS_LOG_PATH_NOT_SET = "REPORTS_LOG_PATH_NOT_SET"
    """The reports_log_path is not set when attempting to access it."""
