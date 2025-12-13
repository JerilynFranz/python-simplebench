"""Base class for JSON objects

This module defines an base class `Hydrator` for objects, which includes methods
for initializing, converting to and from dictionaries, and validating against a
set of allowed parameters.

"""
import inspect
from functools import cache
from typing import Any, Callable, Iterable, Sequence, get_args, get_origin, get_type_hints

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_iterable_of_type, validate_type

from .exceptions import _HydratorErrorTag


def _validate_allowed(
        allowed: dict[str, Any], error_tag: type[ErrorTag]) -> dict[str, Any]:
    """Validate the allowed parameters dictionary.

    :param allowed: The allowed parameters dictionary to validate.
    :param error_tag: The error tag to use for raising exceptions.
    :return: The validated allowed parameters dictionary.
    :raises: SimpleBenchTypeError if the allowed parameters dictionary is invalid.
    :raises: SimpleBenchValueError if the allowed parameters dictionary is empty.
    """
    validate_type(allowed, dict, 'allowed',
                  error_tag.INVALID_ALLOWED_TYPE)  # type: ignore[reportAttributeAccessIssue]

    for value in allowed.values():
        # A valid type annotation is either a simple type (like `int`)
        # or a generic from the typing module (like `list[str]`, which has an __origin__).
        is_simple_type = isinstance(value, type)
        is_generic_type = hasattr(value, '__origin__')
        if not (is_simple_type or is_generic_type):
            raise SimpleBenchTypeError(
                f"All values in `allowed` must be a valid type annotation, but got {value}",
                tag=error_tag.INVALID_ALLOWED_VALUE_TYPE)  # type: ignore[reportAttributeAccessIssue]

    if len(allowed) == 0:
        raise SimpleBenchValueError(
            "The `allowed` dictionary cannot be empty",
            tag=error_tag.INVALID_ALLOWED_EMPTY)  # type: ignore[reportAttributeAccessIssue]
    return allowed


def _validate_skip(skip: Iterable[str], allowed: dict[str, type], error_tag: type[ErrorTag]) -> set[str]:
    """Validate the skip iterable.

    :param skip: The skip iterable to validate.
    :param error_tag: The error tag to use for raising exceptions.
    :return: The validated skip set.
    :raises: SimpleBenchTypeError if the skip iterable is invalid.
    """
    skip_set = set(validate_iterable_of_type(
        skip, str, 'skip',
        error_tag.INVALID_SKIP_TYPE,  # type: ignore[reportAttributeAccessIssue]
        error_tag.INVALID_SKIP_ITEM_TYPE,  # type: ignore[reportAttributeAccessIssue]
        allow_empty=True, exact_type=False))
    if not all(field in allowed for field in skip_set):
        raise SimpleBenchValueError(
            "All values in `skip` must match a key in `allowed`",
            tag=error_tag.INVALID_SKIP_VALUE)  # type: ignore[reportAttributeAccessIssue]

    return skip_set


def _validate_optional(optional: Iterable[str], allowed: dict[str, type], error_tag: type[ErrorTag]) -> set[str]:
    """Validate the optional iterable.

    :param optional: The optional iterable to validate.
    :param allowed: The allowed parameters dictionary to use for validation.
    :param error_tag: The error tag to use for raising exceptions.
    :return: The validated optional set.
    :raises: SimpleBenchTypeError if the optional iterable is invalid.
    :raises: SimpleBenchValueError if the optional iterable contains invalid values.
    """
    optional_set = set(validate_iterable_of_type(
        optional, str, 'optional',
        error_tag.INVALID_OPTIONAL_TYPE,  # type: ignore[reportAttributeAccessIssue]
        error_tag.INVALID_OPTIONAL_ITEM_TYPE,  # type: ignore[reportAttributeAccessIssue]
        allow_empty=True, exact_type=False))
    if not all(field in allowed for field in optional_set):
        raise SimpleBenchValueError(
            "All values in `optional` must match a key in `allowed`",
            tag=error_tag.INVALID_OPTIONAL_ITEM_VALUE)  # type: ignore[reportAttributeAccessIssue]

    return optional_set


