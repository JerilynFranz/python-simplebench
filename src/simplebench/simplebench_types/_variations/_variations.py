"""Types used by SimpleBench for variations

- :class:`VariationColsType` for variation columns used in SimpleBench.
- :class:`ImmutableVariationColsType` for immutable variation columns used in SimpleBench.
- :class:`VariationMarksType` all fields for parameterizing a single variation.
- :class:`ImmutableVariationMarksType` immutable version of :class:`VariationMarksType`.
- :class:`KWArgsVariationsType` for multiple variations of fields for benchmark cases.
- :class:`ImmutableKWArgsVariationsType` immutable version of :class:`KWArgsVariationsType`.

"""
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import TypeAlias

from .._mark import Mark

VariationColsType: TypeAlias = Mapping[str, str]
"""Type alias for variation columns used in SimpleBench.

Maps variation field names to the string used to represent that field in reports.

Example:

.. code-block:: python
    variation_cols: VariationColsType = {
        "input_size": "Input Size",
        "algorithm": "Algorithm",
    }

"""

ImmutableVariationColsType: TypeAlias = MappingProxyType[str, str]
"""Immutable version of :class:`VariationColsType`."""

KWArgsVariationsType: TypeAlias = Mapping[str, Sequence[Mark]]
"""Type alias for kwarg variations used in SimpleBench cases for multiple variations.

Example:

.. code-block:: python
    kwarg_variations: KWArgsVariationsType = {
        "input_size": [
            Mark(label="Small", value=1000),
            Mark(label="Medium", value=10000),
            Mark(label="Large", value=1000000),
        ],
        "algorithm": [
            Mark(label="BubbleSort", value="bubble_sort"),
            Mark(label="QuickSort", value="quick_sort"),
            Mark(label="MergeSort", value="merge_sort"),
        ],
    }

"""

ImmutableKWArgsVariationsType: TypeAlias = MappingProxyType[str, Sequence[Mark]]
"""Immutable version of :class:`KWArgsVariationsType`."""
