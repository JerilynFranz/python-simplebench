"""Validation functions for type hints and instances against those type hints."""
import inspect
import sys
from collections.abc import Callable, Hashable, Iterable, Iterator, Mapping, Sequence, Set
from types import MappingProxyType, NoneType, UnionType
from typing import (
    Annotated,
    Any,
    Final,
    Literal,
    NamedTuple,
    TypeAlias,
    TypedDict,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    is_typeddict,
)

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import Immutable, is_immutable_typeddict_typehint
from simplebench.validators._cache import ValidationCache

from ._error_tags import _TypeHintsErrorTag
from .typed_dict_key_info import TypedDictKeyInfo

if sys.version_info >= (3, 11):
    from typing import Never
else:
    try:
        from typing_extensions import Never
    except ImportError as e:
        raise ImportError(
            "SimpleBench requires 'typing_extensions' for Python < 3.11 "
            "to support Never.") from e

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

ImmutablePrimitiveTypes: TypeAlias = int | str | bytes | bool | float | complex | NoneType
"""Type alias for primitive data types."""

ImmutablePrimitiveTypesTuple: tuple = (int, str, bytes, bool, float, complex, NoneType)
"""Tuple of primitive data types for isinstance checks."""

_IMMUTABLE_PRIMITIVE_TYPES_SET: set[type] = set(ImmutablePrimitiveTypesTuple)
"""Set of primitive data types for quick membership checks."""

class Options(NamedTuple):
    """Options for type hint validation functions.

    :property bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :property int depth: The recursion depth for nested structures.
    :property bool consume_iterators: Whether to consume iterators during validation.
    """
    strict_typed_dict: bool = False
    depth: int = 0
    consume_iterators: bool = False

def is_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        *,
        strict_typed_dict: bool = False,
        depth: int = 0,
        consume_iterators: bool = False) -> bool:
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
    :param bool consume_iterators: Whether to consume iterators during validation.
    :return bool: True if the object matches the type hint, False otherwise.
    """
    if depth < 0:
        raise SimpleBenchValueError(
            f"depth must be non-negative, got {depth}.",
            tag=_TypeHintsErrorTag.NEGATIVE_DEPTH)
    options = Options(
        strict_typed_dict=strict_typed_dict,
        depth=depth,
        consume_iterators=consume_iterators)
    is_valid, _ = _check_instance_of_typehint(obj, type_hint, options, parents=set(), raise_on_error=False)
    return is_valid

def is_immutable(
        obj: Any,
        type_hint: Any,
        *,
        strict_typed_dict: bool = False,
        depth: int = 0,
        consume_iterators: bool = False) -> bool:
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
    :param bool consume_iterators: Whether to consume iterators during validation.
    :return bool: True if the object is Immutable according to the type hint, False otherwise.
    """
    if depth < 0:
        raise SimpleBenchValueError(
            f"depth must be non-negative, got {depth}.",
            tag=_TypeHintsErrorTag.NEGATIVE_DEPTH)
    options = Options(
        strict_typed_dict=strict_typed_dict,
        depth=depth,
        consume_iterators=consume_iterators)
    _, is_imm = _check_instance_of_typehint(obj, type_hint, options, parents=set(), raise_on_error=False)
    return is_imm


