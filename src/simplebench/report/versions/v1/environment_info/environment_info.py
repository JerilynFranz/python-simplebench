"""Immutable GenericEnvironment implementation.

Immutable class representing a benchmark execution environment in a report (V1).

It provides methods to convert to and from dictionary representations and
enforces that all values are of core data mapping types.

It is a Mapping[str, CoreDataTypes] so it can be used as a read-only dictionary
with string keys and core data type values for convenience.

It is a generic environment representation without predefined properties
designed to allow importing and storing arbitrary environment data
that does not match other specific environment types.
"""

import hashlib
from collections.abc import Mapping, Iterator
from types import MappingProxyType
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report import base
from simplebench.report._error_tags import _EnvironmentInfoErrorTag
from simplebench.simplebench_types import CoreDataMapping, CoreDataTypes

from . import _validate
from .environment_info_schema import EnvironmentInfoSchema
from .typeddict_types import EnvironmentInfoData, ImmutableEnvironmentInfoDict

__all__: list[str] = ['EnvironmentInfo']


class EnvironmentInfo(Mapping[str, CoreDataTypes], base.BaseEnvironment):
    """Immutable class representing a benchmark execution environment in a report (V1).

    It provides methods to convert to and from dictionary representations and
    enforces that all values are of core data mapping types.

    It is a Mapping[str, CoreDataTypes] so it can be used as a read-only dictionary
    with string keys and core data type values for convenience.
    """

    SCHEMA: type[base.JSONSchema] = EnvironmentInfoSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON Environment type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON Environment version number."""

    ID: str = SCHEMA.ID
    """The JSON Environment identifier property value for version 1 reports."""

    _init_params_cache: MappingProxyType[str, Any] | None = None
    """Cache for the constructor parameters of the schema data class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(EnvironmentInfoData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = ('_hash_id', '_semantic_type', '_title', '_description', '_data', '_dict_cache')
    """The instance attributes for EnvironmentInfo."""

    def __init__(self,
                 data: Mapping[str, Any],
                 title: str,
                 description: str = '',
                 semantic_type: str = 'simplebench::generic',
                 hash_id: str = '') -> None:
        """Initialize an Environment instance.

        If a 'hash_id' key is present in the input data mapping, its value is validated
        and used as the hash_id property. If not present, the hash_id is computed from the
        rest of the data mapping.

        If 'type' or 'version' keys are not present in the input data mapping, they are
        automatically added with the appropriate values for this class.

        :param data: Keyword arguments representing environment properties.
        Each key-value pair corresponds to a property name and its value.
        The values must be of core data types.
        :type data: Mapping[str, Any]
        :param title: A human-readable title for this environment.
        :type title: str
        :param description: A human-readable description for this environment.
        :type description: str
        :param semantic_type: The semantic type of the environment, formatted as 'namespace::type_name'.
            This dictates how the data should be interpreted. Users can define custom types using their own namespace.
        :type semantic_type: str
        :param hash_id: The hash ID of the environment, a 64-character hexadecimal string.
        :type hash_id: str
        """
        if not isinstance(data, Mapping):
            raise SimpleBenchTypeError('data must be a mapping type', tag=_EnvironmentInfoErrorTag.INVALID_DATA_TYPE)

        self._title: str = _validate.title(title)
        self._description: str = _validate.description(description)
        self._semantic_type: str = _validate.semantic_type(semantic_type)
        self._data: CoreDataMapping = _validate.data_as_core_data_mapping(data, 'data')
        self._hash_id: str = _validate.hash_id(hash_id) or self._generate_hash_id()
        self._dict_cache: ImmutableEnvironmentInfoDict = self._generate_dict()

    def _generate_hash_id(self) -> str:
        """Helper method to compute the hash_id property from the data mapping.

        :return: The hash_id string.
        """
        hash_items: list[str] = [
            f'type:{self.TYPE}',
            f'version:{self.VERSION}',
            f'semantic_type:{self._semantic_type}',
            f'title:{self._title}',
            f'description:{self._description}',
            f'data:{self._data.hash_id()}'
        ]

        hash_input = b'\x00'.join(value.encode('utf-8') for value in hash_items)
        return hashlib.sha256(hash_input).hexdigest()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'EnvironmentInfo':
        """Create an Environment instance from a dictionary.

        Because the data has no predefined structure, this method just
        passes the input data to the constructor.

        .. code-block:: python3
           :caption: Example

            environment = Environment.from_dict(data)

        :param data: The dictionary containing the Environment data.
        :return: An Environment instance.
        """
        if not isinstance(data, Mapping):
            raise SimpleBenchTypeError('data must be a mapping type',
                                       tag=_EnvironmentInfoErrorTag.INVALID_DATA_TYPE)

        allowed_keys = {'type', 'version', 'hash_id', 'semantic_type', 'title', 'description', 'data'}
        extra_keys = set(data.keys()) - allowed_keys
        if extra_keys:
            raise SimpleBenchValueError(
                f'Unexpected keys in input data: {extra_keys}',
                tag=_EnvironmentInfoErrorTag.INVALID_DATA_TYPE)

        if 'title' not in data:
            raise SimpleBenchTypeError('title is a required property for Environment',
                                       tag=_EnvironmentInfoErrorTag.INVALID_TITLE_VALUE)
        data_copy = dict(data)
        title = data_copy.pop('title')
        type_value = data_copy.pop('type', None)
        # Optional, but must match if present
        if type_value is not None and type_value != cls.TYPE:
            raise SimpleBenchTypeError(
                f'Invalid type value: {type_value}',
                tag=_EnvironmentInfoErrorTag.INVALID_TYPE_VALUE)
        # Optional, but must match if present
        version_value = data_copy.pop('version', None)
        if version_value is not None and version_value != cls.VERSION:
            raise SimpleBenchTypeError(
                f'Invalid version value: {version_value}',
                tag=_EnvironmentInfoErrorTag.INVALID_VERSION_VALUE)
        description = data_copy.pop('description', '')
        semantic_type = data_copy.pop('semantic_type', 'simplebench::generic')
        hash_id = data_copy.pop('hash_id', '')
        if 'data' not in data_copy or not isinstance(data_copy['data'], Mapping):
            raise SimpleBenchTypeError(
                'data must be a mapping type and is required',
                tag=_EnvironmentInfoErrorTag.INVALID_DATA_TYPE)

        return cls(data=data_copy['data'],
                   title=title,
                   description=description,
                   semantic_type=semantic_type,
                   hash_id=hash_id)

    def to_dict(self) -> ImmutableEnvironmentInfoDict:
        """The EnvironmentInfo as an immutable dictionary.

        :return ImmutableEnvironmentInfoDict: A dictionary representation of the EnvironmentInfo.
        """
        return self._dict_cache

    def _generate_dict(self) -> ImmutableEnvironmentInfoDict:
        """Returns the Environment as an immutable dictionary suitable for JSON serialization.

        The returned instance is of type :class:`CoreDataMapping` to ensure immutability
        and will always reflect the state of the instance at the time of the first call.

        The exact same instance is returned on subsequent calls to ensure consistency
        and this is true even in multi-threaded scenarios.

        :return ImmutableEnvironmentInfoDict: A dictionary representation of the Environment.
        """
        return CoreDataMapping({
            'type': self.TYPE,
            'version': self.VERSION,
            'hash_id': self.hash_id,
            'semantic_type': self.semantic_type,
            'title': self.title,
            'description': self.description,
            'data': self.data})  # type: ignore[return-value]

    def for_json(self) -> ImmutableEnvironmentInfoDict:
        """Get the JSON-serializable dictionary representation of this EnvironmentInfo.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this EnvironmentInfo.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this EnvironmentInfo.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this EnvironmentInfo.
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        :raises SimpleBenchAttributeError: If any required property is missing.
        """
        return self._hash_id

    @property
    def semantic_type(self) -> str:
        """Get the semantic_type property.

        :return: The semantic_type string.
        :raises SimpleBenchAttributeError: If any required property is missing.
        """
        return self._semantic_type

    @property
    def title(self) -> str:
        """Get the title property.

        :return: The title string.
        :raises SimpleBenchAttributeError: If any required property is missing.
        """
        return self._title

    @property
    def description(self) -> str:
        """Get the description property.

        :return: The description string.
        :raises SimpleBenchAttributeError: If any required property is missing.
        """
        return self._description

    @property
    def data(self) -> CoreDataMapping:
        """Get the data property.

        :return: The data mapping.
        :raises SimpleBenchAttributeError: If any required property is missing.
        """
        return self._data

    def __getitem__(self, key: str) -> CoreDataTypes:
        return self.data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, key: object) -> bool:
        return key in self.data

    def __repr__(self) -> str:
        """Get the string representation of the EnvironmentInfo instance.

        :return: The string representation of the EnvironmentInfo.
        """
        # Get the init parameters excluding 'type', 'version' since they are fixed for this class
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EnvironmentInfo):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        return hash(self.hash_id)

    def __copy__(self) -> 'EnvironmentInfo':
        """Return a copy of this EnvironmentInfo instance.

        Since the class is immutable, this method just returns self.

        :return: The same instance of EnvironmentInfo.
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'EnvironmentInfo':
        """Return a deep copy of this EnvironmentInfo instance.

        Since the class is immutable, this method just returns self.

        :param memo: The memoization dictionary for deepcopy.
        :return: The same instance of EnvironmentInfo.
        """
        return self
