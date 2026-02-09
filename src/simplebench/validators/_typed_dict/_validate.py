"""Validation functions for the TypedDict mimic validator."""

from collections.abc import Mapping
from typing import TypedDict, get_type_hints, Any, Literal, get_origin, get_args, Annotated

from simplebench.exceptions import SimpleBenchTypeError

from ._error_tags import _TypedDictErrorTag


def typed_dict_subclass(td_cls: type[TypedDict], raise_on_error: bool = True) -> bool:  # type: ignore
    """Validate a TypedDict subclass schema.

    This is not a runtime instance validation, but a static schema validation.

    This function checks that the provided TypedDict subclass is declared correctly
    and consistently. It ensures that all keys in the TypedDict's annotations
    are accounted for in either the `__required_keys__` or `__optional_keys__` sets.
    It raises an error if there are any discrepancies.

    It ALWAYS raises an error if the TypedDict subclass is misconfigured
    as this is a structural code validation error and not dependent on instance data.

    Uses typing.get_type_hints to resolve forward references and type aliases.

    :param TypedDict td_cls: The TypedDict subclass to validate
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return bool: True if the TypedDict subclass is valid, False otherwise.
    :raise SimpleBenchTypeError: If raise_on_error is True and the TypedDict subclass is misconfigured or
        type hints cannot be resolved
    """
    try:
        annotations = get_type_hints(td_cls)
    except Exception as exc:  # always raise because this is a code misconfiguration
        raise SimpleBenchTypeError(
            f'Failed to resolve type hints for {td_cls.__name__}: {exc}',
            tag=_TypedDictErrorTag.UNABLE_TO_RESOLVE_TYPE_HINT,
        ) from exc
    required: set[str] = getattr(td_cls, '__required_keys__', set(annotations))
    optional: set[str] = getattr(td_cls, '__optional_keys__', set())
    annotation_set = set(annotations.keys())

    if annotation_set != required.union(optional):
        missing_from_annotations = (required.union(optional)) - annotation_set
        extra_in_annotations = annotation_set - (required.union(optional))
        output = []
        if extra_in_annotations:
            output.append(
                f'Keys {extra_in_annotations} are in annotations but not marked as required/optional '
                f'for class {td_cls.__name__}'
            )
        if missing_from_annotations:
            output.append(
                f'Keys {missing_from_annotations} are marked as required/optional but '
                f'missing from annotations for class {td_cls.__name__}'
            )
        message = '; '.join(output)
        if raise_on_error:
            raise SimpleBenchTypeError(message, tag=_TypedDictErrorTag.MISCONFIGURED_TYPED_DICT)
        return False
    return True


def is_mapping_of_string_to_any(data: Mapping[str, Any], raise_on_error: bool = True) -> bool:
    """Validate that data is a Mapping[str, Any].

    :param Mapping[str, Any] data: The data to validate.
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return bool: True if data is a Mapping[str, Any], False otherwise.
    :raise SimpleBenchTypeError: If data is not a Mapping[str, Any] and raise_on_error is True.
    """
    if not isinstance(data, Mapping):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f'Data must be a Mapping, got {type(data)}', tag=_TypedDictErrorTag.NOT_A_MAPPING
            )
        return False

    for key in data.keys():
        if not isinstance(key, str):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f'All keys in data must be strings, found key of type {type(key)}',
                    tag=_TypedDictErrorTag.MAPPING_KEY_NOT_STRING,
                )
            return False
    return True

def has_required_and_no_extra_keys(
    data: Mapping[str, Any],
    td_cls: type,
    raise_on_error: bool = True,
) -> bool:
    """Validate that data has all required keys and no extra keys.

    :param Mapping[str, Any] data: The data to validate.
    :param type[TypedDict] td_cls: The TypedDict subclass to validate against.
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return bool: True if data has all required keys and no extra keys, False otherwise.
    :raise SimpleBenchTypeError: If raise_on_error is True and required keys are missing or extra keys are present.
    """
    annotations = td_cls.__annotations__
    required: set[str] = getattr(td_cls, '__required_keys__', set(annotations))

    missing = required - data.keys()
    if missing:
        if raise_on_error:
            raise SimpleBenchTypeError(
                f'Missing required keys: {missing}', tag=_TypedDictErrorTag.MISSING_REQUIRED_KEYS
            )
        return False

    extra = data.keys() - annotations.keys()
    if extra:
        if raise_on_error:
            raise SimpleBenchTypeError(f'Extra keys not allowed: {extra}', tag=_TypedDictErrorTag.EXTRA_KEYS_PRESENT)
        return False
    return True


def is_string_key_type(key_type: Any) -> bool:
    """Check if a type is a valid string key type for Mappings.

    :param Any key_type: The type to check.
    :return bool: True if the type is a valid string key type, False otherwise.
    """
    if key_type is str:
        return True
    origin = get_origin(key_type)
    if origin is Literal:
        return all(isinstance(arg, str) for arg in get_args(key_type))
    if origin is Annotated and get_args(key_type) and get_args(key_type)[0] is str:
        return True
    try:
        return issubclass(key_type, str)
    except TypeError:
        return False
