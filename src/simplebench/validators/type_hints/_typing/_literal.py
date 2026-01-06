"""Validator for typing.Literal type hints."""
from typing import Any, Literal

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from .._check_result import CheckResult
from .._constants import _IS_IMMUTABLE, _IS_VALID, _NOT_VALID
from .._error_tags import _TypeHintsErrorTag
from .._immutable import _is_immutable

__all__ = (
    "_check_typing_literal",
)

def _check_typing_literal(
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

    if obj in args:
        return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    if raise_on_error:
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
    return CheckResult(_NOT_VALID, _is_immutable(obj))
