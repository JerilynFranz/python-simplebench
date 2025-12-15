"""Schema for JSON MachineInfo v1 validation."""
# pylint: disable=line-too-long
from simplebench.reporters.json.report.base import JSONSchema


class MachineInfoSchema(JSONSchema):
    """Schema for the JSON MachineInfo output (V1)"""

    VERSION: int = 1
    """The JSON MachineInfo schema version number."""

    TYPE: str = "SimpleBenchMachineInfo::V1"
    """The JSON MachineInfo schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/machine-info.json"
    """The JSON MachineInfo schema $id value for version 1 reports."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = MachineInfoSchema.as_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": cls.ID,
            "title": "Machine Info (V1)",
            "description": "Machine information (V1)",
            "type": "object",
            "properties": {
                "version": {
                    "title": "Version",
                    "description": "Version of the machine information schema",
                    "type": "integer",
                    "const": cls.VERSION
                },
                "type": {
                    "title": "Type",
                    "description": "Type of the machine information",
                    "type": "string",
                    "const": cls.TYPE
                },
                "hash_id": {
                    "title": "Hash ID",
                    "description": "Unique 64 byte hexadecimal hash identifier for the machine information data. This can be used to identify identical machine configurations without revealing details.",
                    "type": "string",
                    "pattern": "^[a-f0-9]{64}$"
                },
                "processor": {
                    "title": "Processor",
                    "description": "Processor information",
                    "type": "string"
                },
                "machine": {
                    "title": "Machine",
                    "description": "Machine type",
                    "type": "string"
                },
                "system": {
                    "title": "System",
                    "description": "Operating system name",
                    "type": "string"
                },
                "release": {
                    "title": "Release",
                    "description": "Operating system release",
                    "type": "string"
                },
                "node": {
                    "title": "Node",
                    "description": "Identifier for the machine (blank by default)",
                    "type": "string",
                    "default": ""
                },
                "execution_environment": {
                    "title": "Execution Environment",
                    "description": "Information about the execution environment(s) or runtime(s).",
                    "type": "object",
                    "properties": {
                        "python": {
                            "$ref": "python-info.json"
                        }
                    },
                    "additionalProperties": True
                },
                "cpu": {
                    "$ref": "cpu-info.json"
                }
            },
            "required": [
                "version",
                "type",
                "hash_id",
                "processor",
                "machine",
                "system",
                "release",
                "execution_environment",
                "cpu"
            ],
            "additionalProperties": False
        }
