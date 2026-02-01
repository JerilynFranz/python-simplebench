"""Typed dictionaries for the V1 MetricsObject data structure.

This module defines four distinct dictionary types for handling MetricsObject data,
all modeled on the JSON schema for a MetricsObject as defined in the
version 1: :class:`~simplebench.report.versions.v1.ResultsInfoSchema`.

    - `MetricsObjectData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `ImmutableMetricsObjectData`: An immutable version of `MetricsObjectData`.
    - `MetricsObjectDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
    - `ImmutableMetricsObjectDict`: An immutable version of `MetricsObjectDict`.

    These types ensure proper validation and serialization of MetricsObject data
"""

from collections.abc import Mapping
from types import MappingProxyType
from typing import TypeAlias

from simplebench.report.base import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

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

# --- For data used as INPUT (e.g., to `from_dict`) ---


class MetricsObjectData(ReportElementTypedDict, total=True):
    """Typed dictionary for V1 MetricsObject data used as INPUT.

    :param Required[Mapping[str, MetricDataTypes]] metrics: The metrics object data.
    """

    metrics: Required[Mapping[str, MetricDataTypes]]


class _RequiredImmutableMetricsObjectData(ReportElementTypedDict, total=True):
    """Typed dictionary for immutable V1 MetricsObject data used as INPUT.

    This class makes all fields and immutable to ensure immutability.


    :param Required[Mapping[str, ImmutableMetricDataTypes]] metrics: The metrics object data.
    """

    metrics: Required[Mapping[str, ImmutableMetricDataTypes]]


class ImmutableMetricsObjectData(_RequiredImmutableMetricsObjectData, total=False):
    """Typed dictionary for immutable V1 MetricsObject data used as INPUT.

    The `__immutable__` field is used to signal that this dictionary is immutable
    to type checking tools. It is a class-level marker and should never be set in instances.

    :param Required[MappingProxyType[str, ImmutableMetricDataTypes]] metrics: The metrics object data.
    """

    __immutable__: NotRequired[Never]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class MetricsObjectDict(ReportElementTypedDict, total=True):
    """Typed dictionary for the JSON representation of a V1 MetricsObject (OUTPUT).

    :param Required[Mapping[str, MetricDictTypes]] metrics: The metrics object data.
    """

    metrics: Required[Mapping[str, MetricDictTypes]]


class _RequiredImmutableMetricsObjectDict(ReportElementTypedDict, total=True):
    """Typed dictionary for the immutable JSON representation of a V1 MetricsObject (OUTPUT).

    This class makes all fields and immutable to ensure immutability.

    The `__immutable__` field is used to signal that this dictionary is immutable
    to type checking tools. It is a class-level marker and should never be set in instances.

    :param Required[MappingProxyType[str, ImmutableMetricDictTypes]] metrics: The metrics object data.
    """

    metrics: Required[MappingProxyType[str, ImmutableMetricDictTypes]]


class ImmutableMetricsObjectDict(_RequiredImmutableMetricsObjectDict, total=False):
    """Typed dictionary for the immutable JSON representation of a V1 MetricsObject (OUTPUT).

    The `__immutable__` field is used to signal that this dictionary is immutable
    to type checking tools. It is a class-level marker and should never be set in instances.

    :param Required[MappingProxyType[str, ImmutableMetricDictTypes]] metrics: The metrics object data.
    """

    __immutable__: NotRequired[Never]
