"""Base class for JSON stats summary representation."""
from __future__ import annotations

from abc import ABC
from typing import Any, Sequence

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_float, validate_string

from ..exceptions import _StatsBlockErrorTag


class Stats(ABC):
    """Base class representing JSON stats summary."""

    @classmethod
    def from_dict(cls, data: dict) -> Stats:
        """Create a JSONStatsSummary instance from a dictionary.

        :param data: Dictionary containing the JSON results data.
        :return: JSONStatsSummary instance.
        """
        cls.validate_type(data.get('type'), 'StatsSummary')
        return cls(
            unit=data.get('unit'),  # type: ignore[reportArgumentType]
            scale=data.get('scale'),  # type: ignore[reportArgumentType]
            rounds=data.get('rounds'),  # type: ignore[reportArgumentType]
            mean=data.get('mean'),  # type: ignore[reportArgumentType]
            median=data.get('median'),  # type: ignore[reportArgumentType]
            minimum=data.get('minimum'),  # type: ignore[reportArgumentType]
            maximum=data.get('maximum'),  # type: ignore[reportArgumentType]
            standard_deviation=data.get('standard_deviation'),  # type: ignore[reportArgumentType]
            relative_standard_deviation=data.get('relative_standard_deviation'),  # type: ignore[reportArgumentType]
            percentiles=data.get('percentiles')  # type: ignore[reportArgumentType]
        )

    @classmethod
    def validate_type(cls, found: Any, expected: str) -> str:
        """Validate the type.

        :param found: The type string to validate.
        :param expected: The expected type string.
        :return: The validated type string.
        :raise SimpleBenchTypeError: If the type is not a string.
        :raises SimpleBenchValueError: If the type is invalid.
        """
        if not isinstance(found, str):
            raise SimpleBenchValueError(
                f"type must be a string, got {type(found)}",
                tag=_StatsBlockErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONStatsSummary: {found} (expected '{expected}')",
                tag=_StatsBlockErrorTag.INVALID_TYPE_VALUE)
        return found

    def __init__(
            self, *,
            unit: str,
            scale: float,
            rounds: int,
            mean: float,
            median: float,
            minimum: float,
            maximum: float,
            standard_deviation: float,
            relative_standard_deviation: float,
            percentiles: Sequence[float]
                ) -> None:
        """Initialize JSONStatsSummary base class.

        :param unit: The unit of measurement.
        :param scale: The scale factor.
        :param rounds: The number of rounds.
        :param mean: The mean value.
        :param median: The median value.
        :param minimum: The minimum value.
        :param maximum: The maximum value.
        :param standard_deviation: The standard deviation.
        :param relative_standard_deviation: The relative standard deviation.
        :param percentiles: The list of percentiles.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """

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
            _StatsBlockErrorTag.INVALID_UNIT_TYPE,
            _StatsBlockErrorTag.INVALID_UNIT_VALUE,
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
            _StatsBlockErrorTag.INVALID_SCALE_TYPE)
        if self._scale <= 0:
            raise SimpleBenchValueError(
                "scale must be a positive float",
                tag=_StatsBlockErrorTag.INVALID_SCALE_VALUE)

    @property
    def rounds(self) -> int:
        """Get the number of rounds.

        :return: The number of rounds.
        """
        return self._rounds

    @rounds.setter
    def rounds(self, value: int) -> None:
        """Set the number of rounds.

        :param value: The number of rounds.
        :raise SimpleBenchTypeError: If rounds is not an integer.
        """
        if not isinstance(value, int):
            raise SimpleBenchTypeError(
                f"rounds must be an integer, got {type(value)}",
                tag=_StatsBlockErrorTag.INVALID_ROUNDS_TYPE)
        if value < 1:
            raise SimpleBenchValueError(
                "rounds must be a positive integer",
                tag=_StatsBlockErrorTag.INVALID_ROUNDS_VALUE)
        self._rounds: int = value

    @property
    def mean(self) -> float:
        """Get the mean value.

        :return: The mean value.
        """
        return self._mean

    @mean.setter
    def mean(self, value: float) -> None:
        """Set the mean value.

        :param value: The mean value.
        :raise SimpleBenchTypeError: If mean is not a float.
        """
        self._mean: float = validate_float(
            value, 'mean',
            _StatsBlockErrorTag.INVALID_MEAN_TYPE)

    @property
    def median(self) -> float:
        """Get the median value.

        :return: The median value.
        """
        return self._median

    @median.setter
    def median(self, value: float) -> None:
        """Set the median value.

        :param value: The median value.
        :raise SimpleBenchTypeError: If median is not a float.
        """
        self._median: float = validate_float(
            value, 'median',
            _StatsBlockErrorTag.INVALID_MEDIAN_TYPE)

    @property
    def minimum(self) -> float:
        """Get the minimum value.

        :return: The minimum value.
        """
        return self._minimum

    @minimum.setter
    def minimum(self, value: float) -> None:
        """Set the minimum value.

        :param value: The minimum value.
        :raise SimpleBenchTypeError: If minimum is not a float.
        """
        self._minimum: float = validate_float(
            value, 'minimum',
            _StatsBlockErrorTag.INVALID_MINIMUM_TYPE)

    @property
    def maximum(self) -> float:
        """Get the maximum value.

        :return: The maximum value.
        """
        return self._maximum

    @maximum.setter
    def maximum(self, value: float) -> None:
        """Set the maximum value.

        :param value: The maximum value.
        :raise SimpleBenchTypeError: If maximum is not a float.
        """
        self._maximum: float = validate_float(
            value, 'maximum',
            _StatsBlockErrorTag.INVALID_MAXIMUM_TYPE)

    @property
    def standard_deviation(self) -> float:
        """Get the standard deviation.

        :return: The standard deviation.
        """
        return self._standard_deviation

    @standard_deviation.setter
    def standard_deviation(self, value: float) -> None:
        """Set the standard deviation.

        :param value: The standard deviation.
        :raise SimpleBenchTypeError: If standard_deviation is not a float.
        """
        self._standard_deviation: float = validate_float(
            value, 'standard_deviation',
            _StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_TYPE)

    @property
    def relative_standard_deviation(self) -> float:
        """Get the relative standard deviation.

        :return: The relative standard deviation.
        """
        return self._relative_standard_deviation

    @relative_standard_deviation.setter
    def relative_standard_deviation(self, value: float) -> None:
        """Set the relative standard deviation.

        :param value: The relative standard deviation.
        :raise SimpleBenchTypeError: If relative_standard_deviation is not a float.
        """
        self._relative_standard_deviation: float = validate_float(
            value, 'relative_standard_deviation',
            _StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_TYPE)

    @property
    def percentiles(self) -> list[float]:
        """Get the list of percentiles.

        The list consists of 101 float values representing the percentiles
        from 0 to 100.

        :return: The list of percentiles.
        """
        return self._percentiles

    @percentiles.setter
    def percentiles(self, value: Sequence[float | int]) -> None:
        """Set the list of percentiles.

        :param value: The list of percentiles.
        :raise SimpleBenchTypeError: If percentiles is not a sequence of float or int.
        """
        if not isinstance(value, Sequence):
            raise SimpleBenchTypeError(
                "percentiles must be a sequence",
                tag=_StatsBlockErrorTag.INVALID_PERCENTILES_TYPE)

        if not all(isinstance(v, (float | int)) for v in value):
            raise SimpleBenchTypeError(
                "percentiles must be a sequence of float or int",
                tag=_StatsBlockErrorTag.INVALID_PERCENTILES_CONTENT_TYPE)

        self._percentiles: list[float] = list(float(v) for v in value)