def _check_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if an object is an instance of a given type hint.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj).__name__}' is not an instance of type hint '{type_hint}'",
            tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)

    # If we have hit the depth limit for the check,
    # Return Valid, but not Immutable (as we can't be sure)
    if options.depth > len(parents):
        return (_IS_VALID, _NOT_IMMUTABLE)

    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if id(obj) in parents:
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Cycle detected in object graph for object of type '{type(obj).__name__}'.",
                tag=_TypeHintsErrorTag.CYCLIC_REFERENCE_DETECTED)
        return (_NOT_VALID, _NOT_IMMUTABLE)

    new_parents = parents | {id(obj)}

    if origin is Annotated:
        type_hint = args[0]
        return _check_instance_of_typehint(obj, type_hint, options, new_parents, raise_on_error)

    if obj is None:
        return _check_none_instance_of_typehint(obj, type_hint, origin, args, options, new_parents, raise_on_error)

    if _is_primitive(obj):
        return _check_primitive_instance_of_typehint(obj, type_hint, options, new_parents, raise_on_error)

    if origin in (Union, UnionType):
        return _union_check(obj, type_hint, origin, args, options, new_parents, raise_on_error)

    if origin is Literal:
        return _literal_check(obj, type_hint, origin, args, raise_on_error)

    # Handle plain types (e.g., int, str, or user-defined classes)
    if isinstance(type_hint, type):
        return _plain_type_check(obj, type_hint)

    # If not a special form, proceed with generic container checks
    container_results: list[CheckResult] = []
    container_results.extend([
        _container_check_typeddict(obj, type_hint, options, new_parents, raise_on_error),
    ])
    if origin:
        container_results.extend([
            _container_check_mapping(obj, type_hint, origin, args, options, new_parents, raise_on_error),
            _container_check_set(obj, type_hint, origin, args, options, new_parents, raise_on_error),
            _container_check_sequence(obj, type_hint, origin, args, options, new_parents, raise_on_error),
            _container_check_iterable(obj, type_hint, origin, args, options, new_parents, raise_on_error),
            _container_check_callable(obj, type_hint, origin, args, raise_on_error),
        ])

    # The container checks return (_IS_VALID, _IS_IMMUTABLE) if they don't apply.
    # A successful validation means ALL checks passed (i.e., were either applicable and valid, or not applicable).
    is_valid = all(result[_VALID] for result in container_results)
    is_imm = all(result[_IMMUTABLE] for result in container_results)

    if is_valid and is_imm:
        _CACHE.add_cache_entry(type_hint, obj, is_imm)

    if raise_on_error and not is_valid:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj).__name__}' is not an instance of type hint '{type_hint}'",
            tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)

    return (is_valid, is_imm)

def _is_primitive(obj: Any) -> bool:
    """
    Check if an object is a primitive data type according.

    :param Any obj: The object to check.
    :return bool: True if the object is a primitive data type, False otherwise.
    """
    try:
        return isinstance(obj, ImmutablePrimitiveTypesTuple)
    except Exception:  # pylint: disable=broad-exception-caught
        return False

