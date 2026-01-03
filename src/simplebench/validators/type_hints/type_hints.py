"""Validation functions for type hints and instances against those type hints."""
import inspect
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence, Set
from types import MappingProxyType, NoneType, UnionType
from typing import (
    Annotated,
    Any,
    Final,
    Literal,
    TypeAlias,
    TypedDict,
    TypeGuard,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    is_typeddict,
)

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import Immutable
from simplebench.validators._cache import ValidationCache

from ._error_tags import _TypeHintsErrorTag

_CACHE = ValidationCache(
    min_cache_size=100,
    max_cache_size=16384,
)

T = TypeVar("T", bound=TypedDict)  # type: ignore[invalidTypeForm]

_VALID: Final[Literal[0]] = 0
"""Index for validity in CheckResult tuple."""
_IMMUTABLE: Final[Literal[1]] = 1
"""Index for immutability in CheckResult tuple."""

_IS_VALID: Final[Literal[True]] = True
"""Indicates that the object matches the type hint."""
_IS_IMMUTABLE: Final[Literal[True]] = True
"""Indicates that the object is immutable according to a check."""
_NOT_VALID: Final[Literal[False]] = False
"""Indicates that the object does not match the type hint."""
_NOT_IMMUTABLE: Final[Literal[False]] = False
"""Indicates that the object is not immutable according to a check."""

CheckResult: TypeAlias = tuple[bool, bool]
"""Type alias for the result of a type hint check.

Tuple of two booleans:
    - First boolean indicates if the object matches the type hint. (`_IS_VALID` index: 0)
    - Second boolean indicates if the object is immutable according to the type hint. (`_IS_IMMUTABLE` index: 1)
"""

PrimitiveTypes: TypeAlias = int | str | bytes | bool | float | complex | NoneType
"""Type alias for primitive data types."""

PrimitiveTypesTuple: tuple = (int, str, bytes, bool, float, complex, NoneType)
"""Tuple of primitive data types for isinstance checks."""

_PRIMITIVE_TYPES_SET: set[type] = {int, str, bytes, bool, float, complex, NoneType}
"""Set of primitive data types for quick membership checks."""

