# -*- coding: utf-8 -*-
"""Iteration class"""
from .constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from .enums import Section
from .exceptions import ErrorTag, SimpleBenchValueError, SimpleBenchTypeError


class Iteration:
    '''Container for the results of a single benchmark iteration.

    Properties:
        n (int): The number of rounds performed in the iteration. (defaults to 1)
        elapsed (float): The per round elapsed time for the operations. (defaults to 0.0)
        unit (str): The unit of measurement for the elapsed time. (defaults to DEFAULT_INTERVAL_UNIT: 'ns')
        scale (float): The scale factor for the elapsed time. (defaults to DEFAULT_INTERVAL_SCALE: 1e-9)
        ops_per_second (float): The number of operations per second. (read only)
        per_round_elapsed (float): The mean time for a single round scaled to the base unit. (read only)
        memory (int): The memory usage in bytes. (defaults to 0)
        peak_memory (int): The peak memory usage in bytes. (defaults to 0)
    '''
    __slots__ = ('_n', '_elapsed', '_unit', '_scale', '_memory', '_peak_memory')

    def __init__(self,
                 *,
                 n: int = 1,
                 elapsed: float = 0.0,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 memory: int = 0,  # in bytes
                 peak_memory: int = 0,  # in bytes
                 ) -> None:
        """"Initialize an Iteration instance.

        Args:
            n (int): The n weight for the iteration. Must be a positive integer. (default: 1)
            elapsed (float): The total elapsed time for the iteration in the specified unit.
                             Must be a non-negative float. (default: 0.0)
            unit (str): The unit of measurement for the elapsed time. Must be a non-empty string.
                        (default: DEFAULT_INTERVAL_UNIT: 'ns')
            scale (float): The scale factor for the elapsed time. Must be a positive float.
                           (default: DEFAULT_INTERVAL_SCALE: 1e-9)
            memory (int): The memory usage in bytes. Must be an integer. (default: 0)
            peak_memory (int): The peak memory usage in bytes. Must be an integer. (default: 0)

        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self.n = n
        self.unit = unit
        self.scale = scale
        self.elapsed = elapsed
        self.memory = memory  # in bytes
        self.peak_memory = peak_memory  # in bytes

    def __eq__(self, other: object) -> bool:
        """Check equality between two Iteration instances.

        Two Iteration instances are considered equal if all their attributes are equal.
        """
        if not isinstance(other, Iteration):
            return NotImplemented
        return (self.n == other.n and
                self.elapsed == other.elapsed and
                self.unit == other.unit and
                self.scale == other.scale and
                self.memory == other.memory and
                self.peak_memory == other.peak_memory)

    @property
    def n(self) -> int:
        '''The n weight of the iteration'''
        return self._n

    @n.setter
    def n(self, value: int) -> None:
        if not isinstance(value, int):
            raise SimpleBenchTypeError('n must be an int', tag=ErrorTag.ITERATION_SET_N_ARG_TYPE)
        if value <= 0:
            raise SimpleBenchValueError('n must be a positive int', tag=ErrorTag.ITERATION_SET_N_ARG_VALUE)
        self._n = value

    @property
    def unit(self) -> str:
        '''The unit of measurement for the elapsed time.'''
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        if not isinstance(value, str):
            raise SimpleBenchTypeError('unit must be a str', tag=ErrorTag.ITERATION_INIT_UNIT_ARG_TYPE)
        if value.strip() == "":
            raise SimpleBenchValueError('unit must be a non-empty str', tag=ErrorTag.ITERATION_INIT_UNIT_ARG_VALUE)
        self._unit = value

    @property
    def scale(self) -> float:
        '''The scale factor for the elapsed time.'''
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        if not isinstance(value, float):
            raise SimpleBenchTypeError('scale must be a float', tag=ErrorTag.ITERATION_INIT_SCALE_ARG_TYPE)
        if value <= 0.0:
            raise SimpleBenchValueError('scale must be a positive float', tag=ErrorTag.ITERATION_INIT_SCALE_ARG_VALUE)
        self._scale = value

    @property
    def elapsed(self) -> float:
        '''The total elapsed time for the iteration in the specified unit.'''
        return self._elapsed

    @elapsed.setter
    def elapsed(self, value: float) -> None:
        if not isinstance(value, float):
            raise SimpleBenchTypeError('elapsed must be a float', tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_TYPE)
        if value < 0.0:
            raise SimpleBenchValueError('elapsed must be non-negative', tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_VALUE)
        self._elapsed = value

    @property
    def memory(self) -> int:
        '''The memory usage in bytes. This is the difference between the allocated
        memory before and after the action.

        The edge case of no memory allocated results in a returned value of 0
        '''
        return self._memory

    @memory.setter
    def memory(self, value: int) -> None:
        if not isinstance(value, int):
            raise SimpleBenchTypeError('memory must be an int',
                                       tag=ErrorTag.ITERATION_SET_MEMORY_ARG_TYPE)
        self._memory = value

    @property
    def peak_memory(self) -> int:
        '''The peak memory usage in bytes.

        This is the maximum memory allocated during the action.
        '''
        return self._peak_memory

    @peak_memory.setter
    def peak_memory(self, value: int) -> None:
        if not isinstance(value, int):
            raise SimpleBenchTypeError('peak_memory must be an int',
                                       tag=ErrorTag.ITERATION_SET_PEAK_MEMORY_ARG_TYPE)
        self._peak_memory = value

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
        if self._elapsed == 0.0:
            return 0.0
        return self._n / (self._elapsed * self._scale)

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
                return self.memory
            case Section.PEAK_MEMORY:
                return self.peak_memory
            case _:
                raise SimpleBenchValueError(
                    f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                    tag=ErrorTag.ITERATION_ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
                )

    def __repr__(self) -> str:
        return (f"Iteration(n={self.n}, elapsed={self.elapsed}, unit='{self.unit}', "
                f"scale={self.scale}, memory={self.memory}, peak_memory={self.peak_memory})")

    def __str__(self) -> str:
        return (f"Iteration: n={self.n}, elapsed={self.elapsed} {self.unit}, "
                f"scale={self.scale}, ops_per_second={self.ops_per_second:.2f}, "
                f"per_round_elapsed={self.per_round_elapsed:.6f} s, "
                f"memory={self.memory} bytes, peak_memory={self.peak_memory} bytes)")
