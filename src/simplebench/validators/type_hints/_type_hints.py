"""Validation functions for type hints and instances against those type hints."""
from collections.abc import Hashable
from types import NoneType, UnionType
from typing import Any, Literal, TypedDict, TypeVar, Union, get_args, get_origin, is_typeddict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from . import _validate as validate
from ._cache import _CACHE
from ._check_result import CheckResult
from ._constants import IS_IMMUTABLE, IS_VALID, NOT_IMMUTABLE, NOT_VALID
from ._error_tags import _TypeHintsErrorTag
from ._forward_references import resolve_type_hint
from ._generic import _check_generic
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
        noncachable_types: set[type[Any]] | None = None,
        resolve_forward_references: bool = True,
        globalns:dict[str, Any] | None = None,
        localns:dict[str, Any] | None = None,
        ) -> bool:
    """
    Check if an object is an instance of a given type hint.
    Supports basic types, generics, Union, Literal, and TypedDict.

    This function acts like a runtime version of `isinstance()` for type hints.

    Example:

    .. code-block:: python
        from typing import TypedDict, TypeAlias
        from simplebench.validators.type_hints import isinstance_of_typehint

        class Person(TypedDict):
            name: str
            age: int
        
        DataType: TypeAlias = list[int] | Person  # TypeAlias is optional, but clarifies intent for static analysis
        data: DataType = {"name": "Alice", "age": 30}
        result = isinstance_of_typehint(data, DataType)
        print(result)  # True

        more_data = Person(name="Bob", age=25)
        result = isinstance_of_typehint(more_data, Person)
        print(result)  # True

        bad_data = {"name": "Charlie", "age": "thirty"}
        result = isinstance_of_typehint(bad_data, Person)
        print(result)  # False
        
    It can validate whether an object conforms to complex type hints the same way
    that static type checkers do - but at runtime. This makes it useful for
    validating function arguments, configuration data, or any other data structures
    against expected types at runtime.

    This is much, much slower than a normal isinstance() check due to the complexity
    of full type hint validation. It is not intended for performance-critical paths.
    If you can use normal :func:`isinstance` checks, do so.

    It does, however, use an internal cache to speed up repeated checks
    for the same object and type hint combination, especially for immutable objects
    and it caches internal validation results for immutable sub-objects.

    While caching improves performance for repeated checks, the first-time
    validation of complex type hints may still be relatively slow.

    Slow in this context means on the order of milliseconds for complex nested
    structures. And it can be much slower if the structure is very deep or complex.
    An example of a pathological case would be a list of millions of items
    where each item must be validated against a complex type hint. A
    type like `list[str | int | dict[str, list[float | None]]]` with
    millions of items would be very slow to validate the first time.

    In such cases, consider simplifying the type hints. For example, using
    `list[Any]` or `list[object]` would be much faster, though less precise
    or simply write a custom validation function for your specific use case.

    It is **MUCH** faster to do something like:

    .. code-block:: python
        if isinstance(data, list):
           valid = all(isinstance(item, (str, int, dict)) for item in data)
        else:
           valid = False
    
    than to do:
    .. code-block:: python
        valid = isinstance_of_typehint(data, list[str | int | dict[str, list[float | None]]])

    This can be greatly mitigated by caching if you use immutable objects and
    repeatedly check the same type hints against them or sub-objects within them.

    Where isinstance_of_typehint is most useful is in validating
    configuration data or other data structures that are not performance-critical
    but need to be validated against complex type hints at runtime.

    Things like nested configuration dictionaries (particularly TypedDicts),
    JSON data structures, or other complex data that benefit from type hint
    validation but are not performance-critical.

    This is a simple and easily understandable method for runtime type hint
    validation, but it cannot cover all edge cases due to the complexity of
    Python's type hinting system. It is designed to handle the most common
    use cases effectively.

    If you need both performance and type hint validation, consider using
    specialized libraries like `pydantic <https://pydantic-docs.helpmanual.io/>`_ 
    or `attrs <https://www.attrs.org/en/stable/>`_ that are optimized
    for runtime data validation with type hints. They are more complex
    to use but can offer far better performance for specific use cases.

    A :class:`~simplebench.types.Immutable` superclass can be used to mark
    user-defined classes as immutable for caching purposes. There is also
    a :class:`~simplebench.types.ImmutableTypedDict` type that can be used
    to mark immutable TypedDicts. If your objects are immutable, caching
    will be much more effective. 

    The checker automatically treats built-in immutable types (NoneType, bool, int, float,
    complex, str, bytes) as immutable for caching purposes and when composed
    using immutable containers such as `frozenset`, `tuple`, and `MappingProxyType`.

    While it tries to be efficient, it cannot be optimized for high-performance scenarios
    in general. You should benchmark your specific use case if performance is a concern.

    .. warning::
        While it tries to handle forward references (such as those generated
        by `from __future__ import annotations`) in type hints if the
        `resolve_forward_references` parameter is `True` (the default),
        it may not cover all edge cases. There *may* be a small performance speedup
        by setting `resolve_forward_references` to `False` if you do not
        have forward references in your type hints.

        If you have complex forward references, consider resolving them manually
        before passing them to this function and not using `from __future__ import annotations`
        if you do not actually have to.
        
        If you pass `globalns` and `localns`, it will use those to help resolve forward
        references in type hints. If you do not provide them, it may not be able to
        resolve all forward references correctly.
        
        There is a performance cost to inferring these namespaces or resolving forward
        references, so if you can provide the type hint without using forward references,
        it is strongly recommended.

        Deeply nested or cyclic structures may lead to performance issues or
        maximum recursion depth errors. The `depth` parameter can help mitigate
        this by limiting the recursion depth.

    It is important to note that type hint validation is not foolproof and
    may not cover all edge cases. This is designed for common use cases.

    Because of the complexity of type hint checks, this function may not be able to
    definitively determine type hint compliance for all type hints, especially with
    deeply nested structures.

    The depth parameter limits the recursion depth for nested structures. If the
    depth limit is reached, the function will return `True` for validity, but
    will not validate any deeper levels of the object. This is to prevent infinite
    recursion in case of cyclic references or excessively deep structures. 

    The `depth` parameter is defined as the number of nested levels to check within the object
    structure (including the top-level object). For example:
        - int has a depth of 0.
        - list[int] has a depth of 1.
        - list[list[int]] has a depth of 2.
        - dict[str, list[int]] has a depth of 2.

    If `strict_typed_dict` parameter is `False`, it can validate any `Mapping` subclass
    against a `TypedDict` definition. If `True`, it will only validate actual `dict` instances.
    The default is `False` (allow any `Mapping` subclass).

    Iterators are single-pass by nature. By default, this function will not consume
    iterators during validation to avoid side effects. If `consume_iterators` is set to
    `True`, it will consume iterators to validate their contents, but this may exhaust
    the iterator and affect subsequent usage.

    :param Any obj: The object to check against the type hint.
    :param Any type_hint: The type hint to check against.
    :param bool strict_typed_dict: Whether to enforce that TypedDict checks require actual TypedDict instances.
    :param int depth: (default=50) The recursion depth limit for nested structures.
    :param bool consume_iterators: (optional, default=False) Whether to consume iterators during validation.
    :param set[type[Any]] | None noncachable_types: (optional, default=False) Set of types that should not be cached
        during validation.
        This is intended for types that are immutable but have high variability (e.g., datetime) making
        caching less effective (and tending to bloat the cache without significant performance benefit).
        The internal default set includes NoneType, bool, int, float, complex, str, and bytes and they
        will always be treated as non-cachable.
    :param bool resolve_forward_references: (optional, default=True) Whether to attempt to resolve forward references
        in type hints.
    :param dict[str, Any] | None globalns: (optional, default=None) global namespace for resolving forward references.
    :param dict[str, Any] | None localns: (optional, default=None) local namespace for resolving forward references.

    :return bool: `True` if the object matches the type hint, `False` otherwise.
    """
    validate.resolve_forward_references_arg(resolve_forward_references)
    if resolve_forward_references:
        type_hint_kwargs = {'type_hint': type_hint}
        if globalns is not None:
            type_hint_kwargs['globalns'] = globalns
        if localns is not None:
            type_hint_kwargs['localns'] = localns
        type_hint = resolve_type_hint(**type_hint_kwargs)

    validate.type_hint_arg(type_hint)
    validate.depth_arg(depth)
    validate.strict_typed_dict_arg(strict_typed_dict)
    validate.consume_iterators_arg(consume_iterators)
    validate.noncachable_types_arg(noncachable_types)

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
    :return CheckResult: Named tuple indicating (is_valid (obj.valid), is_immutable (obj.immutable)).
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
            return CheckResult(cached_result, IS_IMMUTABLE)
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
        return CheckResult(IS_VALID, NOT_IMMUTABLE)

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
        return CheckResult(NOT_VALID, NOT_IMMUTABLE)

    new_parents = parents | {current_state}

    # Unwrap Final, ClassVar and Annotated type hints
    if origin is not None and origin.__module__ == 'typing':
        if origin.__name__ in {'Final', 'ClassVar', 'Annotated'}:
            log.debug("_check_instance_of_typehint: Unwrapping %s type hint '%s'", origin.__name__, type_hint)
            if not args:
                raise SimpleBenchValueError(
                    f"{origin.__name__} type hint '{type_hint}' has no arguments.",
                    tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
            type_hint = args[0]
            return _check_instance_of_typehint(obj, type_hint, options, new_parents, raise_on_error, context=context)

    # Unwrap NewType definitions
    if _is_new_type(type_hint):
        supertype = type_hint.__supertype__
        log.debug("_check_instance_of_typehint: Detected NewType '%s' with supertype '%s'",
                  type_hint, supertype)
        if not isinstance(obj, supertype):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Object of type '{type(obj).__name__}' is not an instance of NewType supertype '{supertype}'",
                    tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)
            return CheckResult(NOT_VALID, NOT_IMMUTABLE)
        log.debug("_check_instance_of_typehint: Unwrapping NewType '%s' to supertype '%s'",
                    type_hint, supertype)
        type_hint = supertype
        return _check_instance_of_typehint(obj, type_hint, options, new_parents, raise_on_error, context="root")

    # Handle TypeVar before generic/container checks and caching
    if isinstance(type_hint, TypeVar):
        log.debug("_check_instance_of_typehint: Handling TypeVar '%s'", type_hint)
        if type_hint.__constraints__:
            # Accept if obj matches any constraint
            for constraint in type_hint.__constraints__:
                if _check_instance_of_typehint(obj, constraint, options, new_parents, False, context=context).valid:
                    return CheckResult(IS_VALID, _is_immutable(obj))
            return CheckResult(NOT_VALID, _is_immutable(obj))
        elif type_hint.__bound__:
            # Accept if obj matches the bound
            return _check_instance_of_typehint(
                obj, type_hint.__bound__, options, new_parents, raise_on_error, context=context)
        else:
            # Unconstrained TypeVar: treat as Any
            return CheckResult(IS_VALID, _is_immutable(obj))

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
        return CheckResult(NOT_VALID, NOT_IMMUTABLE)

    log.debug("_check_instance_of_typehint: Checking if type hint is Any (%s)", type_hint)
    if type_hint is Any:
        log.debug(
            "_check_instance_of_typehint: Type hint is Any, automatically valid")
        return CheckResult(IS_VALID, _is_immutable(obj))

    # fast paths for primitives. Caching would be pointless here. It takes much more time to cache than to check.
    # We don't have to worry about None/NoneType here because they were handled above.
    if type_hint in {object, Hashable}:
        log.debug(
            "_check_instance_of_typehint: Type hint '%s' - checking if object is primitive type", type_hint)
        if isinstance(obj, (float, int, bool, complex, bytes, str)):
            log.debug(
                "_check_instance_of_typehint: Type hint '%s' is automatically valid for primitive objects of type '%s'",
                type_hint, type(obj).__name__)
            return CheckResult(IS_VALID, IS_IMMUTABLE)

    log.debug("_check_instance_of_typehint: Checking if type_hint '%s' is a primitive type hint", type_hint)
    if type_hint in {int, float, complex, bool, bytes, str}:
        log.debug("_check_instance_of_typehint: Checking if object (%s) matches type hint for primitives check '%s'",
                  type(obj).__name__, type_hint)
        if isinstance(obj, type_hint):
            log.debug(
                "_check_instance_of_typehint: Object of type '%s' matches primitive type hint '%s'",
                type(obj).__name__, type_hint)
            return CheckResult(IS_VALID, IS_IMMUTABLE)
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' does not match primitive type hint '{type_hint}'",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(NOT_VALID, IS_IMMUTABLE)

    log.debug(
        "_check_instance_of_typehint: Object of type '%s'' is not a primitive data type', proceeding with full check",
        type(obj).__name__)

    if origin in (Union, UnionType):
        return _check_typing_union(obj, type_hint, origin, args, options, new_parents, raise_on_error)

    if origin is Literal:
        return _check_typing_literal(obj, type_hint, origin, args, raise_on_error)

    if is_typeddict(type_hint):
        return _check_typing_typeddict(obj, type_hint, options, new_parents, raise_on_error)

    result: CheckResult = _check_generic(
            obj, type_hint, origin, args, options, new_parents, raise_on_error, context='root')

    if result.immutable:
        _CACHE.add_cache_entry(type_hint, obj, result.valid, options.noncachable_types)

    if raise_on_error and not result.valid:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj).__name__}' is not an instance of type hint '{type_hint}'",
            tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)

    return result

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
            return CheckResult(cached_result, IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if type_hint in {NoneType, None, Any, object, Hashable}:
        return CheckResult(IS_VALID, IS_IMMUTABLE)

    if origin is Literal and None in args:
        return CheckResult(IS_VALID, IS_IMMUTABLE)

    if origin in (Union, UnionType):
        for arg in args:
            is_valid, _ = _check_instance_of_typehint(
                obj, arg, options, parents, raise_on_error=False, context="none_union_item")
            if is_valid:
                return CheckResult(IS_VALID, IS_IMMUTABLE)

    check_result = CheckResult(NOT_VALID, IS_IMMUTABLE)
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

def _is_new_type(tp: Any) -> bool:
    """Check if a type hint is a NewType definition."""
    log.debug("_is_new_type: Checking if type hint '%s' is a NewType", tp)
    log.debug("_is_new_type: Type hint '%s' is callable: %s", tp, callable(tp))
    log.debug("_is_new_type: Type hint '%s' has __supertype__: %s", tp, hasattr(tp, '__supertype__'))
    log.debug("_is_new_type: Type hint '%s' __annotations__: %s", tp, getattr(tp, '__annotations__', 'N/A'))
    return (
        callable(tp)
        and hasattr(tp, '__supertype__')
    )