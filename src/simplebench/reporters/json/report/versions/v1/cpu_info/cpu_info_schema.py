"""Schema for JSON CPUInfo v1 validation."""
# pylint: disable=line-too-long
from simplebench.reporters.json.report.base import JSONSchema


class CPUInfoSchema(JSONSchema):
    """Schema for the JSON CPUInfo output (V1)"""

    VERSION: int = 1
    """The JSON CPUInfo schema version number."""

    TYPE: str = "SimpleBenchCPUInfo::V1"
    """The JSON CPUInfo schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/cpu-info.json"
    """The JSON CPUInfo schema $id value for version 1 reports."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = CPUInfoSchema.as_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": CPUInfoSchema.ID,
            "title": "CPU (V1)",
            "description": "CPU information (V1)",
            "type": "object",
            "properties": {
                "version": {
                    "description": "The version of the CPU information schema",
                    "type": "integer",
                    "const": CPUInfoSchema.VERSION
                },
                "type": {
                    "title": "Type",
                    "description": "Type of the CPU information schema",
                    "type": "string",
                    "const": CPUInfoSchema.TYPE
                },
                "cpuinfo_version": {
                    "title": "CPU Info Version",
                    "description": "Optional version of the cpuinfo library",
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "minItems": 3
                },
                "cpuinfo_version_string": {
                    "title": "CPU Info Version String",
                    "description": "Optional version of the cpuinfo library as a string",
                    "type": "string"
                },
                "hash_id": {
                    "title": "Hash ID",
                    "description": "Unique 64 byte hexadecimal hash identifier for the CPU information data. This can be used to identify identical CPU configurations without revealing details.",
                    "type": "string",
                    "pattern": "^[a-f0-9]{64}$"
                },
                "arch": {
                    "description": "CPU architecture",
                    "type": "string"
                },
                "bits": {
                    "title": "Bits",
                    "description": "Number of bits of the CPU",
                    "type": "integer",
                    "minimum": 16
                },
                "count": {
                    "title": "Count",
                    "description": "Number of CPU cores",
                    "type": "integer",
                    "minimum": 1
                },
                "arch_string_raw": {
                    "title": "Arch String Raw",
                    "description": "Raw architecture string",
                    "type": "string"
                },
                "brand_raw": {
                    "title": "Brand Raw",
                    "description": "Raw brand string",
                    "type": "string"
                }
            },
            "required": [
                "hash_id",
                "arch",
                "bits",
                "count",
                "arch_string_raw",
                "brand_raw"
            ],
            "additionalProperties": False
        }
