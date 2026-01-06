"""Validation functions for type hints and instances against those type hints."""
from collections.abc import Callable, Collection, Hashable, Iterable, Mapping, Sequence, Set
from types import NoneType, UnionType
from typing import Annotated, Any, Literal, TypedDict, TypeVar, Union, get_args, get_origin, is_typeddict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from ._cache import _CACHE
from ._check_result import CheckResult
from ._collections_abc import (
    _check_collections_abc_callable,
    _check_collections_abc_collection,
    _check_collections_abc_iterable,
    _check_collections_abc_mapping,
    _check_collections_abc_sequence,
    _check_collections_abc_set,
)
from ._constants import _IS_IMMUTABLE, _IS_VALID, _NOT_IMMUTABLE, _NOT_VALID
from ._error_tags import _TypeHintsErrorTag
from ._immutable import _is_immutable
from ._log import log
from ._options import Options
from ._typing import _check_typing_literal, _check_typing_typeddict, _check_typing_union
from ._validation_state import ValidationState

__all__ = (
    "isinstance_of_typehint",
)

T = TypeVar("T", bound=TypedDict)  # type: ignore[invalidTypeForm]


def clear_typehint_cache() -> None:
    """Clear the internal type hint validation cache."""
    _CACHE.clear()

def isinstance_of_typehint(
        obj: Any,
        type_hint: Any,
        *,
        strict_typed_dict: bool = False,
        depth: int = 50,
        consume_iterators: bool = False,
        noncachable_types: set[type[Any]] | None = None) -> bool:
    """
    Check if an object is an instance of a given type hint.
    Supports basic types, generics (Mapping, Sequence, Set), Union, Literal, and TypedDict.

    It is cross-cached with is_immutable for efficiency. If either function
    determines that the object matches the type hint and is Immutable,
    the result is cached for future calls. This means that if is_immutable
    is called first and determines that the object is Immutable, subsequent calls
    to is_instance_of_typehint on the same object will be very fast.

    Because of the complexity of type hint checks, this function may not be able to
    definitively determine type hint compliance for all type hints, especially with
    deeply nested structures.

    The depth parameter limits the recursion depth for nested structures.

    - A depth of 0 allows for one level of recursion: Checking the object itself.
    - A depth of 1 allows for two levels: The object and its immediate children, and so on.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: (default=50) The recursion depth limit for nested structures.
    :param bool consume_iterators: Whether to consume iterators during validation.
    :param set[type[Any]] | None noncachable_types: Set of types that should not be cached during validation.
        The default is {NoneType, bool, int, float, complex, str, bytes}. These types are not cached because
        they frequently occur in data heavy applications while being relatively fast to process and caching
        them would explode the cache size without significant performance benefit.

    :return bool: True if the object matches the type hint, False otherwise.
    """
    if depth < 0:
        raise SimpleBenchValueError(
            f"depth must be non-negative, got {depth}.",
            tag=_TypeHintsErrorTag.NEGATIVE_DEPTH)
    options = Options(
        strict_typed_dict=strict_typed_dict,
        depth=depth,
        consume_iterators=consume_iterators,
        noncachable_types=noncachable_types or {NoneType, bool, int, float, complex, str, bytes})
    result = _check_instance_of_typehint(
        obj, type_hint, options, parents=set(), raise_on_error=False, context="root")
    return result.valid

