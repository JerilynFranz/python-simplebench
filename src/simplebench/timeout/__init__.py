"""Timeout package for the simplebench project."""
# ruff: noqa: F401

from ._error_tags import _TimeoutErrorTag
from .enums import TimeoutState
from .timeout import Timeout

__all__: list[str] = []
