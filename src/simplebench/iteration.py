# -*- coding: utf-8 -*-
"""Iteration class"""

from dataclasses import dataclass

from .constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
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
    '''
    n: int = 1
    elapsed: float = 0.0
    unit: str = DEFAULT_INTERVAL_UNIT
    scale: float = DEFAULT_INTERVAL_SCALE

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
