"""Base class for all PythonInfo classes."""

from abc import ABC

from ._environment import Environment

__all__ = []


class BasePythonInfo(Environment, ABC):
    """Base class for all PythonInfo classes."""
