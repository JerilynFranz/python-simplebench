"""Validators for reporters stuff."""
from __future__ import annotations
import inspect
from typing import Any, Callable, get_type_hints


from ..exceptions import SimpleBenchTypeError, ErrorTag
from ..enums import Section, Format
from .protocols import ReporterCallback

_CASE_IMPORTED: bool = False
"""Indicates whether Case has been imported yet."""
# Placeholder for deferred import of Case
Case = None   # pylint: disable=invalid-name


def deferred_case_import() -> None:
    """Deferrred import of Case to avoid circular imports during initialization."""
    global Case, _CASE_IMPORTED  # pylint: disable=global-statement
    if _CASE_IMPORTED:
        return
    from ..case import Case  # pylint: disable=redefined-outer-name,import-outside-toplevel
    _CASE_IMPORTED = True


def resolve_callback_type_hints(callback: Callable) -> dict[str, type]:
    """Resolve the type hints for a callback function.

    Args:
        callback (Callable): The callback function to resolve type hints for.

    Returns:
        dict[str, type]: A dictionary mapping parameter names to their resolved types.

    Raises:
        SimpleBenchTypeError: If the type hints cannot be resolved.
    """
    try:
        resolved_hints = get_type_hints(
            callback, globalns=callback.__globals__)  # pyright: ignore[reportAttributeAccessIssue]
    except (NameError, TypeError) as e:
        # This can happen if an annotation refers to a type that doesn't exist.
        raise SimpleBenchTypeError(
            f"Invalid callback: {callback}. Could not resolve type hints. Original error: {e}",
            tag=ErrorTag.VALIDATE_INVALID_CALLBACK_UNRESOLVABLE_HINTS
        ) from e
    return resolved_hints


def validate_callback_parameter(callback: Callable,
                                expected_type: type | Any,
                                param_name: str) -> None:
    """Validate a parameter of the callback function.

    The parameter must exist, be of the expected type, and be a keyword-only parameter.

    Args:
        callback (Callable): The callback function to validate.
        expected_type (type | Any): The expected type of the parameter.
        param_name (str): The name of the parameter to validate.

    Raises:
        SimpleBenchTypeError: If the parameter is invalid.
    """
    resolved_hints = resolve_callback_type_hints(callback)
    callback_signature = inspect.signature(callback)
    if param_name not in callback_signature.parameters:
        raise SimpleBenchTypeError(
            f'Invalid callback: {callback}. Must accept an "{param_name}" parameter.',
            tag=ErrorTag.VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER)
    param_type = resolved_hints.get(param_name)
    if param_type is not expected_type:
        raise SimpleBenchTypeError(
            f"Invalid callback: {callback}. '{param_name}' parameter must be of type "
            f"'{expected_type}', not '{param_type}'.",
            tag=ErrorTag.VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE)

    param = callback_signature.parameters[param_name]
    if param.kind is not inspect.Parameter.KEYWORD_ONLY:
        raise SimpleBenchTypeError(
            f'Invalid callback: {callback}. "{param_name}" parameter must be a keyword-only parameter.',
            tag=ErrorTag.VALIDATE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY)


def validate_reporter_callback(callback: ReporterCallback | None) -> ReporterCallback | None:
    """Validate the reporter callback function.

    It must be a callable or None. If callable, it must have the correct signature.
    This is functionally equivalent to the ReporterCallback protocol.

    A callback function must accept the following four keyword-only parameters:
        - case: Case
        - section: Section
        - output_format: Format
        - output: Any

    Args:
        callback (ReporterCallback | None): The callback function to validate.

    Returns:
        ReporterCallback | None: The validated callback function or None.

    Raises:
        SimpleBenchTypeError: If the callback is invalid.
    """
    deferred_case_import()
    if callback is None:
        return None
    if not callable(callback):
        raise SimpleBenchTypeError(
            f'Invalid callback: {callback}. Must be a callable or None.',
            tag=ErrorTag.VALIDATE_INVALID_REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE)
    callback_signature = inspect.signature(callback)
    validate_callback_parameter(callback, Case, 'case')
    validate_callback_parameter(callback, Section, 'section')
    validate_callback_parameter(callback, Format, 'output_format')
    validate_callback_parameter(callback, Any, 'output')
    params = list(callback_signature.parameters.values())
    if len(params) != 4:
        raise SimpleBenchTypeError(
            f'Invalid callback: {callback}. Must accept exactly four keyword-only parameters with the following '
            'names and types: case: Case, section: Section, output_format: Format, output: Any',
            tag=ErrorTag.VALIDATE_INVALID_REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS)
    return callback
