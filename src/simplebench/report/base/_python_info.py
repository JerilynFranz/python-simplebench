"""Base class for all PythonInfo classes."""

from abc import ABC

from ._environment import Environment

__all__: list[str] = []


class BasePythonInfo(Environment, ABC):
    """Base class for all PythonInfo classes."""
