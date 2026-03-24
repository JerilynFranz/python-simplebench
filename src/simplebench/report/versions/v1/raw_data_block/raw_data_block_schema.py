"""Schema for JSON RawDataBlock v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema


class RawDataBlockSchema(JSONSchema):
    """Schema for the JSON RawDataBlock output (V1)"""

    VERSION: int = 1
    """The JSON RawDataBlock schema version number."""

    TYPE: str = 'SimpleBenchRawDataBlock::V1'
    """The JSON RawDataBlock schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/raw-data-block.json'
    """The JSON RawDataBlock schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Raw Data Block (V1)',
        'description': 'Block containing raw measurement data.',
        'type': 'object',
        'properties': {
            'version': {
                'title': 'Schema Version',
                'description': "Version of the schema. Must be '1' for Raw Data Block version 1.",
                'type': 'integer',
                'const': VERSION,
            },
            'type': {
                'title': 'Block Type',
                'description': "The type of the block. Must be 'SimpleBenchRawDataBlock::V1' for Raw Data Block version 1.",
                'type': 'string',
                'const': TYPE,
            },
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 character hexadecimal hash identifier for the stats-block data.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'metric': {
                'title': 'Metric Reference',
                'description': 'Reference to a Metric by hash_id. This links the raw data block to the specific metric it is associated with, allowing for proper interpretation of the data.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'rounds': {
                'title': 'Number of Rounds',
                'description': 'Number of rounds executed for each iteration. The total number of operations is iterations * rounds.',
                'type': 'integer',
                'exclusiveMinimum': 0,
            },
            'data': {
                'title': 'Data',
                'description': 'The raw measurement data as an array of numbers.',
                'type': 'array',
                'items': {'type': 'number'},
            },
        },
        'required': ['version', 'type', 'hash_id', 'semantic_type', 'name', 'description', 'metric', 'rounds', 'data'],
        'additionalProperties': False,
    }

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption='JSON Schema for RawDataBlock V1',
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
            schema_dict = RawDataBlockSchema.as_dict()

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
            schema_json = RawDataBlockSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
