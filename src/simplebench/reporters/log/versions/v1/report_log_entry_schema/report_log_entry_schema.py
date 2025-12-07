"""Schema for log report entry validation."""
# pylint: disable=line-too-long


class ReportLogEntrySchema:
    """Schema for log report entry validation (V1)"""

    VERSION: int = 1
    """The JSON report log entry schema version number."""

    @classmethod
    def json_schema_dict(cls) -> dict[str, object]:
        """Get the JSONReportLogEntry schema as a dictionary.

        Usage:
            schema_dict = JSONReportLogEntrySchema.json_schema_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/report-log-entry-v1.json",  # noqa: E501
            "title": "Log Entry Schema (V1)",
            "description": "SimpleBench Report Log Entry Schema (V1)",
            "type": "object",
            "properties": {
                "version": {
                    "title": "Log Version",
                    "description": "Schema version for the log entry",
                    "type": "integer",
                    "const": 1
                },
                "type": {
                    "title": "Type",
                    "description": "Type of the log entry",
                    "type": "string",
                    "const": "ReportLogEntry::V1"
                },
                "timestamp": {
                    "title": "Timestamp",
                    "description": "Timestamp of the report as an ISO 8601 string in UTC",
                    "type": "string",
                    "format": "date-time"
                },
                "benchmark": {
                    "title": "Benchmark Info",
                    "type": "object",
                    "description": "Information about the benchmark itself",
                    "properties": {
                        "id": {
                            "title": "Benchmark ID",
                            "description": "Unique identifier for the benchmark",
                            "type": "string"
                        },
                        "name": {
                            "title": "Benchmark Name",
                            "description": "Name of the benchmark (qv.the benchmark definition 'title')",
                            "type": "string"
                        },
                        "group": {
                            "title": "Benchmark Group",
                            "description": "Group to which the benchmark belongs",
                            "type": "string"
                        },
                    },
                    "required": [
                        "id",
                        "name",
                        "group"
                    ],
                    "additionalProperties": False
                },
                "report": {
                    "title": "Reporter Info",
                    "description": "Information about the reporter generating the log entry",
                    "type": "object",
                    "properties": {
                        "type": {
                            "title": "Reporter Type",
                            "description": "Type of the reporter that generated the report",
                            "type": "string"
                        },
                        "name": {
                            "title": "Reporter Name",
                            "description": "Name of the reporter that generated the report",
                            "type": "string"
                        },
                        "output_format": {
                            "title": "Output Format",
                            "description": "Format of the output",
                            "type": "string"
                        },
                        "uri": {
                            "title": "URI",
                            "description": "URI reference to the output for the report. If a relative-uri, it is relative to the directory containing the report log file.",  # noqa: E501
                            "type": "string",
                            "format": "uri-reference",
                            "examples": ["20251204023938/default/001_tests_test_pytest_plugin_py_test_sleep.json"]
                        },
                    },
                    "required": [
                        "type",
                        "name",
                        "output_format",
                        "uri"
                    ],
                    "additionalProperties": False
                },
                "vcs": {
                    "title": "VCS Info",
                    "description": "Version control system information",
                    "type": "object",
                    "properties": {
                        "git": {
                            "title": "Git Info",
                            "description": "Git repository information",
                            "type": "object",
                            "properties": {
                                "commit": {
                                    "title": "Commit",
                                    "description": "Git commit hash",
                                    "type": "string"
                                },
                                "date": {
                                    "title": "Date",
                                    "description": "Date of the commit as an ISO 8601 string",
                                    "type": "string",
                                    "format": "date-time"
                                },
                                "dirty": {
                                    "title": "Dirty",
                                    "description": "Indicates if the repository has uncommitted changes",
                                    "type": "boolean"
                                }
                            },
                            "required": [
                                "commit",
                                "date",
                                "dirty"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "additionalProperties": False
                },
                "machine_info": {
                    "title": "Machine Info",
                    "description": "Machine information",
                    "type": "object",
                    "properties": {
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
                        "node": {
                            "title": "Node",
                            "description": "Identifier for the machine (blank by default)",
                            "type": "string",
                            "default": ""
                        },
                        "python": {
                            "title": "Python Info",
                            "type": "object",
                            "description": "Python interpreter information",
                            "properties": {
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
                                "version": {
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
                                    "minItems": 3,
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
                            },
                            "required": [
                                "compiler",
                                "implementation",
                                "implementation_version",
                                "version",
                                "build",
                                "release",
                                "system"
                            ],
                            "additionalProperties": False
                        },
                        "cpu": {
                            "title": "CPU",
                            "description": "CPU information",
                            "type": "object",
                            "properties": {
                                "cpuinfo_version": {
                                    "title": "CPU Info Version",
                                    "description": "Version of the cpuinfo library",
                                    "type": "array",
                                    "items": {
                                        "type": "integer"
                                    },
                                    "minItems": 3,
                                },
                                "cpuinfo_version_string": {
                                    "title": "CPU Info Version String",
                                    "description": "CPU info version as a string",
                                    "type": "string"
                                },
                                "arch": {
                                    "description": "CPU architecture",
                                    "type": "string"
                                },
                                "bits": {
                                    "title": "Bits",
                                    "description": "Number of bits of the CPU",
                                    "type": "integer"
                                },
                                "count": {
                                    "title": "Count",
                                    "description": "Number of CPU cores",
                                    "type": "integer"
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
                                "cpuinfo_version",
                                "cpuinfo_version_string",
                                "arch",
                                "bits",
                                "count",
                                "arch_string_raw",
                                "brand_raw"
                            ],
                            "additionalProperties": False
                        },
                    },
                    "required": [
                        "processor",
                        "machine",
                        "python",
                        "cpu"
                    ],
                    "additionalProperties": False
                }
            },
            "required": [
                "version",
                "type",
                "timestamp",
                "benchmark",
                "report",
                "vcs",
                "machine_info"],
            "additionalProperties": False
        }
