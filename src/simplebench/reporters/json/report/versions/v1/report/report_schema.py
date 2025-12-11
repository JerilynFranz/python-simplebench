"""Schema for JSON reporter v1 validation."""
import json
from functools import cache
from io import StringIO

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.json.report.base import JSONSchema
from simplebench.reporters.json.report.exceptions import _ReportSchemaErrorTag


class ReportSchema(JSONSchema):
    """Schema for the JSON reporter output (V1)"""

    VERSION: int = 1
    """The JSON report schema version number."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = JSONReportSchema.json_schema_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/json-report.json",
            "title": "Report Schema (V1)",
            "description": "SimpleBench JSON Report Schema (V1)",
            "type": "object",
            "properties": {
                "version": {
                    "description": "The version of the JSON report schema",
                    "type": "integer",
                    "const": 1
                },
                "type": {
                    "title": "Type",
                    "description": "Type of the benchmark report",
                    "type": "string",
                    "const": "SimpleBenchReport::V1"
                },
                "group": {
                    "title": "Group",
                    "description": "Group of the benchmark",
                    "type": "string"
                },
                "title": {
                    "title": "Title",
                    "description": "Title of the benchmark",
                    "type": "string"
                },
                "description": {
                    "title": "Description",
                    "description": "Description of the benchmark",
                    "type": "string"
                },
                "variation_cols": {
                    "title": "Variation Columns",
                    "description": "Variation columns for the benchmark",
                    "type": "object"
                },
                "results": {
                    "title": "Results",
                    "description": "Benchmark results",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "title": "Type",
                                "description": "Type of the result",
                                "type": "string"
                            },
                            "group": {
                                "title": "Group",
                                "description": "Group of the result",
                                "type": "string"
                            },
                            "title": {
                                "title": "Title",
                                "description": "Title of the result",
                                "type": "string"
                            },
                            "description": {
                                "title": "Description",
                                "description": "Description of the result",
                                "type": "string"
                            },
                            "n": {
                                "title": "N",
                                "description": "Complexity analysis N value for the result",
                                "type": "number"
                            },
                            "variation_cols": {
                                "title": "Variation Columns",
                                "description": "Variation columns for the result",
                                "type": "object"
                            },
                            "metrics": {
                                "$ref": "#/$defs/metrics"
                            },
                            "extra_info": {
                                "title": "Extra Info",
                                "description": "A free-form object for third-party extensions or extra data.",
                                "type": "object",
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "type",
                            "group",
                            "title",
                            "description",
                            "n",
                            "variation_cols",
                            "metrics",
                            "extra_info"
                        ],
                        "additionalProperties": False
                    },
                    "minItems": 1
                },
                "machine": {
                    "$ref": "machine-info.json"
                }
            },
            "required": [
                "version",
                "type",
                "group",
                "title",
                "description",
                "variation_cols",
                "results",
                "machine"
            ],
            "additionalProperties": False,
            "$defs": {
                "metrics": {
                    "type": "object",
                    "title": "Metrics",
                    "description": (
                        "A collection of metric blocks, indexed by a unique, namespaced metric ID.\n\n"
                        "Examples of valid keys:\n"
                        "- `simplebench_std::time_per_operation`\n"
                        "- `simplebench_std::operations_per_second`\n"
                        "- `simplebench_std::memory_usage`\n"
                        "- `simplebench_std::peak_memory_usage`\n"
                        "- `simplebench_std::wallclock_time`"
                        "\n- `my_plugin::custom_metric`"),
                    "patternProperties": {
                        "^[a-zA-Z0-9_]+::[a-zA-Z0-9_]+$": {
                            "$ref": "#/$defs/metric_block"
                        }
                    },
                    "additionalProperties": False
                },
                "metric_block": {
                    "title": "Metric Block",
                    "description": (
                        "A container for a measurement, which can be a single "
                        "value or a statistical summary."),
                    "oneOf": [
                        {
                            "$ref": "stats-block.json"
                        },
                        {
                            "$ref": "value-block.json"
                        }
                    ]
                }
            }
        }

    @classmethod
    @cache
    def as_string(cls) -> str:
        """Get the JSON schema as a JSON string.

        Usage:
            schema_json = JSONReportSchema.as_string()
        """
        schema_dict = cls.as_dict()
        with StringIO() as jsonfile:
            try:
                json.dump(schema_dict, jsonfile, indent=2)
                jsonfile.seek(0)
            # If an error occurs during dumping, it will be caught below
            # and is pretty much certain to be some version of type error
            # because the schema is a static dict. Bad programmer, no cookie.
            except Exception as exc:
                raise SimpleBenchTypeError(
                    f'Error generating JSON output for JSON Reporter schema: {exc}',
                    tag=_ReportSchemaErrorTag.SCHEMA_EXPORT_ERROR) from exc
            schema_text = jsonfile.read()
        return schema_text
