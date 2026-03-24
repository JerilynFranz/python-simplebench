"""Typed Dict shape for Metric data."""
from typing import Literal, TypeAlias

from simplebench.report.base import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

from ..metric_type import ImmutableMetricTypeData, ImmutableMetricTypeDict, MetricTypeData, MetricTypeDict

__all__: list[str] = []

AllowedCategoryValues: TypeAlias = Literal['VALUE', 'STATS', 'RAW_DATA']

# --- For data used as INPUT (e.g., to `from_dict`) ---

class MetricData(ReportElementTypedDict):
    """Typed dictionary for Metric data.

    All fields except `hash_id`, `version`, and `type` are required.

    :param NotRequired[str] type: The type of the metric type schema. This is an optional field that can be used
        to identify the schema type of the data. For version 1 reports, this should always be
        'SimpleBenchMetricType::V1'.
    :param NotRequired[int] version: The version of the metric type schema. This is an optional field that can be used
        to identify the schema version of the data. For version 1 reports, this should always be 1.
    :param NotRequired[str] hash_id: The unique hash identifier for the metric type. This is an optional
    field that can
        be used to uniquely identify the metric type. If not provided, it will be generated based on
        the other fields of the metric type.
    :param Required[str] label: A human-readable label for the metric.
    :param Required[str] title: A human-readable title for the metric.
    :param Required[str] description: A brief description of the metric.
    :param Required[MetricTypeData] metric_type: The MetricTypeData representing the type of

    """
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]
    label: Required[str]
    title: Required[str]
    description: Required[str]
    metric_type: Required[MetricTypeData]


class ImmutableMetricData(ReportElementTypedDict):
    """Immutable version of MetricData.

    The `__immutable__` field is included in the definition to signal that this dictionary
    is intended to be immutable. It is not used at runtime but serves
    as a class-level marker for type checkers and developers.
    It should never be set to any value.

    :param NotRequired[str] type: The type of the metric type schema. This is an optional field that can be used
        to identify the schema type of the data. For version 1 reports, this should always be
        'SimpleBenchMetricType::V1'.
    :param NotRequired[int] version: The version of the metric type schema. This is an optional field that can be used
        to identify the schema version of the data. For version 1 reports, this should always be 1.
    :param NotRequired[str] hash_id: The unique hash identifier for the metric type. This is an optional
        field that can be used to uniquely identify the metric type. If not provided, it will be generated based on
        the other fields of the metric type.
    :param Required[str] label: A human-readable label for the metric.
    :param Required[str] title: A human-readable title for the metric.
    :param Required[str] description: A brief description of the metric.
    :param Required[ImmutableMetricTypeData] metric_type: The ImmutableMetricTypeData representing
        the type of the metric.

    """
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]
    label: Required[str]
    title: Required[str]
    description: Required[str]
    metric_type: Required[ImmutableMetricTypeData]
    __immutable__: NotRequired[Never]

# --- OUTPUT (e.g., from `to_dict`) ---

class MetricDict(ReportElementTypedDict):
    """Typed dictionary for Metric data output (e.g., from `to_dict`).

    All fields are required.

    :param str type: The type of the metric type schema. For version 1 reports, this should always be
        'SimpleBenchMetricType::V1'.
    :param int version: The version of the metric type schema. For version 1 reports, this should always be 1.
    :param str hash_id: The unique hash identifier for the metric.
        This is a 64 byte hexadecimal string that can be used to identify the generator
        and uniqueness of the data.
    :param str label: A human-readable label for the metric.
    :param str title: A human-readable title for the metric.
    :param str description: A brief description of the metric.
    :param MetricTypeDict metric_type: The MetricTypeDict representing the type of the metric.
    """
    type: str
    version: int
    hash_id: str
    label: str
    title: str
    description: str
    metric_type: MetricTypeDict


class ImmutableMetricDict(ReportElementTypedDict):
    """Immutable version of MetricDict.

    The `__immutable__` field is included in the definition to signal that this dictionary
    is intended to be immutable. It is not used at runtime but serves
    as a class-level marker for type checkers and developers.
    It should never be set to any value.

    :param str type: The type of the metric type schema. For version 1 reports, this should always be
        'SimpleBenchMetricType::V1'.
    :param int version: The version of the metric type schema. For version 1 reports, this should always be 1.
    :param str hash_id: The unique hash identifier for the metric.
    :param str label: A human-readable label for the metric.
    :param str title: A human-readable title for the metric.
    :param str description: A brief description of the metric.
    :param ImmutableMetricTypeDict metric_type: The ImmutableMetricTypeDict representing the type of the metric.
    """
    type: str
    version: int
    hash_id: str
    label: str
    title: str
    description: str
    metric_type: ImmutableMetricTypeDict
    __immutable__: NotRequired[Never]
