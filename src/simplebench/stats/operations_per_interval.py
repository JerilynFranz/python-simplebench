# -*- coding: utf-8 -*-
"""Container for OperationsPerInterval benchmark statistics"""
from __future__ import annotations
from typing import Optional, Sequence, Any

from . import Stats
from ..constants import DEFAULT_OPS_PER_INTERVAL_UNIT, DEFAULT_OPS_PER_INTERVAL_SCALE
from ..iteration import Iteration


class OperationsPerInterval(Stats):
    '''Container for the operations per time interval statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        data: Sequence[int | float] = List of data points. (read only)
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_OPS_PER_INTERVAL_UNIT,
                 scale: float = DEFAULT_OPS_PER_INTERVAL_SCALE,
                 data: Optional[Sequence[int | float]] = None) -> None:
        """Construct OperationsPerInterval stats from Iteration or raw ops data.

        Args:
            iterations (list[Iteration] | None): List of Iteration objects to extract ops data from.
            unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
            scale (float): The scale factor for the interval (e.g. 1 for seconds).
            data (Optional[list[int | float]]): Optional list of ops data points. If not provided,
                ops data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if not data:
            data = []
        if not data and iterations is not None:
            data = [iteration.ops_per_second for iteration in iterations]
        super().__init__(unit=unit, scale=scale, data=data)

    @classmethod
    def from_dict(cls,
                  data: dict[str, Any],
                  unit: Optional[str] = 'ops/s',
                  scale: Optional[int | float] = 1.0) -> OperationsPerInterval:
        """Construct an OperationsPerInterval object from a dictionary.

        By default, the unit is "ops/s" and the scale is 1.0. If provided in the dictionary,
        those values will override the defaults.

        Example:
            ops_dict = {
                "unit": "ops/s",
                "scale": 1,
                "data": [1000, 2000, 1500, 3000, 2500]
            }
            ops_stats = OperationsPerInterval.from_dict(ops_dict)
            print(ops_stats.mean)  # Output: 2000.0

        Args:
            data (dict): A dictionary containing the ops data. Must contain 'data' key with a non-empty
                sequence of data points consisting of integers or floats.
            unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). Defaults to "ops/s".
            scale (int | float): The scale factor for the interval (e.g. 1 for seconds). Defaults to 1.0.
        Returns:
            OperationsPerInterval: An OperationsPerInterval object constructed from the provided dictionary.
        Raises:
            SimpleBenchTypeError: If the data, unit, or scale arguments are of the wrong type.
            SimpleBenchKeyError: If the data dictionary does not contain a 'unit' key and
                no unit argument is provided.
            SimpleBenchValueError: If the data dictionary does not contain a non-empty 'data' key
                with at least one data point, if the scale argument is not greater than zero,
                or if the unit argument is an empty string.
        """
        return super().from_dict(data=data, unit=unit, scale=scale)  # type: ignore[return]
