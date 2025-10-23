# -*- coding: utf-8 -*-
"""Container for the results of a single benchmark test."""
from __future__ import annotations
from copy import copy, deepcopy
from typing import Any, Optional, Sequence
from types import MappingProxyType

from simplebench.exceptions import SimpleBenchValueError, SimpleBenchTypeError, ResultsErrorTag

from .defaults import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT, DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT
from .enums import Section
from .iteration import Iteration
from .stats import OperationsPerInterval, OperationTimings, MemoryUsage, PeakMemoryUsage, Stats
from .validators import validate_non_blank_string, validate_positive_int, validate_positive_float


class Results:
    '''Container for the results of a single benchmark test.

    The Results class holds all relevant information about a benchmark test's execution and its outcomes.
    It is immutable after creation to ensure data integrity.

    Properties:
        group (str): The reporting group to which the benchmark case belongs. (read only)
        title (str): The name of the benchmark case. (read only)
        description (str): A brief description of the benchmark case. (read only)
        n (int): The n weighting the benchmark assigned to the iteration for purposes of Big O analysis. (read only)
        variation_marks (MappingProxyType[str, Any]): A dictionary of variation marks used to identify the
            benchmark variation. (read only)
        variation_cols (MappingProxyType[str, str]): The columns to use for labelling kwarg variations in
            the benchmark. (read only)
        interval_unit (str): The unit of measurement for the interval (e.g. "ns"). (read only)
        interval_scale (float): The scale factor for the interval (e.g. 1e-9 for nanoseconds). (read only)
        ops_per_interval_unit (str): The unit of measurement for operations per interval (e.g. "ops/s"). (read only)
        ops_per_interval_scale (float): The scale factor for operations per interval (e.g. 1.0 for ops/s). (read only)
        memory_unit (str): The unit of measurement for memory usage (e.g. "bytes"). (read only)
        memory_scale (float): The scale factor for memory usage (e.g. 1.0 for bytes). (read only)
        iterations (tuple[Iteration, ...]): A tuple of Iteration objects representing each iteration of
            the benchmark. (read only)
        ops_per_second (OperationsPerInterval): Statistics for operations per interval. (read only)
        per_round_timings (OperationTimings): Statistics for per-round timings. (read only)
        memory (MemoryUsage): Statistics for memory usage. (read only)
        peak_memory (PeakMemoryUsage): Statistics for peak memory usage. (read only)
        total_elapsed (float): The total elapsed time for the benchmark. (read only)
        extra_info (MappingProxyType[str, Any]): Additional information about the benchmark run. This is a
            read-only property that returns a mapping proxy to prevent external mutation. (read only)
    '''
    __slots__ = (
        '_group',
        '_title',
        '_description',
        '_n',
        '_variation_cols',
        '_variation_marks',
        '_interval_unit',
        '_interval_scale',
        '_ops_per_interval_unit',
        '_ops_per_interval_scale',
        '_memory',
        '_memory_unit',
        '_memory_scale',
        '_peak_memory',
        '_iterations',
        '_ops_per_second',
        '_per_round_timings',
        '_total_elapsed',
        '_extra_info',
        '_repr_cache',
    )

    def __init__(self,  # pylint: disable=too-many-arguments, too-many-locals
                 *,
                 group: str,
                 title: str,
                 description: str,
                 n: int,
                 total_elapsed: float,
                 iterations: Sequence[Iteration],
                 variation_cols: dict[str, str] | None = None,
                 variation_marks: dict[str, Any] | None = None,
                 interval_unit: str = DEFAULT_INTERVAL_UNIT,
                 interval_scale: float = DEFAULT_INTERVAL_SCALE,
                 ops_per_interval_unit: str = DEFAULT_INTERVAL_UNIT,
                 ops_per_interval_scale: float = DEFAULT_INTERVAL_SCALE,
                 memory_unit: str = DEFAULT_MEMORY_UNIT,
                 memory_scale: float = DEFAULT_MEMORY_SCALE,
                 ops_per_second: Optional[OperationsPerInterval] = None,
                 per_round_timings: Optional[OperationTimings] = None,
                 memory: Optional[MemoryUsage] = None,
                 peak_memory: Optional[PeakMemoryUsage] = None,
                 extra_info: Optional[dict[str, Any]] = None) -> None:
        """Initialize a Results object.

        Args:
            group (str): The reporting group to which the benchmark case belongs.
            title (str): The name of the benchmark case.
            description (str): A brief description of the benchmark case.
            n (int): The n weighting assigned to the iteration for purposes of Big O analysis.
            total_elapsed (float): The total elapsed time for the benchmark.
            iterations (list[Iteration]): The list of Iteration objects representing each iteration of the benchmark.
            variation_cols (dict[str, str], optional): The columns to use for labelling kwarg variations
                in the benchmark. Defaults to None, which results in an empty dictionary.
            variation_marks (dict[str, Any], optional): A dictionary of variation marks used to identify
                the benchmark variation. Defaults to None, which results in an empty dictionary.
            interval_unit (str, optional): The unit of measurement for the interval (e.g. "ns").
                Defaults to "ns".
            interval_scale (float, optional): The scale factor for the interval (e.g. 1e-9 for nanoseconds).
                Defaults to 1e-9.
            ops_per_interval_unit (str, optional): The unit of measurement for operations per interval (e.g. "ops/s").
                Defaults to "ops/s".
            ops_per_interval_scale (float, optional): The scale factor for operations per interval (e.g. 1.0 for ops/s).
                Defaults to 1.0.
            memory_unit (str, optional): The unit of measurement for memory usage (e.g. "bytes").
                Defaults to "bytes".
            memory_scale (float, optional): The scale factor for memory usage (e.g. 1.0 for bytes).
                Defaults to 1.0.
            ops_per_second (Optional[OperationsPerInterval], optional): The operations per second for the benchmark.
                Defaults to a new OperationsPerInterval object initialized from the benchmark's iterations.
            per_round_timings (Optional[OperationTimings], optional): The per-round timings for the benchmark.
                Defaults to a new OperationTimings object initialized from the benchmark's iterations.
            memory (Optional[MemoryUsage], optional): The memory usage for the benchmark.
                Defaults to a new MemoryUsage object initialized from the benchmark's iterations.
            peak_memory (Optional[PeakMemoryUsage], optional): The peak memory usage for the benchmark.
                Defaults to a new PeakMemoryUsage object initialized from the benchmark's iterations.
            extra_info (Optional[dict[str, Any]], optional): Any extra information to include in the benchmark results.
                Defaults to {}.
        """
        self._group: str = validate_non_blank_string(
            group, 'group',
            ResultsErrorTag.GROUP_INVALID_ARG_TYPE,
            ResultsErrorTag.GROUP_INVALID_ARG_VALUE)
        self._title: str = validate_non_blank_string(
            title, 'title',
            ResultsErrorTag.TITLE_INVALID_ARG_TYPE,
            ResultsErrorTag.TITLE_INVALID_ARG_VALUE)
        self._description: str = validate_non_blank_string(
            description, 'description',
            ResultsErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
            ResultsErrorTag.DESCRIPTION_INVALID_ARG_VALUE)
        self._n: int = validate_positive_int(
            n, 'n',
            ResultsErrorTag.N_INVALID_ARG_TYPE,
            ResultsErrorTag.N_INVALID_ARG_VALUE)
        self._iterations: tuple[Iteration, ...] = self._validate_iterations(iterations)
        self._variation_cols: dict[str, str] = self._validate_variation_cols(variation_cols)
        self._variation_marks: dict[str, Any] = self._validate_variation_marks(variation_marks)
        self._interval_unit: str = validate_non_blank_string(
            interval_unit, 'interval_unit',
            ResultsErrorTag.INTERVAL_UNIT_INVALID_ARG_TYPE,
            ResultsErrorTag.INTERVAL_UNIT_INVALID_ARG_VALUE)
        self._interval_scale: float = validate_positive_float(
            interval_scale, 'interval_scale',
            ResultsErrorTag.INTERVAL_SCALE_INVALID_ARG_TYPE,
            ResultsErrorTag.INTERVAL_SCALE_INVALID_ARG_VALUE)
        self._ops_per_interval_unit: str = validate_non_blank_string(
            ops_per_interval_unit, 'ops_per_interval_unit',
            ResultsErrorTag.OPS_PER_INTERVAL_UNIT_INVALID_ARG_TYPE,
            ResultsErrorTag.OPS_PER_INTERVAL_UNIT_INVALID_ARG_VALUE)
        self._ops_per_interval_scale: float = validate_positive_float(
            ops_per_interval_scale, 'ops_per_interval_scale',
            ResultsErrorTag.OPS_PER_INTERVAL_SCALE_INVALID_ARG_TYPE,
            ResultsErrorTag.OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE)
        self._memory_unit: str = validate_non_blank_string(
            memory_unit, 'memory_unit',
            ResultsErrorTag.MEMORY_UNIT_INVALID_ARG_TYPE,
            ResultsErrorTag.MEMORY_UNIT_INVALID_ARG_VALUE)
        self._memory_scale: float = validate_positive_float(
            memory_scale, 'memory_scale',
            ResultsErrorTag.MEMORY_SCALE_INVALID_ARG_TYPE,
            ResultsErrorTag.MEMORY_SCALE_INVALID_ARG_VALUE)
        self._memory: MemoryUsage = self._validate_memory(memory)
        self._peak_memory: PeakMemoryUsage = self._validate_peak_memory(peak_memory)
        self._ops_per_second: OperationsPerInterval = self._validate_ops_per_second(ops_per_second)
        self._per_round_timings: OperationTimings = self._validate_per_round_timings(per_round_timings)
        self._total_elapsed: float = validate_positive_float(
            total_elapsed, 'total_elapsed',
            ResultsErrorTag.TOTAL_ELAPSED_INVALID_ARG_TYPE,
            ResultsErrorTag.TOTAL_ELAPSED_INVALID_ARG_VALUE)
        self._extra_info = self._validate_extra_info(extra_info)
        self._repr_cache: Optional[str] = None  # cache for __repr__

    def _validate_variation_cols(self, value: dict[str, str] | None) -> dict[str, str]:
        """Validate the variation_cols dictionary.

        Args:
            value (dict[str, str]): The variation_cols dictionary to validate.

        Returns:
            dict[str, str]: A copy of the validated variation_cols dictionary.

        Raises:
            SimpleBenchTypeError: If the variation_cols is not a dictionary or if any key or
                value is not a string.
            SimpleBenchValueError: If any value is a blank string.
        """
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols: {value}. Must be a dictionary.',
                tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE
                )

        for key, val in value.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols key type: {type(key)}. Must be of type str.',
                    tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_TYPE
                )
            if key == '':
                raise SimpleBenchValueError(
                    'Invalid variation_cols key value: empty string. Keys must be non-empty strings.',
                    tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_VALUE
                )
            if not isinstance(val, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols value type: {type(val)}. Must be of type str.',
                    tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_VALUE_TYPE
                )
        # shallow copy to prevent external mutation
        return copy(value)

    def _validate_iterations(self, value: Sequence[Iteration]) -> tuple[Iteration, ...]:
        """Validate the iterations Sequence.

        Args:
            value (Sequence[Iteration]): The iterations Sequence to validate.

        Returns:
            tuple[Iteration, ...]: A copy of the validated iterations as a tuple.
        """
        if not isinstance(value, Sequence):
            raise SimpleBenchTypeError(
                f'Invalid iterations type: {type(value)}. Must be of type list.',
                tag=ResultsErrorTag.ITERATIONS_INVALID_ARG_TYPE
            )
        for iteration in value:
            if not isinstance(iteration, Iteration):
                raise SimpleBenchTypeError(
                    f'Invalid iteration element type: {type(iteration)}. Must be of type Iteration.',
                    tag=ResultsErrorTag.ITERATIONS_INVALID_ARG_IN_SEQUENCE
                )
        # shallow copy to prevent external mutation of iterations sequence itself
        return tuple(value)

    def _validate_variation_marks(self, value: dict[str, Any] | None) -> dict[str, Any]:
        """Validate the variation_marks dictionary.

        Performs shallow copy of the dictionary to help mitigate external mutation. Because
        the values can be of ANY type, including types that do not support deep copying, we do not
        attempt to deep copy the values.

        Args:
            value (dict[str, Any]): The variation_marks dictionary to validate.

        Returns:
            dict[str, Any]: A shallow copy of the validated variation_marks dictionary.

        Raises:
            SimpleBenchTypeError: If the variation_marks is not a dictionary or if any key is not a string.
            SimpleBenchValueError: If any key is a blank string.
        """
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_marks: {value}. Must be a dictionary.',
                tag=ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE
            )

        # shallow copy to prevent external mutation
        # not deep copying values because they can be of ANY type,
        # including types that do not support deep copying
        return_value: dict[str, Any] = {}
        for key in value.keys():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_marks key type: {type(key)}. Must be of type str.',
                    tag=ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_TYPE
                )
            stripped_key = key.strip()
            if stripped_key == '':
                raise SimpleBenchValueError(
                    'Invalid variation_marks key value: blank string. Keys must be non-blank strings.',
                    tag=ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_VALUE
                )
            return_value[stripped_key] = value[key]
        return return_value

    def _validate_peak_memory(self, value: PeakMemoryUsage | None) -> PeakMemoryUsage:
        """Validate the peak_memory object if passed, or create a default one if None.

        The default PeakMemoryUsage object will have its iterations set to the same list
        of Iteration objects as the Results object and initialized with the values from
        `memory_unit` and `memory_scale` for unit and scale.

        Args:
            value (PeakMemoryUsage | None): The peak_memory object to validate or None.

        Returns:
            PeakMemoryUsage: The validated or default PeakMemoryUsage object.

        Raises:
            SimpleBenchTypeError: If the value is not None and not of type PeakMemoryUsage
        """
        if value is None:
            return PeakMemoryUsage(unit=self._memory_unit, scale=self._memory_scale, iterations=self._iterations)

        if not isinstance(value, PeakMemoryUsage):
            raise SimpleBenchTypeError(
                f'Invalid peak_memory type: {type(value)}. Must be of type PeakMemoryUsage.',
                tag=ResultsErrorTag.PEAK_MEMORY_INVALID_ARG_TYPE
            )
        return value

    def _validate_memory(self, value: MemoryUsage | None) -> MemoryUsage:
        """Validate the memory object if passed, or create a default one if None.

        The default MemoryUsage object will have its iterations set to the same list
        of Iteration objects as the Results object and initialized with the values from
        `memory_unit` and `memory_scale` for unit and scale.

        Args:
            value (MemoryUsage | None): The peak_memory object to validate or None.

        Returns:
            MemoryUsage: The validated or default MemoryUsage object.

        Raises:
            SimpleBenchTypeError: If the value is not None and not of type MemoryUsage.
        """
        if value is None:
            return MemoryUsage(unit=self._memory_unit, scale=self._memory_scale, iterations=self._iterations)

        if not isinstance(value, MemoryUsage):
            raise SimpleBenchTypeError(
                f'Invalid memory type: {type(value)}. Must be of type MemoryUsage.',
                tag=ResultsErrorTag.MEMORY_INVALID_ARG_TYPE
            )
        return value

    def _validate_ops_per_second(self, value: OperationsPerInterval | None) -> OperationsPerInterval:
        """Validate the ops_per_second object if passed, or create a default one if None.

        The default OperationsPerInterval object will have its iterations set to the same list
        of Iteration objects as the Results object and initialized with the values from
        `ops_per_interval_unit` and `ops_per_interval_scale` for unit and scale.

        Args:
            value (OperationsPerInterval | None): The ops_per_second object to validate or None.

        Returns:
            OperationsPerInterval: The validated or default OperationsPerInterval object.

        Raises:
            SimpleBenchTypeError: If the value is not None and not of type OperationsPerInterval
        """
        if value is None:
            return OperationsPerInterval(
                unit=self._ops_per_interval_unit, scale=self._ops_per_interval_scale, iterations=self._iterations)

        if not isinstance(value, OperationsPerInterval):
            raise SimpleBenchTypeError(
                f'Invalid ops_per_second type: {type(value)}. Must be of type OperationsPerInterval.',
                tag=ResultsErrorTag.OPS_PER_SECOND_INVALID_ARG_TYPE
            )
        return value

    def _validate_per_round_timings(self, value: OperationTimings | None) -> OperationTimings:
        """Validate the per_round_timings object if passed, or create a default one if None.

        The default OperationTimings object will have its iterations set to the same list
        of Iteration objects as the Results object and initialized with the values from
        `interval_unit` and `interval_scale` for unit and scale.

        Args:
            value (OperationTimings | None): The per_round_timings object to validate or None.

        Returns:
            OperationTimings: The validated or default OperationTimings object.

        Raises:
            SimpleBenchTypeError: If the value is not None and not of type OperationTimings
        """
        if value is None:
            return OperationTimings(unit=self._interval_unit, scale=self._interval_scale, iterations=self._iterations)

        if not isinstance(value, OperationTimings):
            raise SimpleBenchTypeError(
                f'Invalid per_round_timings type: {type(value)}. Must be of type OperationTimings.',
                tag=ResultsErrorTag.PER_ROUND_TIMINGS_INVALID_ARG_TYPE
            )
        return value

    def _validate_extra_info(self, value: dict[str, Any] | None) -> dict[str, Any]:
        """Validate the extra_info object if passed, or create a default one if None.

        Performs deep copy of the dictionary to help mitigate external mutation. This means
        that the extra_info dict must be deepcopy-able.

        Args:
            value (dict[str, Any] | None): The extra_info object to validate or None.

        Returns:
            dict[str, Any]: The validated or default extra_info dictionary.

        Raises:
            SimpleBenchTypeError: If the value is not None and not of type dict[str, Any]
        """
        if value is None:
            return {}

        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid extra_info type: {type(value)}. Must be of type dict[str, Any].',
                tag=ResultsErrorTag.EXTRA_INFO_INVALID_ARG_TYPE
            )

        # Perform deep copy to prevent external mutation
        return deepcopy(value)

    @property
    def group(self) -> str:
        """The reporting group to which the benchmark case belongs."""
        return self._group

    @property
    def title(self) -> str:
        """The name of the benchmark case."""
        return self._title

    @property
    def description(self) -> str:
        """A brief description of the benchmark case."""
        return self._description

    @property
    def n(self) -> int:
        """The number of rounds the benchmark ran per iteration."""
        return self._n

    @property
    def variation_cols(self) -> MappingProxyType[str, str]:
        """The columns to use for labelling kwarg variations in the benchmark."""
        return MappingProxyType(self._variation_cols)

    @property
    def variation_marks(self) -> MappingProxyType[str, Any]:
        """A dictionary of variation marks used to identify the benchmark variation."""
        return MappingProxyType(self._variation_marks)

    @property
    def interval_unit(self) -> str:
        """The unit of measurement for the interval (e.g. "ns")."""
        return self._interval_unit

    @property
    def interval_scale(self) -> float:
        """The scale factor for the interval (e.g. 1e-9 for nanoseconds)."""
        return self._interval_scale

    @property
    def ops_per_interval_unit(self) -> str:
        """The unit of measurement for operations per interval (e.g. "ops/s")."""
        return self._ops_per_interval_unit

    @property
    def ops_per_interval_scale(self) -> float:
        """The scale factor for operations per interval (e.g. 1.0 for ops/s)."""
        return self._ops_per_interval_scale

    @property
    def iterations(self) -> tuple[Iteration, ...]:
        """The tuple of Iteration objects representing each iteration of the benchmark."""
        return self._iterations

    @property
    def ops_per_second(self) -> OperationsPerInterval:
        """Statistics for operations per interval."""
        return self._ops_per_second

    @property
    def per_round_timings(self) -> OperationTimings:
        """Statistics for per-round timings."""
        return self._per_round_timings

    @property
    def memory(self) -> MemoryUsage:
        """Statistics for memory usage."""
        return self._memory

    @property
    def memory_unit(self) -> str:
        """The unit of measurement for memory usage (e.g. "bytes")."""
        return self._memory_unit

    @property
    def memory_scale(self) -> float:
        """The scale factor for memory usage (e.g. 1.0 for bytes)."""
        return self._memory_scale

    @property
    def peak_memory(self) -> PeakMemoryUsage:
        """Statistics for peak memory usage."""
        return self._peak_memory

    @property
    def total_elapsed(self) -> float:
        """The total elapsed time for the benchmark."""
        return self._total_elapsed

    @property
    def extra_info(self) -> dict[str, Any]:
        """Additional information about the benchmark run."""
        return deepcopy(self._extra_info)

    def results_section(self, section: Section) -> Stats:
        """Returns the requested section of the benchmark results.

        Args:
            section (Section): The section of the results to return. Must be Section.OPS or Section.TIMING.

        Returns:
            Stats: The requested section of the benchmark results.
        """
        if not isinstance(section, Section):
            raise SimpleBenchTypeError(
                f'Invalid section type: {type(section)}. Must be of type Section.',
                tag=ResultsErrorTag.RESULTS_SECTION_INVALID_SECTION_ARG_TYPE
            )
        match section:
            case Section.OPS:
                return self.ops_per_second
            case Section.TIMING:
                return self.per_round_timings
            case Section.MEMORY:
                return self.memory
            case Section.PEAK_MEMORY:
                return self.peak_memory
            case _:  # should be unreachable due to the enum type check above, but mypy needs this
                raise SimpleBenchValueError(
                    (f'Invalid section: {section}. Must be Section.OPS, Section.TIMING, '
                     'Section.MEMORY, or Section.PEAK_MEMORY.'),
                    tag=ResultsErrorTag.RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
                )

    def as_dict(self, full_data: bool = False) -> dict[str, Any]:
        '''Returns the benchmark results and statistics as a JSON-serializable dictionary.'''
        results_dict: dict[str, Any] = {
            'type': self.__class__.__name__,
            'group': self.group,
            'title': self.title,
            'description': self.description,
            'n': self.n,
            'variation_cols': dict(self.variation_cols),  # convert MappingProxyType to dict
            'interval_unit': self.interval_unit,
            'interval_scale': self.interval_scale,
            'ops_per_interval_unit': self.ops_per_interval_unit,
            'ops_per_interval_scale': self.ops_per_interval_scale,
            'memory_unit': self.memory_unit,
            'memory_scale': self.memory_scale,
            'total_elapsed': self.total_elapsed,
            'extra_info': self.extra_info,
            'per_round_timings': self.per_round_timings.stats_summary.as_dict,
            'ops_per_second': self.ops_per_second.stats_summary.as_dict,
            'memory': self.memory.stats_summary.as_dict,
            'peak_memory': self.peak_memory.stats_summary.as_dict,
        }
        if full_data:
            results_dict['per_round_timings'] = self.per_round_timings.as_dict
            results_dict['ops_per_second'] = self.ops_per_second.as_dict
            results_dict['memory'] = self.memory.as_dict
            results_dict['peak_memory'] = self.peak_memory.as_dict
        return results_dict

    def __repr__(self) -> str:
        """Return a string representation of the Results object."""
        if self._repr_cache is None:
            self._repr_cache = self._generate_repr()
        return self._repr_cache

    def _generate_repr(self) -> str:
        """Generate the string representation of the Results object."""
        return (f'{self.__class__.__name__}('
                f'group={self.group!r}, '
                f'title={self.title!r}, '
                f'description={self.description!r}, '
                f'n={self.n!r}, '
                f'variation_cols={self.variation_cols!r}, '
                f'variation_marks={self.variation_marks!r}, '
                f'interval_unit={self.interval_unit!r}, '
                f'interval_scale={self.interval_scale!r}, '
                f'ops_per_interval_unit={self.ops_per_interval_unit!r}, '
                f'ops_per_interval_scale={self.ops_per_interval_scale!r}, '
                f'memory_unit={self.memory_unit!r}, '
                f'memory_scale={self.memory_scale!r}, '
                f'total_elapsed={self.total_elapsed!r}, '
                f'iterations={self.iterations!r}, '
                f'ops_per_second={self.ops_per_second!r}, '
                f'per_round_timings={self.per_round_timings!r}, '
                f'memory={self.memory!r}, '
                f'peak_memory={self.peak_memory!r}, '
                f'extra_info={self.extra_info!r})')
