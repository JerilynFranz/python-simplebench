"""Base class for all PythonInfo classes."""
from abc import ABC

from simplebench.base import Hydrator

from .environment import Environment


class BasePythonInfo(Environment, Hydrator, ABC):
    """Base class for all PythonInfo classes."""
