"""JSON raw data block classes"""
from typing import TYPE_CHECKING

from simplebench.exceptions import SimpleBenchValueError

from ._error_tags import _RawDataBlockErrorTag
from .base import BaseRawDataBlock, JSONSchema

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


def raw_data_block_by_version(version: int) -> type[BaseRawDataBlock]:
    """Retrieve a RawDataBlock class for the specified version.

    :param version: The JSON report version number.
    :return: A RawDataBlock class for the specified version.
    """
    _load_deferred_imports()

    return json_class(
        version,
        BaseRawDataBlock,
        _RawDataBlockErrorTag.INVALID_VERSION_TYPE,
        _RawDataBlockErrorTag.UNSUPPORTED_VERSION
    )


def from_dict(data: dict) -> BaseRawDataBlock:
    """Create a json RawDataBlock instance from a dictionary, with validation.

    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON RawDataBlock data.
    :return: RawDataBlock sub-class instance.
    """
    _load_deferred_imports()

    version: int = data.get('version', 0)  # Default to 0 if not present

    report_class: type[BaseRawDataBlock] = json_class(
        version,
        BaseRawDataBlock,
        _RawDataBlockErrorTag.INVALID_VERSION_TYPE,
        _RawDataBlockErrorTag.UNSUPPORTED_VERSION
    )

    # Only perform JSON Schema validation if the jsonschema package is available
    if _JSON_SCHEMA_AVAILABLE:
        schema_class: type[JSONSchema] = report_class.SCHEMA

        try:
            schema_dict = schema_class.as_dict()
            validate(instance=data, schema=schema_dict)  # type: ignore[reportPossiblyUnboundVariable]
        except ValidationError as exc:  # type: ignore[reportPossiblyUnboundVariable]
            raise SimpleBenchValueError(
                f"JSON report data failed validation for version {version}: {exc.message}",
                tag=_RawDataBlockErrorTag.JSON_SCHEMA_VALIDATION_ERROR
            ) from exc

    return report_class.from_dict(data)


def schema(version: int) -> type[JSONSchema]:
    """Retrieve a RawDataBlockSchema instance for the specified version.

    :param version: The JSON report version number.
    :return: A RawDataBlockSchema instance for the specified version.
    """
    _load_deferred_imports()

    return json_class(
        version,
        BaseRawDataBlock,
        _RawDataBlockErrorTag.INVALID_VERSION_TYPE,
        _RawDataBlockErrorTag.UNSUPPORTED_VERSION
    ).SCHEMA
