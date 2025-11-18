"""Validators for reporters stuff."""
import inspect
from types import UnionType
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast, get_type_hints, overload

from rich.table import Table
from rich.text import Text

from simplebench.enums import Format, Section
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.validators.exceptions import ReportersValidatorsErrorTag

# Deferred imports to avoid circular dependencies. This pattern is required for any
# type hints that are resolved at runtime via get_type_hints() and involve a
# circular dependency (e.g., Reporter -> Case -> Choice -> Reporter).
#
# Becase the reporter validators need to specifically validate callbacks that use
# the Case type, we need to defer the import of that type until runtime to avoid
# circular imports. If other core types are needed in the future, they can be added
# here as well.

# Define placeholders for runtime name resolution

if TYPE_CHECKING:
    from simplebench.case import Case
    _CORE_TYPES_IMPORTED = True
else:
    Case = None  # pylint: disable=invalid-name  # type: ignore
    _CORE_TYPES_IMPORTED = False


def _deferred_core_imports() -> None:
    """Deferred import of core types to avoid circular imports during initialization.

    This imports :class:`~simplebench.case.Case`, only when needed at runtime, preventing
    circular import issues during module load time while still allowing its use in type
    hints and runtime validations.
    """
    global Case, _CORE_TYPES_IMPORTED  # pylint: disable=global-statement
    if _CORE_TYPES_IMPORTED:
        return
    from simplebench.case import Case  # pylint: disable=import-outside-toplevel,redefined-outer-name
    _CORE_TYPES_IMPORTED = True


T = TypeVar('T')


def resolve_type_hints(callback: Callable) -> dict[str, type]:
    """Resolve the type hints for a callback function.

    :param callback: The callback function to resolve type hints for.
    :return: A dictionary mapping parameter names to their resolved types.
    :raises ~simplebench.exceptions.SimpleBenchTypeError: If the type hints cannot be
        resolved.
    """
    _deferred_core_imports()
    try:
        resolved_hints = get_type_hints(
            callback, globalns=callback.__globals__)  # pyright: ignore[reportAttributeAccessIssue]
    except (NameError, TypeError) as e:
        # This can happen if an annotation refers to a type that doesn't exist.
        raise SimpleBenchTypeError(
            f"Invalid callback: {callback}. Could not resolve type hints. Original error: {e}",
            tag=ReportersValidatorsErrorTag.INVALID_CALLBACK_UNRESOLVABLE_HINTS
        ) from e
    return resolved_hints


def validate_call_parameter(call: Callable,
                            expected_type: type | Any,
                            param_name: str) -> None:
    """Validate a parameter of the callback function.

    The parameter must exist, be of the expected type, and be a keyword-only parameter.

    :param call: The callback function to validate.
    :param expected_type: The expected type of the parameter.
    :param param_name: The name of the parameter to validate.
    :raises ~simplebench.exceptions.SimpleBenchTypeError: If the parameter is invalid.
    """
    signature = inspect.signature(call)
    if param_name not in signature.parameters:
        raise SimpleBenchTypeError(
            f'Invalid callback: {call}. Must accept an "{param_name}" parameter.',
            tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER)
    resolved_hints = resolve_type_hints(call)
    if param_name not in resolved_hints:
        raise SimpleBenchTypeError(
            f'Invalid callback: {call}. "{param_name}" parameter does not have a type hint',
            tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT)
    param_type = resolved_hints.get(param_name)
    if param_type is not expected_type:
        raise SimpleBenchTypeError(
            f"Invalid callback: {call}. '{param_name}' parameter must be of type "
            f"'{expected_type}', not '{param_type}'.",
            tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE)

    callback_signature = inspect.signature(call)
    param = callback_signature.parameters[param_name]
    if param.kind is not inspect.Parameter.KEYWORD_ONLY:
        raise SimpleBenchTypeError(
            f'Invalid call: {call}. "{param_name}" parameter must be a keyword-only parameter.',
            tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY)


@overload
def validate_reporter_callback(callback: Any) -> ReporterCallback: ...


@overload
def validate_reporter_callback(callback: Any, *, allow_none: bool) -> ReporterCallback | None: ...


