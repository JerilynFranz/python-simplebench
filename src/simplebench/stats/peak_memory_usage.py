# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations
from typing import Optional, Sequence, Any

from . import Stats
from ..constants import DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT
from ..iteration import Iteration


class PeakMemoryUsage(Stats):
    '''Container for the peak memory usage statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the memory usage (e.g., "MB"). (read only)
        scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes). (read only)
        data: tuple[int | float, ...] = Tuple of peak memory usage data points. (read only)
        mean (float): The mean memory usage. (read only)
        median (float): The median memory usage. (read only)
        minimum (float): The minimum memory usage. (read only)
        maximum (float): The maximum memory usage. (read only)
        standard_deviation (float): The standard deviation of the memory usage. (read only)
        relative_standard_deviation (float): The relative standard deviation of the memory usage. (read only)
        percentiles (dict[int, float]): Percentiles of memory usage. (read only)
    '''
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_MEMORY_UNIT,
                 scale: float = DEFAULT_MEMORY_SCALE,
                 data: Optional[Sequence[int | float]] = None):
        """Construct PeakMemoryUsage stats from Iteration or raw memory data.
        Args:
            iterations (Sequence[Iteration] | None): Sequence of Iteration objects to extract peak memory data from.
            unit (str): The unit of measurement for the memory usage (e.g., "MB").
            scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes).
            data (Optional[Sequence[int | float]]): Optional Sequence of peak memory usage data points. If not provided,
                peak memory data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if not data:
            data = []
        if not data and iterations is not None:
            data = [iteration.peak_memory for iteration in iterations]
        super().__init__(unit=unit, scale=scale, data=data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PeakMemoryUsage:
        """Construct a PeakMemoryUsage object from a dictionary.

        By default, the unit is "bytes" and the scale is 1.0. If provided in the dictionary,
        those values will override the defaults.

        Example:
            ops_dict = {
                "unit": "bytes",
                "scale": 1,
                "data": [1000, 2000, 1500, 3000, 2500]
            }
            peak_memory_stats = PeakMemoryUsage.from_dict(ops_dict)
            print(peak_memory_stats.mean)  # Output: 2000.0

        Args:
            data (dict): A dictionary containing the ops data. Must contain 'data' key with a non-empty
                sequence of data points consisting of integers or floats.
            unit (str): The unit of measurement for the benchmark (e.g., "bytes"). Defaults to "bytes".
            scale (int | float): The scale factor for the interval (e.g. 1 for bytes). Defaults to 1.0.
        Returns:
            PeakMemoryUsage: A PeakMemoryUsage object constructed from the provided dictionary.
        Raises:
            SimpleBenchTypeError: If the data, unit, or scale arguments are of the wrong type.
            SimpleBenchKeyError: If the data dictionary does not contain a 'unit' key and
                no unit argument is provided.
            SimpleBenchValueError: If the data dictionary does not contain a non-empty 'data' key
                with at least one data point, if the scale argument is not greater than zero,
                or if the unit argument is an empty string.
        """
        return super().from_dict(data=data)  # type: ignore[return]
