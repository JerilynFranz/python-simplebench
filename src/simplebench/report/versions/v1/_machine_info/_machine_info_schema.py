"""Schema for JSON MachineInfo v1 validation."""

# pylint: disable=line-too-long
from copy import deepcopy
from json import JSONEncoder

from simplebench.doc_utils import format_docstring, format_json_for_docstring
from simplebench.report._base import JSONSchema


class MachineInfoSchema(JSONSchema):
    """Schema for the JSON MachineInfo output (V1)"""

    VERSION: int = 1
    """The JSON MachineInfo schema version number."""

    TYPE: str = 'SimpleBenchMachineInfo::V1'
    """The JSON MachineInfo schema type property value for version 1 reports."""

    ID: str = 'https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/machine-info.json'
    """The JSON MachineInfo schema $id value for version 1 reports."""

    _JSON_SCHEMA_DICT: dict[str, object] = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': ID,
        'title': 'Machine Info (V1)',
        'description': 'Machine information (V1)',
        'type': 'object',
        'properties': {
            'version': {
                'title': 'Version',
                'description': 'Version of the machine information schema',
                'type': 'integer',
                'const': VERSION,
            },
            'type': {
                'title': 'Type',
                'description': 'Type of the machine information',
                'type': 'string',
                'const': TYPE,
            },
            'hash_id': {
                'title': 'Hash ID',
                'description': 'Unique 64 byte hexadecimal hash identifier for the machine information data. This can be used to identify identical machine configurations without revealing details.',
                'type': 'string',
                'pattern': '^[a-f0-9]{64}$',
            },
            'node': {
                'title': 'Node',
                'description': 'Identifier for the machine (blank by default)',
                'type': 'string',
                'default': '',
            },
            'execution_environment': {
                'title': 'Execution Environment',
                'description': 'Information about the execution environment(s) or runtime(s).',
                'type': 'object',
                'properties': {'python': {'$ref': 'python-info.json'}},
                # By design this is open-ended to allow for future extensions for other
                # execution environments without breaking the schema. Thus, additionalProperties is True
                # and there is no required list. 'python' is a pre-defined property,
                # but others may be added later.
                # It requires at least one property to be present (the 'python' property or any future ones).
                'additionalProperties': True,
                'minProperties': 1,
            },
            'cpu': {'$ref': 'cpu-info.json'},
            'memory': {'$ref': 'memory-info.json'},
            'system': {'$ref': 'system-info.json'},
        },
        'required': ['version', 'type', 'hash_id', 'node', 'execution_environment', 'cpu', 'memory', 'system'],
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
            schema_dict = MachineInfoSchema.as_dict()
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
            schema_json = MachineInfoSchema.as_json()

        :return str: The JSON schema as a JSON-formatted string.

        {JSON_SCHEMA_NOTE}
        """
        return cls._JSON_SCHEMA_TEXT
