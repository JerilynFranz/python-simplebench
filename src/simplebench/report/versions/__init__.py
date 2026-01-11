"""Versions package for SimpleBench reports.

Defined report versions are imported here for easy access.

Attributes:
    CURRENT_VERSION: The current report version module used by SimpleBench.
    v1: The module for report version 1.

"""

from . import v1

__all__ = []

CURRENT_VERSION = v1
"""The current report version module used by SimpleBench."""
