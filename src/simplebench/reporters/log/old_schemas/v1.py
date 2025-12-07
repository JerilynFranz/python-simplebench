"""Schema for log reporter metadata validation."""


class LogReportMetadataSchema:
    """Schema for log reporter metadata validation (V1)"""

    json_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://simplebench.readthedocs.io/schemas/log/report-metadata-v1.json",
        "description": "SimpleBench Log Reporter Metadata Schema V1",
        "type": "object",
        "properties": {
            "version": {
                "description": "Schema version",
                "type": "integer"
            },
            "timestamp": {
                "description": "Timestamp of the report as an ISO 8601 string in UTC",
                "type": "string",
                "format": "date-time"
            },
            "benchmark_id": {
                "description": "Unique identifier for the benchmark",
                "type": "string"
            },
            "benchmark_group": {
                "description": "Group to which the benchmark belongs",
                "type": "string"
            },
            "reporter_type": {
                "description": "Type of the reporter",
                "type": "string"
            },
            "reporter_name": {
                "description": "Name of the reporter",
                "type": "string"
            },
            "output_format": {
                "description": "Format of the output",
                "type": "string"
            },
            "benchmark_title": {
                "description": "Title of the benchmark",
                "type": "string"
            },
            "uri": {
                "description": "URI reference to the benchmark output file",
                "type": "string",
                "format": "uri-reference"
            },
            "git": {
                "description": "Git repository information",
                "type": "object",
                "properties": {
                    "commit": {
                        "description": "Git commit hash",
                        "type": "string"
                    },
                    "date": {
                        "description": "Date of the commit as an ISO 8601 string",
                        "type": "string",
                        "format": "date-time"
                    },
                    "dirty": {
                        "description": "Indicates if the repository has uncommitted changes",
                        "type": "boolean"
                    }
                },
                "required": [
                    "commit",
                    "date",
                    "dirty"
                ]
            },
            "machine_info": {
                "description": "Machine information",
                "type": "object",
                "properties": {
                    "processor": {
                        "description": "Processor information",
                        "type": "string"
                    },
                    "machine": {
                        "description": "Machine type",
                        "type": "string"
                    },
                    "python_compiler": {
                        "description": "Python compiler information",
                        "type": "string"
                    },
                    "python_implementation": {
                        "description": "Python implementation",
                        "type": "string"
                    },
                    "python_implementation_version": {
                        "description": "Version of the Python implementation",
                        "type": "string"
                    },
                    "python_version": {
                        "description": "Python version",
                        "type": "string"
                    },
                    "python_build": {
                        "description": "Python build information",
                        "type": "array",
                        "items": {
                                "type": "string"
                        },
                        "minItems": 2,
                        "maxItems": 4
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
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "cpuinfo_version_string": {
                                "description": "CPU info version as a string",
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
            "timestamp",
            "benchmark_id",
            "benchmark_group",
            "reporter_type",
            "reporter_name",
            "output_format",
            "benchmark_title",
            "git",
            "machine_info"
        ]
    }
    """JSON Schema for log reporter metadata validation."""
