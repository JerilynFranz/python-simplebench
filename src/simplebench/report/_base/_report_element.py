"""ReportElement base class.

This class represents a report element in a report that can be serialized.

It implements validation and serialization/deserialization methods to and from dictionaries
for a JSON Schema version.
"""

import hashlib
from abc import ABC
from types import MappingProxyType
from typing import Any, Callable, TypeVar

from typechecked import Immutable

from simplebench.base._hydrator import Hydrator
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag, SimpleBenchAttributeError, SimpleBenchTypeError
from simplebench.report._base._report_element_typed_dict import ReportElementTypedDict
from simplebench.report.validate import report_element_typed_dict_mimic
from simplebench.types import IMMUTABLE_CORE_DATA_TYPES_TUPLE, ImmutableCoreDataMappingType
from simplebench.validators import is_immutable_core_data

from ._json_schema import JSONSchema

T = TypeVar('T', bound=ReportElementTypedDict)

__all__ = []


class _NoMatch:
    """Class representing no match found in instance for report element attribute lookup."""


_NO_MATCH = _NoMatch()
"""Sentinel value indicating no match found in instance for report element attribute lookup."""


@enum_docstrings
class _ReportElementErrorTag(ErrorTag):
    """Error tags for ReportElement errors."""

    INVALID_REPORT_ELEMENT_TO_DICT_METHOD_NONCALLABLE = 'INVALID_REPORT_ELEMENT_TO_DICT_METHOD_NONCALLABLE'
    """The to_dict method of a ReportElement attribute is not callable."""

    INVALID_REPORT_ELEMENT_ATTRIBUTE_MISSING = 'INVALID_REPORT_ELEMENT_ATTRIBUTE_MISSING'
    """A required attribute is missing from a ReportElement instance."""


