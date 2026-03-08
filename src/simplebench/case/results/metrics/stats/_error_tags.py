"""ErrorTags for the simplebench.stats module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions.error_tag import ErrorTag


@enum_docstrings
class _StatsErrorTag(ErrorTag):
    """ErrorTags for the Stats class."""

    INVALID_TIMER_ARG_TYPE = auto()
    """Timer arg must be a str"""
    INVALID_METRIC_CATEGORY = auto()
    """Must be a :data:`MetricCategory.STATISTICAL` Metric"""
    INVALID_FULL_DATA_ARG_TYPE = auto()
    """Invalid full_data argument passed - must be a bool"""
    EMPTY_DATA_ARG = auto()
    """Empty data argument passed to the Stats() constructor"""
    INVALID_METRIC_ARG_TYPE = auto()
    """Invalid metric argument passed to the Stats() constructor - must be a :class:`~simplebench.metrics.Metric`"""
    UNREGISTERED_METRIC = auto()
    """Metric not registered in the metrics registry"""
    INVALID_UNIT_ARG_TYPE = auto()
    """Invalid unit argument passed to the Stats() constructor - must be a str"""
    INVALID_UNIT_ARG_VALUE = auto()
    """Invalid unit argument passed to the Stats() constructor - must be a non-empty str"""
    INVALID_SCALE_ARG_TYPE = auto()
    """Invalid scale argument passed to the Stats() constructor - must be a number (int or float)"""
    INVALID_SCALE_ARG_VALUE = auto()
    """Invalid scale argument passed to the Stats() constructor - must be greater than zero"""
    INVALID_ROUNDS_ARG_TYPE = auto()
    """Invalid rounds argument passed to the Stats() constructor - must be an int"""
    INVALID_ROUNDS_ARG_VALUE = auto()
    """Invalid rounds argument passed to the Stats() constructor - must be greater than zero"""
    INVALID_DATA_ARG_TYPE = auto()
    """Invalid data argument passed to the Stats() constructor - must be a Values instance"""
    INVALID_DATA_ARG_ITEM_TYPE = auto()
    """Invalid data argument item passed to the Stats() constructor - must be a number (int or float)"""
    COMPARISON_INCOMPATIBLE_SCALES = auto()
    """Incompatible scales when comparing two Stats instances"""
    COMPARISON_INCOMPATIBLE_UNITS = auto()
    """Incompatible units when comparing two Stats instances"""
    FROM_DICT_INVALID_DATA_ARG_TYPE = auto()
    """Invalid data argument passed to the Stats.from_dict() method - must be a dict"""
    FROM_DICT_MISSING_UNIT_KEY = auto()
    """Missing unit key in the data dictionary passed to the Stats.from_dict() method"""
    FROM_DICT_MISSING_SCALE_KEY = auto()
    """Missing scale key in the data dictionary passed to the Stats.from_dict() method"""
    FROM_DICT_MISSING_ROUNDS_KEY = auto()
    """Missing rounds key in the data dictionary passed to the Stats.from_dict() method"""
    FROM_DICT_MISSING_DATA_KEY = auto()
    """Missing data key in the data dictionary passed to the Stats.from_dict() method"""


@enum_docstrings
class _StatsSummaryErrorTag(ErrorTag):
    """ErrorTags for the StatsSummary class."""

    INVALID_UNIT_ARG_TYPE = auto()
    """Invalid unit argument passed to the StatsSummary() constructor - must be a str"""
    INVALID_UNIT_ARG_VALUE = auto()
    """Invalid unit argument passed to the StatsSummary() constructor - must be a non-empty str"""
    INVALID_SCALE_ARG_TYPE = auto()
    """Invalid scale argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_SCALE_ARG_VALUE = auto()
    """Invalid scale argument passed to the StatsSummary() constructor - must be greater than zero"""
    INVALID_ROUNDS_ARG_TYPE = auto()
    """Invalid rounds argument passed to the StatsSummary() constructor - must be an int"""
    INVALID_ROUNDS_ARG_VALUE = auto()
    """Invalid rounds argument passed to the StatsSummary() constructor - must be greater than zero"""
    INVALID_MINIMUM_ARG_TYPE = auto()
    """Invalid minimum argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_MAXIMUM_ARG_TYPE = auto()
    """Invalid maximum argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_MEAN_ARG_TYPE = auto()
    """Invalid mean argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_MEDIAN_ARG_TYPE = auto()
    """Invalid median argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_STANDARD_DEVIATION_ARG_TYPE = auto()
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be a number (int or float)"""
    INVALID_STANDARD_DEVIATION_ARG_VALUE = auto()
    """Invalid standard_deviation argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_RELATIVE_STANDARD_DEVIATION_ARG_TYPE = auto()
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be a number (int or float)"""
    INVALID_RELATIVE_STANDARD_DEVIATION_ARG_VALUE = auto()
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be greater than zero"""
    INVALID_PERCENTILES_ARG_TYPE = auto()
    """Invalid percentiles argument passed to the StatsSummary() constructor
    - must be a sequence of numbers (int or float)"""
    INVALID_PERCENTILES_ARG_VALUE = auto()
    """Invalid percentiles item passed to the StatsSummary() constructor in sequence
    - must be a number (int or float)"""
    FROM_DICT_INVALID_DATA_ARG_TYPE = auto()
    """Invalid data argument passed to the StatsSummary.from_dict() method - must be a dict"""
    FROM_DICT_MISSING_KEY = auto()
    """Missing key in the data dictionary passed to the StatsSummary.from_dict() method"""
    FROM_STATS_INVALID_STATS_ARG_TYPE = auto()
    """Invalid stats argument passed to the StatsSummary.from_stats() method - must be a Stats instance"""
    FROM_DICT_MISSING_ROUNDS_KEY = auto()
    """Missing rounds key in the data dictionary passed to the StatsSummary.from_dict() method"""
