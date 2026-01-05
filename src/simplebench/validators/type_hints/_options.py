"""Options for type hint validation functions."""
from typing import NamedTuple


class Options(NamedTuple):
    """Options for type hint validation functions.

    :property bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :property int depth: The recursion depth for nested structures.
    :property bool consume_iterators: Whether to consume iterators during validation.
    """
    strict_typed_dict: bool = False
    """Whether to enforce that TypedDict checks require actual TypedDict instances."""
    depth: int = 0
    """The recursion depth for nested structures."""
    consume_iterators: bool = False
    """Whether to consume iterators during validation."""

__all__ = ('Options',)
