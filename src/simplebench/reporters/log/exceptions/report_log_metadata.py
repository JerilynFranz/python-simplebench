"""ErrorTags for ReportLogMetadata validation errors."""

from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReportLogMetadataErrorTag(ErrorTag):
    """Error tags for ReportLogMetadata validation errors."""
    INVALID_FILEPATH_ARG_TYPE = "INVALID_FILEPATH_ARG_TYPE"
    """The filepath argument provided to ReportLogMetadata.__init__() is not a Path instance."""
    INVALID_TIMESTAMP_ARG_TYPE = "INVALID_TIMESTAMP_ARG_TYPE"
    """The timestamp argument provided to ReportLogMetadata.__init__() is not a float."""
    INVALID_REPORTS_LOG_PATH_ARG_TYPE = "INVALID_REPORTS_LOG_PATH_ARG_TYPE"
    """The reports_log_path argument provided to ReportLogMetadata.__init__() is not a Path instance."""
    INVALID_CASE_ARG_TYPE = "INVALID_CASE_ARG_TYPE"
    """The case argument provided to ReportLogMetadata.__init__() is not a Case instance."""
    INVALID_CHOICE_ARG_TYPE = "INVALID_CHOICE_ARG_TYPE"
    """The choice argument provided to ReportLogMetadata.__init__() is not a Choice instance."""

    # save_to_log() errors
    REPORTS_LOG_PATH_NOT_SET = "REPORTS_LOG_PATH_NOT_SET"
    """The reports_log_path is not set when attempting to save to log."""

    # LogReader errors
    LOG_FILE_NOT_FOUND = "LOG_FILE_NOT_FOUND"
    """The log file could not be found at the specified path."""
    INVALID_LOG_PATH_TYPE = "INVALID_LOG_PATH_TYPE"
    """The log_path provided to LogReader is not a Path instance."""
    LOG_NOT_A_FILE = "LOG_NOT_A_FILE"
    """The log_path provided to LogReader is not a file."""
    LOG_PERMISSION_DENIED = "LOG_PERMISSION_DENIED"
    """Permission denied when trying to read the log file."""
    LOG_OS_ERROR = "LOG_OS_ERROR"
    """An OS error occurred when trying to read the log file."""
    INVALID_LOG_FILE_OBJ_TYPE = "INVALID_LOG_FILE_OBJ_TYPE"
    """The file object provided to LogReader._import_log_entries() is not a TextIOWrapper instance."""
