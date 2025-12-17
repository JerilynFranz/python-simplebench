"""ErrorTags for simplebench.iterations in SimpleBench."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _IterationErrorTag(ErrorTag):
    """ErrorTags for simplebench.iterations in SimpleBench."""
    VALUES_ARG_INVALID_SEQUENCE_TYPE = "VALUES_ARG_INVALID_SEQUENCE_TYPE"
    """Invalid values argument passed to the Iteration() constructor
    - must be a dictionary or sequence of Value tuples"""
    VALUES_ARG_UNREGISTERED_METRIC = "VALUES_ARG_UNREGISTERED_METRIC"
    """Invalid values argument passed to the Iteration() constructor - must contain only registered Metrics"""
    N_ARG_TYPE = "N_ARG_TYPE"
    """Invalid n argument passed to the Iteration() constructor - must be an int or float"""
    N_ARG_VALUE = "N_ARG_VALUE"
    """Invalid n argument passed to the Iteration() constructor - must be greater than zero"""
    ROUNDS_ARG_TYPE = "ROUNDS_ARG_TYPE"
    """Invalid rounds argument passed to the Iteration() constructor - must be an int"""
    ROUNDS_ARG_VALUE = "ROUNDS_ARG_VALUE"
    """Invalid rounds argument passed to the Iteration() constructor - must be greater than zero"""
    VALUES_ARG_TYPE = "VALUES_ARG_TYPE"
    """Invalid values argument passed to the Iteration() constructor - must be a dict of float or int"""
    VALUES_ARG_EMPTY = "VALUES_ARG_EMPTY"
    """Invalid values argument passed to the Iteration() constructor - must not be an empty dict"""
    VALUES_ARG_INVALID_METRIC_TYPE = "VALUES_ARG_INVALID_METRIC_TYPE"
    """Invalid values argument passed to the Iteration() constructor - all keys must be Metrics"""
    VALUES_ARG_INVALID_VALUE_TYPE = "VALUES_ARG_INVALID_VALUE_TYPE"
    """Invalid values argument passed to the Iteration() constructor - all values must be float or int"""
    METRIC_INVALID_METRIC_ARG_TYPE = "METRIC_INVALID_METRIC_ARG_TYPE"
    """Invalid metric argument passed to the Iteration.metric() method - must be a MetricDefinition"""