def _is_primitive_typehint(type_hint: Any) -> bool:
    """
    Check if a type hint directly represents a primitive data type.

    Primitive data types include: int, str, bytes, bool, float, complex, type(None).

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint represents a primitive data type, False otherwise.
    """
    return type_hint in _IMMUTABLE_PRIMITIVE_TYPES_SET

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
    :raises SimpleBenchValueError: If type_hint is not a plain type.
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
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Union types first as an exclusive check. 
    
    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param tuple args: The type arguments of the Union type hint.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails
    :raises SimpleBenchValueError: If type_hint is not a Union type.
    """
    if origin not in (Union, UnionType):  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Union type.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
    new_parents = parents.copy()
    new_parents.add(id(obj))
    for arg in args:
        # Recursively check against each type in the Union
        is_valid, is_imm = _check_instance_of_typehint(
            obj, arg, options, new_parents, raise_on_error=False)

        # If a match is found, return immediately
        if is_valid:
            # We can cache the result for the specific matching type `arg`
            if is_imm:
                _CACHE.add_cache_entry(obj, arg, True)
            return (is_valid, is_imm)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return (_NOT_VALID, _is_immutable(obj))


def _check_primitive_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if a primitive object is an instance of a given type hint.

    :param Any obj: The primitive object to check.
    :param Any type_hint: The type hint to check against.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    if not _is_primitive(obj):  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Object '{obj}' is not a primitive data type.",
            tag=_TypeHintsErrorTag.INVALID_PRIMITIVE_CHECK)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(obj, type_hint)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

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
            if type(arg) not in ImmutablePrimitiveTypesTuple:
                raise SimpleBenchTypeError(
                    f"Literal type hint '{type_hint}' contains a non-primitive value '{arg}'.",
                    tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

        if obj in args:
            return (_IS_VALID, _IS_IMMUTABLE)
        # Fall through if value not in Literal

    # 4. Check Union
    new_parents = parents.copy()
    new_parents.add(id(obj))
    if origin in (Union, UnionType):
        # Recurse for each argument to handle complex cases (e.g. Union[int, Literal['foo']])
        for arg in args:
            check_result = _check_instance_of_typehint(obj, arg, options, new_parents, raise_on_error=False)
            if check_result[_VALID]:
                return check_result

        # If no match in Union
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (_NOT_VALID, _IS_IMMUTABLE)

    # Primitives are always Immutable and it may have taken a lot of checks
    # to determine that it does not match the type hint despite being a primitive.
    result = (_NOT_VALID, _IS_IMMUTABLE)
    _CACHE.add_cache_entry(obj, type_hint, result[_IMMUTABLE])

    # 5. Error - no match found
    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    return result

def _check_none_instance_of_typehint(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """
    Internal function to check if None is an instance of a given type hint.

    :param Any obj: The object to check (should be None).
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    if obj is not None:  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Object is not None, got '{obj}'.",
            tag=_TypeHintsErrorTag.INVALID_NONE_CHECK)

    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if type_hint in {NoneType, None, Any, object, Hashable}:
        return (_IS_VALID, _IS_IMMUTABLE)

    if origin is Literal and None in args:
        return (_IS_VALID, _IS_IMMUTABLE)

    new_parents = parents.copy()
    new_parents.add(id(obj))
    if origin in (Union, UnionType):
        if NoneType in args or Any in args:  # fast path
            return (_IS_VALID, _IS_IMMUTABLE)

        # Slow path: Recursively check args (handles Annotated[None], etc.)
        for arg in args:
            check_result = _check_instance_of_typehint(obj, arg, options, new_parents, raise_on_error=False)
            if check_result[_VALID]:
                return (_IS_VALID, _IS_IMMUTABLE)

    check_result = (_NOT_VALID, _IS_IMMUTABLE)
    _CACHE.add_cache_entry(obj, type_hint, check_result[_IMMUTABLE])

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Type hint '{type_hint}' does not allow None.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    return check_result

