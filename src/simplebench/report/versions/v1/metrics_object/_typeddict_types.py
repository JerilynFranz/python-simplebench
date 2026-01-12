"""Typed dictionaries for the V1 MetricsObject data structure.

This module defines two distinct dictionary types for handling MetricsObject data,
both modeled on the JSON schema for version 1 MetricsObject in
version 1: :class:`~simplebench.report.versions.v1.results_info.results_info_schema.MetricsObjectSchema`.

    - `MetricsObjectData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `MetricsObjectDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.

    These types ensure proper validation and serialization of MetricsObject data
"""
import sys
from collections.abc import Mapping
from typing import TypeAlias

from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict

from .._raw_data_block._raw_data_block_dict import RawDataBlockData, RawDataBlockDict
from .._stats_block._stats_block_dict import StatsBlockData, StatsBlockDict
from .._value_block._value_block_dict import ValueBlockData, ValueBlockDict

if sys.version_info >= (3, 11):
    from typing import Required
else:
    from typing_extensions import Required

MetricDataTypes: TypeAlias = ValueBlockData | StatsBlockData | RawDataBlockData
MetricDictTypes: TypeAlias = ValueBlockDict | StatsBlockDict | RawDataBlockDict

# --- For data used as INPUT (e.g., to `from_dict`) ---

class MetricsObjectData(ReportElementTypedDict, total=True):
    """Typed dictionary for V1 MetricsObject data used as INPUT.
        
    :param Required[Mapping[str, MetricDataTypes]] metrics: The metrics object data.
    """
    metrics: Required[Mapping[str, MetricDataTypes]]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class MetricsObjectDict(ReportElementTypedDict, total=True):
    """Typed dictionary for the JSON representation of a V1 MetricsObject (OUTPUT).

    :param Required[Mapping[str, MetricDictTypes]] metrics: The metrics object data.
    """
    metrics: Required[Mapping[str, MetricDictTypes]]
