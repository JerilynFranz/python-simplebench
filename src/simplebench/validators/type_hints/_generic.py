"""Helper functions to validate user-defined generic types against type hints."""
from collections.abc import Callable, Collection, Iterable, Mapping, Sequence, Set
from typing import Any, Protocol

from simplebench.exceptions import SimpleBenchTypeError

from ._cache import _CACHE
from ._check_result import CheckResult
from ._constants import IS_IMMUTABLE, IS_VALID, NOT_IMMUTABLE, NOT_VALID
from ._error_tags import _TypeHintsErrorTag
from ._immutable import _is_immutable
from ._log import log
from ._options import Options
from ._validation_state import ValidationState

__all__ = (
    "_check_generic",
)

def _check_generic(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False,
        context: str = "") -> CheckResult:
    """
    Check user-defined generic types.

    :param Any obj: The object to check.
    :param Any type_hint: The user-defined generic type hint.
    :param Any origin: The origin of the generic type.
    :param tuple args: The type arguments for the generic.
    :param options: Validation options.
    :param set parents: Parent validation states for cycle detection.
    :param bool raise_on_error: Whether to raise on validation failure.
    :param str context: Context of the validation for error reporting.
    :return: CheckResult indicating (is_valid, is_immutable).
    """
    from ._collections_abc import (  # pylint: disable=import-outside-toplevel
        _check_collections_abc_callable,
        _check_collections_abc_collection,
        _check_collections_abc_iterable,
        _check_collections_abc_mapping,
        _check_collections_abc_sequence,
        _check_collections_abc_set,
    )
    from ._type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel
    from ._typing import _check_typing_typeddict  # pylint: disable=import-outside-toplevel

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

    obj_is_immutable: bool = _is_immutable(obj)

    # handler for non-runtime Protocols
    if (hasattr(type_hint, '__mro__')
        and any(base is Protocol for base in type_hint.__mro__)
        and not getattr(type_hint, '_is_runtime_protocol', False)):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f'Protocol {type_hint} is not runtime checkable.',
                tag=_TypeHintsErrorTag.NON_RUNTIME_CHECKABLE_PROTOCOL)
        return CheckResult(NOT_VALID, obj_is_immutable)

    if origin is None and isinstance(type_hint, type):
        if issubclass(type_hint, Mapping):
            log.debug("_check_generic: Detected Mapping type hint '%s'", type_hint)
            origin = type_hint
            args = (Any, Any)
        elif issubclass(type_hint, Iterable):
            log.debug("_check_generic: Detected Iterable type hint '%s'", type_hint)
            origin = type_hint
            args = (Any,)
        elif issubclass(type_hint, Callable):
            log.debug("_check_generic: Detected Callable type hint '%s'", type_hint)
            origin = type_hint
            args = (..., Any)

    # Check instance type for generics
    if origin is None:
        valid = isinstance(obj, type_hint)
        if valid:
            if obj_is_immutable:
                _CACHE.add_cache_entry(type_hint, obj, IS_VALID, options.noncachable_types)
            return CheckResult(IS_VALID, obj_is_immutable)
        if raise_on_error:
            raise SimpleBenchTypeError(
                f'Object of type {type(obj).__name__} is not an instance of {type_hint} (origin = {origin}, args = {args})',
                tag=_TypeHintsErrorTag.VALIDATION_FAILED
            )
        return CheckResult(NOT_VALID, obj_is_immutable)
        
    try:
        if not isinstance(obj, origin):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f'Object of type {type(obj).__name__} is not an instance of {origin.__name__}',
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED
                )
            return CheckResult(NOT_VALID, obj_is_immutable)
    except TypeError:
        raise SimpleBenchTypeError(
            f'Origin {origin} ({type_hint}) is not a valid type for isinstance check.',
            tag=_TypeHintsErrorTag.VALIDATION_FAILED
        )

    # If no args, treat as non-parameterized generic
    try:
        if not args and isinstance(obj, type_hint):
            if obj_is_immutable:
                _CACHE.add_cache_entry(type_hint, obj, IS_VALID, options.noncachable_types)
            return CheckResult(IS_VALID, obj_is_immutable)
    except TypeError:
        pass

    # Dispatch to the appropriate container check.
    # The order (most specific to most general) is important.
    # The if..elif chain ensures that only one container check is applied
    # and that it is the most specific one available.
    result: CheckResult | None = None

    new_parents = parents.copy()
    new_parents.add(ValidationState(id(obj), type_hint, context))

    if origin:
        # Fast fail path for collections.abc
        is_collections_abc: bool
        try:
            is_collections_abc = issubclass(origin, (Iterable, Callable))
        except TypeError:
            is_collections_abc = False

        # primary check path for all collections.abc types
        # Order of checks is important: most specific to most general
        # Each check is mutually exclusive due to the if..elif structure
        # and is designed to pick the most specific applicable check.
        if is_collections_abc:
            if issubclass(origin, Mapping):
                result = _check_collections_abc_mapping(
                    obj, type_hint, origin, args, options, new_parents, raise_on_error)
            elif issubclass(origin, Set):
                result = _check_collections_abc_set(
                    obj, type_hint, origin, args, options, new_parents, raise_on_error)
            elif issubclass(origin, Sequence):
                result = _check_collections_abc_sequence(
                    obj, type_hint, origin, args, options, new_parents, raise_on_error)
            elif issubclass(origin, Collection):
                result = _check_collections_abc_collection(
                    obj, type_hint, origin, args, options, new_parents, raise_on_error)
            elif issubclass(origin, Iterable):
                result = _check_collections_abc_iterable(
                    obj, type_hint, origin, args, options, new_parents, raise_on_error)
            elif issubclass(origin, Callable):
                result = _check_collections_abc_callable(
                    obj, type_hint, origin, args, raise_on_error)

    if result is not None:
        if result.valid and result.immutable:
            _CACHE.add_cache_entry(type_hint, obj, result.immutable, options.noncachable_types)
        if raise_on_error and not result.valid:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an instance of generic type hint '{type_hint}'",
                tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)
        return result

    # Fallback for other generics, including user-defined generics.
    log.debug(
        "_check_generic: Fallback check for object of type '%s' against generic type hint '%s'",
        type(obj).__name__, type_hint)

    # Validate each __orig_class__ parameter if available
    if hasattr(obj, '__orig_class__'):
        obj_args = getattr(obj.__orig_class__, '__args__', ())
        if len(obj_args) == len(args):
            for item, hint in zip(obj_args, args):
                is_valid, is_imm = _check_instance_of_typehint(
                    item, hint, options, parents, raise_on_error, context="generic_parameter")
                obj_is_immutable = obj_is_immutable and is_imm
                if not is_valid:
                    if raise_on_error:
                        raise SimpleBenchTypeError(
                            f"Generic parameter '{item}' does not match type hint '{hint}'.",
                            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                    return CheckResult(NOT_VALID, NOT_IMMUTABLE)

            if obj_is_immutable:
                _CACHE.add_cache_entry(type_hint, obj, IS_VALID, options.noncachable_types)
            return CheckResult(IS_VALID, obj_is_immutable)

    # Validate type parameters for user-defined generics if __orig_class__ is not present
    if not hasattr(obj, '__orig_class__'):
        obj_type = type(obj)
        obj_origin = getattr(obj_type, '__origin__', None)
        obj_args = getattr(obj_type, '__args__', None)
        if obj_origin is origin and obj_args is not None and len(obj_args) == len(args):
            for item, hint in zip(obj_args, args):
                is_valid, is_imm = _check_instance_of_typehint(
                    item, hint, options, parents, raise_on_error, context="generic_parameter")
                obj_is_immutable = obj_is_immutable and is_imm
                if not is_valid:
                    if raise_on_error:
                        raise SimpleBenchTypeError(
                            f"Generic parameter '{item}' does not match type hint '{hint}'.",
                            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                    return CheckResult(NOT_VALID, NOT_IMMUTABLE)
            if obj_is_immutable:
                _CACHE.add_cache_entry(type_hint, obj, IS_VALID, options.noncachable_types)
            return CheckResult(IS_VALID, obj_is_immutable)

    # Fallback: check contained items if possible
    if hasattr(obj, '__iter__'):
        for item in obj:
            is_valid, is_imm = _check_instance_of_typehint(
                item, args[0], options, parents, raise_on_error, context="generic_item")
            obj_is_immutable = obj_is_immutable and is_imm
            if not is_valid:
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Object of type '{type(obj).__name__}' is not an instance of generic type hint '{type_hint}'",
                        tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)
                return CheckResult(NOT_VALID, NOT_IMMUTABLE)

    result = CheckResult(IS_VALID, obj_is_immutable)

    if obj_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, result.valid, options.noncachable_types)

    if raise_on_error and not result.valid:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj).__name__}' is not an instance of generic type hint '{type_hint}'",
            tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)
    return result

