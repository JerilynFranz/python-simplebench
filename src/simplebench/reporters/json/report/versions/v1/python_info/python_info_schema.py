"""Schema for JSON PythonInfo v1 validation."""
# pylint: disable=line-too-long
from simplebench.reporters.json.report.base import JSONSchema


class PythonInfoSchema(JSONSchema):
    """Schema for the JSON PythonInfo output (V1)"""

    VERSION: int = 1
    """The JSON PythonInfo schema version number."""

    TYPE: str = "SimpleBenchPythonInfo::V1"
    """The JSON PythonInfo schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/python-info.json"
    """The JSON PythonInfo schema $id value for version 1 reports."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = PythonInfoSchema.as_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": cls.ID,
            "title": "Python Info (V1)",
            "type": "object",
            "description": "Python interpreter information (V1)",
            "properties": {
                "version": {
                    "title": "Version",
                    "description": "JSON schema version number.",
                    "type": "integer",
                    "const": cls.VERSION
                },
                "type": {
                    "title": "Type",
                    "description": "JSON schema type property value for version 1 reports.",
                    "type": "string",
                    "const": cls.TYPE
                },
                "hash_id": {
                    "title": "Hash ID",
                    "description": "Unique 64 byte hexadecimal hash identifier for the Python interpreter information data. This can be used to identify identical Python interpreter configurations without revealing details.",
                    "type": "string",
                    "pattern": "^[a-f0-9]{64}$"
                },
                "compiler": {
                    "title": "Python Compiler",
                    "description": "Python compiler information",
                    "type": "string"
                },
                "implementation": {
                    "title": "Python Implementation",
                    "description": "Python implementation",
                    "type": "string"
                },
                "implementation_version": {
                    "title": "Python Implementation Version",
                    "description": "Version of the Python implementation",
                    "type": "string"
                },
                "python_version": {
                    "title": "Python Version",
                    "description": "Python version",
                    "type": "string"
                },
                "build": {
                    "title": "Python Build",
                    "description": "Python build information",
                    "type": "array",
                    "items": {
                            "type": "string"
                    },
                    "minItems": 3
                },
                "release": {
                    "title": "Release",
                    "description": "Release information",
                    "type": "string"
                },
                "system": {
                    "title": "System",
                    "description": "System information",
                    "type": "string"
                }
            },
            "required": [
                "version",
                "type",
                "hash_id",
                "compiler",
                "implementation",
                "implementation_version",
                "python_version",
                "build",
                "release",
                "system"
            ],
            "additionalProperties": False
        }
