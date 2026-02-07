"""Timeout package for the simplebench project."""
# ruff: noqa: F401

from ._error_tags import _TimeoutErrorTag
from .enums import TimeoutState
from .thread_id import ThreadId
from .timeout import Timeout

__all__ = ['ThreadId', 'Timeout', 'TimeoutState']
