"""ErrorTags for ReportLogEntry validation errors."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReportLogEntryErrorTag(ErrorTag):
    """Error tags for ReportLogEntry validation errors."""

    INVALID_VERSION_VALUE = auto()
    """The version in the JSON report log entry data has an invalid value."""
    INVALID_SCHEMA_URI_TYPE = auto()
    """The $schema field in the JSON report log entry data is not a string."""
    INVALID_SCHEMA_URI_VALUE = auto()
    """The $schema field in the JSON report log entry data has an invalid value."""
    MISSING_FROM_DICT_IMPLEMENTATION = auto()
    """The from_dict method is not implemented in the ReportLogEntry sub-class."""
    INVALID_TYPE_TYPE = auto()
    """The type field in the JSON report log entry data is not a string."""
    INVALID_TYPE_VALUE = auto()
    """The type in the JSON report log entry data is invalid."""
    INVALID_VERSION_TYPE = auto()
    """The version field in the JSON report log entry data is not an integer."""
    UNSUPPORTED_VERSION = auto()
    """The version in the JSON report log entry data is not supported."""
    INVALID_INPUT_DATA_TYPE = auto()
    """The input data provided to ReportLogEntry.from_dict() is not a dictionary."""
    INVALID_INPUT_DATA_KEYS_TYPE = auto()
    """One or more keys in the input data provided to ReportLogEntry.from_dict() are not strings."""

    INVALID_FILEPATH_ARG_TYPE = auto()
    """The filepath argument provided to ReportLogEntry.__init__() is not a Path instance."""
    INVALID_TIMESTAMP_ARG_TYPE = auto()
    """The timestamp argument provided to ReportLogEntry.__init__() is not a float."""
    INVALID_REPORTS_LOG_PATH_ARG_TYPE = auto()
    """The reports_log_path argument provided to ReportLogEntry.__init__() is not a Path instance."""
    INVALID_CASE_ARG_TYPE = auto()
    """The case argument provided to ReportLogEntry.__init__() is not a Case instance."""
    INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument provided to ReportLogEntry.__init__() is not a Choice instance."""

    # save_to_log() errors
    REPORTS_LOG_PATH_NOT_SET = auto()
    """The reports_log_path is not set when attempting to save to log."""

    # LogReader errors
    LOG_FILE_NOT_FOUND = auto()
    """The log file could not be found at the specified path."""
    INVALID_LOG_PATH_TYPE = auto()
    """The log_path provided to LogReader is not a Path instance."""
    LOG_NOT_A_FILE = auto()
    """The log_path provided to LogReader is not a file."""
    LOG_PERMISSION_DENIED = auto()
    """Permission denied when trying to read the log file."""
    LOG_OS_ERROR = auto()
    """An OS error occurred when trying to read the log file."""
    INVALID_LOG_FILE_OBJ_TYPE = auto()
    """The file object provided to LogReader._import_log_entries() is not a TextIOWrapper instance."""