def is_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        *,
        strict_typed_dict: bool = False,
        depth: int = 0) -> bool:
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
    A depth of 0 allows for one level of recursion (checking the object and its immediate children),
    while a depth of 1 allows for two levels, and so on.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: The recursion depth for nested structures.
    :return bool: True if the object matches the type hint, False otherwise.
    """
    if depth < 0:
        raise SimpleBenchValueError(
            f"depth must be non-negative, got {depth}.",
            tag=_TypeHintsErrorTag.NEGATIVE_DEPTH)
    is_valid, _ = _check_instance_of_typehint(
        obj, type_hint, strict_typed_dict, depth, parents=set(), raise_on_error=False)
    return is_valid

def is_immutable(
        obj: Any,
        type_hint: Any,
        *,
        strict_typed_dict: bool = False,
        depth: int = 0) -> bool:
    """
    Check if an object is Immutable according to a given type hint.
    Supports basic types, generics (Mapping, Sequence, Set), Union, Literal, and TypedDict.

    It is cross-cached with is_instance_of_typehint for efficiency. If either function
    determines that the object is Immutable, the result is cached for future calls.

    This means that if is_instance_of_typehint is called first and determines that the object
    is Immutable, subsequent calls to is_immutable on the same object will be very fast.

    Due to the complexity of immutability checks, this function may not be able to
    definitively determine immutability for all type hints, especially with deeply
    nested structures.

    The immutability definition follows SimpleBench's definition of :class:`~simplebench.types.Immutable`.

    While an object may be considered Immutable by Python standards (e.g., a tuple),
    it may not be considered Immutable by SimpleBench if it contains mutable elements
    (e.g., a tuple containing a list).

    Additionally, a determination of being NOT Immutable does not imply mutability;
    it may simply mean that the function could not verify immutability given the
    provided type hint and depth. It is a conservative check that assumes mutability
    unless it can be proven otherwise.

    The depth parameter limits the recursion depth for nested structures.
    A depth of 0 allows for one level of recursion (checking the object and its immediate children),
    while a depth of 1 allows for two levels, and so on.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: The recursion depth for nested structures.
    :return bool: True if the object is Immutable according to the type hint, False otherwise.
    """
    if depth < 0:
        raise SimpleBenchValueError(
            f"depth must be non-negative, got {depth}.",
            tag=_TypeHintsErrorTag.NEGATIVE_DEPTH)
    _, is_immutable = _check_instance_of_typehint(
        obj, type_hint, strict_typed_dict, depth, parents=set(), raise_on_error=False)
    return is_immutable


def _check_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        strict_typed_dict: bool,
        depth: int,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if an object is an instance of a given type hint.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: The recursion depth for nested structures.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    # Check the cache first
    cached_result = _CACHE.valid_in_cache(obj, type_hint)
    if cached_result is not None:  # Only cached if Immutable
        return (cached_result, _IS_IMMUTABLE)

    # If we have hit the depth limit for the check,
    # Return Valid, but not Immutable (as we can't be sure)
    if depth > len(parents):
        return (_IS_VALID, _NOT_IMMUTABLE)

    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is Annotated:
        return _check_instance_of_typehint(obj, args[0], strict_typed_dict, depth, parents, raise_on_error)

    if obj is None:
        return _check_none_instance_of_typehint(
             obj, type_hint, origin, args, strict_typed_dict, depth, parents, raise_on_error)

    if _is_primitive(obj): # This prevents generic checks on primitive data types
        return _check_primitive_instance_of_typehint(
            obj, type_hint,  strict_typed_dict, depth, parents, raise_on_error)

    if origin in (Union, UnionType):
        return _union_check(obj, type_hint, origin, args, strict_typed_dict, depth, parents, raise_on_error)

    if origin is Literal:
        return _literal_check(obj, type_hint, origin, args, raise_on_error)

    # Handle plain types (e.g., int, str, or user-defined classes)
    if isinstance(type_hint, type):
        check_result = _plain_type_check(obj, type_hint)
        if check_result[_VALID]:
            return check_result

    # If not a special form, proceed with generic container checks
    container_results: list[CheckResult] = []
    container_results.extend([
        _container_check_typeddict(obj, type_hint, strict_typed_dict, depth, parents, raise_on_error),
    ])
    if origin:
        container_results.extend([
            _container_check_mapping(obj, origin, args, strict_typed_dict, depth, parents, raise_on_error),
            _container_check_set(obj, origin, args, strict_typed_dict, depth, parents, raise_on_error),
            _container_check_sequence(obj, origin, args, strict_typed_dict, depth, parents, raise_on_error),
            _container_check_iterable(obj, origin, args, strict_typed_dict, depth, parents, raise_on_error),
            _container_check_callable(obj, origin, args, strict_typed_dict, depth, parents, raise_on_error),
        ])

    # If any check fails, return False; if all pass, return True
    if container_results:
        is_valid = all(container_results[_IS_VALID] for container_results in container_results)
        is_immutable = all(container_results[_IS_IMMUTABLE] for containerResults in container_results)
        if is_valid and is_immutable:
            _CACHE.add_cache_entry(obj, type_hint, True)
        if raise_on_error and not is_valid:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (is_valid, is_immutable)

    # Fallback to original logic
    return is_instance_of_generic(obj, type_hint)


def _is_primitive(obj: Any) -> bool:
    """
    Check if an object is a primitive data type according.

    :param Any obj: The object to check.
    :return bool: True if the object is a primitive data type, False otherwise.
    """
    try:
        return isinstance(obj, PrimitiveTypesTuple)
    except Exception:  # pylint: disable=broad-exception-caught
        return False

def _is_primitive_typehint(type_hint: Any) -> bool:
    """
    Check if a type hint directly represents a primitive data type.

    Primitive data types include: int, str, bytes, bool, float, complex, type(None).

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint represents a primitive data type, False otherwise.
    """
    return type_hint in _PRIMITIVE_TYPES_SET

def _is_immutable(obj: Any) -> bool:
    """
    Check if an object is Immutable according to SimpleBench's definition.

    :param Any obj: The object to check.
    :return bool: True if the object is Immutable, False otherwise.
    """
    try:
        return isinstance(obj, Immutable)
    except Exception:  # pylint: disable=broad-exception-caught
        return False

def _check_immutable_protocol_compliance(*,
        obj: Any,
        raise_on_error: bool = False) -> CheckResult:
    """
    Check if an object complies with the Immutable protocol.

    :param Any obj: The object to check.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    if isinstance(obj, Immutable):
        return (_IS_VALID, _IS_IMMUTABLE)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint 'Immutable'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return (_NOT_VALID, _IS_IMMUTABLE)

