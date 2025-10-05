# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations
from typing import Optional, Sequence, Any

from . import Stats
from ..constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from ..iteration import Iteration


class OperationTimings(Stats):
    '''Container for the operation timing statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the timings (e.g., "ns"). (read only)
        scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds). (read only)
        data: (tuple[int | float, ...]) = Tuple of timing data points. (read only)
        mean (float): The mean time per operation. (read only)
        median (float): The median time per operation. (read only)
        minimum (float): The minimum time per operation. (read only)
        maximum (float): The maximum time per operation. (read only)
        standard_deviation (float): The standard deviation of the time per operation. (read only)
        relative_standard_deviation (float): The relative standard deviation of the time per operation. (read only)
        percentiles (dict[int, float]): Percentiles of time per operation. (read only)
    '''
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 data: Optional[Sequence[int | float]] = None):
        """Construct OperationTimings stats from Iteration or raw timing data.

        Args:
            iterations (Sequence[Iteration] | None): Sequence of Iteration objects to extract timing data from.
            unit (str): The unit of measurement for the timings (e.g., "ns").
            scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds).
            data (Optional[Sequence[int | float]]): Optional Sequence of timing data points. If not provided,
                timing data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if not data:
            data = []
        if not data and iterations is not None:
            data = [iteration.per_round_elapsed for iteration in iterations]
        super().__init__(unit=unit, scale=scale, data=data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OperationTimings:
        """Construct an OperationTimings object from a dictionary.

        By default, the unit is "s" and the scale is 1.0. If provided in the dictionary,
        those values will override the defaults.

        Example:
            ops_dict = {
                "unit": "s",
                "scale": 1,
                "data": [1000, 2000, 1500, 3000, 2500]
            }
            timing_stats = OperationTimings.from_dict(ops_dict)
            print(timing_stats.mean)  # Output: 2000.0

        Args:
            data (dict): A dictionary containing the ops data. Must contain 'data' key with a non-empty
                sequence of data points consisting of integers or floats.

        Returns:
            OperationTimings: An OperationTimings object constructed from the provided dictionary.

        Raises:
            SimpleBenchTypeError: If the data, unit, or scale arguments are of the wrong type.
            SimpleBenchKeyError: If the data dictionary does not contain the 'unit', 'scale' or 'data' keys
            SimpleBenchValueError: If the data dictionary does not contain a non-empty 'data' key with at
                least one data point, if the scale argument is not greater than zero, or if the unit
                argument is an empty string.
        """
        return super().from_dict(data=data)  # type: ignore[return]
