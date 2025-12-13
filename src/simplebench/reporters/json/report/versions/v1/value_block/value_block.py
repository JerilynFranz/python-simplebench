"""Class for JSON value block representation."""
import re
from typing import Any

from simplebench.exceptions import SimpleBenchValueError
from simplebench.reporters.json.report.base import JSONSchema
from simplebench.reporters.json.report.base import ValueBlock as ValueBlockBase
from simplebench.reporters.json.report.exceptions import _ValueBlockErrorTag
from simplebench.validators import validate_positive_float, validate_string, validate_type

from .value_block_schema import ValueBlockSchema


class ValueBlock(ValueBlockBase):
    """Class representing a value block (V1)."""

    SCHEMA: type[JSONSchema] = ValueBlockSchema
    """JSON schema class for the value block."""

    VERSION: int = SCHEMA.VERSION
    """Version of the value block schema."""

    TYPE: str = SCHEMA.TYPE
    """Type of the value block schema."""

    ID: str = SCHEMA.ID
    """ID of the value block schema."""

    def __init__(
            self,
            *,
            semantic_type: str,
            timer: str | None = None,
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
        self.semantic_type = semantic_type
        self.timer = timer
        self.unit = unit
        self.scale = scale
        self.value = value

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ValueBlock":
        """Create a ValueBlock instance from a dictionary.

        :param data: Dictionary containing the JSON results data.
        :return: A ValueBlock instance.
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

    def to_dict(self) -> dict[str, Any]:
        """Convert the ValueBlock instance to a dictionary.

        :return: Dictionary representation of the ValueBlock instance.
        """
        output: dict[str, Any] = {
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

    _SEMANTIC_TYPE_PATTERN = re.compile(r"^[a-zA-Z0-9_]+::[a-zA-Z0-9_]+$")
    """Pattern for validating the semantic type string."""

    @classmethod
    def validate_semantic_type_pattern(cls, value: Any) -> str:
        """Validate the semantic type.
        :param value: The semantic type string to validate.
        :return: The validated semantic type string.
        :raise SimpleBenchTypeError: If the semantic type is not a string.
        :raises SimpleBenchValueError: If the semantic type string is invalid.
        """
        type_name: str = validate_string(
            value, 'semantic_type',
            _ValueBlockErrorTag.INVALID_VALUE_TYPE,
            _ValueBlockErrorTag.INVALID_VALUE_VALUE,
            allow_blank=False)

        if not cls._SEMANTIC_TYPE_PATTERN.match(type_name):
            raise SimpleBenchValueError(
                f"Invalid type format for ValueBlock: {type_name}",
                tag=_ValueBlockErrorTag.INVALID_VALUE_PATTERN)

        return type_name

    @property
    def semantic_type(self) -> str:
        """Get the semantic type value.

        :return: The semantic type value.
        """
        return self._semantic_type

    @semantic_type.setter
    def semantic_type(self, value: str) -> None:
        """Set the semantic type value.

        :param value: The semantic type value.
        :raise SimpleBenchTypeError: If type is not a string.
        :raise SimpleBenchValueError: If type is an invalid format.
        """
        self._semantic_type: str = self.validate_semantic_type_pattern(value)

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
        self._scale: float = validate_positive_float(
            value, 'scale',
            _ValueBlockErrorTag.INVALID_SCALE_TYPE,
            _ValueBlockErrorTag.INVALID_SCALE_VALUE)

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
        self._value: float | int = validate_type(
            value, (float, int), 'value',
            _ValueBlockErrorTag.INVALID_VALUE_TYPE)
