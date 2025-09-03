# -*- coding: utf-8 -*-
"""Iteration class"""

from dataclasses import dataclass

from .constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT


@dataclass(kw_only=True)
class Iteration:
    '''Container for the results of a single benchmark iteration.

    Properties:
        n (int): The number of rounds performed in the iteration.
        elapsed (float): The elapsed time for the operations.
        unit (str): The unit of measurement for the elapsed time.
        scale (float): The scale factor for the elapsed time.
        ops_per_second (float): The number of operations per second. (read only)
        per_round_elapsed (float): The mean time for a single round scaled to the base unit. (read only)
    '''
    n: int = 0
    elapsed: int = 0
    unit: str = DEFAULT_INTERVAL_UNIT
    scale: float = DEFAULT_INTERVAL_SCALE

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
        return self.elapsed * self.scale / self.n if self.n else 0.0

    @property
    def ops_per_second(self) -> float:
        '''The number of operations per second.

        This is calculated as the inverse of the elapsed time.

        The edge cases of 0 elapsed time or n results in a returned value of 0.
        This would otherwise be an impossible value and so flags a measurement error.
        '''
        if not self.elapsed:
            return 0
        return self.n / (self.elapsed * self.scale)
