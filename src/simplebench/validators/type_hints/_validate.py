"""Validation functions for type hints module

Use by importing _validate module and calling _validate.validation_function(arguments).
"""
import types
from collections.abc import Set
from typing import Any, TypeVar

from simplebench.exceptions import SimpleBenchValueError

from ._error_tags import _TypeHintsErrorTag


def resolve_forward_references_arg(resolve_forward_references: Any) -> None:
    """Check that the resolve_forward_references argument is a boolean.
    
    :raises SimpleBenchValueError: If resolve_forward_references is not a boolean.
    """
    if not isinstance(resolve_forward_references, bool):
        raise SimpleBenchValueError(
            f'resolve_forward_references must be a boolean, got {resolve_forward_references!r}.',
            tag=_TypeHintsErrorTag.INVALID_RESOLVE_FORWARD_REFERENCES)

def noncachable_types_arg(noncachable_types: Any) -> None:
    """Check that the noncachable_types argument is a set of types.
    
    :raises SimpleBenchValueError: If noncachable_types is not a `Set` of types or is `None`.
    """
    if noncachable_types is None:
        return
    if not isinstance(noncachable_types, Set) or not all(isinstance(t, type) for t in noncachable_types):
        raise SimpleBenchValueError(
            f'noncachable_types must be a Set of types, got {noncachable_types!r}.',
            tag=_TypeHintsErrorTag.INVALID_NONCACHABLE_TYPES)

def consume_iterators_arg(consume_iterators: Any) -> None:
    """Check that the consume_iterators argument is a boolean.
    
    :raises SimpleBenchValueError: If consume_iterators is not a boolean.
    """
    if not isinstance(consume_iterators, bool):
        raise SimpleBenchValueError(
            f'consume_iterators must be a boolean, got {consume_iterators!r}.',
            tag=_TypeHintsErrorTag.INVALID_CONSUME_ITERATORS)

def strict_typed_dict_arg(strict: Any) -> None:
    """Check that the strict_typed_dict argument is a boolean.
    
    :raises SimpleBenchValueError: If strict is not a boolean.
    """
    if not isinstance(strict, bool):
        raise SimpleBenchValueError(
            f'strict_typed_dict must be a boolean, got {strict!r}.',
            tag=_TypeHintsErrorTag.INVALID_STRICT_TYPED_DICT)


def depth_arg(depth: Any) -> None:
    """Check that the depth argument is a non-negative integer.
    
    :raises SimpleBenchValueError: If the depth is not a non-negative integer.
    """
    if not isinstance(depth, int) or depth < 0:
        raise SimpleBenchValueError(
            f'depth must be a non-negative integer, got {depth!r}.',
            tag=_TypeHintsErrorTag.NEGATIVE_DEPTH)

def type_hint_arg(type_hint: Any) -> None:
    """Check that the type hint is a type hint rather than a concrete type.
    
    :raises SimpleBenchValueError: If the type_hint is not a type hint.
    """
    if type_hint in {None, Any}:
        return
    if isinstance(type_hint, str):
        raise SimpleBenchValueError(
            'Type hint must not be a string.',
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
    if not (
        isinstance(type_hint, type)
        or hasattr(type_hint, '__origin__')
        or (hasattr(types, 'UnionType') and isinstance(type_hint, types.UnionType))
        or isinstance(type_hint, TypeVar)
        or hasattr(type_hint, '__supertype__')  # NewType
    ):
        raise SimpleBenchValueError(
            f'Type hint must be a type or generic alias, got {type(type_hint).__name__}.',
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
