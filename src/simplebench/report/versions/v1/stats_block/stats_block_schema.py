"""Schema for JSON StatsBlock v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema

__all__: list[str] = []


class StatsBlockSchema(JSONSchema):
    """Schema for the JSON StatsBlock output (V1)"""

    VERSION: int = 1
    """The JSON StatsBlock schema version number."""

    TYPE: str = 'SimpleBenchStatsBlock::V1'
    """The JSON StatsBlock schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json'
    """The JSON StatsBlock schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Statistics Block (V1)',
        'description': 'Block containing statistical measurements',
        'type': 'object',
        'properties': {
            'type': {
                'title': 'Block Type',
                'description': "The type of the block. Must be 'SimpleBenchStatsBlock::V1' for Statistics Block version 1.",
                'type': 'string',
                'const': TYPE,
            },
            'version': {
                'title': 'Schema Version',
                'description': 'The version of the schema. Must be 1 for Statistics Block version 1.',
                'type': 'integer',
                'const': VERSION,
            },
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the stats-block data. This can be used to identify identical Python interpreter configurations without revealing details.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'metric': {
                'title': 'Metric Reference',
                'description': 'Reference to a Metric by hash_id.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'iterations': {
                'title': 'Number of Iterations',
                'description': "Number of measured iterations.",
                'type': 'integer',
                'exclusiveMinimum': 0,
            },
            'rounds': {
                'title': 'Number of Rounds',
                'description': 'Number of rounds executed for each iteration. The total number of operations is iterations * rounds.',
                'type': 'integer',
                'exclusiveMinimum': 0,
            },
            'mean': {'title': 'Mean', 'description': 'The mean of the per-iteration measurements.', 'type': 'number'},
            'median': {
                'title': 'Median',
                'description': 'The median of the per-iteration measurements.',
                'type': 'number',
            },
            'minimum': {
                'title': 'Minimum',
                'description': 'The minimum value of the per-iteration measurements.',
                'type': 'number',
            },
            'maximum': {
                'title': 'Maximum',
                'description': 'The maximum value of the per-iteration measurements.',
                'type': 'number',
            },
            'stdev': {
                'title': 'Standard Deviation',
                'description': 'The standard deviation of a single underlying operation (round). If rounds > 1, this value is scaled from the standard deviation of the iterations to counter the effect of averaging. null is used if the standard deviation cannot be calculated (e.g., if iterations < 2).   This is not the standard deviation of the per-iteration measurements, but rather an estimate of the variability of a single round, which is more useful for understanding the stability of the measurements and for comparing across benchmarks with different numbers of rounds.',
                'type': ['number', 'null'],
            },
            'relative_stdev': {
                'title': 'Relative Standard Deviation',
                'description': 'The relative standard deviation (coefficient of variation), based on the scaled standard deviation of a single round. It is calculated as stdev / mean. This is a unitless measure of variability relative to the mean, which allows for comparison of stability across benchmarks with different scales. null is used if the relative standard deviation cannot be calculated (e.g., if mean is 0 or stdev is null).',
                'type': ['number', 'null'],
            },
            'drift_index': {
                'title': 'Drift Index',
                'description': 'Pearson correlation between measurement values and their sequential position indices. Range [-1.0, 1.0]. 0.0 indicates no monotonic trend. Positive values indicate measurements increasing over iterations; negative values indicate measurements settling. Does not detect periodic patterns; see autocorrelation for that. null is used if the drift index cannot be calculated (e.g., if iterations < 2).',
                'type': ['number', 'null'],
                'minimum': -1.0,
                'maximum': 1.0,
            },
            'autocorrelation': {
                'title': 'Lag-1 Autocorrelation',
                'description': 'Pearson lag-1 autocorrelation of the measurement sequence. Range [-1.0, 1.0]. Near 0.0 indicates independent samples (ideal). Strong positive values indicate slow-moving environmental effects. Strong negative values indicate alternating fast/slow patterns. null is used if the autocorrelation cannot be calculated (e.g., if iterations < 2).',
                'type': ['number', 'null'],
                'minimum': -1.0,
                'maximum': 1.0,
            },
            'percentiles': {
                'title': 'Percentiles',
                'description': 'Percentiles of the per-iteration measurements.',
                'type': 'array',
                'items': {'type': 'number'},
                'minItems': 101,
                'maxItems': 101,
            },
        },
        'required': [
            'type',
            'version',
            'hash_id',
            'iterations',
            'rounds',
            'mean',
            'median',
            'minimum',
            'maximum',
            'stdev',
            'relative_stdev',
            'drift_index',
            'autocorrelation',
            'percentiles',
        ],
        'additionalProperties': False,
    }

    _JSON_SCHEMA_TEXT: str = JSONEncoder(indent=2).encode(_JSON_SCHEMA_DICT)
    """The JSON schema as a pretty-printed JSON string."""

    _JSON_SCHEMA_NOTE: str = format_json_for_docstring(
        json_data=_JSON_SCHEMA_TEXT,
        caption='JSON Schema for StatsBlock V1',
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
            schema_dict = StatsBlockSchema.as_dict()

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
            schema_json = StatsBlockSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
