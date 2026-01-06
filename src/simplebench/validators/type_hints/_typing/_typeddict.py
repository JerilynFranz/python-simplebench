"""Helper functions to validate container types against type hints."""
import sys
from collections.abc import Mapping
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
from ._typed_dict_key_info import TypedDictKeyInfo

if sys.version_info >= (3, 11):
    from typing import Never
else:
    try:
        from typing_extensions import Never
    except ImportError as e:
        raise ImportError(
            "SimpleBench requires 'typing_extensions' for Python < 3.11 "
            "to support Never.") from e

__all__ = (
    "_check_typing_typeddict",
)

def _check_typing_typeddict(
        obj: Any,
        type_hint: Any,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle TypedDict types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If type_hint is not a TypedDict.
    """
    from .._type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_typeddict: Checking object of type '%s' against TypedDict type hint '%s'",
        type(obj).__name__, type_hint)
    # Fast path checks
    if not is_typeddict(type_hint):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a TypedDict.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if options.strict_typed_dict:
        if not isinstance(obj, dict):
            # Not instance of dict, cannot be a strict TypedDict instance
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Object of type '{type(obj).__name__}' is not a dict, "
                    f"required for strict TypedDict type hint '{type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
    if not isinstance(obj, Mapping):  # This acts as a fast-fail for non-Mapping objects and a type guard
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not a Mapping, "
                f"required for TypedDict type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)  # Not a Mapping, cannot structurally conform to TypedDict

    # From here on, we know that type_hint IS a TypedDict and that the object is a Mapping.
    # All TypedDict checks are structural so we can proceed.

    # TypedDict keys must be strings
    if not all(isinstance(k, str) for k in obj.keys()):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"TypedDict keys must be strings, found non-string keys in object of type '{type(obj).__name__}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    # Make sure that if the TypedDict is defined as Immutable, the Mapping obj is also Immutable
    # Note: This only checks the top-level container not nested elements here.
    # Nested elements are checked below. Standard TypedDicts are mutable by definition (dict-based)
    # and will fail this check if the type hint is defined as Immutable.
    container_is_immutable: bool = isinstance(obj, Immutable)
    is_immutable_typed_dict: bool = is_immutable_typeddict_typehint(type_hint)
    if is_immutable_typed_dict and not container_is_immutable:
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"TypedDict type hint '{type_hint}' is defined as Immutable, "
                f"but object of type '{type(obj).__name__}' is not Immutable.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    required_keys: set[str] = set(type_hint.__required_keys__)
    optional_keys: set[str] = set(type_hint.__optional_keys__)
    allowed_keys: set[str] = required_keys.union(optional_keys)
    if is_immutable_typed_dict:
        # If the TypedDict is defined as Immutable, we need to check that all values are also Immutable.
        # This is a structural check, so we don't need to check the container type itself.
        # Immutable TypedDicts may have a special key __immutable__ that we ignore for validation
        required_keys.discard('__immutable__')
        optional_keys.discard('__immutable__')
        allowed_keys.discard('__immutable__')

    new_parents = parents | {ValidationState(id(obj), type_hint, "typeddict")}

    # check for 'extra_items' if typeddict class explicitly sets it
    # If not set, default is Never (no extra items allowed)
    extra_items_type_hint: Any = getattr(type_hint, '__extra_items__', Never)
    log.debug(
        "_container_check_typeddict: TypedDict '%s' extra_items type hint: '%s'",
        type_hint, extra_items_type_hint)
    if extra_items_type_hint is Never:  # No extra items allowed
        for key in obj.keys():
            if key not in allowed_keys:
                log.debug(
                    "_container_check_typeddict: Extra key '%s' found in TypedDict object, "
                    "but not defined in type hint '%s'", key, type_hint)
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Extra key '{key}' found in TypedDict, but not defined in type hint '{type_hint}'.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    else: # Extra items allowed, check their types
        for key, value in obj.items():
            if key not in allowed_keys:
                check_result = _check_instance_of_typehint(
                    value, extra_items_type_hint, options, new_parents,
                    raise_on_error=False, context="typeddict_extra_item")
                if not check_result.valid:
                    if raise_on_error:
                        raise SimpleBenchTypeError(
                            f"Extra key '{key}' in TypedDict does not match extra_items type hint "
                            f"'{extra_items_type_hint}'.",
                            tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                    return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
                container_is_immutable = container_is_immutable and check_result.immutable

    # Now check each defined key in the TypedDict
    annotations: dict[str, Any] = get_type_hints(type_hint)
    for key, value_type in annotations.items():
        if key == '__immutable__' and is_immutable_typed_dict:
            continue
        if key in obj:
            dict_key_info = TypedDictKeyInfo(key, type_hint)
            check_result = _check_instance_of_typehint(
                value_type, dict_key_info.value_type, options, new_parents,
                raise_on_error=False, context="typeddict_value")
            if not check_result.valid:
                log.debug(
                    "_container_check_typeddict: Key '%s' in TypedDict object does not match "
                    "type hint '%s'", key, dict_key_info.value_type)
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Value for key '{key}' in TypedDict does not match type hint '{dict_key_info.value_type}'.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
            container_is_immutable = container_is_immutable and check_result.immutable
        else:
            if key in required_keys:
                log.debug(
                    "_container_check_typeddict: Required key '%s' missing in TypedDict object for "
                    "type hint '%s'", key, type_hint)
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Required key '{key}' missing in TypedDict.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    # Successful TypedDict check
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True, options.noncachable_types)
    return CheckResult(_IS_VALID, container_is_immutable)
