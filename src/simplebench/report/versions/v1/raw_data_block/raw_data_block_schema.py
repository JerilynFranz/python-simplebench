"""Schema for JSON RawDataBlock v1 validation."""
# pylint: disable=line-too-long
from simplebench.report.base import JSONSchema


class RawDataBlockSchema(JSONSchema):
    """Schema for the JSON RawDataBlock output (V1)"""

    VERSION: int = 1
    """The JSON RawDataBlock schema version number."""
    TYPE: str = "SimpleBenchRawDataBlock::V1"
    """The JSON RawDataBlock schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/raw-data-block.json"
    """The JSON RawDataBlock schema $id value for version 1 reports."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = ValueBlockSchema.as_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": cls.ID,
            "title": "Raw Data Block (V1)",
            "description": "Block containing raw measurement data.",
            "type": "object",
            "properties": {
                "version": {
                    "title": "Schema Version",
                    "description": "Version of the schema. Must be '1' for Raw Data Block version 1.",
                    "type": "integer",
                    "const": cls.VERSION
                },
                "type": {
                    "title": "Block Type",
                    "description": "The type of the block. Must be 'SimpleBenchRawDataBlock::V1' for Raw Data Block version 1.",
                    "type": "string",
                    "const": cls.TYPE
                },
                "semantic_type": {
                    "title": "Measurement Type",
                    "description": "The semantic type of the measurements, formatted as 'namespace::type_name'. This dictates how the data should be interpreted. Standard types use the 'simplebench_std' namespace. Users can define custom types using their own namespace.",
                    "type": "string",
                    "pattern": "^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$",
                    "examples": [
                        "simplebench_std::wallclock_time",
                        "simplebench_std::cpu_time",
                        "my_plugin::context_switches"
                    ]
                },
                "timer": {
                    "title": "Timer",
                    "description": "The timing function used for this measurement (e.g., 'perf_counter'). Should be included for any timing-related metrics.",
                    "type": "string"
                },
                "cpu_timer": {
                    "title": "CPU Timer",
                    "description": "The CPU timing function used for this measurement (e.g., 'process_time_ns'). Should be included for any CPU time-related metrics.",
                    "type": "string"
                },
                "unit": {
                    "title": "Measurement Unit",
                    "description": "Unit of the measurement value",
                    "type": "string",
                    "minLength": 1
                },
                "scale": {
                    "title": "Measurement Scale",
                    "description": "Scale of the measurement value",
                    "type": "number",
                    "exclusiveMinimum": 0
                },
                "data": {
                    "title": "Data",
                    "description": "The raw measurement data as an array of numbers.",
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                }
            },
            "required": [
                "version",
                "type",
                "semantic_type",
                "unit",
                "scale",
                "data"
            ],
            "additionalProperties": False
        }
