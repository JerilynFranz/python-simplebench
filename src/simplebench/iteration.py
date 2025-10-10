# -*- coding: utf-8 -*-
"""Iteration class"""
from .defaults import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from .enums import Section
from .exceptions import ErrorTag, SimpleBenchValueError, SimpleBenchTypeError
from .validators import (validate_non_blank_string, validate_int, validate_positive_int,
                         validate_positive_float, validate_non_negative_float)


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
        self._n = validate_positive_int(
                    n, 'n',
                    ErrorTag.ITERATION_N_ARG_TYPE,
                    ErrorTag.ITERATION_N_ARG_VALUE)
        self._unit = validate_non_blank_string(
                    unit, 'unit',
                    ErrorTag.ITERATION_UNIT_ARG_TYPE,
                    ErrorTag.ITERATION_UNIT_ARG_VALUE)
        self._scale = validate_positive_float(
                    scale, 'scale',
                    ErrorTag.ITERATION_SCALE_ARG_TYPE,
                    ErrorTag.ITERATION_SCALE_ARG_VALUE)
        self._elapsed = validate_non_negative_float(
            elapsed, 'elapsed',
            ErrorTag.ITERATION_ELAPSED_ARG_TYPE,
            ErrorTag.ITERATION_ELAPSED_ARG_VALUE)
        self._memory = validate_int(
            memory, 'memory',
            ErrorTag.ITERATION_MEMORY_ARG_TYPE)
        self._peak_memory = validate_int(
            peak_memory, 'peak_memory',
            ErrorTag.ITERATION_PEAK_MEMORY_ARG_TYPE)

    def __eq__(self, other: object) -> bool:
        """Check equality between two Iteration instances.

        Two Iteration instances are considered equal if all their attributes are equal.
        """
        if not isinstance(other, Iteration):
            return False
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

    @property
    def unit(self) -> str:
        '''The unit of measurement for the elapsed time.'''
        return self._unit

    @property
    def scale(self) -> float:
        '''The scale factor for the elapsed time.'''
        return self._scale

    @property
    def elapsed(self) -> float:
        '''The total elapsed time for the iteration in the specified unit.'''
        return self._elapsed

    @property
    def memory(self) -> int:
        '''The memory usage in bytes. This is the difference between the allocated
        memory before and after the action.

        The edge case of no memory allocated results in a returned value of 0
        '''
        return self._memory

    @property
    def peak_memory(self) -> int:
        '''The peak memory usage in bytes.

        This is the maximum memory allocated during the action.
        '''
        return self._peak_memory

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
            case _:  # needed for mypy
                raise SimpleBenchValueError(
                    f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                    tag=ErrorTag.ITERATION_ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
                )

    def __repr__(self) -> str:
        """Return a string representation of the Iteration instance."""
        unit = self.unit.replace("'", "\\'")
        return (f"Iteration(n={self.n}, elapsed={self.elapsed}, unit='{unit}', "
                f"scale={self.scale}, memory={self.memory}, peak_memory={self.peak_memory})")