class ReportElement(Hydrator, Immutable, ABC):
    """abstract class representing a report element in a report."""

    VERSION: int = 0
    """The report element version number.

    It must be overridden in subclasses to specify the correct version.
    """

    TYPE: str = ''
    """The report element type property value.

    It must be overridden in subclasses to specify the correct type.
    """

    ID: str = ''
    """The report element $id property value.

    It must be overridden in subclasses to specify the correct $id.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class used to validate the report element class.

    It must be overridden in subclasses to specify the correct schema class.
    """

    def __init__(self) -> None:
        """Abstract base __init__ method for all report element classes."""
        raise NotImplementedError('__init__ is an abstract method and must be implemented by a subclass.')

    def _to_dict_helper(self, dict_type: type[T]) -> T:
        """Helper method to convert a mapping to a ReportElementDictType.

        It iterates over the properties defined in the ReportElement's
        dict_type and constructs an immutable mapping representation
        that is type cast to the requested ReportElementDictType subclass for output.

        :param Mapping[str, Any] data: The input mapping to convert.
        :param ReportElementDictType cls: The target ReportElementDictType class.
        :return ReportElementTypedDict: An immutable mapping representing the report element
            that is type cast to the requested ReportElementTypedDict subclass.
        :raises SimpleBenchTypeError: If any attribute cannot be converted to a dictionary.
        """
        property_keys = self.init_params(dict_type).keys()
        data: dict[str, Any] = {}

        # This loop handles calling to_dict on any properties that
        # themselves have a to_dict method. This ensures nested objects,
        # known or unknown, are properly serialized in the future as needed.
        cls = self.__class__
        for key in property_keys:
            if key == '__immutable__':  # class variable for typechecked.ImmutableTypedDict
                continue
            match key:
                case 'type':
                    data['type'] = cls.TYPE
                    continue

                case 'version':
                    data['version'] = cls.VERSION
                    continue

            value: Callable[[], ImmutableCoreDataMappingType] | ImmutableCoreDataMappingType | _NoMatch = getattr(
                self, key, _NO_MATCH
            )
            to_dict_fn: Callable[[], ImmutableCoreDataMappingType] | None = getattr(value, 'to_dict', None)

            # Attribute doesn't exist on instance
            if isinstance(value, _NoMatch):
                raise SimpleBenchAttributeError(
                    f"ReportElement subclass {cls.__name__} is missing expected attribute '{key}'",
                    tag=_ReportElementErrorTag.INVALID_REPORT_ELEMENT_ATTRIBUTE_MISSING,
                )

            # Already an ImmutableCoreDataMappingType
            elif is_immutable_core_data(value):
                data[key] = value

            # Has a callable to_dict method
            elif callable(to_dict_fn):
                data[key] = to_dict_fn()

            # Invalid type for to_dict conversion
            else:
                raise SimpleBenchTypeError(
                    f"Attribute '{key}' of {cls.__name__} class "
                    f'is of type {type(value).__name__}, does not have a callable to_dict method, '
                    'and is not an ImmutableCoreDataMappingType. It cannot be converted to a dictionary.',
                    tag=_ReportElementErrorTag.INVALID_REPORT_ELEMENT_TO_DICT_METHOD_NONCALLABLE,
                )

        for key, value in data.items():
            if isinstance(value, IMMUTABLE_CORE_DATA_TYPES_TUPLE):
                continue
            raise SimpleBenchTypeError(
                f"ReportElement._to_dict_helper produced invalid data for key '{key}': "
                f'value of type {type(value).__name__} is not a core data primitive or an immutable mapping.',
                tag=_ReportElementErrorTag.INVALID_REPORT_ELEMENT_TO_DICT_METHOD_NONCALLABLE,
            )

        # Return validated immutable mapping that mimics the requested ReportElementTypedDict subclass
        return report_element_typed_dict_mimic(MappingProxyType(data), dict_type)

    def _hash_id_helper(self, cls_type: type) -> str:
        """Helper method to compute the hash_id property for ReportElement subclasses.

        It guides the computation of the hash_id property by iterating over the
        __init__ parameters defined in the passed cls_type and constructing a
        hash input string based on the parameter names and their corresponding
        values in the instance. Special handling is provided for attributes that
        are themselves ReportElement subclasses, using their hash_id values in the
        computation.

        :param cls_type: The TypedDict class whose __init__ parameters guide the hash_id computation.
        :return: The hash_id string.
        """
        param_keys: set[str] = set(self.init_params(cls_type).keys()) - {'type', 'version', 'hash_id', '__immutable__'}
        hash_items: list[str] = []
        for key in param_keys:
            if not hasattr(self, key):
                raise SimpleBenchAttributeError(
                    f"Missing required property '{key}'",
                    tag=_ReportElementErrorTag.INVALID_REPORT_ELEMENT_ATTRIBUTE_MISSING,
                )
            value = getattr(self, key)

            # Special handling for 'hash_id' property for ReportElement sub-objects
            # Their hash_id must be computed first to ensure consistent hashing
            # and used in place of the full object representation in the parent object's hash_id.
            # Because of caching, this will not recompute the sub-object's hash_id if already computed.
            if isinstance(value, ReportElement):
                value_hash_id = getattr(value, 'hash_id', _NO_MATCH)
                if value_hash_id is _NO_MATCH:
                    raise SimpleBenchAttributeError(
                        f"Missing required 'hash_id' property on sub-object for attribute '{key}' "
                        f'or its class {value.__class__.__name__}',
                        tag=_ReportElementErrorTag.INVALID_REPORT_ELEMENT_ATTRIBUTE_MISSING,
                    )
                hash_items.append(f'{key}:{value_hash_id}')
            else:
                hash_items.append(f'{key}:{value}')

        cls = self.__class__
        if hasattr(cls, 'TYPE'):
            hash_items.append(f'type:{cls.TYPE}')
        if hasattr(cls, 'VERSION'):
            hash_items.append(f'version:{cls.VERSION}')
        hash_items.sort()
        hash_input = '\x00'.join(hash_items).encode('utf-8')

        return hashlib.sha256(hash_input).hexdigest()
