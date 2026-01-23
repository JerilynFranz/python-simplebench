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

import base64
import hashlib
from collections.abc import Mapping, Sequence, Set
from types import MappingProxyType
from typing import Any, cast

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _GenericEnvironmentErrorTag
from simplebench.report.base import Environment, JSONSchema
from simplebench.simplebench_types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, CoreDataTypes, ImmutableCoreDataMappingType
from simplebench.validators import validate_core_data_mapping

from . import _validate
from .generic_environment_schema import GenericEnvironmentSchema

__all__ = []


class GenericEnvironment(Environment, Mapping[str, CoreDataTypes]):
    """Immutable class representing a benchmark execution environment in a report (V1).

    It provides methods to convert to and from dictionary representations and
    enforces that all values are of core data mapping types.

    It is a Mapping[str, CoreDataTypes] so it can be used as a read-only dictionary
    with string keys and core data type values for convenience.
    """

    SCHEMA: type[JSONSchema] = GenericEnvironmentSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON GenericEnvironment type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON GenericEnvironment version number."""

    ID: str = SCHEMA.ID
    """The JSON GenericEnvironment identifier property value for version 1 reports."""

    def __init__(self, data: Mapping[str, Any]) -> None:
        """Initialize a GenericEnvironment instance.

        If a 'hash_id' key is present in the input data mapping, its value is validated
        and used as the hash_id property. If not present, the hash_id is computed from the
        rest of the data mapping.

        If 'type' or 'version' keys are not present in the input data mapping, they are
        automatically added with the appropriate values for this class.

        :param data: Keyword arguments representing environment properties.
        Each key-value pair corresponds to a property name and its value.
        The values must be of core data types.
        """
        if not isinstance(data, Mapping):
            raise SimpleBenchTypeError('data must be a mapping type', tag=_GenericEnvironmentErrorTag.INVALID_DATA_TYPE)

        local_data = dict(data)  # Make a shallow local copy to avoid modifying the input

        self._hash_id: str = ''
        if 'hash_id' in local_data:
            self._hash_id = _validate.hash_id(local_data.pop('hash_id'))

        self._from_dict: ImmutableCoreDataMappingType = _validate.data_as_core_data_mapping(local_data, 'data')
        validated_data = validate_core_data_mapping(local_data, 'data', max_depth=5)
        thawed_data = dict(validated_data)  # Make a mutable copy for internal use
        self._hash_id = self._generate_hash_id(thawed_data) if self._hash_id == '' else self._hash_id
        thawed_data['hash_id'] = self._hash_id
        if 'type' not in thawed_data:
            thawed_data['type'] = self.TYPE
        if 'version' not in thawed_data:
            thawed_data['version'] = self.VERSION
        validated_data = cast(ImmutableCoreDataMappingType, MappingProxyType(thawed_data))  # Make immutable for storage
        self._from_dict: ImmutableCoreDataMappingType = validated_data

    def _generate_hash_id(self, data: Any) -> str:
        """Helper method to compute the hash_id property from the data mapping.

        :param data: The data mapping to compute the hash_id from.
        :return: The hash_id string.
        """
        hash_items: list[bytes] = []

        # Handle core data primitive types directly - strings, bytes, numbers, booleans, None,
        if isinstance(data, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
            encoded = base64.b64encode(str(data).encode('utf-8'))
            return hashlib.sha256(encoded).hexdigest()

        elif isinstance(data, Mapping):
            for key in sorted(data.keys()):
                value = data[key]
                if isinstance(value, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                    key_enc = base64.b64encode(str(key).encode('utf-8'))
                    val_enc = base64.b64encode(str(value).encode('utf-8'))
                    hash_items.append(key_enc + b':' + val_enc)

                elif isinstance(value, (Sequence, Mapping, Set)):
                    subhash = self._generate_hash_id(value)
                    key_enc = base64.b64encode(str(key).encode('utf-8'))
                    hash_items.append(key_enc + b':' + subhash.encode('utf-8'))

                else:
                    raise SimpleBenchTypeError(
                        f'Unsupported data type for hash_id generation: {type(value)}',
                        tag=_GenericEnvironmentErrorTag.INVALID_DATA_TYPE,
                    )

        elif isinstance(data, Set):
            sorted_data = data
            try:
                sorted_data = sorted(data)
            except TypeError:
                # If the set contains unorderable types, we fall back to unsorted processing
                pass
            for item in sorted_data:
                if isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                    item_enc = base64.b64encode(str(item).encode('utf-8'))
                    hash_items.append(item_enc)

                elif isinstance(item, (Sequence, Mapping, Set)):
                    subhash = self._generate_hash_id(item)
                    hash_items.append(subhash.encode('utf-8'))

                else:
                    raise SimpleBenchTypeError(
                        f'Unsupported data type for hash_id generation: {type(item)}',
                        tag=_GenericEnvironmentErrorTag.INVALID_DATA_TYPE,
                    )

        elif isinstance(data, Sequence) and not isinstance(data, (str, bytes, bytearray)):
            for item in data:
                if isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                    item_enc = base64.b64encode(str(item).encode('utf-8'))
                    hash_items.append(item_enc)

                elif isinstance(item, (Sequence, Mapping, Set)):
                    subhash = self._generate_hash_id(item)
                    hash_items.append(subhash.encode('utf-8'))

                else:
                    raise SimpleBenchTypeError(
                        f'Unsupported data type for hash_id generation: {type(item)}',
                        tag=_GenericEnvironmentErrorTag.INVALID_DATA_TYPE,
                    )
        else:
            raise SimpleBenchTypeError(
                f'Unsupported data type for hash_id generation: {type(data)}',
                tag=_GenericEnvironmentErrorTag.INVALID_DATA_TYPE,
            )

        hash_input = b'\x00'.join(hash_items)
        return hashlib.sha256(hash_input).hexdigest()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'GenericEnvironment':
        """Create a GenericEnvironment instance from a dictionary.

        Because the data has no predefined structure, this method just
        passes the input data to the constructor.

        .. code-block:: python3
           :caption: Example

            generic_environment = GenericEnvironment.from_dict(data)

        :param data: The dictionary containing the GenericEnvironment data.
        :return: A GenericEnvironment instance.
        """
        return cls(data)

    def to_dict(self) -> ImmutableCoreDataMappingType:
        """Returns the GenericEnvironment as an immutable MappingProxyType dictionary suitable for JSON serialization.

        The returned instance is of type :class:`MappingProxyType` to ensure immutability
        and will always reflect the state of the instance at the time of the first call.

        The exact same instance is returned on subsequent calls to ensure consistency
        and this is true even in multi-threaded scenarios.

        :return ImmutableCoreDataMappingType: A dictionary representation of the GenericEnvironment.
        """
        return self._from_dict

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        :raises SimpleBenchAttributeError: If any required property is missing.
        """
        return self._hash_id

    def __getitem__(self, key: str) -> CoreDataTypes:
        return self._from_dict[key]

    def __iter__(self) -> Any:
        return iter(self._from_dict)

    def __len__(self) -> int:
        return len(self._from_dict)

    def __contains__(self, key: object) -> bool:
        return key in self._from_dict

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self._from_dict)!r})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GenericEnvironment):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        return hash(self.hash_id)
