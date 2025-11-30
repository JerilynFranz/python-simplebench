"""Report fields for CSV reporter."""
from enum import Enum

from simplebench.enums import enum_docstrings


@enum_docstrings
class CSVField(str, Enum):
    """Fields available for CSV reporter output."""
    N = "N"
    """The O() complexity value."""
    ITERATIONS = "Iterations"
    """The number of iterations performed."""
    ROUNDS = "Rounds"
    """The number of rounds performed."""
    ELAPSED_SECONDS = "Elapsed Seconds"
    """The total elapsed time in seconds."""
    MEAN = "mean"
    """The statistical mean value."""
    MEDIAN = "median"
    """The statistical median value."""
    MIN = "min"
    """The statistical minimum value."""
    MAX = "max"
    """The statistical maximum value."""
    P5 = "5th"
    """The statistical 5th percentile."""
    P95 = "95th"
    """The statistical 95th percentile."""
    STD_DEV = "std dev"
    """The adjusted standard deviation of operation times."""
    RSD_PERCENT = "rsd%"
    """The relative standard deviation percentage."""
