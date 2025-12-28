"""V1 ValueBlock representation.

This module provides the `ValueBlock` class, which represents a single named
value in a JSON report.

The `ValueBlock` class is immutable and implements validation and serialization
methods to and from dictionaries that conform to the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/value-block.json

As a V1 implementation, it serves as a frozen snapshot of the value block
representation, ensuring backward compatibility with future versions of the JSON
report schema.

An instance can be created in two ways:
1. By directly instantiating the `ValueBlock` class with the required parameters.
2. By using the `from_dict` class method to create an instance from a
   dictionary that matches the JSON schema.

The class also implements equality, hashing, and copy protocols to allow for
comparison, use in hash-based collections, and efficient copying.
"""
from copy import copy
from typing import Any

from simplebench.report.base import BaseValueBlock, JSONSchema
from simplebench.report.versions.v1.types import ValueBlockData, ValueBlockDict

from . import validate
from .value_block_schema import ValueBlockSchema


class ValueBlock(BaseValueBlock):
    """Class representing a value block (V1).

    :param str semantic_type: The semantic type string for the value block.
    :param (str | None) timer: The timer string or None.
    :param str unit: The unit of measurement.
    :param float scale: The scale factor.
    :param float | int value: The value of the block.
    :raise SimpleBenchTypeError: If any parameter is of incorrect type.
    :raise SimpleBenchValueError: If any parameter has an invalid value.
    """

    SCHEMA: type[JSONSchema] = ValueBlockSchema
    """JSON schema class for the value block."""

    VERSION: int = SCHEMA.VERSION
    """Version of the value block schema."""

    TYPE: str = SCHEMA.TYPE
    """Type of the value block schema."""

    ID: str = SCHEMA.ID
    """ID of the value block schema."""

    __slots__ = (
        '_semantic_type',
        '_timer',
        '_unit',
        '_scale',
        '_value',
    )

    def __init__(
            self,
            *,
            semantic_type: str,
            timer: str | None = None,
            unit: str,
            scale: float,
            value: float | int) -> None:
        """Initialize JSONStatsSummary base class.

        :param str semantic_type: The semantic type string for the value block. ('type' field in JSON data)
        :param (str | None) timer: The timer string or None.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
        :param float | int value: The value of the block.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """
        self._semantic_type: str = validate.semantic_type(semantic_type)
        self._timer: str | None = validate.timer(timer)
        self._unit: str = validate.unit(unit)
        self._scale: float = validate.scale(scale)
        self._value: float = validate.value(value)

    @classmethod
    def from_dict(cls, data: ValueBlockData) -> "ValueBlock":  # type: ignore[override]
        """Create a ValueBlock instance from a dictionary.

        The input dictionary must conform to the JSON schema for ValueBlock V1,
        with the exceptions that the `type` and `version` fields are optional;
        if omitted, they are assumed to be the V1 :attr:`ValueBlockSchema.TYPE` and
        :attr:`ValueBlockSchema.VERSION` constants.

        :param ValueBlockData data: Dictionary containing the JSON results data.
        :return ValueBlock: A ValueBlock instance.
        """
        init_params = cls.init_params()
        init_params['type'] = str
        init_params['version'] = int
        kwargs = cls.import_data(
            data=data,
            allowed=init_params,
            skip={'type', 'version'},
            optional={'timer', 'type', 'version'},
            default={'type': cls.TYPE, 'version': cls.VERSION},
            match_on={'type': cls.TYPE, 'version': cls.VERSION},
        )
        return cls(**kwargs)

    def to_dict(self) -> ValueBlockDict:
        """Convert the ValueBlock instance to a dictionary.

        The returned dictionary conforms to the JSON schema for ValueBlock V1
        and is suitable for serialization.

        The returned :class:`ValueBlockDict` has a stricter definition than
        :class:`ValueBlockData`. It requires the `type` and `version` fields
        to be present and guarantees that the `value` field is a `float`.

        :return ValueBlockDict: Dictionary representation of the ValueBlock instance.
        """
        output: ValueBlockDict = {
            'type': self.TYPE,
            'version': self.VERSION,
            'semantic_type': self.semantic_type,
            'unit': self.unit,
            'scale': self.scale,
            'value': self.value,
        }
        if self.timer is not None:
            output['timer'] = self.timer
        return output

    @property
    def semantic_type(self) -> str:
        """Get the semantic type value.

        :return: The semantic type value.
        """
        return self._semantic_type

    @property
    def timer(self) -> str | None:
        """Get the timer value.

        :return: The timer value or None.
        """
        return self._timer

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return: The unit of measurement.
        """
        return self._unit

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self._scale

    @property
    def value(self) -> float:
        """Get the value.

        :return: The value as a float.
        """
        return self._value

    def __hash__(self) -> int:
        """Get the hash of the ValueBlock instance.

        :return: The hash value.
        """
        return hash((
            self.semantic_type,
            self.timer,
            self.unit,
            self.scale,
            self.value,
        ))

    def __eq__(self, other: object) -> bool:
        """Check equality between two ValueBlock instances.

        :param other: The other ValueBlock instance to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, ValueBlock):
            return NotImplemented
        return (
            self.semantic_type == other.semantic_type and
            self.timer == other.timer and
            self.unit == other.unit and
            self.scale == other.scale and
            self.value == other.value
        )

    def __repr__(self) -> str:
        """Get the string representation of the ValueBlock instance.

        :return: The string representation.
        """
        params: dict[str, str | float | None] = {
            'semantic_type': self.semantic_type,
            'timer': self.timer,
            'unit': self.unit,
            'scale': self.scale,
            'value': self.value,
        }
        if self.timer is None:  # deletion instead of addition preserves ordering
            del params['timer']
        formatted_params = ', '.join(
            f"{key}={value!r}" for key, value in params.items()
        )

        return f"ValueBlock({formatted_params})"

    def __deepcopy__(self, memo: dict[int, Any]) -> "ValueBlock":
        """Create a deep copy of the ValueBlock instance.

        Since the ValueBlock instance and its contained attributes are immutable,
        a shallow copy is functionally identical to a deep copy. This method
        overrides the default `copy.deepcopy` to perform a more efficient shallow copy.

        :param memo: Memoization dictionary for deep copy.
        :return: A deep copy of the ValueBlock instance.
        """
        return copy(self)
