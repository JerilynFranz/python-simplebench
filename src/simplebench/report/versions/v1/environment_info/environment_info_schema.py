"""Schema for JSON Environment v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema


class EnvironmentInfoSchema(JSONSchema):
    """Schema for the JSON Environment output (V1)"""

    VERSION: int = 1
    """The JSON Environment schema version number."""

    TYPE: str = 'SimpleBenchEnvironment::V1'
    """The JSON Environment schema type property value for version 1 reports."""

    ID: str = (
        'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/environment-info.json'
    )
    """The JSON Environment schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Environment (V1)',
        'description': 'Environment information (V1)',
        'type': 'object',
        'properties': {
            'version': {
                'description': 'The version of the Environment schema',
                'type': 'integer',
                'const': VERSION,
            },
            'type': {
                'title': 'Type',
                'description': 'Type of the Environment schema',
                'type': 'string',
                'const': TYPE,
            },
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the Environment data. This can be used to identify the generator and uniqueness of the data.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'semantic_type': {
                'title': 'Semantic Type',
                'description': "The semantic type of the environment, formatted as 'namespace::type_name'. This dictates how the data should be interpreted. Users can define custom types using their own namespace.",
                'type': 'string',
                'pattern': '^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$',
                'default': 'simplebench::generic',
                'examples': [
                    'simplebench::python',
                ],
            },
            'title': {
                'title': 'Title',
                'description': 'A human-readable title for this environment.',
                'type': 'string',
                'pattern': r'^\S.*$',  # Non-empty string that does not start with whitespace
            },
            'description': {
                'title': 'Description',
                'description': 'A human-readable description for this environment.',
                'type': 'string',
                'default': '',
            },
            'data': {
                'description': 'The raw Environment data collected from the system.',
                'type': 'object',
                'title': 'Environment data',
                'propertyNames': {'pattern': r'^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$'},
                'additionalProperties': {
                    'oneOf': [
                        {'$ref': '#/$defs/data'},
                        {'type': ['string', 'number', 'boolean', 'null', 'array']},
                    ]
                }
            }
        },
        'required': ['hash_id', 'type', 'version', 'semantic_type', 'title', 'data'],
        'additionalProperties': False,
        '$defs': {
            'data': {
                'type': 'object',
                'title': 'Environment data element',
                'propertyNames': {'pattern': r'^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$'},
                'additionalProperties': {
                    'oneOf': [
                        {'$ref': '#/$defs/data'},
                        {'type': ['string', 'number', 'boolean', 'null', 'array']},
                    ]
                },
            },
        }
    }
    """The JSON schema as a dictionary."""

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption='JSON Schema for Environment V1',
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
            schema_dict = EnvironmentInfoSchema.as_dict()

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
            schema_json = EnvironmentInfoSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
