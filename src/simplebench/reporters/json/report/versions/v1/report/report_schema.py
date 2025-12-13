"""Schema for JSON reporter v1 validation."""
# pylint: disable=line-too-long
from simplebench.reporters.json.report.base import JSONSchema


class ReportSchema(JSONSchema):
    """Schema for the JSON reporter output (V1)"""

    VERSION: int = 1
    """The JSON report schema version number."""

    TYPE: str = "SimpleBenchReport::V1"
    """The JSON report schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/json-report.json"
    """The JSON report schema ID URL for version 1 reports."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = ReportSchema.as_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": cls.ID,
            "title": "Report Schema (V1)",
            "description": "SimpleBench JSON Report Schema (V1)",
            "type": "object",
            "properties": {
                "version": {
                    "description": "The version of the JSON report schema",
                    "type": "integer",
                    "const": cls.VERSION
                },
                "type": {
                    "title": "Type",
                    "description": "Type of the benchmark report",
                    "type": "string",
                    "const": cls.TYPE
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
                    "$ref": "results-info.json",
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
            "additionalProperties": False
        }
