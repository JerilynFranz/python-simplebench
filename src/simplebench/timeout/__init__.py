"""Timeout package for the simplebench project."""
from .enums import TimeoutState
from .exceptions import _TimeoutErrorTag
from .timeout import Timeout

__all__ = [
    "Timeout",
    "_TimeoutErrorTag",
    "TimeoutState",
]