def _plain_type_check(
        obj: Any,
        type_hint: Any) -> CheckResult:
    """Handle plain type hints (e.g., int, str, user-defined classes).
    
    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    if not isinstance(type_hint, type): # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a plain type.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    is_valid = isinstance(obj, type_hint)
    if is_valid:
        is_imm = isinstance(obj, Immutable)
        if is_imm:
            _CACHE.add_cache_entry(type(obj), type_hint, True)
        return (_IS_VALID, is_imm)
    return (_NOT_VALID, _is_immutable(obj))

def _literal_check(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        raise_on_error: bool = False) -> CheckResult:
    """Handle Literal types.
    
    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Literal type hint.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    """
    if origin is not Literal:  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Literal type.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)


    is_valid = obj in args
    if is_valid:
        # Literals are always immutable values
        _CACHE.add_cache_entry(obj, type_hint, True)
        return (_IS_VALID, _IS_IMMUTABLE)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return (_NOT_VALID, _is_immutable(obj))

def _union_check(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        strict_typed_dict: bool,
        depth: int,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Union types first as an exclusive check. 
    
    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param tuple args: The type arguments of the Union type hint.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: The recursion depth for nested structures.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    """
    if origin not in (Union, UnionType):  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Union type.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    for arg in args:
        # Recursively check against each type in the Union
        is_valid, is_immutable = _check_instance_of_typehint(
            obj, arg, strict_typed_dict, depth, parents, raise_on_error=False)

        # If a match is found, return immediately
        if is_valid:
            # We can cache the result for the specific matching type `arg`
            if is_immutable:
                _CACHE.add_cache_entry(obj, arg, True)
            return (is_valid, is_immutable)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return (_NOT_VALID, _is_immutable(obj))


