"""JSON report log entry factory and validation."""

from simplebench.exceptions import SimpleBenchValueError

from .base import ReportLogEntry, ReportLogEntrySchema
from .exceptions import _ReportLogEntryErrorTag, _ReportLogEntrySchemaErrorTag
from .versions import json_class

_JSON_SCHEMA_AVAILABLE: bool = False
try:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError

    _JSON_SCHEMA_AVAILABLE = True
except ImportError:
    pass


def from_dict(data: dict) -> ReportLogEntry:
    """Create a ReportLogEntry instance from a dictionary, with validation.

    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON report data.
    :return: JSONReport sub-class instance.
    """
    version: int = data.get('version', 0)  # Default to 0 if not present

    report_class: type[ReportLogEntry] = json_class(
        version,
        ReportLogEntry,
        _ReportLogEntryErrorTag.INVALID_VERSION_TYPE,
        _ReportLogEntryErrorTag.UNSUPPORTED_VERSION
    )

    # Only perform JSON Schema validation if the jsonschema package is installed
    if _JSON_SCHEMA_AVAILABLE:
        schema_class: type[ReportLogEntrySchema] = json_class(
            version,
            ReportLogEntrySchema,
            _ReportLogEntrySchemaErrorTag.INVALID_VERSION_TYPE,
            _ReportLogEntrySchemaErrorTag.UNSUPPORTED_VERSION
        )

        try:
            schema = schema_class.json_schema_dict()
            validate(instance=data, schema=schema)  # type: ignore[reportPossiblyUnboundVariable]
        except ValidationError as exc:  # type: ignore[reportPossiblyUnboundVariable]
            raise SimpleBenchValueError(
                f"JSON report data failed validation for version {version}: {exc.message}",
                tag=_ReportLogEntrySchemaErrorTag.JSON_SCHEMA_VALIDATION_ERROR
            ) from exc

    return report_class.from_dict(data)
