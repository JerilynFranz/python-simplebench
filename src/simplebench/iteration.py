# -*- coding: utf-8 -*-
"""Iteration class"""

from dataclasses import dataclass

from .constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from .enums import Section
from .exceptions import ErrorTag, SimpleBenchValueError, SimpleBenchTypeError


@dataclass(kw_only=True)
class Iteration:
    '''Container for the results of a single benchmark iteration.

    Properties:
        n (int): The number of rounds performed in the iteration. (defaults to 1)
        elapsed (float): The elapsed time for the operations. (defaults to 0.0)
        unit (str): The unit of measurement for the elapsed time. (defaults to 'ns')
        scale (float): The scale factor for the elapsed time. (defaults to 1e-9)
        ops_per_second (float): The number of operations per second. (read only)
        per_round_elapsed (float): The mean time for a single round scaled to the base unit. (read only)
        memory_usage (int): The memory usage in bytes. (defaults to 0)
        peak_memory_usage (int): The peak memory usage in bytes. (defaults to 0)
        custom_metric (float): The value of a custom metric. (defaults to 0.0)
    '''
    n: int = 1
    elapsed: float = 0.0
    unit: str = DEFAULT_INTERVAL_UNIT
    scale: float = DEFAULT_INTERVAL_SCALE
    memory_usage: int = 0  # in bytes
    peak_memory_usage: int = 0  # in bytes
    custom_metric: float | int = 0.0  # custom metric value

    def __post_init__(self):
        if not isinstance(self.n, int):
            raise SimpleBenchTypeError('n must be an int', tag=ErrorTag.ITERATION_INIT_N_ARG_TYPE)
        if self.n <= 0:
            raise SimpleBenchValueError('n must be positive', tag=ErrorTag.ITERATION_INIT_N_ARG_VALUE)
        if not isinstance(self.elapsed, float):
            raise SimpleBenchTypeError('elapsed must be a float', tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_TYPE)
        if self.elapsed < 0.0:
            raise SimpleBenchValueError('elapsed must be non-negative', tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_VALUE)
        if not isinstance(self.unit, str):
            raise SimpleBenchTypeError('unit must be a str', tag=ErrorTag.ITERATION_INIT_UNIT_ARG_TYPE)
        if not self.unit:
            raise SimpleBenchValueError('unit must be a non-empty str', tag=ErrorTag.ITERATION_INIT_UNIT_ARG_VALUE)
        if not isinstance(self.scale, float):
            raise SimpleBenchTypeError('scale must be a float', tag=ErrorTag.ITERATION_INIT_SCALE_ARG_TYPE)
        if self.scale <= 0.0:
            raise SimpleBenchValueError('scale must be a positive float', tag=ErrorTag.ITERATION_INIT_SCALE_ARG_VALUE)
        if not isinstance(self.memory_usage, int):
            raise SimpleBenchTypeError('memory_usage must be an int', tag=ErrorTag.ITERATION_INIT_MEMORY_ARG_TYPE)
        if not isinstance(self.peak_memory_usage, int):
            raise SimpleBenchTypeError('peak_memory_usage must be an int',
                                       tag=ErrorTag.ITERATION_INIT_PEAK_MEMORY_ARG_TYPE)
        if not isinstance(self.custom_metric, float):
            raise SimpleBenchTypeError('custom_metric must be an int or float',
                                       tag=ErrorTag.ITERATION_INIT_CUSTOM_METRIC_ARG_TYPE)

    @property
    def per_round_elapsed(self) -> float:
        '''The mean time for a single round scaled to the base unit.
        If elapsed is 0, returns 0.0

        The per round computation is the elapsed time divided by n
        where n is the number of rounds.

        The scaling to the base unit is done using the scale factor.
        This has the effect of converting the elapsed time into the base unit.
        For example, if the scale factor is 1e-9 then elapsed time in nanoseconds
        will be converted to seconds.

        Returns:
            The mean time for a single round scaled to the base unit.
        '''
        return self.elapsed * self.scale / self.n

    @property
    def ops_per_second(self) -> float:
        '''The number of operations per second.

        This is calculated as the inverse of the elapsed time.

        The edge cases of 0 elapsed time results in a returned value of 0.0
        This would otherwise be an impossible value and so flags a measurement error.
        '''
        if self.elapsed == 0.0:
            return 0.0
        return self.n / (self.elapsed * self.scale)

    @property
    def memory(self) -> int:
        '''The memory usage in bytes. This is the difference between the allocated
        memory before and after the action.

        The edge case of no memory allocated results in a returned value of 0
        '''
        return self.memory_usage

    @memory.setter
    def memory(self, value: int) -> None:
        if not isinstance(value, int):
            raise SimpleBenchTypeError('memory_usage must be an int',
                                       tag=ErrorTag.ITERATION_SET_MEMORY_ARG_TYPE)
        self.memory_usage = value

    @property
    def peak_memory(self) -> int:
        '''The peak memory usage in bytes.

        This is the maximum memory allocated during the action.
        '''
        return self.peak_memory_usage

    @peak_memory.setter
    def peak_memory(self, value: int) -> None:
        if not isinstance(value, int):
            raise SimpleBenchTypeError('peak_memory_usage must be an int',
                                       tag=ErrorTag.ITERATION_SET_PEAK_MEMORY_ARG_TYPE)
        self.peak_memory_usage = value

    @property
    def custom(self) -> float | int:
        '''The value of a custom metric.

        This can be used to store any additional metric that is relevant to the benchmark.
        '''
        return self.custom_metric

    @custom.setter
    def custom(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise SimpleBenchTypeError('custom_metric must be a float or int',
                                       tag=ErrorTag.ITERATION_SET_CUSTOM_METRIC_ARG_TYPE)
        self.custom_metric = value

    def iteration_section(self, section: Section) -> int | float:
        """Returns the requested section of the benchmark results.

        Args:
            section (Section): The section of the results to return. Must be Section.OPS or Section.TIMING.

        Returns:
            Stats: The requested section of the benchmark results.
        """
        if not isinstance(section, Section):
            raise SimpleBenchTypeError(
                f'Invalid section type: {type(section)}. Must be of type Section.',
                tag=ErrorTag.ITERATION_ITERATION_SECTION_INVALID_SECTION_ARG_TYPE
            )
        match section:
            case Section.OPS:
                return self.ops_per_second
            case Section.TIMING:
                return self.per_round_elapsed
            case Section.MEMORY:
                return self.memory_usage
            case Section.PEAK_MEMORY:
                return self.peak_memory_usage
            case Section.CUSTOM:
                return self.custom_metric
            case _:
                raise SimpleBenchValueError(
                    f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                    tag=ErrorTag.ITERATION_ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
                )
