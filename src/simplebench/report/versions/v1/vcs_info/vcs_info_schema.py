"""Schema for JSON VCSInfo v1 validation."""
# pylint: disable=line-too-long
from simplebench.reporters.json.report.base import JSONSchema


class VCSInfoSchema(JSONSchema):
    """Schema for the JSON VCSInfo output (V1)"""

    VERSION: int = 1
    """The JSON VCSInfo schema version number."""

    TYPE: str = "SimpleBenchVCSInfo::V1"
    """The JSON VCSInfo schema type property value for version 1 reports."""

    ID: str = "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/vcs-info.json"
    """The JSON VCSInfo schema $id value for version 1 reports."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = VCSInfoSchema.as_dict()
        """
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/vcs-info.json",
            "title": "VCS Info (V1)",
            "description": "Version control system information (V1)",
            "type": "object",
            "properties": {
                "version": {
                    "title": "Version",
                    "description": "The version of the VCS info schema",
                    "type": "integer",
                    "const": 1
                },
                "type": {
                    "title": "Type",
                    "description": "The type of the VCS info schema",
                    "type": "string",
                    "const": "SimpleBenchVCSInfo::V1"
                },
                "vcs": {
                    "title": "VCS Type",
                    "description": "The type of version control system",
                    "type": "string",
                    "enum": ["git", "hg", "svn", "perforce", "tfvc"]
                },
                "commit_id": {
                    "title": "Commit ID",
                    "description": "The unique identifier (hash, changeset ID, etc.) of the current revision",
                    "type": "string",
                    "minLength": 1
                },
                "branch": {
                    "title": "Branch",
                    "description": "The current branch name",
                    "type": "string"
                },
                "repository_url": {
                    "title": "Repository URL",
                    "description": "Optional URL of the primary remote repository (e.g., 'origin' in Git, 'default' in Mercurial)",
                    "type": "string",
                    "format": "uri"
                },
                "is_dirty": {
                    "title": "Is Dirty",
                    "description": "Indicates if there are uncommitted changes in the working tree",
                    "type": "boolean"
                },
                "commit_datetime": {
                    "title": "Commit Datetime",
                    "description": "The UTC datetime of the current commit in ISO 8601 format",
                    "type": "string",
                    "format": "date-time",
                    "examples": ["2024-01-15T12:34:56Z"]
                }
            },
            "required": [
                "version",
                "type",
                "vcs",
                "commit_id",
                "branch",
                "is_dirty",
                "commit_datetime"
            ],
            "additionalProperties": False
        }
