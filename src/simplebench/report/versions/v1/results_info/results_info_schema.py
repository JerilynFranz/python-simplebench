"""Schema for JSON ResultsInfo v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema

__all__: list[str] = []


class ResultsInfoSchema(JSONSchema):
    """Schema for the JSON ResultsInfo output (V1)"""

    VERSION: int = 1
    """The JSON ResultsInfo schema version number."""

    TYPE: str = 'SimpleBenchResultsInfo::V1'
    """The JSON ResultsInfo schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/results-info.json'
    """The JSON ResultsInfo schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Results Schema (V1)',
        'description': 'SimpleBench JSON Results Schema (V1)',
        'type': 'object',
        'properties': {
            'version': {
                'title': 'Version',
                'description': 'Version of the schema',
                'type': 'integer',
                'const': VERSION,
            },
            'type': {'title': 'Type', 'description': 'Type of the result', 'type': 'string', 'const': TYPE},
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the results-info data. This can be used to identify identical Python interpreter configurations without revealing details.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'group': {'title': 'Group', 'description': 'Group of the result', 'type': 'string'},
            'title': {'title': 'Title', 'description': 'Title of the result', 'type': 'string'},
            'description': {'title': 'Description', 'description': 'Description of the result', 'type': 'string'},
            'n': {'title': 'N', 'description': 'Complexity analysis N value for the result', 'type': 'number'},
            'variation_marks': {
                'title': 'Variation Marks',
                'description': 'Variation marks for the result. Variation marks identify the kwargs combination used for a specific benchmark result',
                'type': 'object',
                'additionalProperties': {'type': 'string'},
            },
            'metrics': {'$ref': '#/$defs/metrics'},
            'extra_info': {
                'title': 'Extra Info',
                'description': 'A free-form object for third-party extensions or extra data.',
                'type': 'object',
                'additionalProperties': True,
            },
        },
        'required': [
            'type',
            'version',
            'hash_id',
            'group',
            'title',
            'description',
            'n',
            'variation_marks',
            'metrics',
            'extra_info',
        ],
        'additionalProperties': False,
        '$defs': {
            'metrics': {
                'type': 'object',
                'title': 'Metrics',
                'description': 'A collection of metric blocks, indexed by a unique, namespaced metric ID.\n\nExamples of valid keys:\n- `simplebench_std::time_per_operation`\n- `simplebench_std::operations_per_second`\n- `simplebench_std::memory_usage`\n- `simplebench_std::peak_memory_usage`\n- `simplebench_std::wallclock_time`\n- `my_plugin::custom_metric`',
                'patternProperties': {
                    '^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$': {
                        '$ref': '#/$defs/metric_block'
                    }
                },
                'additionalProperties': False,
            },
            'metric_block': {
                'title': 'Metric Block',
                'description': 'A container for a measurement, which can be a single value, a statistical summary, or raw data.',
                'oneOf': [{'$ref': 'stats-block.json'}, {'$ref': 'value-block.json'}, {'$ref': 'raw-data-block.json'}],
                'discriminator': {'propertyName': 'type'},
            },
        },
    }

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption='JSON Schema for ResultsInfo V1',
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
            schema_dict = ResultsInfoSchema.as_dict()
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
            schema_json = ResultsInfoSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
