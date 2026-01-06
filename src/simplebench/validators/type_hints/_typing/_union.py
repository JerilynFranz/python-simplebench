"""Validation functions for type hints and instances against those type hints."""
from types import UnionType
from typing import Any, Union

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from .._cache import _CACHE
from .._check_result import CheckResult
from .._constants import NOT_VALID
from .._error_tags import _TypeHintsErrorTag
from .._immutable import _is_immutable
from .._log import log
from .._options import Options
from .._validation_state import ValidationState

__all__ = (
    "_check_typing_union",
)

def _check_typing_union(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Union types first as an exclusive check. 
    
    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param tuple args: The type arguments of the Union type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails
    :raises SimpleBenchValueError: If type_hint is not a Union type.
    """
    from .._type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug("_union_check: Checking object of type '%s' against Union type hint '%s'",
                type(obj).__name__, type_hint)
    if origin not in (Union, UnionType):  # Sanity check for bad calls
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Union type.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
    new_parents = parents.copy()
    new_parents.add(ValidationState(id(obj), type_hint, "union"))
    for arg in args:
        # Recursively check against each type in the Union
        is_valid, is_imm = _check_instance_of_typehint(
            obj, arg, options, new_parents, raise_on_error=False, context="union_item")

        # If a match is found, return immediately
        if is_valid:
            # We can cache the result for the specific matching type `arg`
            if is_imm:
                _CACHE.add_cache_entry(arg, obj, True, options.noncachable_types)
            return CheckResult(is_valid, is_imm)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return CheckResult(NOT_VALID, _is_immutable(obj))