def _check_primitive_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        strict_typed_dict: bool,
        depth: int,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if a primitive object is an instance of a given type hint.

    :param Any obj: The primitive object to check.
    :param Any type_hint: The type hint to check against.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: The recursion depth for nested structures.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    # 1. Check against specific primitive types (int, str, bytes, bool, float, bytes, complex, NoneType)
    # This does not include container types (Mapping, Sequence, Set) which are handled elsewhere
    # or Union/Literal which are also handled elsewhere.
    if _is_primitive(type_hint): # fast path for primitive types/objects
        if isinstance(obj, type_hint):
            return (_IS_VALID, _IS_IMMUTABLE)

    # 2. Check against universal types
    if type_hint is Any or type_hint is object or type_hint is Hashable:
        return (_IS_VALID, _IS_IMMUTABLE)

    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # 3. Check Literal
    if origin is Literal:
        for arg in args:
            if type(arg) not in PrimitiveTypesTuple:
                raise SimpleBenchTypeError(
                    f"Literal type hint '{type_hint}' contains a non-primitive value '{arg}'.",
                    tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

        if obj in args:
            return (_IS_VALID, _IS_IMMUTABLE)
        # Fall through if value not in Literal

    # 4. Check Union
    if origin in (Union, UnionType):
        # Recurse for each argument to handle complex cases (e.g. Union[int, Literal['foo']])
        for arg in args:
            check_result = _check_instance_of_typehint(
                obj, arg, strict_typed_dict, depth, parents, raise_on_error=False)
            if check_result[_VALID]:
                return check_result

        # If no match in Union
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (_NOT_VALID, _IS_IMMUTABLE)

    # 5. Error - no match found
    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return (_NOT_VALID, _IS_IMMUTABLE)

def _check_none_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        strict_typed_dict: bool,
        depth: int,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if None is an instance of a given type hint.

    :param Any obj: The object to check (should be None).
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: The recursion depth for nested structures.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    if obj is not None:  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Object is not None, got '{obj}'.",
            tag=_TypeHintsErrorTag.INVALID_NONE_CHECK)

    if type_hint in {NoneType, None, Any, object, Hashable}:
        return (_IS_VALID, _IS_IMMUTABLE)

    if origin is Literal and None in args:
        return (_IS_VALID, _IS_IMMUTABLE)

    if origin in (Union, UnionType):
        if NoneType in args or Any in args:  # fast path
            return (_IS_VALID, _IS_IMMUTABLE)

        # Slow path: Recursively check args (handles Annotated[None], etc.)
        for arg in args:
            check_result = _check_instance_of_typehint(
                obj, arg, strict_typed_dict, depth, parents, raise_on_error=False)
            if check_result[_VALID]:
                return (_IS_VALID, _IS_IMMUTABLE)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Type hint '{type_hint}' does not allow None.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return (_NOT_VALID, _IS_IMMUTABLE)

