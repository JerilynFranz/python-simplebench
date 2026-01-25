"""Benchmark case state definitions."""
from enum import Enum

from simplebench.doc_utils import enum_docstrings


@enum_docstrings
class CaseState(str, Enum):
    """States of a benchmark case during its lifecycle.

    Defined Case States are:
      - PENDING: The benchmark case is pending execution.
      - RUNNING: The benchmark case is currently running.
      - COMPLETED: The benchmark case has completed successfully.
      - FAILED: The benchmark case has failed during execution.
      - TIMED_OUT: The benchmark case has timed out during execution.

    """

    PENDING = "PENDING"
    """The benchmark case is pending execution."""
    RUNNING = "RUNNING"
    """The benchmark case is currently running."""
    COMPLETED = "COMPLETED"
    """The benchmark case has completed successfully."""
    FAILED = "FAILED"
    """The benchmark case has failed during execution."""
    TIMED_OUT = "TIMED_OUT"
    """The benchmark case has timed out during execution."""
