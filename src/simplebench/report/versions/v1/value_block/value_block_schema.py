"""Schema for JSON ValueBlock v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

# pylint: disable=line-too-long
from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema

__all__: list[str] = []


class ValueBlockSchema(JSONSchema):
    """Schema for the JSON ValueBlock output (V1)"""

    VERSION: int = 1
    """The JSON ValueBlock schema version number."""

    TYPE: str = 'SimpleBenchValueBlock::V1'
    """The JSON ValueBlock schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/value-block.json'
    """The JSON ValueBlock schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Value Block (V1)',
        'description': 'Block containing a single value measurement.',
        'type': 'object',
        'properties': {
            'version': {
                'title': 'Schema Version',
                'description': f"Version of the schema. Must be '{VERSION}' for Value Block version 1.",
                'type': 'integer',
                'const': VERSION,
            },
            'type': {
                'title': 'Block Type',
                'description': f"The type of the block. Must be '{TYPE}' for Value Block version 1.",
                'type': 'string',
                'const': TYPE,
            },
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the value-block data.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'semantic_type': {
                'title': 'Measurement Type',
                'description': "The semantic type of the measurements, formatted as 'namespace::type_name'. This dictates how the data should be interpreted. Standard types use the 'simplebench_std' namespace. Users can define custom types using their own namespace.",
                'type': 'string',
                'pattern': '^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$',
                'examples': [
                    'simplebench_std::wallclock_time',
                    'simplebench_std::cpu_time',
                    'my_plugin::context_switches',
                ],
            },
            'timer_metric': {
                'title': 'Timer Metric',
                'description': "The timer metric associated with this measurement (e.g., 'PERF_COUNTER'). Should be included for any timing-related metrics.",
                'type': 'string',
            },
            'unit': {
                'title': 'Measurement Unit',
                'description': 'Unit of the measurement value',
                'type': 'string',
                'minLength': 1,
            },
            'scale': {
                'title': 'Measurement Scale',
                'description': 'Scale of the measurement value',
                'type': 'number',
                'exclusiveMinimum': 0,
            },
            'value': {'title': 'Value', 'description': 'The single measurement value.', 'type': 'number'},
        },
        'required': ['version', 'type', 'hash_id', 'semantic_type', 'unit', 'scale', 'value'],
        'additionalProperties': False,
    }
    """The JSON schema as a dictionary."""

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption='JSON Schema for ValueBlock V1',
        intro_text='The JSON schema is as follows:',
    )
    """Note containing the JSON schema for docstrings."""

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """Get the JSON schema as a dictionary.

        It always returns a fresh copy of the schema dictionary to prevent accidental
        modifications.

        Usage:
            schema_dict = ValueBlockSchema.as_dict()

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
            schema_json = ValueBlockSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
