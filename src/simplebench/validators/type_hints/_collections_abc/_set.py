"""Helper functions to validate container types against type hints."""
from collections.abc import Set
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import Immutable

from .._cache import _CACHE
from .._check_result import CheckResult
from .._constants import IS_IMMUTABLE, IS_VALID, NOT_IMMUTABLE, NOT_VALID
from .._error_tags import _TypeHintsErrorTag
from .._log import log
from .._options import Options
from .._validation_state import ValidationState

__all__ = (
    "_check_collections_abc_set",
)

def _check_collections_abc_set(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Set types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Set type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If origin is not a subclass of Set.
    """
    from .._type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_set: Checking object of type '%s' against Set type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Set):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Set.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if not isinstance(obj, Set):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not a Set, but type hint is '{type_hint}'",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(NOT_VALID, NOT_IMMUTABLE)

    if not isinstance(obj, origin):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an instance of '{origin.__name__}' "
                f"for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(NOT_VALID, NOT_IMMUTABLE)

    item_type: Any = Any
    if len(args) == 1:
        item_type = args[0]
    elif len(args) > 1:
        raise SimpleBenchValueError(
            f"Set type hint '{origin}' has invalid number of arguments: {len(args)}",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    new_parents = parents | {ValidationState(id(obj), type_hint, "set")}
    container_is_immutable: bool = isinstance(obj, Immutable)
    for item in obj:
        is_valid, is_imm = _check_instance_of_typehint(
            item, item_type, options, new_parents, raise_on_error, context="set_item")
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Set does not match type hint '{args[0] if args else Any}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(NOT_VALID, NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and is_imm

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, IS_IMMUTABLE, options.noncachable_types)
    return CheckResult(IS_VALID, container_is_immutable)
