"""Schema for JSON MetricType v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema


class MetricTypeSchema(JSONSchema):
    """Schema for the JSON MetricType output (V1)"""

    VERSION: int = 1
    """The JSON MetricType schema version number."""

    TYPE: str = 'SimpleBenchMetricType::V1'
    """The JSON MetricType schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/metric-type.json'
    """The JSON MetricType schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Metric Type (V1)',
        'description': 'Metric Type information (V1)',
        'type': 'object',
        'properties': {
            'version': {
                'description': 'The version of the Metric Type schema',
                'type': 'integer',
                'const': VERSION,
            },
            'type': {
                'title': 'Type',
                'description': 'Type of the Metric Type schema',
                'type': 'string',
                'const': TYPE,
            },
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the Metric Type data. This can be used to identify the generator and uniqueness of the data.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'semantic_type': {
                'title': 'Semantic Type',
                'description': "The semantic type of the metric, formatted as 'namespace::type_name'. This dictates how the data should be interpreted. Standard types use the 'simplebench_std' namespace. Users can define custom types using their own namespace.",
                'type': 'string',
                'pattern': '^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$',
            },
            'label': {
                'title': 'Label',
                'description': 'A human-readable label for the metric',
                'type': 'string',
                'minLength': 1,
            },
            'description': {
                'title': 'Description',
                'description': 'A brief description of the metric',
                'type': 'string',
                'minLength': 1,
            },
            'category': {
                'title': 'Category',
                'description': 'The category of the metric, one of VALUE, STATS, or RAW_DATA',
                'type': 'string',
                'enum': ['VALUE', 'STATS', 'RAW_DATA'],
            },
            'unit': {
                'title': 'Measurement Unit',
                'description': 'Unit of the measurement values',
                'type': 'string',
                'minLength': 1,
            },
            'scale': {
                'title': 'Measurement Scale',
                'description': 'Scale of the measurement values',
                'type': 'number',
                'exclusiveMinimum': 0,
            },
        },
        'required': ['hash_id', 'type', 'version', 'description', 'label', 'unit', 'scale', 'semantic_type', 'category'],
        'additionalProperties': False,
    }
    """The JSON schema as a dictionary."""

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption='JSON Schema for MetricType V1',
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
            schema_dict = MetricTypeSchema.as_dict()

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
            schema_json = MetricTypeSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
