"""Helper functions to validate container types against type hints."""
import inspect
from collections.abc import Callable
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from .._check_result import CheckResult
from .._constants import IS_VALID, NOT_IMMUTABLE, NOT_VALID
from .._error_tags import _TypeHintsErrorTag
from .._log import log

__all__ = (
    "_check_collections_abc_callable",
)

def _check_collections_abc_callable(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        raise_on_error: bool = False) -> CheckResult:
    """Handle Callable types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Callable type hint.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If origin is not a subclass of Callable.
    """
    from .._type_hints import _is_subtype_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_callable: Checking object of type '%s' against Callable type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Callable):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Callable.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    if not callable(obj):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not callable.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(NOT_VALID, NOT_IMMUTABLE)

    # If no args, just being callable is enough. Callables are not immutable.
    if not args:
        return CheckResult(IS_VALID, NOT_IMMUTABLE)

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
                        return CheckResult(NOT_VALID, NOT_IMMUTABLE)
            except (ValueError, TypeError):
                pass  # Built-ins or C callables may not have signatures
        return CheckResult(IS_VALID, NOT_IMMUTABLE)

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
            return CheckResult(NOT_VALID, NOT_IMMUTABLE)

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
                    return CheckResult(NOT_VALID, NOT_IMMUTABLE)

        # Check return type if possible
        if return_type is not None and sig.return_annotation is not inspect.Signature.empty:
            # Check if the actual return annotation is a subtype of the expected return type (covariance)
            if not _is_subtype_of_typehint(sig.return_annotation, return_type):
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Callable's annotated return type '{sig.return_annotation}' does not match "
                        f"expected type hint '{return_type}'.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return CheckResult(NOT_VALID, NOT_IMMUTABLE)
    except (ValueError, TypeError):
        # Builtins or C callables may not have signatures; fallback to just callable
        return CheckResult(IS_VALID, NOT_IMMUTABLE)

    return CheckResult(IS_VALID, NOT_IMMUTABLE)
