"""Schema for JSON Report v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema

__all__: list[str] = []


class ReportSchema(JSONSchema):
    """Schema for the JSON Report output (V1)"""

    VERSION: int = 1
    """The JSON report schema version number."""

    TYPE: str = 'SimpleBenchReport::V1'
    """The JSON report schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/json-report.json'
    """The JSON report schema ID URL for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Report Schema (V1)',
        'description': 'SimpleBench JSON Report Schema (V1)',
        'type': 'object',
        'properties': {
            'version': {'description': 'The version of the JSON report schema', 'type': 'integer', 'const': VERSION},
            'type': {'title': 'Type', 'description': 'Type of the benchmark report', 'type': 'string', 'const': TYPE},
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the report data.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'timestamp': {
                'title': 'Timestamp',
                'description': 'Timestamp of the benchmark report in ISO 8601 format (UTC)',
                'type': 'string',
                'format': 'date-time',
                'examples': ['2023-04-01T12:00:00Z'],
            },
            'group': {'title': 'Group', 'description': 'Group of the benchmark', 'type': 'string'},
            'title': {'title': 'Title', 'description': 'Title of the benchmark', 'type': 'string'},
            'description': {'title': 'Description', 'description': 'Description of the benchmark', 'type': 'string'},
            'variation_cols': {
                'title': 'Variation Columns',
                'description': 'Variation columns for the benchmark. Variation columns define the names for parameters for benchmark variations in a run and their display label.',
                'type': 'object',
                'additionalProperties': {'type': 'string'},
            },
            'results': {
                'title': 'Results',
                'description': 'Benchmark results',
                'type': 'array',
                'items': {'$ref': 'results-info.json'},
                'minItems': 1,
            },
            'machine': {'$ref': 'machine-info.json'},
        },
        'required': [
            'version',
            'type',
            'hash_id',
            'timestamp',
            'group',
            'title',
            'description',
            'variation_cols',
            'results',
            'machine',
        ],
        'additionalProperties': False,
    }

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption='JSON Schema for Report V1',
        intro_text='The JSON schema is as follows:',
    )
    """Note containing the JSON schema for docstrings."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = ReportSchema.as_dict()

        :return dict[str, object]: The JSON schema as a dictionary.
        """
        return deepcopy(cls._JSON_SCHEMA_DICT)

    @classmethod
    @format_docstring(JSON_SCHEMA_NOTE=_JSON_SCHEMA_NOTE)
    def as_json(cls) -> str:
        # The `{JSON_SCHEMA_NOTE}` placeholder in the docstring below is
        # dynamically replaced by the `@format_docstring` decorator
        # for use in generated documentation. It is not a typo, but an intentional
        # use of a placeholder.
        """Get the JSON schema as a JSON-formatted string.

        It serializes the schema dictionary to a JSON string.

        Usage:
            schema_json = ReportSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
