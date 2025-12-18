"""Class for JSON raw data block representation."""
from typing import Any

from simplebench.report._error_tags import _RawDataBlockErrorTag
from simplebench.report.base import JSONSchema
from simplebench.report.base import RawDataBlock as RawDataBlockBase
from simplebench.types import Values
from simplebench.validators import (
    validate_namespaced_identifier,
    validate_positive_float,
    validate_string,
    validate_type,
)

from .raw_data_block_schema import RawDataBlockSchema


class RawDataBlock(RawDataBlockBase):
    """Class representing a raw data block (V1).
    :param str semantic_type: The semantic type string for the raw data block. ('type' field in JSON data)
    :param (str | None) timer: The timer string or None.
    :param str unit: The unit of measurement.
    :param float scale: The scale factor.
    :param Values data: The raw data values of the block.
    :raise SimpleBenchTypeError: If any parameter is of incorrect type.
    :raise SimpleBenchValueError: If any parameter has an invalid value.
    """

    SCHEMA: type[JSONSchema] = RawDataBlockSchema
    """JSON schema class for the raw data block."""

    VERSION: int = SCHEMA.VERSION
    """Version of the raw data block schema."""

    TYPE: str = SCHEMA.TYPE
    """Type of the raw data block schema."""

    ID: str = SCHEMA.ID
    """ID of the raw data block schema."""

    def __init__(
            self,
            *,
            semantic_type: str,
            timer: str | None = None,
            unit: str,
            scale: float,
            data: Values) -> None:
        """Initialize JSONStatsSummary base class.

        :param str semantic_type: The semantic type string for the value block. ('type' field in JSON data)
        :param (str | None) timer: The timer string or None.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
        :param Values data: The raw data values of the block.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """
        self.semantic_type = semantic_type
        self.timer = timer
        self.unit = unit
        self.scale = scale
        self.data = data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RawDataBlock":
        """Create a RawDataBlock instance from a dictionary.

        :param data: Dictionary containing the JSON raw data block data.
        :return: A RawDataBlock instance.
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
            process_as={'data': Values},
        )
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the RawDataBlock instance to a dictionary.

        :return: Dictionary representation of the RawDataBlock instance.
        """
        output: dict[str, Any] = {
            'type': self.TYPE,
            'version': self.VERSION,
            'semantic_type': self.semantic_type,
            'unit': self.unit,
            'scale': self.scale,
            'data': self.data,
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
            _RawDataBlockErrorTag.INVALID_TIMER_TYPE,
            _RawDataBlockErrorTag.INVALID_TIMER_VALUE,
            allow_blank=False)

        return timer_name

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
        self._semantic_type: str = validate_namespaced_identifier(
            value, 'semantic_type',
            _RawDataBlockErrorTag.INVALID_SEMANTIC_TYPE_TYPE,
            _RawDataBlockErrorTag.INVALID_SEMANTIC_TYPE_VALUE)

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
            _RawDataBlockErrorTag.INVALID_UNIT_TYPE,
            _RawDataBlockErrorTag.INVALID_UNIT_VALUE,
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
            _RawDataBlockErrorTag.INVALID_SCALE_TYPE,
            _RawDataBlockErrorTag.INVALID_SCALE_VALUE)

    @property
    def data(self) -> Values:
        """Get the data.

        :return: The data.
        """
        return self._data

    @data.setter
    def data(self, value: Values) -> None:
        """Set the data.

        :param value: The data.
        :raise SimpleBenchTypeError: If data is not of type Values.
        """
        self._data: Values = validate_type(
            value, Values, 'data',
            _RawDataBlockErrorTag.INVALID_DATA_TYPE)
