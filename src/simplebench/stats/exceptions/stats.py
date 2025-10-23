"""ErrorTags for the simplebench.stats module."""
from simplebench.exceptions.base import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class StatsErrorTag(ErrorTag):
    """ErrorTags for the Stats class."""
    INVALID_UNIT_ARG_TYPE = "INVALID_UNIT_ARG_TYPE"
    """Invalid unit argument passed to the Stats() constructor - must be a str"""
    INVALID_UNIT_ARG_VALUE = "INVALID_UNIT_ARG_VALUE"
    """Invalid unit argument passed to the Stats() constructor - must be a non-empty str"""
    INVALID_SCALE_ARG_TYPE = "INVALID_SCALE_ARG_TYPE"
    """Invalid scale argument passed to the Stats() constructor - must be a number (int or float)"""
    INVALID_SCALE_ARG_VALUE = "INVALID_SCALE_ARG_VALUE"
    """Invalid scale argument passed to the Stats() constructor - must be greater than zero"""
    INVALID_DATA_ARG_TYPE = "INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the Stats() constructor - must be a list of numbers (int or float) or None"""
    INVALID_DATA_ARG_ITEM_TYPE = "INVALID_DATA_ARG_ITEM_TYPE"
    """Invalid data argument item passed to the Stats() constructor - must be a number (int or float)"""
    COMPARISON_INCOMPATIBLE_SCALES = "COMPARISON_INCOMPATIBLE_SCALES"
    """Incompatible scales when comparing two Stats instances"""
    COMPARISON_INCOMPATIBLE_UNITS = "COMPARISON_INCOMPATIBLE_UNITS"
    """Incompatible units when comparing two Stats instances"""
    FROM_DICT_INVALID_DATA_ARG_TYPE = "FROM_DICT_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the Stats.from_dict() method - must be a dict"""
    FROM_DICT_MISSING_UNIT_KEY = "FROM_DICT_MISSING_UNIT_KEY"
    """Missing unit key in the data dictionary passed to the Stats.from_dict() method"""
    FROM_DICT_MISSING_SCALE_KEY = "FROM_DICT_MISSING_SCALE_KEY"
    """Missing scale key in the data dictionary passed to the Stats.from_dict() method"""
    FROM_DICT_MISSING_DATA_KEY = "FROM_DICT_MISSING_DATA_KEY"
    """Missing data key in the data dictionary passed to the Stats.from_dict() method"""


@enum_docstrings
class StatsSummaryErrorTag(ErrorTag):
    """ErrorTags for the StatsSummary class."""
    INVALID_UNIT_ARG_TYPE = "INVALID_UNIT_ARG_TYPE"
    """Invalid unit argument passed to the StatsSummary() constructor - must be a str"""
    INVALID_UNIT_ARG_VALUE = "INVALID_UNIT_ARG_VALUE"
    """Invalid unit argument passed to the StatsSummary() constructor - must be a non-empty str"""
    INVALID_SCALE_ARG_TYPE = "INVALID_SCALE_ARG_TYPE"
    """Invalid scale argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_SCALE_ARG_VALUE = "INVALID_SCALE_ARG_VALUE"
    """Invalid scale argument passed to the StatsSummary() constructor - must be greater than zero"""
    INVALID_MINIMUM_ARG_TYPE = "INVALID_MINIMUM_ARG_TYPE"
    """Invalid minimum argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_MAXIMUM_ARG_TYPE = "INVALID_MAXIMUM_ARG_TYPE"
    """Invalid maximum argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_MEAN_ARG_TYPE = "INVALID_MEAN_ARG_TYPE"
    """Invalid mean argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_MEDIAN_ARG_TYPE = "INVALID_MEDIAN_ARG_TYPE"
    """Invalid median argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_STANDARD_DEVIATION_ARG_TYPE = "INVALID_STANDARD_DEVIATION_ARG_TYPE"
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be a number (int or float)"""
    INVALID_STANDARD_DEVIATION_ARG_VALUE = "INVALID_STANDARD_DEVIATION_ARG_VALUE"
    """Invalid standard_deviation argument passed to the StatsSummary() constructor - must be a number (int or float)"""
    INVALID_RELATIVE_STANDARD_DEVIATION_ARG_TYPE = (
        "INVALID_RELATIVE_STANDARD_DEVIATION_ARG_TYPE")
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be a number (int or float)"""
    INVALID_RELATIVE_STANDARD_DEVIATION_ARG_VALUE = (
        "INVALID_RELATIVE_STANDARD_DEVIATION_ARG_VALUE")
    """Invalid relative_standard_deviation argument passed to the StatsSummary() constructor
    - must be greater than zero"""
    INVALID_PERCENTILES_ARG_TYPE = "INVALID_PERCENTILES_ARG_TYPE"
    """Invalid percentiles argument passed to the StatsSummary() constructor
    - must be a sequence of numbers (int or float)"""
    INVALID_PERCENTILES_ARG_VALUE = "INVALID_PERCENTILES_ARG_VALUE"
    """Invalid percentiles item passed to the StatsSummary() constructor in sequence
    - must be a number (int or float)"""
    FROM_DICT_INVALID_DATA_ARG_TYPE = "FROM_DICT_INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the StatsSummary.from_dict() method - must be a dict"""
    FROM_DICT_MISSING_KEY = "FROM_DICT_MISSING_KEY"
    """Missing key in the data dictionary passed to the StatsSummary.from_dict() method"""
    FROM_STATS_INVALID_STATS_ARG_TYPE = "FROM_STATS_INVALID_STATS_ARG_TYPE"
    """Invalid stats argument passed to the StatsSummary.from_stats() method - must be a Stats instance"""
