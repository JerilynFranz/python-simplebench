"""Base class for JSON value block representation."""
import re
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_float, validate_string

from ..exceptions import _ValueBlockErrorTag


class ValueBlock:
    """Base class representing a value block."""

    _TYPE_PATTERN = re.compile(r"^[a-zA-Z0-9_]+::[a-zA-Z0-9_]+$")

    @classmethod
    def from_dict(cls, data: dict) -> "ValueBlock":
        """Create a ValueBlock instance from a dictionary.

        :param data: Dictionary containing the JSON results data.
        :return: JSONStatsSummary instance.
        """
        known_keys: set[str] = {'type', 'timer', 'unit', 'scale', 'value'}
        extra_keys = set(data.keys()) - known_keys
        if extra_keys:
            raise SimpleBenchTypeError(
                f"Unexpected keys in data dictionary: {extra_keys}",
                tag=_ValueBlockErrorTag.INVALID_DATA_ARG_EXTRA_KEYS)

        missing_keys = known_keys - data.keys() - {'timer'}
        if missing_keys:
            raise SimpleBenchTypeError(
                f"Missing required keys in data dictionary: {missing_keys}",
                tag=_ValueBlockErrorTag.INVALID_DATA_ARG_MISSING_KEYS)

        return cls(
            semantic_type=data.get('type'),  # type: ignore[reportArgumentType]
            timer=data.get('timer'),  # type: ignore[reportArgumentType]
            unit=data.get('unit'),  # type: ignore[reportArgumentType]
            scale=data.get('scale'),  # type: ignore[reportArgumentType]
            value=data.get('value')  # type: ignore[reportArgumentType]
        )

    @classmethod
    def validate_timer(cls, value: Any) -> str | None:
        """Validate the timer.
        :param value: The timer string to validate.
        :return: The validated timer string or None.
        :raise SimpleBenchTypeError: If the timer is not a string or None.
        :raises SimpleBenchValueError: If the timer string is invalid.
        """
        if value is None:
            return None

        timer_name: str = validate_string(
            value, 'timer',
            _ValueBlockErrorTag.INVALID_VALUE_TIMER_TYPE,
            _ValueBlockErrorTag.INVALID_VALUE_TIMER_VALUE,
            allow_blank=False)

        return timer_name

    @classmethod
    def validate_type_pattern(cls, value: Any) -> str:
        """Validate the type.
        :param value: The type string to validate.
        :return: The validated type string.
        :raise SimpleBenchTypeError: If the type is not a string.
        :raises SimpleBenchValueError: If the type string is invalid.
        """
        type_name: str = validate_string(
            value, 'type',
            _ValueBlockErrorTag.INVALID_VALUE_TYPE,
            _ValueBlockErrorTag.INVALID_VALUE_VALUE,
            allow_blank=False)

        if not cls._TYPE_PATTERN.match(type_name):
            raise SimpleBenchValueError(
                f"Invalid type format for ValueBlock: {type_name}",
                tag=_ValueBlockErrorTag.INVALID_VALUE_PATTERN)

        return type_name

    def __init__(
            self,
            *,
            semantic_type: str,
            timer: str | None,
            unit: str,
            scale: float,
            value: float | int) -> None:
        """Initialize JSONStatsSummary base class.

        :param semantic_type: The semantic type string for the value block. ('type' field in JSON data)
        :param timer: The timer string or None.
        :param unit: The unit of measurement.
        :param scale: The scale factor.
        :param value: The value of the block.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """

    @property
    def type(self) -> str:
        """Get the semantic type value.

        :return: The semantic type value.
        """
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """Set the semantic type value.

        :param value: The semantic type value.
        :raise SimpleBenchTypeError: If type is not a string.
        :raise SimpleBenchValueError: If type is an invalid format.
        """
        self._type: str = self.validate_type_pattern(value)

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return: The unit of measurement.
        """
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        """Set the unit of measurement.

        :param value: The unit of measurement.
        :raise SimpleBenchTypeError: If unit is not a string.
        :raise SimpleBenchValueError: If unit is an empty string.
        """
        self._unit: str = validate_string(
            value, 'unit',
            _ValueBlockErrorTag.INVALID_UNIT_TYPE,
            _ValueBlockErrorTag.INVALID_UNIT_VALUE,
            allow_blank=False)

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        """Set the scale factor.

        :param value: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        :raise SimpleBenchValueError: If scale is not a positive number.
        """
        self._scale: float = validate_float(
            value, 'scale',
            _ValueBlockErrorTag.INVALID_SCALE_TYPE)
        if self._scale <= 0:
            raise SimpleBenchValueError(
                "scale must be a positive float",
                tag=_ValueBlockErrorTag.INVALID_SCALE_VALUE)

    @property
    def value(self) -> float | int:
        """Get the value.

        :return: The value as a float or int.
        """
        return self._value

    @value.setter
    def value(self, value: float | int) -> None:
        """Set the value.

        :param value: The value.
        :raise SimpleBenchTypeError: If value is not a float or int.
        """
        if not isinstance(value, (float, int)):
            raise SimpleBenchTypeError(
                f"value must be a float or int, got {type(value)}",
                tag=_ValueBlockErrorTag.INVALID_VALUE_TYPE)
        self._value: float | int = value
