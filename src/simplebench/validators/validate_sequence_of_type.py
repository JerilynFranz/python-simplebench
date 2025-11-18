"""Validator for sequence of specified type(s)."""
from typing import Any, Sequence, TypeVar, overload

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators.exceptions.validators import ValidatorsErrorTag

T = TypeVar("T")


@overload
def validate_sequence_of_type(
        value: Any,
        types: type[T],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        *,
        allow_empty: bool = True,
        exact_type: bool = False) -> list[T]: ...


@overload
def validate_sequence_of_type(
        value: Any,
        types: tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        *,
        allow_empty: bool = True,
        exact_type: bool = False) -> list[Any]: ...


def validate_sequence_of_type(
        value: Any,
        types: type[T] | tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        *,
        allow_empty: bool = True,
        exact_type: bool = False) -> list[T] | list[Any]:
    """Validate that a value is a sequence of specified type(s).

    When a single type is provided, the return type is automatically inferred as list[T].
    When multiple types are provided, the return type is list[Any], which allows the
    caller to narrow the type with an explicit annotation.

    :param Sequence[Any] value: The sequence of values to validate.
    :param types: A single type or tuple of allowed types.
    :type types: type[T] | tuple[type, ...]
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :param bool allow_empty: If set to True, allow an empty sequence. Otherwise raise an error.
    :param bool exact_type: If set to True, require that the types be exactly the
        types specified, not subclasses. Otherwise allow subclass matches.
    :return: For single type, returns list[T]. For multiple types,
        returns list[Any] which can be narrowed with explicit type annotation.
    :rtype: list[T] | list[Any]
    :raises SimpleBenchTypeError: If the value is not a sequence or contains invalid types.
    :raises SimpleBenchValueError: If the sequence is empty and allow_empty is False.

    Examples:
        Single type (automatic inference):

        .. code-block:: python

            names = validate_sequence_of_type(['Alice'], str, 'names', ...)
            # Type: list[str]

        Multiple types (manual narrowing):

        .. code-block:: python

            mixed: list[str | int] = validate_sequence_of_type(
                ['a', 1], (str, int), 'items', ...
            )
            # Type: list[str | int]
    """

    if not isinstance(value, Sequence) or isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value).__name__}. '
            f'Must be an iterable (list, tuple, etc.).',
            tag=type_tag
        )
    value = list(value)  # Convert to list for length check and indexing

    if isinstance(types, type):
        pass
    else:
        if not all(isinstance(t, type) for t in types):
            raise SimpleBenchTypeError(
                f'Invalid types argument: {types}. Must be a type or tuple of types.',
                tag=ValidatorsErrorTag.VALIDATE_SEQUENCE_OF_TYPE_INVALID_TYPES_ARG
            )

    if not isinstance(field_name, str):
        raise SimpleBenchTypeError(
            f'Invalid field_name argument type: {type(field_name)}. Must be a str.',
            tag=ValidatorsErrorTag.VALIDATE_SEQUENCE_OF_TYPE_INVALID_FIELD_NAME_ARG_TYPE
        )

    if not isinstance(type_tag, ErrorTag):
        raise SimpleBenchTypeError(
            f'Invalid type_tag argument type: {type(type_tag)}. Must be an ErrorTag.',
            tag=ValidatorsErrorTag.VALIDATE_SEQUENCE_OF_TYPE_INVALID_TYPE_TAG_TYPE
        )

    if not isinstance(value_tag, ErrorTag):
        raise SimpleBenchTypeError(
            f'Invalid value_tag argument type: {type(value_tag)}. Must be an ErrorTag.',
            tag=ValidatorsErrorTag.VALIDATE_SEQUENCE_OF_TYPE_INVALID_VALUE_TAG_TYPE
        )

    if not isinstance(allow_empty, bool):
        raise SimpleBenchTypeError(
            f'Invalid allow_empty argument type: {type(allow_empty)}. Must be a bool.',
            tag=ValidatorsErrorTag.VALIDATE_SEQUENCE_OF_TYPE_INVALID_ALLOW_EMPTY_ARG_TYPE
        )

    if not isinstance(exact_type, bool):
        raise SimpleBenchTypeError(
            f'Invalid exact_type argument type: {type(exact_type)}. Must be a bool.',
            tag=ValidatorsErrorTag.VALIDATE_SEQUENCE_OF_TYPE_INVALID_EXACT_TYPE_ARG_TYPE
        )

    if len(value) == 0 and not allow_empty:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: sequence cannot be empty.',
            tag=value_tag
        )

    # Format type names for error messages
    if isinstance(types, tuple):
        type_names = ' or '.join(t.__name__ for t in types)
    else:
        type_names = types.__name__

    result: list[Any] = []
    types_set: set[type] = set(types) if isinstance(types, tuple) else {types}
    for i, item in enumerate(value):
        if exact_type:  # exact type matches only
            if type(item) not in types_set:
                raise SimpleBenchTypeError(
                    f'Invalid {field_name} element at index {i}: {type(item).__name__}. '
                    f'Must be {type_names}.',
                    tag=type_tag)
        elif not isinstance(item, types):  # types and their subclasses match
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item).__name__}. '
                f'Must be {type_names} or subclasses of them.',
                tag=type_tag
            )
        result.append(item)

    return result