def _validate_default(default: dict[str, Any], optional: set[str], error_tag: type[ErrorTag]) -> dict[str, Any]:
    """Validate the default dictionary.

    :param default: The default dictionary to validate.
    :param optional: The optional set to use for validation.
    :param error_tag: The error tag to use for raising exceptions.
    :return: The validated default dictionary.
    :raises: SimpleBenchTypeError if the default dictionary is invalid.
    :raises: SimpleBenchValueError if the default dictionary contains invalid values.
    """
    if not isinstance(default, dict):
        raise SimpleBenchTypeError(
            "The `default` parameter must be of type `dict`",
            tag=error_tag.INVALID_DEFAULT_TYPE)  # type: ignore[reportAttributeAccessIssue]

    if not all(field in optional for field in default.keys()):
        raise SimpleBenchValueError(
            "All keys in `default` must match a key in `optional`",
            tag=error_tag.INVALID_DEFAULT_KEY)  # type: ignore[reportAttributeAccessIssue]

    return default


def _validate_match_on(match_on: dict[str, Any], allowed: dict[str, type], error_tag: type[ErrorTag]) -> dict[str, Any]:
    """Validate the match_on dictionary.

    :param match_on: The match_on dictionary to validate.
    :param allowed: The allowed parameters dictionary to use for validation.
    :param error_tag: The error tag to use for raising exceptions.
    :return: The validated match_on dictionary.
    :raises: SimpleBenchTypeError if the match_on dictionary is invalid.
    :raises: SimpleBenchValueError if the match_on dictionary contains invalid values.
    """
    if not isinstance(match_on, dict):
        raise SimpleBenchTypeError(
            "The `match_on` parameter must be of type `dict`",
            tag=error_tag.INVALID_MATCH_ON_TYPE)  # type: ignore[reportAttributeAccessIssue]

    if not all(field in allowed for field in match_on.keys()):
        raise SimpleBenchValueError(
            "All keys in `match_on` must match a key in `allowed`",
            tag=error_tag.INVALID_MATCH_ON_KEY)  # type: ignore[reportAttributeAccessIssue]

    return match_on


def _validate_process_as(
        process_as: dict[str, Callable[[Any], Any]],
        allowed: dict[str, type],
        error_tag: type[ErrorTag]) -> dict[str, Callable[[Any], Any]]:
    """Validate the process_as dictionary.

    :param process_as: The process_as dictionary to validate.
    :param allowed: The allowed parameters dictionary to use for validation.
    :param error_tag: The error tag to use for raising exceptions.
    :return: The validated process_as dictionary.
    :raises: SimpleBenchTypeError if the process_as dictionary is invalid.
    :raises: SimpleBenchValueError if the process_as dictionary contains invalid values.
    """
    if not isinstance(process_as, dict):
        raise SimpleBenchTypeError(
            "The `process_as` parameter must be of type `dict`",
            tag=error_tag.INVALID_PROCESS_AS_TYPE)  # type: ignore[reportAttributeAccessIssue]

    if not all(field in allowed for field in process_as.keys()):
        raise SimpleBenchValueError(
            "All keys in `process_as` must match a key in `allowed`",
            tag=error_tag.INVALID_PROCESS_AS_KEY)  # type: ignore[reportAttributeAccessIssue]

    for call in process_as.values():
        # must be callable with exactly one parameter and a return type annotation
        if not callable(call):
            raise SimpleBenchTypeError(
                "All values in `process_as` must be callable",
                tag=error_tag.INVALID_PROCESS_AS_VALUE)  # type: ignore[reportAttributeAccessIssue]

        call_signature = inspect.signature(call)
        if len(call_signature.parameters) != 1:
            raise SimpleBenchTypeError(
                "All values in `process_as` must be callable with exactly one parameter",
                tag=error_tag.INVALID_PROCESS_AS_VALUE)  # type: ignore[reportAttributeAccessIssue]
        param = list(call_signature.parameters.values())[0]
        if param.kind not in [inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.POSITIONAL_ONLY]:
            raise SimpleBenchTypeError(
                "All values in `process_as` must be callable with a single positional parameter",
                tag=error_tag.INVALID_PROCESS_AS_VALUE)  # type: ignore[reportAttributeAccessIssue]

        return_annotation = call_signature.return_annotation
        if return_annotation == inspect.Parameter.empty or not issubclass(return_annotation, type):
            raise SimpleBenchTypeError(
                "All values in `process_as` must be callable with a return type annotation",
                tag=error_tag.INVALID_PROCESS_AS_VALUE)  # type: ignore[reportAttributeAccessIssue]

    return process_as