def _container_check_typeddict(
        obj: Any,
        type_hint: Any,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Check if obj matches a TypedDict type hint.

    If not a TypedDict and not strict_typed_dict, returns True to allow other checks to proceed normally.
    If it is a TypedDict or structurally conforms to a TypedDict, checks keys and values recursively if specified.

    If not a TypedDict, returns (_IS_VALID, _IS_IMMUTABLE) to allow other checks to proceed normally.
    The semantic is 'If not a TypedDict, this check does not apply and should not cause a failure.'

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check (may or may not be a TypedDict).
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    # Fast path checks
    if not is_typeddict(type_hint):
        return (_IS_VALID, _IS_IMMUTABLE)  # Not a TypedDict type hint, so this check does not apply

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if options.strict_typed_dict:
        if not isinstance(obj, dict):
            return (_NOT_VALID, _NOT_IMMUTABLE)  # Not instance of dict, cannot be a strict TypedDict instance
    if not isinstance(obj, Mapping):  # This acts as a fast-fail for non-Mapping objects and a type guard
        return (_NOT_VALID, _NOT_IMMUTABLE)  # Not a Mapping, cannot structurally conform to TypedDict

    # From here on, we know that type_hint IS a TypedDict and that the object is a Mapping.
    # All TypedDict checks are structural so we can proceed.

    # TypedDict keys must be strings
    if not all(isinstance(k, str) for k in obj.keys()):
        return (_NOT_VALID, _NOT_IMMUTABLE)

    # Make sure that if the TypedDict is defined as Immutable, the Mapping obj is also Immutable
    # Note: This only checks the top-level container not nested elements here.
    # Nested elements are checked below. Standard TypedDicts are mutable by definition (dict-based)
    # and will fail this check if the type hint is defined as Immutable.
    container_is_immutable: bool = isinstance(obj, Immutable)
    is_immutable_typed_dict: bool = is_immutable_typeddict_typehint(type_hint)
    if is_immutable_typed_dict and not container_is_immutable:
        return (_NOT_VALID, _NOT_IMMUTABLE)  # TypedDict is defined as Immutable but object is not Immutable

    required_keys: set[str] = set(type_hint.__required_keys__)
    optional_keys: set[str] = set(type_hint.__optional_keys__)
    allowed_keys: set[str] = required_keys.union(optional_keys)
    if is_immutable_typed_dict:
        # Immutable TypedDicts may have a special key __immutable__ that we ignore for validation
        required_keys.discard('__immutable__')
        optional_keys.discard('__immutable__')
        allowed_keys.discard('__immutable__')

    new_parents = parents.copy()
    new_parents.add(id(obj))

    # check for 'extra_items' if typeddict class explicitly sets it
    extra_items_type_hint: Any = getattr(type_hint, '__extra_items__', Never)
    if extra_items_type_hint is Never:  # No extra items allowed
        for key in obj.keys():
            if key not in allowed_keys:
                return (_NOT_VALID, _NOT_IMMUTABLE)
    else: # Extra items allowed, check their types
        for key in obj.keys():
            if key not in allowed_keys:
                check_result = _check_instance_of_typehint(
                    obj[key], extra_items_type_hint, options, new_parents, raise_on_error=False)
                if not check_result[_VALID]:
                    if raise_on_error:
                        raise SimpleBenchTypeError(
                            f"Extra key '{key}' in TypedDict does not match extra_items type hint "
                            f"'{extra_items_type_hint}'.",
                            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                    return (_NOT_VALID, _NOT_IMMUTABLE)
                container_is_immutable = container_is_immutable and check_result[_IMMUTABLE]

    # Now check each defined key in the TypedDict
    annotations: dict[str, Any] = get_type_hints(type_hint)
    for key in annotations:
        if key == '__immutable__' and is_immutable_typed_dict:
            continue
        if key in obj:
            dict_key_info = TypedDictKeyInfo(key, type_hint)
            check_result = _check_instance_of_typehint(
                obj[key], dict_key_info.value_type, options, new_parents, raise_on_error=False)
            if not check_result[_VALID]:
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Value for key '{key}' in TypedDict does not match type hint '{dict_key_info.value_type}'.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return (_NOT_VALID, _NOT_IMMUTABLE)
            container_is_immutable = container_is_immutable and check_result[_IMMUTABLE]
        else:
            if key in required_keys:
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Required key '{key}' missing in TypedDict.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return (_NOT_VALID, _NOT_IMMUTABLE)

    # Successful TypedDict check
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True)
    return (_IS_VALID, container_is_immutable)

def _annotation_is_str_typehint(annotation: Any) -> bool:
    """Check if an annotation is a string type hint (forward reference).

    :param Any annotation: The annotation to check.
    :return bool: True if the annotation is a string type hint, False otherwise.
    """
    return isinstance(annotation, str)

def _container_check_mapping(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Check if obj matches Mapping type hint.
    
    If not a Mapping, returns True to allow other checks to proceed normally.
    The semantic is 'If not a Mapping, this check does not apply and should not cause a
    failure.'

    If it is a Mapping, checks keys and values recursively if specified and args are provided.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    """
    if not issubclass(origin, Mapping):
        return (_IS_VALID, _IS_IMMUTABLE)  # Not a Mapping type hint, so this check does not apply

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    key_type: Any = Any
    value_type: Any = Any
    match(len(args)):
        case 0:
            pass  # No type arguments, so we accept any key/value types
        case 2:
            key_type, value_type = args
        case _:
            raise SimpleBenchValueError(
                f"Mapping type hint '{origin}' has invalid number of arguments: {len(args)}",
                tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
    new_parents = parents.copy()
    new_parents.add(id(obj))
    container_is_immutable: bool = isinstance(obj, Immutable)
    for key, value in obj.items():
        key_check = _check_instance_of_typehint(key, key_type, options, new_parents, raise_on_error=False)
        if not key_check[_VALID]:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Key '{key}' in Mapping does not match type hint '{key_type}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return (_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and key_check[_IMMUTABLE]
        value_check = _check_instance_of_typehint(value, value_type, options, new_parents, raise_on_error=False)
        if not value_check[_VALID]:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Value for key '{key}' in Mapping does not match type hint '{value_type}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return (_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and value_check[_IMMUTABLE]

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True)
    return (_IS_VALID, container_is_immutable)

def _container_check_set(
        obj: Set,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Check if obj matches Set type hint.

    If type_hint is not a Set, returns True to allow other checks to proceed normally.
    The semantic is 'If not a Set, this check does not apply and should not cause a
    failure.' If it is a Set, checks items recursively if specified and args are provided.

    :param Set obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    """
    if not issubclass(origin, Set):
        return (_IS_VALID, _IS_IMMUTABLE)  # Not a Set, so this check does not apply

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if not isinstance(obj, Set): # fast fail path
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj)}' is not a Set for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (_NOT_VALID, _NOT_IMMUTABLE)

    container_is_immutable: bool = isinstance(obj, Immutable)

    new_parents = parents.copy()
    new_parents.add(id(obj))
    for item in obj:
        item_check = _check_instance_of_typehint(
            item, args[0] if args else Any, options, new_parents, raise_on_error=False)
        if not item_check[_VALID]:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Set does not match type hint '{args[0] if args else Any}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return (_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and item_check[_IMMUTABLE]

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True)
    return (_IS_VALID, container_is_immutable)

