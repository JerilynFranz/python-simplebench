"""JSON report classes"""
from typing import TYPE_CHECKING

from simplebench.exceptions import SimpleBenchValueError

from .base import JSONReport, JSONReportSchema
from .exceptions import _JSONReportErrorTag, _JSONReportSchemaErrorTag

_JSON_SCHEMA_AVAILABLE: bool = False
try:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError

    _JSON_SCHEMA_AVAILABLE = True
except ImportError:
    pass

_JSON_CLASS_LOADED: bool = False

if TYPE_CHECKING:
    from .versions import json_class
    _JSON_CLASS_LOADED = True  # To avoid import issues during type checking
else:
    json_class = None   # pylint: disable=invalid-name


def _load_deferred_imports() -> None:
    """Load deferred imports."""
    global _JSON_CLASS_LOADED, json_class  # pylint: disable=global-statement
    if not _JSON_CLASS_LOADED:
        from .versions import json_class  # pylint: disable=import-outside-toplevel
        _JSON_CLASS_LOADED = True


def from_dict(data: dict) -> JSONReport:
    """Create a JSONReport instance from a dictionary, with validation.

    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON report data.
    :return: JSONReport sub-class instance.
    """
    _load_deferred_imports()

    version: int = data.get('version', 0)  # Default to 0 if not present

    report_class: type[JSONReport] = json_class(
        version,
        JSONReport,
        _JSONReportErrorTag.INVALID_VERSION_TYPE,
        _JSONReportErrorTag.UNSUPPORTED_VERSION
    )

    # Only perform JSON Schema validation if the jsonschema package is available
    if _JSON_SCHEMA_AVAILABLE:
        schema_class: type[JSONReportSchema] = json_class(
            version,
            JSONReportSchema,
            _JSONReportSchemaErrorTag.INVALID_VERSION_TYPE,
            _JSONReportSchemaErrorTag.UNSUPPORTED_VERSION
        )

        try:
            schema = schema_class.json_schema_dict()
            validate(instance=data, schema=schema)  # type: ignore[reportPossiblyUnboundVariable]
        except ValidationError as exc:  # type: ignore[reportPossiblyUnboundVariable]
            raise SimpleBenchValueError(
                f"JSON report data failed validation for version {version}: {exc.message}",
                tag=_JSONReportErrorTag.JSON_SCHEMA_VALIDATION_ERROR
            ) from exc

    return report_class.from_dict(data)
