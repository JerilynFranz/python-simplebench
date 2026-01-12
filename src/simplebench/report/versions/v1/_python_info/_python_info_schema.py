"""Schema for JSON PythonInfo v1 validation."""
# ruff: noqa: E501

from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report.base import JSONSchema


class PythonInfoSchema(JSONSchema):
    """Schema for the JSON PythonInfo output (V1)"""

    VERSION: int = 1
    """The JSON PythonInfo schema version number."""

    TYPE: str = 'SimpleBenchPythonInfo::V1'
    """The JSON PythonInfo schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/python-info.json'
    """The JSON PythonInfo schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Python Info (V1)',
        'type': 'object',
        'description': 'Python interpreter information (V1)',
        'properties': {
            'version': {
                'title': 'Version',
                'description': 'JSON schema version number.',
                'type': 'integer',
                'const': VERSION,
            },
            'type': {
                'title': 'Type',
                'description': 'JSON schema type property value for version 1 reports.',
                'type': 'string',
                'const': TYPE,
            },
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the python-info data.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'python_version': {
                'title': 'Python Version',
                'description': 'Python version',
                'type': 'string',
                'pattern': r'^\S.*$',
            },
            'implementation': {
                'title': 'Python Implementation',
                'description': 'Python implementation',
                'type': 'string',
                'pattern': r'^\S.*$',
            },
            'implementation_version': {
                'title': 'Python Implementation Version',
                'description': 'Version of the Python implementation',
                'type': 'string',
            },
            'compiler': {'title': 'Python Compiler', 'description': 'Python compiler information', 'type': 'string'},
            'revision': {
                'title': 'Python Revision',
                'description': 'Python source code revision identifier',
                'type': 'string',
            },
            'buildno': {'title': 'Python Build Number', 'description': 'Python build number', 'type': 'string'},
            'builddate': {'title': 'Python Build Date', 'description': 'Python build date', 'type': 'string'},
            'command_line_flags': {
                'title': 'Command Line Flags',
                'description': 'Command line flags used to start Python',
                'type': 'string',
            },
            'environment_variables': {
                'title': 'Environment Variables',
                'description': 'Python-specific environment variables',
                'type': 'object',
                'additionalProperties': {'type': 'string'},
            },
            'gc_is_enabled': {
                'title': 'Garbage Collector Is Enabled',
                'description': 'Whether the garbage collector is enabled',
                'type': 'boolean',
            },
            'gc_thresholds': {
                'title': 'Garbage Collection Thresholds',
                'description': 'Garbage collection thresholds',
                'type': 'array',
                'items': {'type': 'integer'},
                'minItems': 3,
                'maxItems': 3,
            },
            'thread_switch_interval': {
                'title': 'Thread Switch Interval',
                'description': 'Thread switch interval in seconds',
                'type': 'number',
            },
            'architecture_bits': {
                'title': 'Architecture Bits',
                'description': "Architecture bits (e.g., '32bit', '64bit')",
                'type': 'string',
            },
            'architecture_linkage': {
                'title': 'Architecture Linkage',
                'description': "Architecture linkage (e.g., 'ELF', 'WindowsPE')",
                'type': 'string',
            },
        },
        'required': [
            'version',
            'type',
            'hash_id',
            'python_version',
            'implementation',
            'implementation_version',
            'compiler',
            'revision',
            'buildno',
            'builddate',
            'command_line_flags',
            'environment_variables',
            'gc_is_enabled',
            'gc_thresholds',
            'thread_switch_interval',
            'architecture_bits',
            'architecture_linkage',
        ],
        'additionalProperties': False,
    }

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

        The caller can modify the returned dictionary as needed or cache it for performance.

        Usage:
            schema_dict = PythonInfoSchema.as_dict()

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
            schema_json = PythonInfoSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
