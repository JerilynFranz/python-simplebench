"""Helper function to validate primitive types against type hints."""
from collections.abc import Hashable
from types import UnionType
from typing import TYPE_CHECKING, Any, Literal, Union, get_args, get_origin

from simplebench.exceptions import SimpleBenchTypeError

from ._error_tags import _TypeHintsErrorTag

if TYPE_CHECKING:
    from .check_result import CheckResult
    from .options import Options
    from .validation_state import ValidationState


def _check_primitive_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if a primitive object is an instance of a given type hint.

    :param Any obj: The primitive object to check.
    :param Any type_hint: The type hint to check against.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    from .type_hints import (  # pylint: disable=import-outside-toplevel
        _CACHE,
        _IMMUTABLE,
        _IS_IMMUTABLE,
        _IS_VALID,
        _NOT_VALID,
        ImmutablePrimitiveTypesTuple,
        _check_instance_of_typehint,
        log,
    )
    log.debug(
        "_check_primitive_instance_of_typehint: Checking primitive object of type '%s' against type hint '%s'",
        type(obj).__name__, type_hint)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    # 1. Check against specific primitive types (int, str, bytes, bool, float, bytes, complex, NoneType)
    # This does not include container types (Mapping, Sequence, Set) which are handled elsewhere
    # or Union/Literal which are also handled elsewhere.
    if _is_primitive_typehint(type_hint) and isinstance(obj, type_hint):
        return (_IS_VALID, _IS_IMMUTABLE)
    log.debug(
        "_check_primitive_instance_of_typehint: Primitive object of type '%s' "
        "did not match direct primitive type hint '%s'",
        type(obj).__name__, type_hint)

    # 2. Check against universal types
    if type_hint is Any or type_hint is object or type_hint is Hashable:
        return (_IS_VALID, _IS_IMMUTABLE)

    log.debug(
        "_check_primitive_instance_of_typehint: Primitive object of type '%s' "
        "did not match universal type hint '%s'",
        type(obj).__name__, type_hint)

    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # 3. Check Literal
    if origin is Literal:
        for arg in args:
            if type(arg) not in ImmutablePrimitiveTypesTuple:
                raise SimpleBenchTypeError(
                    f"Literal type hint '{type_hint}' contains a non-primitive value '{arg}'.",
                    tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

        if obj in args:
            return (_IS_VALID, _IS_IMMUTABLE)
        # Fall through if value not in Literal

    log.debug(
        "_check_primitive_instance_of_typehint: Primitive object of type '%s' "
        "did not match Literal type hint '%s'",
        type(obj).__name__, type_hint)

    # 4. Check Union
    if origin in (Union, UnionType):
        for arg in args:
            # Primitives are self-contained, so we don't need to pass new_parents here.
            # This avoids creating unnecessary sets and ValidationState objects.
            is_valid, _ = _check_instance_of_typehint(
                obj, arg, options, parents, raise_on_error=False, context="primitive_union_item")
            if is_valid:
                # Primitives are always immutable, so we can return immediately.
                result = (_IS_VALID, _IS_IMMUTABLE)
                _CACHE.add_cache_entry(type_hint, obj, result[_IMMUTABLE])
                return result

    log.debug(
        "_check_primitive_instance_of_typehint: Primitive object of type '%s' "
        "did not match Union type hint '%s'",
        type(obj).__name__, type_hint)

    # Primitives are always Immutable and it may have taken a lot of checks
    # to determine that it does not match the type hint despite being a primitive.
    result = (_NOT_VALID, _IS_IMMUTABLE)
    _CACHE.add_cache_entry(type_hint, obj, result[_IMMUTABLE])

    # 5. Error - no match found
    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    return result
