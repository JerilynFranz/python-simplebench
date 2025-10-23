"""ErrorTags for the simplebench.stats.operations_per_interval module."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class OperationsPerIntervalErrorTag(ErrorTag):
    """Error tags for the OperationsPerInterval class."""
    INVALID_ITERATIONS_ARG_TYPE = "INVALID_ITERATIONS_ARG_TYPE"
    """Invalid iterations argument passed to the OperationsPerInterval() constructor
    - must be a Sequence of Iteration objects or None"""
    INVALID_ITERATIONS_ITEM_ARG_TYPE = "INVALID_ITERATIONS_ITEM_ARG_TYPE"
    """Invalid type of item passed to the OperationsPerInterval() constructor in the iterations argument
    - all items must be Iteration objects"""
    INVALID_DATA_ARG_TYPE = "INVALID_DATA_ARG_TYPE"
    """Invalid data argument passed to the OperationsPerInterval() constructor
    - must be a sequence of numbers (int or float) or None"""
    INVALID_DATA_ARG_VALUE = "INVALID_DATA_ARG_VALUE"
    """Invalid data argument value passed to the OperationsPerInterval() constructor
    - must be a non-empty sequence of numbers (int or float)"""
    NO_DATA_OR_ITERATIONS_PROVIDED = "NO_DATA_OR_ITERATIONS_PROVIDED"
    """No data or iterations provided to the OperationsPerInterval() constructor"""
