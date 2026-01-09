"""Schema for JSON MemoryInfo v1 validation."""
# pylint: disable=line-too-long
from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report._base import JSONSchema


class MemoryInfoSchema(JSONSchema):
    """Schema for the JSON MemoryInfo output (V1)"""

    VERSION: int = 1
    """The JSON MemoryInfo schema version number."""
    TYPE: str = "SimpleBenchMemoryInfo::V1"
    """The JSON MemoryInfo schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json"
    """The JSON MemoryInfo schema $id value for version 1 reports."""
    _JSON_SCHEMA_DICT: dict[str, object] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": ID,
            "title": "Memory Info (V1)",
            "type": "object",
            "description": "Memory information (V1)",
            "properties": {
                "version": {
                    "title": "Version",
                    "description": "JSON schema version number.",
                    "type": "integer",
                    "const": VERSION
                },
                "type": {
                    "title": "Type",
                    "description": "JSON schema type property value for version 1 reports.",
                    "type": "string",
                    "const": TYPE
                },
                "hash_id": {
                    "title": "Hash ID",
                    "description": "Unique 64 byte hexadecimal hash identifier for the memory information data. This can be used to identify identical memory configurations without revealing details.",
                    "type": "string",
                    "pattern": "^[a-f0-9]{64}$"
                },
                "virtual_memory": {
                    "title": "Virtual Memory",
                    "description": "Virtual Memory Information",
                    "type": "object",
                    "properties": {
                        "total": {
                            "title": "Total Physical Memory",
                            "description": "Total physical memory in bytes.",
                            "type": "integer",
                            "minimum": 0
                        },
                        "available": {
                            "title": "Available Memory",
                            "description": "Available memory in bytes.",
                            "type": "integer",
                            "minimum": 0
                        },
                        "percent": {
                            "title": "Used Percentage",
                            "description": "Percentage of memory used.",
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 100.0
                        },
                        "used": {
                            "title": "Used Memory",
                            "description": "Used memory in bytes.",
                            "type": "integer",
                            "minimum": 0
                        },
                        "free": {
                            "title": "Free Memory",
                            "description": "Free memory in bytes.",
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "total",
                        "available",
                        "percent",
                        "used",
                        "free"
                    ],
                    "additionalProperties": False
                },
                "swap_memory": {
                    "title": "Swap Memory",
                    "description": "Swap Memory Information",
                    "type": "object",
                    "properties": {
                        "total": {
                            "title": "Total Swap Memory",
                            "description": "Total swap memory in bytes.",
                            "type": "integer",
                            "minimum": 0
                        },
                        "used": {
                            "title": "Used Swap Memory",
                            "description": "Used swap memory in bytes.",
                            "type": "integer",
                            "minimum": 0
                        },
                        "free": {
                            "title": "Free Swap Memory",
                            "description": "Free swap memory in bytes.",
                            "type": "integer",
                            "minimum": 0
                        },
                        "percent": {
                            "title": "Used Percentage",
                            "description": "Percentage of swap memory used.",
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 100.0
                        },
                        "swap_in": {
                            "title": "Swap In",
                            "description": "Swap memory sent to disk in bytes.",
                            "type": "integer",
                            "minimum": 0
                        },
                        "swap_out": {
                            "title": "Swap Out",
                            "description": "Swap memory received from disk in bytes.",
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [
                        "total",
                        "used",
                        "free",
                        "percent",
                        "swap_in",
                        "swap_out"
                    ],
                    "additionalProperties": False
                }

            },
            "required": [
                "version",
                "type",
                "hash_id",
                "total_physical",
                "total_swap"
            ],
            "additionalProperties": False
        }

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption="JSON Schema for MemoryInfo V1",
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
            schema_dict = MemoryInfoSchema.as_dict()

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
            schema_json = MemoryInfoSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
