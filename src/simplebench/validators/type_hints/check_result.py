"""CheckResult type alias for type hint validation results."""
from typing import NamedTuple


class CheckResult(NamedTuple):
    """Contains the result of a type hint validation check."""
    valid: bool
    """Indicates if the object matches the type hint."""
    immutable: bool
    """Indicates if the object is immutable according to validation rules."""

__all__ = ('CheckResult',)
