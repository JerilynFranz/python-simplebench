"""Constants used in type hint validation."""

from typing import Final, Literal

_IS_VALID: Final[Literal[True]] = True
"""Indicates that the object matches the type hint."""
_IS_IMMUTABLE: Final[Literal[True]] = True
"""Indicates that the object is immutable according to a check."""
_NOT_VALID: Final[Literal[False]] = False
"""Indicates that the object does not match the type hint."""
_NOT_IMMUTABLE: Final[Literal[False]] = False
"""Indicates that the object is not immutable according to a check."""

__all__ = ("_IS_IMMUTABLE", "_IS_VALID", "_NOT_IMMUTABLE", "_NOT_VALID")
