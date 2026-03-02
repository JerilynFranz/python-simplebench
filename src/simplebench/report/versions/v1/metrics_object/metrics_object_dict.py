"""Typed dictionaries for the V1 MetricsObject data structure.

This module defines four distinct dictionary types for handling MetricsObject data,
all modeled on the JSON schema for a MetricsObject as defined in the
version 1: :class:`~simplebench.report.versions.v1.ResultsInfoSchema`.

- :class:`MetricsObjectData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, allowing any mapping of strings to valid metric item data types.
- :class:`ImmutableMetricsObjectData`: An immutable variant of `MetricsObjectData` for
    type-checking purposes.
- :class:`MetricsObjectDict`: For use as OUTPUT (e.g., from `to_dict`). It is stricter, guaranteeing that all metric items are of the output dictionary types.
- :class:`ImmutableMetricsObjectDict`: An immutable variant of `MetricsObjectDict` for type-checking purposes.


    These types ensure proper validation and serialization of MetricsObject data
"""
from collections.abc import Mapping
from typing import TypeAlias

from simplebench.simplebench_types import CoreDataMapping

from ..raw_data_block import ImmutableRawDataBlockData, ImmutableRawDataBlockDict, RawDataBlockData, RawDataBlockDict
from ..stats_block import ImmutableStatsBlockData, ImmutableStatsBlockDict, StatsBlockData, StatsBlockDict
from ..value_block import ImmutableValueBlockData, ImmutableValueBlockDict, ValueBlockData, ValueBlockDict

__all__: list[str] = []

# --- Type aliases for metric item types ---

ImmutableMetricDataTypes: TypeAlias = ImmutableValueBlockData | ImmutableStatsBlockData | ImmutableRawDataBlockData
"""Type alias for the possible types of INPUT metric items in the immutable metrics data dictionary."""

MetricDataTypes: TypeAlias = ValueBlockData | StatsBlockData | RawDataBlockData | ImmutableMetricDataTypes
"""Type alias for the possible types of INPUT metric items in the metrics data dictionary."""

ImmutableMetricDictTypes: TypeAlias = ImmutableValueBlockDict | ImmutableStatsBlockDict | ImmutableRawDataBlockDict
"""Type alias for the possible types of OUTPUT metric items in the immutable metrics dictionary."""

MetricDictTypes: TypeAlias = ValueBlockDict | StatsBlockDict | RawDataBlockDict | ImmutableMetricDictTypes
"""Type alias for the possible types of OUTPUT metric items in the metrics dictionary."""

MetricsObjectData: TypeAlias = Mapping[str, MetricDataTypes]
"""Type alias for the dictionary type used as INPUT to create a MetricsObject via `from_dict`."""

ImmutableMetricsObjectData: TypeAlias = CoreDataMapping[CoreDataMapping]
"""Type alias for the dictionary type used as INPUT to create a MetricsObject via `from_dict`,
where all metric items are immutable."""

MetricsObjectDict: TypeAlias = Mapping[str, MetricDictTypes]
"""Type alias for the dictionary type returned by `to_dict` on a MetricsObject, where
all metric items are of the output dictionary types."""

ImmutableMetricsObjectDict: TypeAlias = CoreDataMapping[CoreDataMapping]
"""Type alias for the dictionary type returned by `to_dict` on a MetricsObject, where
all metric items are of the output dictionary types and the overall dictionary is immutable."""
