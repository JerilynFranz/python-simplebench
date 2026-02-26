"""Base class for all PythonInfo classes."""

from abc import ABC

from ._environment import BaseEnvironment

__all__: list[str] = []


class BasePythonInfo(BaseEnvironment, ABC):
    """Base class for all PythonInfo classes."""
