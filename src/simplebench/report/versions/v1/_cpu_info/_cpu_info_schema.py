"""Schema for JSON CPUInfo v1 validation."""
# pylint: disable=line-too-long
from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report._base import JSONSchema


class CPUInfoSchema(JSONSchema):
    """Schema for the JSON CPUInfo output (V1)"""

    VERSION: int = 1
    """The JSON CPUInfo schema version number."""

    TYPE: str = "SimpleBenchCPUInfo::V1"
    """The JSON CPUInfo schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/cpu-info.json"
    """The JSON CPUInfo schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": ID,
            "title": "CPU (V1)",
            "description": "CPU information (V1)",
            "type": "object",
            "properties": {
                "version": {
                    "description": "The version of the CPU information schema",
                    "type": "integer",
                    "const": VERSION
                },
                "type": {
                    "title": "Type",
                    "description": "Type of the CPU information schema",
                    "type": "string",
                    "const": TYPE
                },
                "hash_id": {
                    "title": "Hash ID",
                    "description": "Unique 64 byte hexadecimal hash identifier for the CPU information data. This can be used to identify the generator and uniqueness of the data.",
                    "type": "string",
                    "pattern": "^[a-f0-9]{64}$"
                },
                "data": {
                    "title": "CPU Info Data",
                    "description": "Raw CPU information data collected from the system using the cpuinfo library.",
                    "type": "object",
                    "additionalProperties": True
                },
            },
            "required": [
                "hash_id",
                "type",
                "version",
                "data"
            ],
            "additionalProperties": False
        }

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption="JSON Schema for ValueBlock V1",
        intro_text="The JSON schema is as follows:"
    )
    """Note containing the JSON schema for docstrings."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = CPUInfoSchema.as_dict()

        :return dict[str, object]: The JSON schema as a dictionary.
        """
        return deepcopy(cls._JSON_SCHEMA_DICT)

    @classmethod
    @format_docstring(JSON_SCHEMA_NOTE=_JSON_SCHEMA_NOTE)
    def as_json(cls) -> str:
        # The `{JSON_SCHEMA_NOTE}` placeholder in the docstring below is
        # dynamically replaced by the `@format_docstring` decorator
        # for use in generated documentation. It is not a typo, but an intentional
        # use of a placeholder.
        """Get the JSON schema as a JSON-formatted string.

        It serializes the schema dictionary to a JSON string.

        Usage:
            schema_json = CPUInfoSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
