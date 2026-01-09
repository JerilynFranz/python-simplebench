"""Base class for all PythonInfo classes."""
from abc import ABC

from .environment import Environment


class BasePythonInfo(Environment, ABC):
    """Base class for all PythonInfo classes."""
