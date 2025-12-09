"""Base class for JSON results representation."""
from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_float, validate_string

from .. import stats
from ..exceptions import _JSONResultsErrorTag

if TYPE_CHECKING:
    from .json_stats import JSONStats


class JSONResults(ABC):
    """Base class representing JSON results."""

    VERSION: int = 0
    """The JSON results version number.

    :note: This should be overridden in sub-classes."""

    @classmethod
    def from_dict(cls, data: dict) -> JSONResults:
        """Create a JSONResults instance from a dictionary.

        :param data: Dictionary containing the JSON results data.
        :return: JSONResults instance.
        """
        cls.validate_type(data.get('type'), 'Results')
        return cls(
            group=data.get('group'),  # type: ignore[reportArgumentType]
            title=data.get('title'),  # type: ignore[reportArgumentType]
            description=data.get('description'),  # type: ignore[reportArgumentType]
            n=data.get('n'),  # type: ignore[reportArgumentType]
            variation_cols=data.get('variation_cols', {}),  # type: ignore[reportArgumentType]
            interval_unit=data.get('interval_unit'),  # type: ignore[reportArgumentType]
            interval_scale=data.get('interval_scale'),  # type: ignore[reportArgumentType]
            ops_per_interval_unit=data.get('ops_per_interval_unit'),  # type: ignore[reportArgumentType]
            ops_per_interval_scale=data.get('ops_per_interval_scale'),  # type: ignore[reportArgumentType]
            memory_unit=data.get('memory_unit'),  # type: ignore[reportArgumentType]
            memory_scale=data.get('memory_scale'),  # type: ignore[reportArgumentType]
            total_elapsed=data.get('total_elapsed'),  # type: ignore[reportArgumentType]
            extra_info=data.get('extra_info', {}),  # type: ignore[reportArgumentType]
            per_round_timings=data.get('per_round_timings'),  # type: ignore[reportArgumentType]
            ops_per_second=data.get('ops_per_second'),  # type: ignore[reportArgumentType]
            memory=data.get('memory'),  # type: ignore[reportArgumentType]
            peak_memory=data.get('peak_memory')  # type: ignore[reportArgumentType]
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
                tag=_JSONResultsErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONResults: {found} (expected '{expected}')",
                tag=_JSONResultsErrorTag.INVALID_TYPE_VALUE)
        return found

    def __init__(self, *,
                 group: str,
                 title: str,
                 description: str,
                 n: float,
                 variation_cols: dict[str, str],
                 interval_unit: str,
                 interval_scale: float,
                 ops_per_interval_unit: str,
                 ops_per_interval_scale: float,
                 memory_unit: str,
                 memory_scale: float,
                 total_elapsed: float,
                 extra_info: dict[str, Any],
                 per_round_timings: dict[str, Any],
                 ops_per_second: dict[str, Any],
                 memory: dict[str, Any],
                 peak_memory: dict[str, Any]
                 ) -> None:
        """Initialize JSONResults base class.

        :param group: The group name.
        :param title: The title of the results.
        :param description: The description of the results.
        :param n: The n complexity of results.
        """
        self.group = group
        self.title = title
        self.description = description
        self.n = n
        self.variation_cols = variation_cols
        self.interval_unit = interval_unit
        self.interval_scale = interval_scale
        self.ops_per_interval_unit = ops_per_interval_unit
        self.ops_per_interval_scale = ops_per_interval_scale
        self.memory_unit = memory_unit
        self.memory_scale = memory_scale
        self.total_elapsed = total_elapsed
        self.extra_info = extra_info
        self.per_round_timings = per_round_timings
        self.ops_per_second = ops_per_second
        self.memory = memory
        self.peak_memory = peak_memory

    @property
    def group(self) -> str:
        """Get the group property."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        """Set the group property."""
        self._group: str = validate_string(
            value, 'group',
            _JSONResultsErrorTag.INVALID_GROUP_TYPE,
            _JSONResultsErrorTag.INVALID_GROUP_VALUE_EMPTY_STRING,
            allow_empty=False)

    @property
    def title(self) -> str:
        """Get the title property."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the title property."""
        self._title: str = validate_string(
            value, 'title',
            _JSONResultsErrorTag.INVALID_TITLE_TYPE,
            _JSONResultsErrorTag.INVALID_TITLE_VALUE_EMPTY_STRING,
            allow_empty=False)

    @property
    def description(self) -> str:
        """Get the description property."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the description property."""
        self._description: str = validate_string(
            value, 'description',
            _JSONResultsErrorTag.INVALID_DESCRIPTION_TYPE,
            _JSONResultsErrorTag.INVALID_DESCRIPTION_EMPTY_STRING,
            allow_empty=False)

    @property
    def n(self) -> float:
        """Get the n property."""
        return self._n

    @n.setter
    def n(self, value: float) -> None:
        """Set the n property."""
        self._n: float = validate_float(
            value, 'n', _JSONResultsErrorTag.INVALID_N_TYPE)
        if self._n < 1:
            raise SimpleBenchValueError(
                f"n must be >= 1, got {self._n}",
                tag=_JSONResultsErrorTag.INVALID_N_VALUE)

    @property
    def variation_cols(self) -> dict[str, str]:
        """Get the variation columns.

        :return: A dictionary of variation columns.
        """
        return self._variation_cols

    @variation_cols.setter
    def variation_cols(self, value: dict[str, str]) -> None:
        """Set the variation columns.

        :param value: A dictionary of variation columns.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f"variation_cols must be a dictionary, got {type(value)}",
                tag=_JSONResultsErrorTag.INVALID_VARIATION_COLS_TYPE)

        if not all(isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
            raise SimpleBenchTypeError(
                "All keys and values in variation_cols must be strings",
                tag=_JSONResultsErrorTag.INVALID_VARIATION_COLS_CONTENT)

        self._variation_cols: dict[str, str] = value

    @property
    def interval_unit(self) -> str:
        """Get the interval unit.

        :return: The interval unit.
        """
        return self._interval_unit

    @interval_unit.setter
    def interval_unit(self, value: str) -> None:
        """Set the interval unit.

        :param value: The interval unit.
        """
        self._interval_unit: str = validate_string(
            value, 'interval_unit',
            _JSONResultsErrorTag.INVALID_INTERVAL_UNIT_TYPE,
            _JSONResultsErrorTag.INVALID_INTERVAL_UNIT_VALUE,
            allow_empty=False)

    @property
    def interval_scale(self) -> float:
        """Get the interval scale.

        :return: The interval scale.
        """
        return self._interval_scale

    @interval_scale.setter
    def interval_scale(self, value: float) -> None:
        """Set the interval scale.

        :param value: The interval scale.
        """
        self._interval_scale: float = validate_float(
            value, 'interval_scale',
            _JSONResultsErrorTag.INVALID_INTERVAL_SCALE_TYPE)
        if self._interval_scale <= 0.0:
            raise SimpleBenchValueError(
                f"interval_scale must be > 0.0, got {self._interval_scale}",
                tag=_JSONResultsErrorTag.INVALID_INTERVAL_SCALE_VALUE)

    @property
    def ops_per_interval_unit(self) -> str:
        """Get the operations per interval unit.

        :return: The operations per interval unit.
        """
        return self._ops_per_interval_unit

    @ops_per_interval_unit.setter
    def ops_per_interval_unit(self, value: str) -> None:
        """Set the operations per interval unit.

        :param value: The operations per interval unit.
        """
        self._ops_per_interval_unit: str = validate_string(
            value, 'ops_per_interval_unit',
            _JSONResultsErrorTag.INVALID_OPS_PER_INTERVAL_UNIT_TYPE,
            _JSONResultsErrorTag.INVALID_OPS_PER_INTERVAL_UNIT_VALUE,
            allow_empty=False)

    @property
    def ops_per_interval_scale(self) -> float:
        """Get the operations per interval scale.

        :return: The operations per interval scale.
        """
        return self._ops_per_interval_scale

    @ops_per_interval_scale.setter
    def ops_per_interval_scale(self, value: float) -> None:
        """Set the operations per interval scale.

        :param value: The operations per interval scale.
        """
        self._ops_per_interval_scale: float = validate_float(
            value, 'ops_per_interval_scale',
            _JSONResultsErrorTag.INVALID_OPS_PER_INTERVAL_SCALE_TYPE)
        if self._ops_per_interval_scale <= 0.0:
            raise SimpleBenchValueError(
                f"ops_per_interval_scale must be > 0.0, got {self._ops_per_interval_scale}",
                tag=_JSONResultsErrorTag.INVALID_OPS_PER_INTERVAL_SCALE_VALUE)

    @property
    def memory_unit(self) -> str:
        """Get the memory unit.

        :return: The memory unit.
        """
        return self._memory_unit

    @memory_unit.setter
    def memory_unit(self, value: str) -> None:
        """Set the memory unit.

        :param value: The memory unit.
        """
        self._memory_unit: str = validate_string(
            value, 'memory_unit',
            _JSONResultsErrorTag.INVALID_TYPE_TYPE,
            _JSONResultsErrorTag.INVALID_TYPE_VALUE,
            allow_empty=False)

    @property
    def memory_scale(self) -> float:
        """Get the memory scale.

        :return: The memory scale.
        """
        return self._memory_scale

    @memory_scale.setter
    def memory_scale(self, value: float) -> None:
        """Set the memory scale.

        :param value: The memory scale.
        """
        self._memory_scale: float = validate_float(
            value, 'memory_scale',
            _JSONResultsErrorTag.INVALID_TYPE_TYPE)
        if self._memory_scale <= 0.0:
            raise SimpleBenchValueError(
                f"memory_scale must be > 0.0, got {self._memory_scale}",
                tag=_JSONResultsErrorTag.INVALID_TYPE_VALUE)

    @property
    def total_elapsed(self) -> float:
        """Get the total elapsed time.

        :return: The total elapsed time.
        """
        return self._total_elapsed

    @total_elapsed.setter
    def total_elapsed(self, value: float) -> None:
        """Set the total elapsed time.

        :param value: The total elapsed time.
        """
        self._total_elapsed: float = validate_float(
            value, 'total_elapsed',
            _JSONResultsErrorTag.INVALID_TYPE_TYPE)
        if self._total_elapsed < 0.0:
            raise SimpleBenchValueError(
                f"total_elapsed must be >= 0.0, got {self._total_elapsed}",
                tag=_JSONResultsErrorTag.INVALID_TYPE_VALUE)

    @property
    def extra_info(self) -> dict[str, Any]:
        """Get the extra info.

        :return: The extra info dictionary.
        """
        return self._extra_info

    @extra_info.setter
    def extra_info(self, value: dict[str, Any]) -> None:
        """Set the extra info.

        :param value: The extra info dictionary.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f"extra_info must be a dictionary, got {type(value)}",
                tag=_JSONResultsErrorTag.INVALID_TYPE_TYPE)
        self._extra_info: dict[str, Any] = value

    @property
    def per_round_timings(self) -> JSONStats:
        """Get the per round timings.

        :return: The per round timings ReportStatsSummary.
        """
        return self._per_round_timings

    @per_round_timings.setter
    def per_round_timings(self, value: dict[str, Any]) -> None:
        """Set the per round timings.

        :param value: The per round timings ReportStatsSummary.
        """
        self._per_round_timings: JSONStats = stats.from_dict(
                                                        value,
                                                        self.__class__.VERSION)

    @property
    def ops_per_second(self) -> JSONStats:
        """Operations per second JSONStatsSummary.

        :return: Operations per second JSONStatsSummary.
        """
        return self._ops_per_second

    @ops_per_second.setter
    def ops_per_second(self, value: dict[str, Any]) -> None:
        """Set the operations per second JSONStatsSummary.

        :param value: Operations per second JSONStatsSummary.
        """
        self._ops_per_second: JSONStats = stats.from_dict(
                                                    value,
                                                    self.__class__.VERSION)

    @property
    def memory(self) -> JSONStats:
        """Memory JSONStatsSummary.

        :return: Memory JSONStatsSummary.
        """
        return self._memory

    @memory.setter
    def memory(self, value: dict[str, Any]) -> None:
        """Set the memory JSONStatsSummary.

        :param value: Memory JSONStatsSummary.
        """
        self._memory: JSONStats = stats.from_dict(
                                            value,
                                            self.__class__.VERSION)

    @property
    def peak_memory(self) -> JSONStats:
        """Peak memory JSONStatsSummary.

        :return: Peak memory JSONStatsSummary.
        """
        return self._peak_memory

    @peak_memory.setter
    def peak_memory(self, value: dict[str, Any]) -> None:
        """Set the peak memory JSONStatsSummary.

        :param value: Peak memory JSONStatsSummary.
        """
        self._peak_memory: JSONStats = stats.from_dict(
                                                value,
                                                self.__class__.VERSION)
