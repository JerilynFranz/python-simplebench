"""Calibration mode for simplebench."""

from enum import Enum

from simplebench.doc_utils import enum_docstrings


@enum_docstrings
class Calibrate(str, Enum):
    """Calibration mode for simplebench.

    Defined modes are:
      - WALL: Automatically calibrate the number of rounds for wall clock precision.
      - CPU: Automatically calibrate the number of rounds for CPU time precision.
    """

    WALL = 'wall'
    """Automatically calibrate the number of rounds for wall clock precision."""
    CPU = 'cpu'
    """Automatically calibrate the number of rounds for CPU time precision."""
