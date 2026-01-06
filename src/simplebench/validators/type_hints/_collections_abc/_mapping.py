"""Helper functions to validate container types against type hints."""
from collections.abc import Mapping
from typing import Any, get_type_hints, is_typeddict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import Immutable

from .._cache import _CACHE
from .._check_result import CheckResult
from .._constants import _IS_IMMUTABLE, _IS_VALID, _NOT_IMMUTABLE, _NOT_VALID
from .._error_tags import _TypeHintsErrorTag
from .._log import log
from .._options import Options
from .._validation_state import ValidationState

__all__ = (
    "_check_collections_abc_mapping",
)

def _check_collections_abc_mapping(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Mapping types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Mapping type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If origin is not a subclass of Mapping.
    """
    from .._type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_mapping: Checking object of type '%s' against Mapping type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Mapping):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Mapping.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    if not isinstance(obj, origin):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an instance of '{origin.__name__}' "
                f"for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    key_type: Any = Any
    value_type: Any = Any
    match(len(args)):
        case 0:
            pass  # No type arguments, so we accept any key/value types
        case 2:
            key_type, value_type = args
        case _:
            raise SimpleBenchValueError(
                f"Mapping type hint '{origin}' has invalid number of arguments: {len(args)}",
                tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)
    new_parents = parents | {ValidationState(id(obj), type_hint, "mapping")}
    container_is_immutable: bool = isinstance(obj, Immutable)
    for key, value in obj.items():
        # Check key type
        is_valid, is_imm = _check_instance_of_typehint(
            key, key_type, options, new_parents, raise_on_error, context="mapping_key")
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Key '{key}' in Mapping does not match type hint '{key_type}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and is_imm

        # Check value type
        is_valid, is_imm = _check_instance_of_typehint(
            value, value_type, options, new_parents, raise_on_error, context="mapping_value")
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Value for key '{key}' in Mapping does not match type hint '{value_type}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and is_imm

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True, options.noncachable_types)
    return CheckResult(_IS_VALID, container_is_immutable)
