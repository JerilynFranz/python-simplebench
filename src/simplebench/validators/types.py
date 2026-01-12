"""Validators for type checking of values."""

from typing import Any, TypeVar, cast, overload

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError
from simplebench.type_proxies.lazy_type_proxy import LazyTypeProxy
from simplebench.validators._error_tags import _ValidatorsErrorTag

T = TypeVar('T')


@overload
def validate_type(
    value: Any, types: tuple[type | LazyTypeProxy[Any], ...], name: str, error_tag: ErrorTag, *, message: str = ''
) -> Any: ...


@overload
def validate_type(value: Any, types: type[T], name: str, error_tag: ErrorTag, *, message: str = '') -> T: ...


@overload
def validate_type(value: Any, types: LazyTypeProxy[T], name: str, error_tag: ErrorTag, *, message: str = '') -> T: ...


def validate_type(
    value: Any,
    types: type[T] | tuple[type | LazyTypeProxy[Any], ...] | LazyTypeProxy[T],
    name: str,
    error_tag: ErrorTag,
    *,
    message: str = '',
) -> T | Any:
    """Validate that a value is of the expected type.

        (validation primitive - does not depend on other validators)

    The returned value is guaranteed to be of type expected and acts to type-narrow
    the returned value for static type checking if a single type is provided.

    If multiple types are provided in a tuple for the expected type, the caller can
    type-narrow the type of the returned type by declaring the untupled types by
    assigning the return value to a variable with an explicit type annotation.

    The value itself is always returned unchanged if it passes the validation.

    Example:

        .. code-block:: python

            mixed: str | int = validate_type(
                value=some_value, expected=(str, int), name='mixed', error_tag=ErrorTag.INVALID_EXPECTED_ARG_TYPE
            )

    :param Any value: The value to validate.
    :param type types: The expected type of the value.
    :type types: type[T] | tuple[type, ...] | LazyType[T]
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag error_tag: The error tag to use for type errors.
    :param str message: Specific message to include in the error for type errors.
        Defaults to a generic message. A string format substitution will be done with
        the targets ``{name}`` and ``{value}`` on a passed string. (kwarg-only, optional)
    :return: The validated (unmodifed) value of the expected type.
    :rtype: T | Any
    :raises SimpleBenchTypeError: If the value is not of the expected type.
    """

    if not isinstance(types, (type, tuple, LazyTypeProxy)):
        raise SimpleBenchTypeError(
            f'Invalid expected argument type: {type(types)}. Must be a type, tuple of types, or LazyType.',
            tag=_ValidatorsErrorTag.VALIDATE_TYPE_INVALID_EXPECTED_ARG_TYPE,
        )

    if isinstance(types, tuple):
        for item in types:
            if not isinstance(item, (type, LazyTypeProxy)):
                raise SimpleBenchTypeError(
                    f'Invalid expected argument item type in tuple: {type(item)}. Must be a type or LazyType.',
                    tag=_ValidatorsErrorTag.VALIDATE_TYPE_INVALID_EXPECTED_ARG_ITEM_TYPE,
                )

    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f'Invalid name argument type: {type(name)}. Must be a str.',
            tag=_ValidatorsErrorTag.VALIDATE_TYPE_INVALID_NAME_ARG_TYPE,
        )
    if not isinstance(error_tag, ErrorTag):
        raise SimpleBenchTypeError(
            f'Invalid error_tag argument type: {type(error_tag)}. Must be an ErrorTag.',
            tag=_ValidatorsErrorTag.VALIDATE_TYPE_INVALID_ERROR_TAG_TYPE,
        )

    formatted_message: str = message.format(name=name, value=value)

    # We use `cast` here to inform the static type checker that we know
    # LazyTypeProxy is a valid type for `isinstance` due to its metaclass.
    # This suppresses the Pylance warning without affecting runtime behavior.
    if not isinstance(value, cast(type, types)):
        raise SimpleBenchTypeError(
            formatted_message or f'Invalid "{name}" type: {type(value)}. Must be {repr(types)}.', tag=error_tag
        )
    return value  # type: ignore[return-value]