def _container_check_typeddict(
        obj: Any,
        type_hint: Any,
        strict_typed_dict: bool,
        depth: int,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Check if obj matches a TypedDict type hint.

    If not a TypedDict and not strict_typed_dict, returns True to allow other checks to proceed normally.
    If it is a TypedDict or structurally conforms to a TypedDict, checks keys and values recursively if specified.

    If not a TypedDict, returns (_IS_VALID, _IS_IMMUTABLE) to allow other checks to proceed normally.
    The semantic is 'If not a TypedDict, this check does not apply and should not cause a failure.'

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check (may or may not be a TypedDict).
    :param bool strict_typed_dict: Whether to enforce that it REALLY is a TypedDict
        or only that conforms structurally to the TypedDict definition.
    :param int depth: The recursion depth for nested structures.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return bool: True if obj matches the TypedDict type hint, False otherwise.
    """
    if not isinstance(obj, dict) and not strict_typed_dict:  # Allow structural TypedDict checks
        origin = get_origin(type_hint)
        if origin and issubclass(origin, Mapping):
            # Check if obj is a Mapping with string keys
            if not isinstance(obj, Mapping):
                return (_NOT_VALID, _NOT_IMMUTABLE)
            if not all(isinstance(k, str) for k in obj.keys()):
                return (_NOT_VALID, _NOT_IMMUTABLE)
            if recurse:
                annotations = get_type_hints(type_hint)
                for key, value_type in annotations.items():
                    if key in obj:
                        if not is_instance_of_typehint(obj[key], value_type, recurse=True):
                            return False
            return True
        return False

    if not isinstance(obj, dict):
        return False
    if not all(isinstance(k, str) for k in obj.keys()):
        return False
    if recurse:
        annotations = get_type_hints(type_hint)
        for key, value_type in annotations.items():
            if key in obj:
                if not is_instance_of_typehint(obj[key], value_type, recurse=True):
                    return False
    return True

def _container_check_mapping(*, origin: Any, args: tuple, obj: Mapping, recurse: bool) -> bool:
    """Check if obj matches Mapping type hint.
    
    If not a Mapping, returns True to allow other checks to proceed normally.
    The semantic is 'If not a Mapping, this check does not apply and should not cause a
    failure.'

    If it is a Mapping, checks keys and values recursively if specified and args are provided.

    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Mapping obj: The object to check.
    :param bool recurse: Whether to perform deep validation of nested structures.
    :return bool: True if obj matches the Mapping type hint, False otherwise.
    """
    if issubclass(origin, Mapping):
        result = isinstance(obj, Mapping)
        if result and recurse and len(args) == 2:
            key_type, value_type = args
            for k, v in obj.items():
                if not is_instance_of_typehint(
                    k, key_type, recurse=True) or not is_instance_of_typehint(v, value_type, recurse=True):
                    result = False
                    break
        return result
    return True

def _container_check_set(*, origin: Any, args: tuple, obj: Set, recurse: bool) -> bool:
    """Check if obj matches Set type hint.

    If not a Set, returns True to allow other checks to proceed normally.
    The semantic is 'If not a Set, this check does not apply and should not cause a
    failure.'
    If it is a Set, checks items recursively if specified and args are provided.

    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Set obj: The object to check.
    :param bool recurse: Whether to perform deep validation of nested structures.
    :return bool: True if obj matches the Set type hint, False otherwise.
    """
    if issubclass(origin, Set) and not issubclass(origin, (str, bytes)):
        result = isinstance(obj, Set) and not isinstance(obj, (str, bytes))
        if result and recurse and args:
            item_type = args[0]
            for item in obj:
                if not is_instance_of_typehint(item, item_type, recurse=True):
                    result = False
                    break
        return result
    return True

def _container_check_sequence(*, origin: Any, args: tuple, obj: Sequence, recurse: bool) -> bool:
    """Check if obj matches Sequence type hint.
    If not a Sequence, returns True to allow other checks to proceed normally.
    The semantic is 'If not a Sequence, this check does not apply and should not cause
    a failure.'
    If it is a Sequence, checks items recursively if specified and args are provided.

    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Sequence obj: The object to check.
    :param bool recurse: Whether to perform deep validation of nested structures.
    :return bool: True if obj matches the Sequence type hint, False otherwise.
    """
    if issubclass(origin, Sequence) and not issubclass(origin, (str, bytes)):
        result = isinstance(obj, Sequence) and not isinstance(obj, (str, bytes))
        if result and recurse and args:
            item_type = args[0]
            for item in obj:
                if not is_instance_of_typehint(item, item_type, recurse=True):
                    result = False
                    break
        return result
    return True

def _container_check_iterable(*, origin: Any, args: tuple, obj: Iterable, recurse: bool) -> bool:
    """Check if obj matches Iterable type hint.
    If not an Iterable, returns True to allow other checks to proceed normally.
    The semantic is 'If not an Iterable, this check does not apply and should not cause
    a failure.'
    If it is an Iterable, checks items recursively if specified and args are provided.

    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Iterable obj: The object to check.
    :param bool recurse: Whether to perform deep validation of nested structures.
    :return bool: True if obj matches the Iterable type hint, False otherwise.
    """
    if issubclass(origin, Iterable) and not issubclass(origin, (str, bytes)):
        result = isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))
        if result and recurse and args:
            item_type = args[0]
            for item in obj:
                if not is_instance_of_typehint(item, item_type, recurse=True):
                    result = False
                    break
        return result
    return True

def _container_check_callable(*, origin: Any, args: tuple, obj: Any, recurse: bool) -> bool:
    """Check if obj matches Callable type hint.
    If not a Callable, returns True to allow other checks to proceed normally.
    If it is a Callable, checks parameters and return type recursively if specified and args are provided.

    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Any obj: The object to check.
    :param bool recurse: Whether to perform deep validation of nested structures.
    :return bool: True if obj matches the Callable type hint, False otherwise.
    """
    if not (origin and issubclass(origin, Callable)):
        return True

    if not callable(obj):
        return False

    # If no args, just being callable is enough
    if not args:
        return True

    # Callable[..., ReturnType] (ellipsis means any arguments)
    if args[0] is Ellipsis:
        if recurse and len(args) == 2:
            # Optionally check return type if possible
            try:
                sig = inspect.signature(obj)
                return_annotation = sig.return_annotation
                if return_annotation is not inspect.Signature.empty:
                    return is_instance_of_typehint(return_annotation, args[1], recurse=True)
            except (ValueError, TypeError):
                pass  # Built-ins or C callables may not have signatures
        return True

    # Callable[[ArgTypes...], ReturnType]
    param_types = args[0]
    return_type = args[1] if len(args) > 1 else None

    try:
        sig = inspect.signature(obj)
        params = list(sig.parameters.values())
        # Check number of parameters matches
        if len(param_types) != len(params):
            return False
        if recurse:
            # Check parameter types if possible
            for param, expected_type in zip(params, param_types):
                if param.annotation is not inspect.Parameter.empty:
                    if not is_instance_of_typehint(param.annotation, expected_type, recurse=True):
                        return False
            # Check return type if possible
            if return_type is not None and sig.return_annotation is not inspect.Signature.empty:
                if not is_instance_of_typehint(sig.return_annotation, return_type, recurse=True):
                    return False
    except (ValueError, TypeError):
        # Builtins or C callables may not have signatures; fallback to just callable
        return True

    return True

def is_instance_of_generic(obj: Any, type_hint: Any) -> bool:
    """
    Check if an object is an instance of a generic type hint.
    Handles simple types, lists, sequences, and dictionaries.

    :param obj: The object to check.
    :param type_hint: The type hint to check against.
    :return: True if the object matches the type hint, False otherwise.
    """
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Case 1: Simple type (e.g., int, str)
    if origin is None:
        if isinstance(type_hint, type):
            return isinstance(obj, type_hint)
        return False  # Should not happen with valid type hints

    # Case 2: Dictionary or Mapping
    if inspect.isclass(origin) and issubclass(origin, Mapping):
        if not isinstance(obj, Mapping):
            return False
        key_type, value_type = args
        return all(is_instance_of_generic(
            k, key_type) and is_instance_of_generic(v, value_type) for k, v in obj.items())

    # Case 3: Iterable (but not a Mapping)
    if inspect.isclass(origin) and issubclass(origin, Iterable):
        # If the object is a string/bytes but the type hint is a different kind of iterable (e.g. list[str]),
        # it's a mismatch. We should not iterate over the string's characters.
        if isinstance(obj, (str, bytes)):
            return issubclass(origin, (str, bytes))

        if not isinstance(obj, Iterable):
            return False

        item_type = args[0]
        return all(is_instance_of_generic(item, item_type) for item in obj)

    # Fallback for other types (like Union, etc., which can be added here)
    return isinstance(obj, origin)

def _is_immutable_data_typehint(type_hint: Any) -> bool:
    """
    Check if a type hint represents an immutable data type.

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint represents an immutable data type, False otherwise.
    """
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is Annotated:
        return _is_immutable_data_typehint(args[0])

    if type_hint in PrimitiveTypesTuple:
        return True

    if origin is frozenset:
        if args:
            item_type = args[0]
            return _is_immutable_data_typehint(item_type)
        return True  # frozenset with no args is immutable

    if origin is tuple:
        if args and args[-1] is Ellipsis:
            item_type = args[0]
            return _is_immutable_data_typehint(item_type)
        for item_type in args:
            if not _is_immutable_data_typehint(item_type):
                return False
        return True

    if origin is MappingProxyType:
        if len(args) == 2:
            key_type, value_type = args
            return (_is_immutable_data_typehint(key_type)
                    and _is_immutable_data_typehint(value_type))
        return True  # MappingProxyType with no args is immutable

    return False