def _is_instance_of_generic(obj: Any, type_hint: Any) -> bool:
    """
    Check if an object is an instance of a generic type hint.
    Handles simple types, lists, sequences, and dictionaries.
    """
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Case 1: Simple type (e.g., int, str)
    if origin is None:
        if isinstance(type_hint, type):
            return isinstance(obj, type_hint)
        return False  # Should not happen with valid type hints

    # Case 2: List or Sequence
    if origin in (list, Iterable, Sequence):
        if not isinstance(obj, (list, tuple, set)):
            return False
        item_type = args[0]
        return all(_is_instance_of_generic(item, item_type) for item in obj)

    # Case 3: Dictionary
    if origin is dict:
        if not isinstance(obj, dict):
            return False
        key_type, value_type = args
        return all(_is_instance_of_generic(
            k, key_type) and _is_instance_of_generic(v, value_type) for k, v in obj.items())

    # Fallback for other types (like Union, etc., which can be added here)
    return isinstance(obj, origin)


class Hydrator:
    """Base class providing convience methods for processing a JSON object."""

    @cache
    @classmethod
    def init_params(cls) -> dict[str, Any]:
        """Return a dictionary of the parameters that can be passed to the constructor.

        It is used to help determine which fields are required for the constructor
        and what their types are.

        Only keyword-only parameters are included. It uses `get_type_hints` to
        resolve annotations, including simple and generic types.

        It is cached to avoid recomputing it every time it is called.
        """
        output: dict[str, Any] = {}
        try:
            type_hints = get_type_hints(cls.__init__)
        except (AttributeError, TypeError, NameError):
            return {}

        init_params = inspect.signature(cls.__init__).parameters
        for name, param in init_params.items():
            if param.kind != inspect.Parameter.KEYWORD_ONLY:
                continue

            if name in type_hints:
                output[name] = type_hints[name]

        return output

    @classmethod
    def import_data(  # noqa: C901
            cls, *,
            data: dict[str, Any],
            allowed: dict[str, type],
            skip: Iterable[str] | None = None,
            optional: Iterable[str] | None = None,
            default: dict[str, Any] | None = None,
            match_on: dict[str, Any] | None = None,
            process_as: dict[str, Callable[[Any], Any]] | None = None,
            error_tag: type[ErrorTag] = _HydratorErrorTag) -> dict[str, Any]:
        """Process and validate the data dictionary.

        :param data: The data dictionary to process.
        :param allowed: A dictionary of allowed input keys and their types. It cannot be empty.
        :param skip: A list of input keys to NOT include in the output. Only keys that are present
                    in the `allowed` dictionary can be skipped.
        :param optional: An iterable of input keys that are optional and that can be omitted from the output
                    if missing. Only keys that are present in the `allowed` dictionary
                    can be optional.
        :param default: A dictionary of default values for keys if they are not present.
                    If a key is present in the input data, the default value is not used.
                    If a value is set by the default, it is not considered missing.
                    Only keys that are present in the `optional` dictionary can have default values.
        :param match_on: A dictionary of keys and values that must match the corresponding keys in
                        the input data. This is processed AFTER the default values are applied.
                        Only keys that are present in the `allowed` dictionary can have match_on rules.
        :param process_as: A dictionary of keys and functions to apply to the corresponding values in
                        the input data before storing in the output. This is processed AFTER the
                        match_on rules for input are checked.
                        Only keys that are present in the `allowed` dictionary can have process_as rules.
        :param error_tag: The error tag to use for raising exceptions. Default is `_BuilderErrorTag`.
            If passed, it will be used to raise exceptions with a custom error tag. This is useful
            for overriding the default error tag with a custom one. The same enum keys are used to raise
            exceptions with a custom error tag.
        :return: The processed and validated data dictionary.
        :raises: SimpleBenchTypeError if the data does not match the rules.

        Raises:
            SimpleBenchValueError: If the data does not match the rules.
        """
        error_tag = validate_type(
                        error_tag, type[ErrorTag], 'error_tag',
                        _HydratorErrorTag.INVALID_ERROR_TAG_TYPE)

        validate_type(data, dict, 'data',
                      error_tag.INVALID_DATA_TYPE)  # type: ignore[reportAttributeAccessIssue]
        if not all(isinstance(key, str) for key in data.keys()):
            raise SimpleBenchTypeError(
                "All keys in the data dictionary must be of type 'str'",
                tag=error_tag.INVALID_DATA_KEY_TYPE)  # type: ignore[reportAttributeAccessIssue]

        allowed_fields: dict[str, type] = _validate_allowed(allowed=allowed,
                                                            error_tag=error_tag)

        skip_fields: set[str] = _validate_skip(skip=skip or set(),
                                               allowed=allowed_fields,
                                               error_tag=error_tag)

        optional_fields: set[str] = _validate_optional(optional=optional or set(),
                                                       allowed=allowed_fields,
                                                       error_tag=error_tag)

        default_fields: dict[str, Any] = _validate_default(default=default or {},
                                                           optional=optional_fields,
                                                           error_tag=error_tag)

        match_on_fields: dict[str, Any] = _validate_match_on(match_on=match_on or {},
                                                             allowed=allowed_fields,
                                                             error_tag=error_tag)

        process_as_fields: dict[str, Callable[[Any], Any]] = _validate_process_as(
                                                                process_as=process_as or {},
                                                                allowed=allowed_fields,
                                                                error_tag=error_tag)

        # Apply default values to the data dictionary
        for field, default_value in default_fields.items():
            if field not in data:
                data[field] = default_value

        # Apply match_on rules to the data dictionary
        for field, expected_value in match_on_fields.items():
            if data.get(field) != expected_value:
                raise SimpleBenchValueError(
                    f"The value of '{field}' must be '{expected_value}'",
                    tag=error_tag.INVALID_MATCH_ON_VALUE)  # type: ignore[reportAttributeAccessIssue]

        # Validate the data dictionary against the allowed fields
        for field in data.keys():
            if field not in allowed_fields:
                raise SimpleBenchValueError(
                    f"The key '{field}' is not allowed",
                    tag=error_tag.INVALID_DATA_KEY)  # type: ignore[reportAttributeAccessIssue]

        # Validate the data dictionary against the optional fields
        for field in allowed_fields:
            if field not in data and field not in optional_fields:
                raise SimpleBenchValueError(
                    f"The key '{field}' is missing",
                    tag=error_tag.INVALID_DATA_KEY)  # type: ignore[reportAttributeAccessIssue]

        # Shallow copy the data dictionary to the output dictionary
        output: dict[str, Any] = data.copy()

        # Apply process_as rules to the output dictionary
        # Only apply the process_as rules to the fields that are actually
        # present in the data dictionary
        for field, process_func in process_as_fields.items():
            if field in output:
                output[field] = process_func(output[field])

        # Remove the skipped fields from the output dictionary
        for field in skip_fields:
            if field in output:
                del output[field]

        # Validate the processed output dictionary against the allowed field types
        for field, value in output.items():
            if not _is_instance_of_generic(value, allowed_fields[field]):
                raise SimpleBenchTypeError(
                    f"The value of '{field}' does not match the expected type '{allowed_fields[field]}'",
                    tag=error_tag.INVALID_DATA_VALUE_TYPE)  # type: ignore[reportAttributeAccessIssue]

        return output