def _container_check_sequence(
        obj: Sequence,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Check if obj matches Sequence type hint.

    If the type_hint is not a Sequence, returns True to allow other checks to proceed normally.
    The semantic is 'If not a Sequence, this check does not apply and should not cause
    a failure.' If it is a Sequence, checks items recursively if specified and args are provided.

    :param Sequence obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    """
    if not issubclass(origin, Sequence):
        return (_IS_VALID, _IS_IMMUTABLE)  # Not a Sequence type hint, so this check does not apply

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    # Broad check first
    if not isinstance(obj, Sequence):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj)}' is not a Sequence for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (_NOT_VALID, _NOT_IMMUTABLE)

    # Special case: str and bytes are Sequences but we treat them as primitives
    # and not container types here. We don't need to check their items.
    if isinstance(obj, (str, bytes)):
        if origin in (list, tuple):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Object of type '{type(obj)}' is a primitive str/bytes, "
                    f"not a '{origin.__name__}' Sequence for type hint '{type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return (_NOT_VALID, _NOT_IMMUTABLE)
        return (_IS_VALID, _IS_IMMUTABLE)

    if not isinstance(obj, origin):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an instance of '{origin.__name__}' "
                f"for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (_NOT_VALID, _NOT_IMMUTABLE)

    container_is_immutable: bool = isinstance(obj, Immutable)

    new_parents = parents.copy()
    new_parents.add(id(obj))
    item_type_hint: Any = args[0] if args else Any
    for item in obj:
        item_check = _check_instance_of_typehint(item, item_type_hint, options, new_parents, raise_on_error=False)
        if not item_check[_VALID]:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Sequence does not match type hint '{item_type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return (_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and item_check[_IMMUTABLE]

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True)
    return (_IS_VALID, container_is_immutable)

def _container_check_iterable(
        obj: Iterable,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[int],
        raise_on_error: bool = False) -> CheckResult:
    """Check if obj matches a generic Iterable type hint.

    This function should only be called after checks for more specific container
    types (Mapping, Sequence, Set) have already failed.

    It handles the safe, non-consuming validation of Iterators by default.

    :param Iterable obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param Options options: Options for type hint validation.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    """
    if not issubclass(origin, Iterable):
        return (_IS_VALID, _IS_IMMUTABLE)  # Not an Iterable type hint, so this check does not apply

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return (cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    # This check must come before the Iterator check, as str/bytes are Iterable but not Iterator.
    if isinstance(obj, (str, bytes)):
        # We treat str/bytes as primitives. If we're here, it means a more specific
        # check like Sequence[str] didn't catch it, so we consider it valid against
        # a generic Iterable hint (e.g., Iterable[str]).
        return (_IS_VALID, _IS_IMMUTABLE)

    # Short-circuit for single-pass Iterators if configured to do so.
    # We assume it is NOT immutable since we cannot check its items without consuming it.
    if isinstance(obj, Iterator) and not options.consume_iterators:
        return (_IS_VALID, _NOT_IMMUTABLE)

    if not isinstance(obj, Iterable):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an instance of '{origin.__name__}' "
                f"for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (_NOT_VALID, _NOT_IMMUTABLE)

    container_is_immutable: bool = isinstance(obj, Immutable)
    new_parents = parents.copy()
    new_parents.add(id(obj))

    item_type_hint: Any = args[0] if args else Any
    for item in obj:
        item_check = _check_instance_of_typehint(item, item_type_hint, options, new_parents, raise_on_error=False)
        if not item_check[_VALID]:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Iterable does not match type hint '{item_type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return (_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and item_check[_IMMUTABLE]

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True)
    return (_IS_VALID, container_is_immutable)

def _container_check_callable(
        obj: Callable,
        type_hint: Any,
        origin: Any,
        args: tuple,
        raise_on_error: bool = False) -> CheckResult:
    """Check if obj matches Callable type hint.
    If not a Callable, returns True to allow other checks to proceed normally.
    If it is a Callable, checks parameters and return type recursively if specified
    and args are provided.

    :param Callable obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the type hint.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    """
    if not issubclass(origin, Callable):
        return (_IS_VALID, _IS_IMMUTABLE)  # Not a Callable type hint, so this check does not apply

    if not callable(obj):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not callable.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return (_NOT_VALID, _NOT_IMMUTABLE)

    # If no args, just being callable is enough. Callables are not immutable.
    if not args:
        return (_IS_VALID, _NOT_IMMUTABLE)

    # Callable[..., ReturnType] (ellipsis means any arguments)
    if args[0] is Ellipsis:
        if len(args) == 2:  # Optionally check return type if possible
            try:
                sig = inspect.signature(obj)
                return_annotation = sig.return_annotation
                expected_return_type = args[1]
                if return_annotation is not inspect.Signature.empty:
                    # Check if the actual return type is a subtype of the expected one (covariance)
                    if not _is_subtype_of_typehint(return_annotation, expected_return_type):
                        if raise_on_error:
                            raise SimpleBenchTypeError(
                                f"Callable's annotated return type '{return_annotation}' is not compatible with "
                                f"expected return type '{expected_return_type}'.",
                                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                        return (_NOT_VALID, _NOT_IMMUTABLE)
            except (ValueError, TypeError):
                pass  # Built-ins or C callables may not have signatures
        return (_IS_VALID, _NOT_IMMUTABLE)

    # Callable[[ArgTypes...], ReturnType]
    param_types = args[0]
    return_type = args[1] if len(args) > 1 else None

    try:
        sig = inspect.signature(obj)
        params = list(sig.parameters.values())
        # Check number of parameters matches
        if len(param_types) != len(params):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Callable has {len(params)} parameters, expected {len(param_types)} "
                    f"for type hint '{type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return (_NOT_VALID, _NOT_IMMUTABLE)

        # Check parameter types if possible
        for param, expected_type in zip(params, param_types):
            if param.annotation is not inspect.Parameter.empty:
                # Check if the expected param type is a subtype of the actual one (contravariance)
                if not _is_subtype_of_typehint(expected_type, param.annotation):
                    if raise_on_error:
                        raise SimpleBenchTypeError(
                            f"Expected parameter type '{expected_type}' is not compatible with "
                            f"callable's annotated parameter type '{param.annotation}' for param '{param.name}'.",
                            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                    return (_NOT_VALID, _NOT_IMMUTABLE)

        # Check return type if possible
        if return_type is not None and sig.return_annotation is not inspect.Signature.empty:
            # Check if the actual return annotation is a subtype of the expected return type (covariance)
            if not _is_subtype_of_typehint(sig.return_annotation, return_type):
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Callable's annotated return type '{sig.return_annotation}' does not match "
                        f"expected type hint '{return_type}'.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return (_NOT_VALID, _NOT_IMMUTABLE)
    except (ValueError, TypeError):
        # Builtins or C callables may not have signatures; fallback to just callable
        return (_IS_VALID, _NOT_IMMUTABLE)

    return (_IS_VALID, _NOT_IMMUTABLE)

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

    if type_hint in ImmutablePrimitiveTypesTuple:
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
