"""Schema for JSON reporter v1 validation."""
import json
from functools import cache
from io import StringIO

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.json.report.base.json_report_schema import JSONReportSchema as BaseJSONReportSchema

from .exceptions import _JSONReportSchemaErrorTag


class JSONReportSchema(BaseJSONReportSchema):
    """Schema for the JSON reporter output (V1)"""

    VERSION: int = 1
    """The JSON report schema version number."""

    @classmethod
    def json_schema_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = JSONReportSchema.json_schema_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/report-v1.json",
            "title": "Report Schema (V1)",
            "description": "SimpleBench JSON Report Schema V1",
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
                                "description": "Complexity n value",
                                "type": "number"
                            },
                            "variation_cols": {
                                "title": "Variation Columns",
                                "description": "Variation columns for the result",
                                "type": "object"
                            },
                            "interval_unit": {
                                "title": "Interval Unit",
                                "description": "Interval unit for the result",
                                "type": "string"
                            },
                            "interval_scale": {
                                "title": "Interval Scale",
                                "description": "Interval scale for the result",
                                "type": "number"
                            },
                            "ops_per_interval_unit": {
                                "title": "Operations Per Interval Unit",
                                "description": "Operations per interval unit for the result",
                                "type": "string"
                            },
                            "ops_per_interval_scale": {
                                "title": "Operations Per Interval Scale",
                                "description": "Operations per interval scale for the result",
                                "type": "number"
                            },
                            "memory_unit": {
                                "title": "Memory Unit",
                                "description": "Memory unit for the result",
                                "type": "string"
                            },
                            "memory_scale": {
                                "title": "Memory Scale",
                                "description": "Memory scale for the result",
                                "type": "number"
                            },
                            "total_elapsed": {
                                "title": "Total Elapsed",
                                "description": "Total elapsed time for the result",
                                "type": "number"
                            },
                            "extra_info": {
                                "title": "Extra Info",
                                "description": "A free-form object for third-party extensions or extra data.",
                                "type": "object",
                                "additionalProperties": True
                            },
                            "per_round_timings": {
                                "title": "Per Round Timings",
                                "description": "Per round timings for the result",
                                "$ref": "#/$defs/stats_block"
                            },
                            "ops_per_second": {
                                "title": "Operations Per Second",
                                "description": "Operations per second for the result",
                                "$ref": "#/$defs/stats_block"
                            },
                            "memory": {
                                "title": "Memory",
                                "description": "Memory usage for the result",
                                "$ref": "#/$defs/stats_block"
                            },
                            "peak_memory": {
                                "title": "Peak Memory",
                                "description": "Peak memory usage for the result",
                                "$ref": "#/$defs/stats_block"
                            }
                        },
                        "required": [
                            "type",
                            "group",
                            "title",
                            "description",
                            "n",
                            "variation_cols",
                            "interval_unit",
                            "interval_scale",
                            "ops_per_interval_unit",
                            "ops_per_interval_scale",
                            "memory_unit",
                            "memory_scale",
                            "total_elapsed",
                            "extra_info",
                            "per_round_timings",
                            "ops_per_second",
                            "memory",
                            "peak_memory"
                        ],
                        "additionalProperties": False
                    },
                    "minItems": 1
                },
                "metadata": {
                    "title": "Metadata",
                    "description": "Metadata about the benchmark run",
                    "type": "object",
                    "properties": {
                        "processor": {
                            "title": "Processor",
                            "description": "Processor information",
                            "type": "string"
                        },
                        "machine": {
                            "title": "Machine",
                            "description": "Machine information",
                            "type": "string"
                        },
                        "python_compiler": {
                            "title": "Python Compiler",
                            "description": "Python compiler information",
                            "type": "string"
                        },
                        "python_implementation": {
                            "title": "Python Implementation",
                            "description": "Python implementation information",
                            "type": "string"
                        },
                        "python_implementation_version": {
                            "title": "Python Implementation Version",
                            "description": "Python implementation version information",
                            "type": "string"
                        },
                        "python_version": {
                            "title": "Python Version",
                            "description": "Python version information",
                            "type": "string"
                        },
                        "python_build": {
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
                        },
                        "cpu": {
                            "title": "CPU",
                            "description": "CPU information",
                            "type": "object",
                            "properties": {
                                "python_version": {
                                    "description": "Python version used for CPU information",
                                    "type": "string"
                                },
                                "cpuinfo_version": {
                                    "title": "CPUInfo Version",
                                    "description": "Version of the cpuinfo library",
                                    "type": "array",
                                    "items": {
                                            "type": "integer"
                                    },
                                    "minItems": 3,
                                },
                                "cpuinfo_version_string": {
                                    "title": "CPUInfo Version String",
                                    "description": "Version string of the cpuinfo library",
                                    "type": "string"
                                },
                                "arch": {
                                    "title": "CPU Architecture",
                                    "description": "CPU architecture",
                                    "type": "string"
                                },
                                "bits": {
                                    "title": "CPU Bits",
                                    "description": "Number of bits of the CPU",
                                    "type": "integer"
                                },
                                "count": {
                                    "title": "CPU Core Count",
                                    "description": "Number of CPU cores",
                                    "type": "integer"
                                },
                                "arch_string_raw": {
                                    "title": "Raw Architecture String",
                                    "description": "Raw architecture string",
                                    "type": "string"
                                },
                                "brand_raw": {
                                    "title": "Raw Brand String",
                                    "description": "Raw brand string",
                                    "type": "string"
                                }
                            },
                            "required": [
                                "cpuinfo_version",
                                "cpuinfo_version_string",
                                "arch",
                                "bits",
                                "count",
                                "arch_string_raw",
                                "brand_raw"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "required": [
                        "version",
                        "processor",
                        "machine",
                        "python_compiler",
                        "python_implementation",
                        "python_implementation_version",
                        "python_version",
                        "python_build",
                        "release",
                        "system",
                        "cpu"
                    ],
                    "additionalProperties": False
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
                "metadata"
            ],
            "additionalProperties": False,
            "$defs": {
                "stats_block": {
                    "type": "object",
                    "title": "Statistics Block",
                    "description": "Block containing statistical measurements",
                    "properties": {
                        "type": {
                            "title": "Measurement Type",
                            "description": "Type of the measurements",
                            "type": "string",
                            "enum": [
                                "operations_per_second",
                                "timing",
                                "memory",
                                "peak_memory"]
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
                            "description": "Number of measured iterations",
                            "type": "integer",
                            "exclusiveMinimum": 0
                        },
                        "rounds": {
                            "title": "Number of Rounds",
                            "description": "Number of rounds executed for each iteration",
                            "type": "integer",
                            "exclusiveMinimum": 0
                        },
                        "mean": {
                            "title": "Mean",
                            "description": "Mean of the measurements",
                            "type": "number"
                        },
                        "median": {
                            "title": "Median",
                            "description": "Median of the measurements",
                            "type": "number"
                        },
                        "minimum": {
                            "title": "Minimum",
                            "description": "Minimum value of the measurements",
                            "type": "number"
                        },
                        "maximum": {
                            "title": "Maximum",
                            "description": "Maximum value of the measurements",
                            "type": "number"
                        },
                        "standard_deviation": {
                            "title": "Standard Deviation",
                            "description": "Standard deviation of the measurements",
                            "type": "number"
                        },
                        "relative_standard_deviation": {
                            "title": "Relative Standard Deviation",
                            "description": "Relative standard deviation of the measurements",
                            "type": "number"
                        },
                        "percentiles": {
                            "title": "Percentiles",
                            "description": "Percentiles of the measurements",
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 101,
                            "maxItems": 101
                        }
                    },
                    "required": [
                        "type",
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
            }
        }

    @classmethod
    @cache
    def json_schema(cls) -> str:
        """Get the JSON schema as a JSON string.

        Usage:
            schema_json = JSONReportSchema.json_schema()
        """
        schema_dict = cls.json_schema_dict()
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
                    tag=_JSONReportSchemaErrorTag.SCHEMA_EXPORT_ERROR) from exc
            schema_text = jsonfile.read()
        return schema_text
