"""Class for JSON raw data block representation."""
from typing import Any

from simplebench.decorators import immutable
from simplebench.report.base import JSONSchema
from simplebench.report.base import RawDataBlock as RawDataBlockBase
from simplebench.types import Values

from .raw_data_block_schema import RawDataBlockSchema
from .validators import (
    validate_cpu_timer,
    validate_data,
    validate_scale,
    validate_semantic_type,
    validate_timer,
    validate_unit,
)


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
            cpu_timer: str | None = None,
            unit: str,
            scale: float,
            data: Values) -> None:
        """Initialize RawDataBlock class.

        :param str semantic_type: The semantic type string for the raw data block. ('type' field in JSON data)
        :param (str | None) timer: The timer string or None.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
        :param Values data: The raw data values of the block.
        :param (str | None) timer: The timer string or None.
        :param (str | None) cpu_timer: The CPU timer string or None.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """
        self.semantic_type = semantic_type
        self.timer = timer
        self.cpu_timer = cpu_timer
        self.unit = unit
        self.scale = scale
        self.data = data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RawDataBlock":
        """Create a RawDataBlock instance from a dictionary that represents the
        JSON raw data block. It must conform to the :class:`RawDataBlockSchema`.

        :param data: Dictionary containing the JSON raw data block data.
        :return RawDataBlock: A RawDataBlock instance.
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
        if self.cpu_timer is not None:
            output['cpu_timer'] = self.cpu_timer

        return output

    @property
    def semantic_type(self) -> str:
        """Get the semantic type value.

        :return: The semantic type value.
        """
        return self._semantic_type

    @semantic_type.setter
    @immutable
    def semantic_type(self, value: str) -> None:
        """Set the semantic type value.

        :param str value: The semantic type value.
        :raise SimpleBenchTypeError: If type is not a string.
        :raise SimpleBenchValueError: If type is an invalid format.
        """
        self._semantic_type: str = validate_semantic_type(value)

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return: The unit of measurement.
        """
        return self._unit

    @unit.setter
    @immutable
    def unit(self, value: str) -> None:
        """Set the unit of measurement.

        :param value: The unit of measurement.
        :raise SimpleBenchTypeError: If unit is not a string.
        :raise SimpleBenchValueError: If unit is an empty string.
        """
        self._unit: str = validate_unit(value)

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self._scale

    @scale.setter
    @immutable
    def scale(self, value: float) -> None:
        """Set the scale factor.

        :param value: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        :raise SimpleBenchValueError: If scale is not a positive number.
        """
        self._scale: float = validate_scale(value)

    @property
    def cpu_timer(self) -> str | None:
        """Get the CPU timer.

        :return str | None: The CPU timer.
        """
        return self._cpu_timer

    @cpu_timer.setter
    @immutable
    def cpu_timer(self, value: str | None) -> None:
        """Set the CPU timer.

        :param value: The CPU timer.
        :raise SimpleBenchTypeError: If cpu_timer is not a string or None.
        :raise SimpleBenchValueError: If cpu_timer is an invalid string.
        """
        self._cpu_timer: str | None = validate_cpu_timer(value)

    @property
    def timer(self) -> str | None:
        """Get the timer.

        :return str | None: The timer.
        """
        return self._timer

    @timer.setter
    @immutable
    def timer(self, value: str | None) -> None:
        """Set the timer.

        :param value: The timer.
        :raise SimpleBenchTypeError: If timer is not a string or None.
        :raise SimpleBenchValueError: If timer is an invalid string.
        """
        self._timer: str | None = validate_timer(value)

    @property
    def data(self) -> Values:
        """Get the data.

        :return: The data.
        """
        return self._data

    @data.setter
    @immutable
    def data(self, values: Values) -> None:
        """Set the data.

        :param values: The data.
        :raise SimpleBenchTypeError: If data is not of type Values.
        """
        self._data: Values = validate_data(values)
