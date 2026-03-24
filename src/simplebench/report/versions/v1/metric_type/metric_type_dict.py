"""Typed Dict shape for MetricType data."""
from typing import Literal, TypeAlias

from simplebench.report.base import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

__all__: list[str] = []

AllowedCategoryValues: TypeAlias = Literal['VALUE', 'STATS', 'RAW_DATA']

# --- For data used as INPUT (e.g., to `from_dict`) ---

class MetricTypeData(ReportElementTypedDict):
    """Typed dictionary for MetricType data.

    All fields except `hash_id` are required.

    :param NotRequired[str] type: The type of the metric type schema. This is an optional field that can be used
        to identify the schema type of the data. For version 1 reports, this should always be 
        'SimpleBenchMetricType::V1'.
    :param NotRequired[int] version: The version of the metric type schema. This is an optional field that can be used
        to identify the schema version of the data. For version 1 reports, this should always be 1.
    :param NotRequired[str] hash_id: The unique hash identifier for the metric type. This is an optional field that can
        be used to uniquely identify the metric type. If not provided, it will be generated based on
        the other fields of the metric type.
    :param Required[float] scale: The scale factor for the metric.
    :param Required[str] label: A human-readable label for the metric.
    :param Required[str] description: A brief description of the metric.
    :param Required[str] unit: The unit of measurement for the metric (e.g., 'seconds', 'bytes').
    :param Required[str] semantic_type: A string representing the semantic type of the metric, e.g.
        'simplebench_std::operations_per_second'.
    :param Required[str] category: The category of the metric, one of `VALUE`, `STATS`, or `RAW_DATA`.

    """
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]
    scale: Required[float]
    label: Required[str]
    description: Required[str]
    unit: Required[str]
    semantic_type: Required[str]
    category: Required[AllowedCategoryValues]


class ImmutableMetricTypeData(MetricTypeData):
    """Immutable version of MetricTypeData.

    The `__immutable__` field is included in the definition to signal that this dictionary
    is intended to be immutable. It is not used at runtime but serves
    as a class-level marker for type checkers and developers. It should never be set
    to any value.

    :param NotRequired[str] type: The type of the metric type schema. This is an optional field that can be used
        to identify the schema type of the data. For version 1 reports, this should always be
        'SimpleBenchMetricType::V1'.
    :param NotRequired[int] version: The version of the metric type schema. This is an optional field that can be used
        to identify the schema version of the data. For version 1 reports, this should always be 1.
    :param NotRequired[str] hash_id: The unique hash identifier for the metric type. This is an optional field that can be used to uniquely
        identify the metric type. If not provided, it will be generated based on the other fields of the metric type.
    :param Required[float] scale: The scale factor for the metric.
    :param Required[str] label: A human-readable label for the metric.
    :param Required[str] description: A brief description of the metric.
    :param Required[str] unit: The unit of measurement for the metric (e.g., 'seconds', 'bytes').
    :param Required[str] semantic_type: A string representing the semantic type of the metric, e.g.
        'simplebench_std::operations_per_second'.
    :param Required[str] category: The category of the metric, one of `VALUE`, `STATS`, or `RAW_DATA`.
    """
    __immutable__: NotRequired[Never]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class MetricTypeDict(ReportElementTypedDict):
    """Typed dictionary for MetricType output data.

    This is the same as MetricTypeData but is used for output purposes, such as when converting a
    MetricType instance to a dictionary for serialization. It includes all the same fields as MetricTypeData,
    except that hash_id, type, and version are now required in the output since they will always
    be generated for a MetricType instance, even if they were not provided in the input data.

    :param Required[str] type: The type of the metric type schema. For version 1 reports, this will always be
        'SimpleBenchMetricType::V1'.
    :param Required[int] version: The version of the metric type schema. For version 1 reports, this will always be 1.
    :param Required[str] hash_id: The unique hash identifier for the metric type. It is a unique identifier for the
        metric type. It will be generated based on the other fields of the metric type if not provided in the input
        data, but it is always included in the output data. identify the metric type.
    :param Required[float] scale: The scale factor for the metric.
    :param Required[str] label: A human-readable label for the metric.
    :param Required[str] description: A brief description of the metric.
    :param Required[str] unit: The unit of measurement for the metric (e.g., 'seconds', 'bytes').
    :param Required[str] semantic_type: A string representing the semantic type of the metric, e.g.
        'simplebench_std::operations_per_second'.
    :param Required[str] category: The category of the metric, one of `VALUE`, `STATS`, or `RAW_DATA`.
    """
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    scale: Required[float]
    label: Required[str]
    description: Required[str]
    unit: Required[str]
    semantic_type: Required[str]
    category: Required[AllowedCategoryValues]


class ImmutableMetricTypeDict(MetricTypeDict):
    """Immutable version of MetricTypeDict.

    The `__immutable__` field is included in the definition to signal that this dictionary
    is intended to be immutable. It is not used at runtime but serves
    as a class-level marker for type checkers and developers. It should never be set
    to any value.

    :param Required[str] type: The type of the metric type schema. For version 1 reports, this will always be
        'SimpleBenchMetricType::V1'.
    :param Required[int] version: The version of the metric type schema. For version 1 reports, this will always be 1.
    :param Required[str] hash_id: The unique hash identifier for the metric type. It is a unique identifier for the
        metric type. It will be generated based on the other fields of the metric type if not provided in the input
        data, but it is always included in the output data. identify the metric type.
    :param Required[float] scale: The scale factor for the metric.
    :param Required[str] label: A human-readable label for the metric.
    :param Required[str] description: A brief description of the metric.
    :param Required[str] unit: The unit of measurement for the metric (e.g., 'seconds', 'bytes').
    :param Required[str] semantic_type: A string representing the semantic type of the metric, e.g.
        'simplebench_std::operations_per_second'.
    :param Required[str] category: The category of the metric, one of `VALUE`, `STATS`, or `RAW_DATA`.
    """
    __immutable__: NotRequired[Never]
