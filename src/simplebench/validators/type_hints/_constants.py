"""Constants used in type hint validation."""

from typing import Final, Literal

IS_VALID: Final[Literal[True]] = True
"""Indicates that the object matches the type hint."""
IS_IMMUTABLE: Final[Literal[True]] = True
"""Indicates that the object is immutable according to a check."""
NOT_VALID: Final[Literal[False]] = False
"""Indicates that the object does not match the type hint."""
NOT_IMMUTABLE: Final[Literal[False]] = False
"""Indicates that the object is not immutable according to a check."""

__all__ = ("IS_IMMUTABLE", "IS_VALID", "NOT_IMMUTABLE", "NOT_VALID")
