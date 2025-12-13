"""Schema for JSON StatsBlock v1 validation."""
# pylint: disable=line-too-long
from simplebench.reporters.json.report.base import JSONSchema


class StatsBlockSchema(JSONSchema):
    """Schema for the JSON StatsBlock output (V1)"""

    VERSION: int = 1
    """The JSON StatsBlock schema version number."""

    TYPE: str = "SimpleBenchStatsBlock::V1"
    """The JSON StatsBlock schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json"
    """The JSON StatsBlock schema $id value for version 1 reports."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = StatsBlockSchema.as_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": cls.ID,
            "title": "Statistics Block (V1)",
            "description": "Block containing statistical measurements",
            "type": "object",
            "properties": {
                "type": {
                    "title": "Block Type",
                    "description": "The type of the block. Must be 'SimpleBenchStatsBlock::V1' for Statistics Block version 1.",
                    "type": "string",
                    "const": cls.TYPE
                },
                "version": {
                    "title": "Schema Version",
                    "description": "The version of the schema. Must be 1 for Statistics Block version 1.",
                    "type": "integer",
                    "const": cls.VERSION
                },
                "semantic_type": {
                    "title": "Measurement Type",
                    "description": "The semantic type of the measurements, formatted as 'namespace::type_name'. This dictates how the data should be interpreted. Standard types use the 'simplebench_std' namespace. Users can define custom types using their own namespace.",
                    "type": "string",
                    "pattern": "^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$",
                    "examples": [
                        "simplebench_std::time_per_operation",
                        "simplebench_std::operations_per_second",
                        "simplebench_std::memory_usage",
                        "simplebench_std::peak_memory_usage",
                        "my_plugin::syscalls_per_operation"
                    ]
                },
                "name": {
                    "title": "Measurement Name",
                    "description": "Human-readable name of the measurement.",
                    "type": "string",
                    "minLength": 1
                },
                "description": {
                    "title": "Measurement Description",
                    "description": "A brief description of the measurement's content or purpose.",
                    "type": "string"
                },
                "timer": {
                    "title": "Timer",
                    "description": "The timing function used for this measurement (e.g., 'perf_counter'). Should be included for any timing-related metrics.",
                    "type": "string"
                },
                "unit": {
                    "title": "Measurement Unit",
                    "description": "Unit of the measurement values",
                    "type": "string",
                    "minLength": 1
                },
                "scale": {
                    "title": "Measurement Scale",
                    "description": "Scale of the measurement values",
                    "type": "number",
                    "exclusiveMinimum": 0
                },
                "iterations": {
                    "title": "Number of Iterations",
                    "description": "Number of measured iterations. This corresponds to the number of items in the 'measurements' array.",
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "rounds": {
                    "title": "Number of Rounds",
                    "description": "Number of rounds executed for each iteration. The total number of operations is iterations * rounds.",
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "mean": {
                    "title": "Mean",
                    "description": "The mean of the per-iteration measurements.",
                    "type": "number"
                },
                "median": {
                    "title": "Median",
                    "description": "The median of the per-iteration measurements.",
                    "type": "number"
                },
                "minimum": {
                    "title": "Minimum",
                    "description": "The minimum value of the per-iteration measurements.",
                    "type": "number"
                },
                "maximum": {
                    "title": "Maximum",
                    "description": "The maximum value of the per-iteration measurements.",
                    "type": "number"
                },
                "standard_deviation": {
                    "title": "Standard Deviation",
                    "description": "The standard deviation of a single underlying operation (round). If rounds > 1, this value is scaled from the standard deviation of the iterations to counter the effect of averaging.",
                    "type": "number"
                },
                "relative_standard_deviation": {
                    "title": "Relative Standard Deviation",
                    "description": "The relative standard deviation (coefficient of variation), based on the scaled standard deviation of a single round.",
                    "type": "number"
                },
                "percentiles": {
                    "title": "Percentiles",
                    "description": "Percentiles of the per-iteration measurements.",
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 101,
                    "maxItems": 101
                },
                "measurements": {
                    "title": "Measurements",
                    "description": "Raw data series of measurements collected (one value per iteration). The values are the AVERAGE per iteration (i.e., total time for the iteration divided by number of rounds). This array may be empty if raw measurements were not recorded.",
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "default": []
                }
            },
            "required": [
                "type",
                "version",
                "name",
                "semantic_type",
                "unit",
                "scale",
                "iterations",
                "rounds",
                "mean",
                "median",
                "minimum",
                "maximum",
                "standard_deviation",
                "relative_standard_deviation",
                "percentiles"
            ],
            "additionalProperties": False
        }
