"""JSON report classes"""
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from simplebench.exceptions import SimpleBenchValueError

from .base_json_report import JSONReport
from .base_json_report_schema import JSONReportSchema
from .exceptions import _JSONReportErrorTag, _JSONReportSchemaErrorTag
from .versions import json_class


def from_dict(data: dict) -> JSONReport:
    """Create a JSONReport instance from a dictionary, with validation.

    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON report data.
    :return: JSONReport sub-class instance.
    """
    version: int = data.get('version', 0)  # Default to 0 if not present

    report_class: type[JSONReport] = json_class(
        version,
        JSONReport,
        _JSONReportErrorTag.INVALID_VERSION_TYPE,
        _JSONReportErrorTag.UNSUPPORTED_VERSION
    )

    schema_class: type[JSONReportSchema] = json_class(
        version,
        JSONReportSchema,
        _JSONReportSchemaErrorTag.INVALID_VERSION_TYPE,
        _JSONReportSchemaErrorTag.UNSUPPORTED_VERSION
    )

    try:
        schema = schema_class.json_schema_dict()
        validate(instance=data, schema=schema)
    except ValidationError as exc:
        raise SimpleBenchValueError(
            f"JSON report data failed validation for version {version}: {exc.message}",
            tag=_JSONReportErrorTag.JSON_SCHEMA_VALIDATION_ERROR
        ) from exc

    return report_class.from_dict(data)
