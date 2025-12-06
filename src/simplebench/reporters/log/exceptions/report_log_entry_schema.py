"""ErrorTags for ReportLogEntrySchema errors."""

from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReportLogEntrySchemaErrorTag(ErrorTag):
    """Error tags for ReportLogEntrySchema validation errors."""
    INVALID_VERSION_TYPE = "INVALID_VERSION_TYPE"
    """The version field in the ReportLogEntrySchema is not an integer."""
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    """The version in the ReportLogEntrySchema is not supported."""
    JSON_SCHEMA_VALIDATION_ERROR = "JSON_SCHEMA_VALIDATION_ERROR"
    """The JSON report log entry data failed schema validation."""

    INVALID_SCHEMA_VERSION_TYPE = "INVALID_SCHEMA_VERSION_TYPE"
    """The schema_version is not of type integer."""
    INVALID_SCHEMA_VERSION_VALUE = "INVALID_SCHEMA_VERSION_VALUE"
    """The schema_version has an invalid value."""
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    """A required field is missing from the log entry data."""
    INVALID_FIELD_TYPE = "INVALID_FIELD_TYPE"
    """A field in the log entry data is of an incorrect type."""
    INVALID_FIELD_VALUE = "INVALID_FIELD_VALUE"
    """A field in the log entry data has an invalid value."""
    EXTRA_UNEXPECTED_FIELD = "EXTRA_UNEXPECTED_FIELD"
    """An unexpected extra field is present in the log entry data."""