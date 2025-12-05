"""Schema for JSON reporter v1 validation."""
import json
from functools import cache
from io import StringIO

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.json.report.base_json_report_schema import JSONReportSchema as BaseJSONReportSchema

from .exceptions import _JSONReportSchemaErrorTag


class JSONReportSchema(BaseJSONReportSchema):
    """Schema for the JSON reporter output (V1)"""

    VERSION: int = 1
    """The JSON report schema version number."""

    @classmethod
    def json_schema_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        Usage:
            schema_dict = JSONReportSchema.json_schema_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/report-v1.json",
            "description": "SimpleBench JSON Report Schema V1",
            "version": 1,
            "type": "object",
            "properties": {
                "type": {
                    "description": "Type of the benchmark",
                    "type": "string"
                },
                "group": {
                    "description": "Group of the benchmark",
                    "type": "string"
                },
                "title": {
                    "description": "Title of the benchmark",
                    "type": "string"
                },
                "description": {
                    "description": "Description of the benchmark",
                    "type": "string"
                },
                "variation_cols": {
                    "description": "Variation columns for the benchmark",
                    "type": "object"
                },
                "results": {
                    "description": "Benchmark results",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "description": "Type of the result",
                                "type": "string"
                            },
                            "group": {
                                "description": "Group of the result",
                                "type": "string"
                            },
                            "title": {
                                "description": "Title of the result",
                                "type": "string"
                            },
                            "description": {
                                "description": "Description of the result",
                                "type": "string"
                            },
                            "n": {
                                "description": "Complexity n value",
                                "type": "number"
                            },
                            "variation_cols": {
                                "description": "Variation columns for the result",
                                "type": "object"
                            },
                            "interval_unit": {
                                "description": "Interval unit for the result",
                                "type": "string"
                            },
                            "interval_scale": {
                                "description": "Interval scale for the result",
                                "type": "number"
                            },
                            "ops_per_interval_unit": {
                                "description": "Operations per interval unit for the result",
                                "type": "string"
                            },
                            "ops_per_interval_scale": {
                                "description": "Operations per interval scale for the result",
                                "type": "number"
                            },
                            "memory_unit": {
                                "description": "Memory unit for the result",
                                "type": "string"
                            },
                            "memory_scale": {
                                "description": "Memory scale for the result",
                                "type": "number"
                            },
                            "total_elapsed": {
                                "description": "Total elapsed time for the result",
                                "type": "number"
                            },
                            "extra_info": {
                                "description": "Extra information for the result",
                                "type": "object"
                            },
                            "per_round_timings": {
                                "description": "Per round timings for the result",
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "description": "Type of the per round timing",
                                        "type": "string"
                                    },
                                    "unit": {
                                        "description": "Unit of the per round timing",
                                        "type": "string"
                                    },
                                    "scale": {
                                        "description": "Scale of the per round timing",
                                        "type": "number"
                                    },
                                    "rounds": {
                                        "description": "Number of rounds for the per round timing",
                                        "type": "integer"
                                    },
                                    "mean": {
                                        "description": "Mean of the per round timing",
                                        "type": "number"
                                    },
                                    "median": {
                                        "description": "Median of the per round timing",
                                        "type": "number"
                                    },
                                    "minimum": {
                                        "description": "Minimum of the per round timing",
                                        "type": "number"
                                    },
                                    "maximum": {
                                        "description": "Maximum of the per round timing",
                                        "type": "number"
                                    },
                                    "standard_deviation": {
                                        "description": "Standard deviation of the per round timing",
                                        "type": "number"
                                    },
                                    "relative_standard_deviation": {
                                        "description": "Relative standard deviation of the per round timing",
                                        "type": "number"
                                    },
                                    "percentiles": {
                                        "description": "Percentiles of the per round timing",
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
                                    "rounds",
                                    "mean",
                                    "median",
                                    "minimum",
                                    "maximum",
                                    "standard_deviation",
                                    "relative_standard_deviation",
                                    "percentiles"
                                ]
                            },
                            "ops_per_second": {
                                "description": "Operations per second for the result",
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "description": "Type of the operations per second",
                                        "type": "string"
                                    },
                                    "unit": {
                                        "description": "Unit of the operations per second",
                                        "type": "string"
                                    },
                                    "scale": {
                                        "description": "Scale of the operations per second",
                                        "type": "number"
                                    },
                                    "rounds": {
                                        "description": "Number of rounds for the operations per second",
                                        "type": "integer"
                                    },
                                    "mean": {
                                        "description": "Mean of the operations per second",
                                        "type": "number"
                                    },
                                    "median": {
                                        "description": "Median of the operations per second",
                                        "type": "number"
                                    },
                                    "minimum": {
                                        "description": "Minimum of the operations per second",
                                        "type": "number"
                                    },
                                    "maximum": {
                                        "description": "Maximum of the operations per second",
                                        "type": "number"
                                    },
                                    "standard_deviation": {
                                        "description": "Standard deviation of the operations per second",
                                        "type": "number"
                                    },
                                    "relative_standard_deviation": {
                                        "description": "Relative standard deviation of the operations per second",
                                        "type": "number"
                                    },
                                    "percentiles": {
                                        "description": "Percentiles of the operations per second",
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
                                    "rounds",
                                    "mean",
                                    "median",
                                    "minimum",
                                    "maximum",
                                    "standard_deviation",
                                    "relative_standard_deviation",
                                    "percentiles"
                                ]
                            },
                            "memory": {
                                "description": "Memory usage for the result",
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "description": "Type of the memory usage",
                                        "type": "string"
                                    },
                                    "unit": {
                                        "description": "Unit of the memory usage",
                                        "type": "string"
                                    },
                                    "scale": {
                                        "description": "Scale of the memory usage",
                                        "type": "number"
                                    },
                                    "rounds": {
                                        "description": "Number of rounds for the memory usage",
                                        "type": "integer"
                                    },
                                    "mean": {
                                        "description": "Mean of the memory usage",
                                        "type": "number"
                                    },
                                    "median": {
                                        "description": "Median of the memory usage",
                                        "type": "number"
                                    },
                                    "minimum": {
                                        "description": "Minimum of the memory usage",
                                        "type": "number"
                                    },
                                    "maximum": {
                                        "description": "Maximum of the memory usage",
                                        "type": "number"
                                    },
                                    "standard_deviation": {
                                        "description": "Standard deviation of the memory usage",
                                        "type": "number"
                                    },
                                    "relative_standard_deviation": {
                                        "description": "Relative standard deviation of the memory usage",
                                        "type": "number"
                                    },
                                    "percentiles": {
                                        "description": "Percentiles of the memory usage",
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
                                    "rounds",
                                    "mean",
                                    "median",
                                    "minimum",
                                    "maximum",
                                    "standard_deviation",
                                    "relative_standard_deviation",
                                    "percentiles"
                                ]
                            },
                            "peak_memory": {
                                "description": "Peak memory usage for the result",
                                "type": "object",
                                "properties": {
                                    "description": "Peak memory usage for the result",
                                    "type": {
                                        "type": "string"
                                    },
                                    "unit": {
                                        "description": "Unit of the peak memory usage",
                                        "type": "string"
                                    },
                                    "scale": {
                                        "description": "Scale of the peak memory usage",
                                        "type": "number"
                                    },
                                    "rounds": {
                                        "description": "Number of rounds for the peak memory usage",
                                        "type": "integer"
                                    },
                                    "mean": {
                                        "description": "Mean of the peak memory usage",
                                        "type": "number"
                                    },
                                    "median": {
                                        "description": "Median of the peak memory usage",
                                        "type": "number"
                                    },
                                    "minimum": {
                                        "description": "Minimum of the peak memory usage",
                                        "type": "number"
                                    },
                                    "maximum": {
                                        "description": "Maximum of the peak memory usage",
                                        "type": "number"
                                    },
                                    "standard_deviation": {
                                        "description": "Standard deviation of the peak memory usage",
                                        "type": "number"
                                    },
                                    "relative_standard_deviation": {
                                        "description": "Relative standard deviation of the peak memory usage",
                                        "type": "number"
                                    },
                                    "percentiles": {
                                        "description": "Percentiles of the peak memory usage",
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
                                    "rounds",
                                    "mean",
                                    "median",
                                    "minimum",
                                    "maximum",
                                    "standard_deviation",
                                    "relative_standard_deviation",
                                    "percentiles"
                                ]
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
                        ]
                    },
                    "minItems": 1
                },
                "metadata": {
                    "description": "Metadata about the benchmark run",
                    "version": 1,
                    "type": "object",
                    "properties": {
                        "processor": {
                            "description": "Processor information",
                            "type": "string"
                        },
                        "machine": {
                            "description": "Machine information",
                            "type": "string"
                        },
                        "python_compiler": {
                            "description": "Python compiler information",
                            "type": "string"
                        },
                        "python_implementation": {
                            "description": "Python implementation information",
                            "type": "string"
                        },
                        "python_implementation_version": {
                            "description": "Python implementation version information",
                            "type": "string"
                        },
                        "python_version": {
                            "description": "Python version information",
                            "type": "string"
                        },
                        "python_build": {
                            "description": "Python build information",
                            "type": "array",
                            "items": {
                                    "type": "string"
                                },
                            "minItems": 2,
                            "maxItems": 2
                        },
                        "release": {
                            "description": "Release information",
                            "type": "string"
                        },
                        "system": {
                            "description": "System information",
                            "type": "string"
                        },
                        "cpu": {
                            "description": "CPU information",
                            "type": "object",
                            "properties": {
                                "python_version": {
                                    "description": "Python version used for CPU information",
                                    "type": "string"
                                },
                                "cpuinfo_version": {
                                    "description": "Version of the cpuinfo library",
                                    "type": "array",
                                    "items": {
                                            "type": "integer"
                                    },
                                    "minItems": 2,
                                    "maxItems": 2
                                },
                                "cpuinfo_version_string": {
                                    "description": "Version string of the cpuinfo library",
                                    "type": "string"
                                },
                                "arch": {
                                    "description": "CPU architecture",
                                    "type": "string"
                                },
                                "bits": {
                                    "description": "Number of bits of the CPU",
                                    "type": "integer"
                                },
                                "count": {
                                    "description": "Number of CPU cores",
                                    "type": "integer"
                                },
                                "arch_string_raw": {
                                    "description": "Raw architecture string",
                                    "type": "string"
                                },
                                "brand_raw": {
                                    "description": "Raw brand string",
                                    "type": "string"
                                }
                            },
                            "required": [
                                "python_version",
                                "cpuinfo_version",
                                "cpuinfo_version_string",
                                "arch",
                                "bits",
                                "count",
                                "arch_string_raw",
                                "brand_raw"
                            ]
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
                    ]
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
            ]
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
