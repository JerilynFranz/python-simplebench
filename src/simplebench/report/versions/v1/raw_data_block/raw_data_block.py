"""Class for JSON raw data block representation."""
from collections.abc import Mapping
from typing import Any, cast

from simplebench.report._base import BaseRawDataBlock, JSONSchema
from simplebench.report.versions.v1.raw_data_block.raw_data_block_dict import RawDataBlockData, RawDataBlockDict
from simplebench.types import Values
from simplebench.validators import validate_core_data_mapping

from . import validate
from .raw_data_block_schema import RawDataBlockSchema


class RawDataBlock(BaseRawDataBlock):
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
        self._semantic_type = validate.semantic_type(semantic_type)
        self._timer = validate.timer(timer)
        self._cpu_timer = validate.cpu_timer(cpu_timer)
        self._unit = validate.unit(unit)
        self._scale = validate.scale(scale)
        self._data = validate.data(data)
        self._to_dict_cache: RawDataBlockDict | None = None  # Cache for to_dict output


    @property
    def dict_type(self) -> type[RawDataBlockDict]:
        """The ReportElementTypedDict type associated with this RawDataBlock class.

        :return: The ReportElementTypedDict type.
        """
        return RawDataBlockDict

    @property
    def data_type(self) -> type[RawDataBlockData]:
        """The ReportElementTypedDict type used for input data to `from_dict`.

        :return: The ReportElementTypedDict type for input data.
        """
        return RawDataBlockData

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RawDataBlock":
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
            allowed_fields=init_params,
            skip_fields={'type', 'version'},
            optional_fields={'timer', 'type', 'version'},
            defaults={'type': cls.TYPE, 'version': cls.VERSION},
            match_on={'type': cls.TYPE, 'version': cls.VERSION},
            process_as={'data': Values},
        )
        return cls(**kwargs)

    def to_dict(self) -> RawDataBlockDict:
        """Convert the RawDataBlock instance to a dictionary.

        The returned dictionary conforms to the 'shape' of the :class:`RawDataBlockDict` type,
        is immutable, and can be serialized to JSON.

        :return: Dictionary representation of the RawDataBlock instance.
        """
        if self._to_dict_cache is None:
            value = self._to_dict_helper()
            self._to_dict_cache = cast(RawDataBlockDict,
                validate_core_data_mapping(value, 'RawDataBlock.to_dict output'))
        return self._to_dict_cache

    @property
    def semantic_type(self) -> str:
        """Get the semantic type value.

        :return: The semantic type value.
        """
        return self._semantic_type

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
    def cpu_timer(self) -> str | None:
        """Get the CPU timer.

        :return str | None: The CPU timer.
        """
        return self._cpu_timer

    @property
    def timer(self) -> str | None:
        """Get the timer.

        :return str | None: The timer.
        """
        return self._timer

    @property
    def data(self) -> Values:
        """Get the data.

        :return: The data.
        """
        return self._data

    def __repr__(self) -> str:
        """Get the string representation of the RawDataBlock instance.

        :return: String representation of the RawDataBlock instance.
        """
        return (
            f"RawDataBlock(semantic_type={self.semantic_type!r}, "
            f"timer={self.timer!r}, cpu_timer={self.cpu_timer!r}, "
            f"unit={self.unit!r}, scale={self.scale!r}, "
            f"data={self.data!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality between two RawDataBlock instances.

        :param other: The other object to compare with.
        :return: True if both instances are equal, False otherwise.
        """
        if not isinstance(other, RawDataBlock):
            return NotImplemented

        return (
            self.semantic_type == other.semantic_type and
            self.timer == other.timer and
            self.cpu_timer == other.cpu_timer and
            self.unit == other.unit and
            self.scale == other.scale and
            self.data == other.data
        )

    def __hash__(self) -> int:
        """Get the hash of the RawDataBlock instance.

        :return: Hash of the RawDataBlock instance.
        """
        return hash((
            self.semantic_type,
            self.timer,
            self.cpu_timer,
            self.unit,
            self.scale,
            self.data))