def _check_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False,
        *,
        context: str) -> CheckResult:
    """
    Internal function to check if an object is an instance of a given type hint.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :param str context: The context of the validation check.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    log.debug("_check_instance_of_typehint: Checking object of type '%s' against type hint '%s' in context '%s'",
              type(obj).__name__, type_hint, context)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        log.debug(
            "_check_instance_of_typehint: Cache hit for object of type '%s' and type hint '%s'",
            type(obj).__name__, type_hint)
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj).__name__}' is not an instance of type hint '{type_hint}'",
            tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)

    log.debug(
        "_check_instance_of_typehint: Cache miss for object of type '%s' and type hint '%s'",
        type(obj).__name__, type_hint)

    # If we have hit the depth limit for the check,
    # Return Valid, but not Immutable (as we can't be sure)
    if options.depth < len(parents):
        log.debug(
            "_check_instance_of_typehint: Depth limit reached for object of type '%s' and type hint '%s'",
            type(obj).__name__, type_hint)
        return CheckResult(_IS_VALID, _NOT_IMMUTABLE)

    origin = get_origin(type_hint)
    args = get_args(type_hint)

    log.debug(
        "_check_instance_of_typehint: Origin of type hint '%s' is '%s' with args '%s'",
        type_hint, origin, args)

    current_state = ValidationState(id(obj), type_hint, context)
    if current_state in parents:
        log.debug("_check_instance_of_typehint: Cycle detected for object of type '%s'", type(obj).__name__)
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Cycle detected in object graph for object of type '{type(obj).__name__}'.",
                tag=_TypeHintsErrorTag.CYCLIC_REFERENCE_DETECTED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    new_parents = parents | {current_state}

    if origin is Annotated:
        log.debug("_check_instance_of_typehint: Handling Annotated type hint '%s'", type_hint)
        if not args:
            raise SimpleBenchValueError(
                f"Annotated type hint '{type_hint}' has no arguments.",
                tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
        type_hint = args[0]
        return _check_instance_of_typehint(obj, type_hint, options, new_parents, raise_on_error, context=context)

    if obj is None:
        return _check_none_instance_of_typehint(obj, type_hint, origin, args, options, new_parents, raise_on_error)
    elif type_hint in {None, NoneType}:
        log.debug(
            "_check_instance_of_typehint: Object of type '%s' does not match NoneType type hint",
            type(obj).__name__)
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not None for type hint '{type_hint}'",
                tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    log.debug("_check_instance_of_typehint: Checking if type hint is Any (%s)", type_hint)
    if type_hint is Any:
        log.debug(
            "_check_instance_of_typehint: Type hint is Any, automatically valid")
        return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    # fast paths for primitives. Caching would be pointless here. It takes much more time to cache than to check.
    # We don't have to worry about None/NoneType here because they were handled above.
    if type_hint in {object, Hashable}:
        log.debug(
            "_check_instance_of_typehint: Type hint '%s' - checking if object is primitive type", type_hint)
        if isinstance(obj, (float, int, str, bool, bytes, complex, bytes, str)):
            log.debug(
                "_check_instance_of_typehint: Type hint '%s' is automatically valid for primitive objects of type '%s'",
                type_hint, type(obj).__name__)
            return CheckResult(_IS_VALID, _IS_IMMUTABLE)
    log.debug("_check_instance_of_typehint: Checking if type_hint '%s' is a primitive type hint", type_hint)
    if type_hint in {int, float, complex, str, bytes, bool, bytes, str}:
        log.debug("_check_instance_of_typehint: Checking if object (%s) matches type hint for primitives check '%s'",
                  type(obj).__name__, type_hint)
        if isinstance(obj, type_hint):
            log.debug(
                "_check_instance_of_typehint: Object of type '%s' matches primitive type hint '%s'",
                type(obj).__name__, type_hint)
            return CheckResult(_IS_VALID, _IS_IMMUTABLE)
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' does not match primitive type hint '{type_hint}'",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _IS_IMMUTABLE)

    log.debug(
        "_check_instance_of_typehint: Object of type '%s'' is not a primitive data type', proceeding with full check",
        type(obj).__name__)

    if origin in (Union, UnionType):
        return _check_typing_union(obj, type_hint, origin, args, options, new_parents, raise_on_error)

    if origin is Literal:
        return _check_typing_literal(obj, type_hint, origin, args, raise_on_error)

    # If we have an unsubscripted generic container, get_origin() returns None.
    # We need to manually set the origin and args to handle it like a
    # subscripted generic (e.g., `list` becomes `list[Any]`).
    if origin is None and isinstance(type_hint, type):
        if issubclass(type_hint, Mapping):
            origin = type_hint
            args = (Any, Any)
        elif issubclass(type_hint, Iterable):
            origin = type_hint
            args = (Any,)
        elif issubclass(type_hint, Callable):
            origin = type_hint
            args = (..., Any)

    # If there are no args, it's a plain type (int, str, list, dict, custom class, etc.)
    # This handles both primitive types and unsubscripted generic containers.
    if not args and isinstance(type_hint, type):
        return _plain_type_check(obj, type_hint, options)

    # Dispatch to the appropriate container check.
    # The order (most specific to most general) is important.
    # The if..elif chain ensures that only one container check is applied
    # and that it is the most specific one available.
    result: CheckResult | None = None
    if is_typeddict(type_hint):
        result = _check_typing_typeddict(obj, type_hint, options, new_parents, raise_on_error)
    elif origin:
        if issubclass(origin, Mapping):
            result = _check_collections_abc_mapping(obj, type_hint, origin, args, options, new_parents, raise_on_error)
        elif issubclass(origin, Set):
            result = _check_collections_abc_set(obj, type_hint, origin, args, options, new_parents, raise_on_error)
        elif issubclass(origin, Sequence):
            result = _check_collections_abc_sequence(obj, type_hint, origin, args, options, new_parents, raise_on_error)
        elif issubclass(origin, Collection):
            result = _check_collections_abc_collection(
                obj, type_hint, origin, args, options, new_parents, raise_on_error)
        elif issubclass(origin, Iterable):
            result = _check_collections_abc_iterable(obj, type_hint, origin, args, options, new_parents, raise_on_error)
        elif issubclass(origin, Callable):
            result = _check_collections_abc_callable(obj, type_hint, origin, args, raise_on_error)

    # If no collections check was applicable, it's an unhandled type.
    if result is None:
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not a recognized container for type hint '{type_hint}'",
                tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    is_valid, is_imm = result

    if is_valid and is_imm:
        _CACHE.add_cache_entry(type_hint, obj, is_imm, options.noncachable_types)

    if raise_on_error and not is_valid:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj).__name__}' is not an instance of type hint '{type_hint}'",
            tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)

    return CheckResult(is_valid, is_imm)

def _plain_type_check(
        obj: Any,
        type_hint: Any,
        options: Options) -> CheckResult:
    """Handle plain type hints (e.g., int, str, user-defined classes).
    
    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Options options: Options for type hint validation.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchValueError: If type_hint is not a plain type.
    """
    if not isinstance(type_hint, type): # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a plain type.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    is_valid = isinstance(obj, type_hint)
    if is_valid:
        is_imm = _is_immutable(obj)
        if is_imm:
            _CACHE.add_cache_entry(type_hint, obj, True, options.noncachable_types)
        return CheckResult(_IS_VALID, is_imm)
    return CheckResult(_NOT_VALID, _is_immutable(obj))

def _check_none_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if None is an instance of a given type hint.

    :param Any obj: The object to check (should be None).
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    log.debug(
        "_check_none_instance_of_typehint: Checking None against type hint '%s'", type_hint)
    if obj is not None:  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Object is not None, got '{obj}'.",
            tag=_TypeHintsErrorTag.INVALID_NONE_CHECK)

    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if type_hint in {NoneType, None, Any, object, Hashable}:
        return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    if origin is Literal and None in args:
        return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    if origin in (Union, UnionType):
        for arg in args:
            is_valid, _ = _check_instance_of_typehint(
                obj, arg, options, parents, raise_on_error=False, context="none_union_item")
            if is_valid:
                return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    check_result = CheckResult(_NOT_VALID, _IS_IMMUTABLE)
    _CACHE.add_cache_entry(type_hint, obj, check_result.immutable, options.noncachable_types)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Type hint '{type_hint}' does not allow None.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    return check_result

def _is_subtype_of_typehint(subtype: Any, basetype: Any) -> bool:
    """
    Checks if a given type is a subtype of or compatible with a base type.
    This is a complex problem, so we'll handle the common cases.

    .. warning::
        This function does not handle all edge cases and complex type hints.

    :param Any subtype: The potential subtype.
    :param Any basetype: The potential base type.
    :return bool: True if subtype is a subtype of basetype, False otherwise.
    """
    log.debug("_is_subtype_of_typehint: Checking if '%s' is a subtype of '%s'", subtype, basetype)
    # Handle origins and args
    origin_subtype = get_origin(subtype)
    args_subtype = get_args(subtype)
    origin_basetype = get_origin(basetype)
    args_basetype = get_args(basetype)

    if subtype is Any or basetype is Any:
        return True

    # Case 1: Simple, non-generic types (int, str, etc.)
    if origin_subtype is None and origin_basetype is None:
        if not isinstance(subtype, type) or not isinstance(basetype, type):
            return subtype == basetype # e.g. comparing Literals
        return issubclass(subtype, basetype)

    # Case 2: Generic containers (list, set, sequence)
    # These are covariant, so list[A] is a subtype of list[B] if A is a subtype of B.
    if origin_subtype and origin_basetype and issubclass(origin_subtype, origin_basetype):
        if len(args_subtype) == len(args_basetype):
            # This is a simplification; real covariance/contravariance is more complex
            return all(_is_subtype_of_typehint(
                arg_subtype, arg_basetype) for arg_subtype, arg_basetype in zip(args_subtype, args_basetype))

    # Fallback for non-matching structures
    return False