def validate_reporter_callback(callback: Any, *, allow_none: bool = False) -> ReporterCallback | None:
    """Validate the reporter callback function.

    Verifies the callback function has the correct signature.

    If called without an ``allow_none`` parameter, the returned value will be guaranteed
    to conform to the :class:`~.ReporterCallback` protocol and type checkers will
    automatically type-narrow it.

    If called with an ``allow_none=True`` parameter, the validator will accept **either**
    a :class:`~.ReporterCallback` conformant method or ``None`` as valid.

    If an explicit ``allow_none`` parameter is passed, regardless of whether
    ``allow_none=True`` or ``allow_none=False``, the return type determined by static type
    checkers will be ``ReporterCallback | None``.

    A callback function must accept the following four keyword-only parameters:

    * ``case: Case``
    * ``section: Section``
    * ``output_format: Format``
    * ``output: Any``

    :param callback: The callback function to validate.
    :param allow_none: Whether to allow ``None`` as a valid value for the callback.
        Defaults to ``False``.
    :return: The validated callback function or ``None``.
    :raises ~simplebench.exceptions.SimpleBenchTypeError: If the callback is invalid.
    """
    _deferred_core_imports()
    if callback is None and allow_none:
        return None
    if not callable(callback):
        raise SimpleBenchTypeError(
            f'Invalid callback: {callback}. Must be a callable or None.',
            tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE)
    callback_signature = inspect.signature(callback)
    validate_call_parameter(callback, Case, 'case')
    validate_call_parameter(callback, Section, 'section')
    validate_call_parameter(callback, Format, 'output_format')
    validate_call_parameter(callback, Any, 'output')
    params = list(callback_signature.parameters.values())
    if len(params) != 4:
        raise SimpleBenchTypeError(
            'Invalid callback: {callback}. Must accept exactly four keyword-only parameters '
            'with the following names and types: case: Case, section: Section, '
            'output_format: Format, output: Any',
            tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS)

    resolved_hints = resolve_type_hints(callback)
    if 'return' not in resolved_hints:
        raise SimpleBenchTypeError(
            'Invalid call argument. Must have a return type annotation.',
            tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_MISSING_RETURN_ANNOTATION)
    actual_type = resolved_hints.get('return')

    # Normalize NoneType to None for comparison
    if actual_type is type(None):
        actual_type = None
    if actual_type is not None:
        raise SimpleBenchTypeError(
            f"Invalid call argument. Return type must be None, not '{actual_type}'.",
            tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_INCORRECT_RETURN_ANNOTATION_TYPE)

    return cast(ReporterCallback, callback)


def validate_report_renderer(renderer: ReportRenderer) -> ReportRenderer:
    """Validate the report renderer method.

    Verifies the renderer method has the correct signature.
    This is functionally equivalent to the :class:`~.ReportRenderer` protocol.

    A renderer function must accept the following three keyword-only parameters:

    * ``case: Case``
    * ``section: Section``
    * ``options: ReporterOptions``

    :param renderer: The renderer function to validate.
    :return: The validated renderer function.
    :raises ~simplebench.exceptions.SimpleBenchTypeError: If the renderer is invalid.
    """
    _deferred_core_imports()
    if not callable(renderer):
        raise SimpleBenchTypeError(
            f'Invalid renderer: {renderer}. Must be a callable.',
            tag=ReportersValidatorsErrorTag.REPORT_RENDERER_NOT_CALLABLE)
    signature = inspect.signature(renderer)
    validate_call_parameter(renderer, Case, 'case')
    validate_call_parameter(renderer, Section, 'section')
    validate_call_parameter(renderer, ReporterOptions, 'options')
    params = list(signature.parameters.values())
    if len(params) != 3:
        raise SimpleBenchTypeError(
            'Invalid renderer: {renderer}. Must accept exactly three keyword-only '
            'parameters with the following names and types: case: Case, section: Section, '
            'options: ReporterOptions',
            tag=ReportersValidatorsErrorTag.REPORT_RENDERER_INCORRECT_NUMBER_OF_PARAMETERS)

    resolved_hints = resolve_type_hints(renderer)
    if 'return' not in resolved_hints:
        raise SimpleBenchTypeError(
            'Invalid renderer return type: Must have a return type annotation.',
            tag=ReportersValidatorsErrorTag.REPORT_RENDERER_MISSING_RETURN_ANNOTATION)
    actual_return_type: type | Any = resolved_hints['return']
    allowed_return_types: set[type | Any] = {str, bytes, Text, Table}

    # just a simple type in the allowed set
    if actual_return_type in allowed_return_types:
        return renderer

    # A Union type, e.g., Union[str, bytes] or str | bytes
    if isinstance(actual_return_type, UnionType):
        return_types = set(actual_return_type.__args__)
        if allowed_return_types.issuperset(return_types):
            return renderer
        raise SimpleBenchTypeError(
            f"Invalid renderer return type: Return type must only include types "
            f"'{allowed_return_types}, 'actual return type of '{actual_return_type} "
            "includes other types'.",
            tag=ReportersValidatorsErrorTag.REPORT_RENDERER_INCORRECT_RETURN_ANNOTATION_TYPE)

    # Something else entirely. Whatever it is, it is not valid.
    raise SimpleBenchTypeError(
        f"Unexpected renderer return type: Return type must be one of types "
        f"'{allowed_return_types}', but found '{actual_return_type}'.",
        tag=ReportersValidatorsErrorTag.REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE)
