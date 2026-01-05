"""Validation state for type hint validation."""
from typing import Any, NamedTuple

__all__ = ('ValidationState',)


class ValidationState(NamedTuple):
    """Represents the state of a validation check for cycle detection.

    :property int obj_id: The ID of the object being checked.
    :property Any type_hint: The type hint being checked against.
    :property str context: The context of the validation check.
    """
    obj_id: int
    """The ID of the object being checked."""
    type_hint: Any
    """The type hint being checked against."""
    context: str
    """The context of the validation check."""
