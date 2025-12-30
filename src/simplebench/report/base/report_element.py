"""ReportElement base class.

This class represents a report element in a report that can be serialized.

It implements validation and serialization/deserialization methods to and from dictionaries
for a JSON Schema version.
"""
from abc import ABC
from typing import Any, Mapping

from simplebench.base import Hydrator
from simplebench.report.base.report_element_typed_dict import ReportElementTypedDict
from simplebench.validators import validate_core_data_mapping

from .json_schema import JSONSchema


class ReportElement(Hydrator, ABC):
    """abstract class representing a report element in a report."""

    VERSION: int = 0
    """The report element version number.

    It must be overridden in subclasses to specify the correct version.
    """

    TYPE: str = ""
    """The report element type property value.

    It must be overridden in subclasses to specify the correct type.
    """

    ID: str = ""
    """The report element $id property value.

    It must be overridden in subclasses to specify the correct $id.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class used to validate the report element class.

    It must be overridden in subclasses to specify the correct schema class.
    """
    def __init__(self) -> None:
        """Abstract base __init__ method for all report element classes."""
        raise NotImplementedError(
            "__init__ is an abstract method and must be implemented by a subclass."
        )

    def _to_dict_helper(self) -> ReportElementDictType:
        """Helper method to convert a mapping to a ReportElementDictType.
        :param Mapping[str, Any] data: The input mapping to convert.
        :param ReportElementDictType cls: The target ReportElementDictType class.
        :return: The converted ReportElementDictType.
        :rtype: ReportElementDictType
        """
        property_keys = self.init_params(self.dict_type).keys()
        data: dict[str, Any] = {}
        # This loop handles calling to_dict on any properties that
        # themselves have a to_dict method. This ensures nested objects,
        # known or unknown, are properly serialized in the future as needed.
        for key in property_keys:
            if key in {'type', 'version'}:
                continue
            value = getattr(self, key)
            to_dict_fn = getattr(value, "to_dict", None)
            data[key] = to_dict_fn() if callable(to_dict_fn) else value
        data['type'] = StatsBlock.TYPE
        data['version'] = StatsBlock.VERSION

        # We control the data structure here, so this cast is safe
        self._to_dict_cache = cast(StatsBlockDict,
            validate_core_data_mapping(data, 'StatsBlock.to_dict output'))
        return self._to_dict_cache