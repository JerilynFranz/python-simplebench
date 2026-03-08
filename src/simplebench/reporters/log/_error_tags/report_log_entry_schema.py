"""ErrorTags for ReportLogEntrySchema errors."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReportLogEntrySchemaErrorTag(ErrorTag):
    """Error tags for ReportLogEntrySchema validation errors."""

    INVALID_VERSION_TYPE = auto()
    """The version field in the ReportLogEntrySchema is not an integer."""
    UNSUPPORTED_VERSION = auto()
    """The version in the ReportLogEntrySchema is not supported."""
    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """The JSON report log entry data failed schema validation."""

    INVALID_SCHEMA_VERSION_TYPE = auto()
    """The schema_version is not of type integer."""
    INVALID_SCHEMA_VERSION_VALUE = auto()
    """The schema_version has an invalid value."""
    MISSING_REQUIRED_FIELD = auto()
    """A required field is missing from the log entry data."""
    INVALID_FIELD_TYPE = auto()
    """A field in the log entry data is of an incorrect type."""
    INVALID_FIELD_VALUE = auto()
    """A field in the log entry data has an invalid value."""
    EXTRA_UNEXPECTED_FIELD = auto()
    """An unexpected extra field is present in the log entry data."""
