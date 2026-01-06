"""Helper functions to validate container types against type hints."""
import inspect
import sys
from collections.abc import Callable, Collection, Iterable, Iterator, Mapping, Sequence, Set
from typing import Any, get_type_hints, is_typeddict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import Immutable, is_immutable_typeddict_typehint

from .._cache import _CACHE
from .._check_result import CheckResult
from .._constants import _IS_IMMUTABLE, _IS_VALID, _NOT_IMMUTABLE, _NOT_VALID
from .._error_tags import _TypeHintsErrorTag
from .._log import log
from .._options import Options
from .._validation_state import ValidationState

__all__ = (
    "_check_collections_abc_sequence",
)

def _check_collections_abc_sequence(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Sequence types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Sequence type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If origin is not a subclass of Sequence.
    """
    from .._type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_sequence: Checking object of type '%s' against Sequence type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Sequence):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Sequence.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    # Broad check first
    if not isinstance(obj, Sequence):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not a Sequence, but type hint is '{type_hint}'",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    # Special case: str and bytes are Sequences but we treat them as primitives
    # and not container types here. We don't need to check their items.
    if isinstance(obj, (str, bytes)):
        if origin in (list, tuple):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Object of type '{type(obj)}' is a primitive str/bytes, "
                    f"not a '{origin.__name__}' Sequence for type hint '{type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    if not isinstance(obj, origin):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an instance of '{origin.__name__}' "
                f"for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    container_is_immutable: bool = isinstance(obj, Immutable)

    new_parents = parents | {ValidationState(id(obj), type_hint, "sequence")}
    item_type_hint: Any = args[0] if args else Any
    for item in obj:
        is_valid, is_imm = _check_instance_of_typehint(
            item, item_type_hint, options, new_parents, raise_on_error=False, context="sequence_item")
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Sequence does not match type hint '{item_type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and is_imm

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True, options.noncachable_types)
    return CheckResult(_IS_VALID, container_is_immutable)
