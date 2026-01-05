"""Helper functions to validate container types against type hints."""
import inspect
import sys
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence, Set
from typing import Any, get_type_hints, is_typeddict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import Immutable, is_immutable_typeddict_typehint

from ._cache import _CACHE
from ._constants import _IS_IMMUTABLE, _IS_VALID, _NOT_IMMUTABLE, _NOT_VALID
from ._error_tags import _TypeHintsErrorTag
from ._check_result import CheckResult
from ._log import log
from ._options import Options
from .typed_dict_key_info import TypedDictKeyInfo
from ._validation_state import ValidationState

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
    "_container_check_typeddict",
    "_container_check_mapping",
    "_container_check_set",
    "_container_check_sequence",
    "_container_check_iterable",
    "_container_check_callable",
)

def _container_check_typeddict(
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
    from .type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

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
    extra_items_type_hint: Any = getattr(type_hint, '__extra_items__', Never)
    if extra_items_type_hint is Never:  # No extra items allowed
        for key in obj.keys():
            if key not in allowed_keys:
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
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Value for key '{key}' in TypedDict does not match type hint '{dict_key_info.value_type}'.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
            container_is_immutable = container_is_immutable and check_result.immutable
        else:
            if key in required_keys:
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Required key '{key}' missing in TypedDict.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    # Successful TypedDict check
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True, options.noncachable_types)
    return CheckResult(_IS_VALID, container_is_immutable)

def _annotation_is_str_typehint(annotation: Any) -> bool:
    """Check if an annotation is a string type hint (forward reference).

    :param Any annotation: The annotation to check.
    :return bool: True if the annotation is a string type hint, False otherwise.
    """
    return isinstance(annotation, str)

def _container_check_mapping(
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
    from .type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_mapping: Checking object of type '%s' against Mapping type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Mapping):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Mapping.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

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

def _container_check_set(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Set types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Set type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If origin is not a subclass of Set.
    """
    from .type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_set: Checking object of type '%s' against Set type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Set):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Set.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    if not isinstance(obj, Set):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not a Set, but type hint is '{type_hint}'",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
    item_type: Any = Any
    if len(args) == 1:
        item_type = args[0]
    elif len(args) > 1:
        raise SimpleBenchValueError(
            f"Set type hint '{origin}' has invalid number of arguments: {len(args)}",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    new_parents = parents | {ValidationState(id(obj), type_hint, "set")}
    container_is_immutable: bool = isinstance(obj, Immutable)
    for item in obj:
        is_valid, is_imm = _check_instance_of_typehint(
            item, item_type, options, new_parents, raise_on_error, context="set_item")
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Set does not match type hint '{args[0] if args else Any}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and is_imm

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, _IS_IMMUTABLE, options.noncachable_types)
    return CheckResult(_IS_VALID, container_is_immutable)

def _container_check_sequence(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Sequence types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Sequence type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If origin is not a subclass of Sequence.
    """
    from .type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_sequence: Checking object of type '%s' against Sequence type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Sequence):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not a Sequence.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    # Broad check first
    if not isinstance(obj, Sequence):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not a Sequence, but type hint is '{type_hint}'",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    # Special case: str and bytes are Sequences but we treat them as primitives
    # and not container types here. We don't need to check their items.
    if isinstance(obj, (str, bytes)):
        if origin in (list, tuple):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Object of type '{type(obj)}' is a primitive str/bytes, "
                    f"not a '{origin.__name__}' Sequence for type hint '{type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    if not isinstance(obj, origin):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an instance of '{origin.__name__}' "
                f"for type hint '{type_hint}'.",
                tag=_TypeHintsErrorTag.VALIDATION_FAILED)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    container_is_immutable: bool = isinstance(obj, Immutable)

    new_parents = parents | {ValidationState(id(obj), type_hint, "sequence")}
    item_type_hint: Any = args[0] if args else Any
    for item in obj:
        is_valid, is_imm = _check_instance_of_typehint(
            item, item_type_hint, options, new_parents, raise_on_error=False, context="sequence_item")
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Sequence does not match type hint '{item_type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and is_imm

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True, options.noncachable_types)
    return CheckResult(_IS_VALID, container_is_immutable)

def _container_check_iterable(
        obj: Any,
        type_hint: Any,
        origin: Any,
        args: tuple,
        options: Options,
        parents: set[ValidationState],
        raise_on_error: bool = False) -> CheckResult:
    """Handle Iterable types.

    :param Any obj: The object to check.
    :param Any type_hint: The type hint to check against.
    :param Any origin: The origin type of the type hint.
    :param tuple args: The type arguments of the Iterable type hint.
    :param Options options: Options for type hint validation.
    :param set[ValidationState] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: Whether to raise an exception on validation failure.
    :return CheckResult: Tuple indicating (is_valid, is_immutable).
    :raises SimpleBenchTypeError: If raise_on_error is True and validation fails.
    :raises SimpleBenchValueError: If origin is not a subclass of Iterable.
    """
    from .type_hints import _check_instance_of_typehint  # pylint: disable=import-outside-toplevel

    log.debug(
        "_container_check_iterable: Checking object of type '%s' against Iterable type hint '%s'",
        type(obj).__name__, type_hint)
    if not issubclass(origin, Iterable):
        raise SimpleBenchValueError(
            f"Type hint '{type_hint}' is not an Iterable.",
            tag=_TypeHintsErrorTag.INVALID_TYPE_HINT)

    # Check the cache first
    cached_result = _CACHE.valid_in_cache(type_hint, obj)
    if cached_result is not None:  # Only cached if Immutable
        if cached_result or not raise_on_error:
            return CheckResult(cached_result, _IS_IMMUTABLE)
        raise SimpleBenchTypeError(
            f"Object of type '{type(obj)}' does not match type hint '{type_hint}'.",
            tag=_TypeHintsErrorTag.VALIDATION_FAILED)

    # This check must come before the Iterator check, as str/bytes are Iterable but not Iterator.
    if isinstance(obj, (str, bytes)):
        # We treat str/bytes as primitives. If we're here, it means a more specific
        # check like Sequence[str] didn't catch it, so we consider it valid against
        # a generic Iterable hint (e.g., Iterable[str]).
        return CheckResult(_IS_VALID, _IS_IMMUTABLE)

    # Short-circuit for single-pass Iterators if configured to do so.
    # We assume it is NOT immutable since we cannot check its items without consuming it.
    if isinstance(obj, Iterator) and not options.consume_iterators:
        return CheckResult(_IS_VALID, _NOT_IMMUTABLE)

    if not isinstance(obj, Iterable):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f"Object of type '{type(obj).__name__}' is not an Iterable, but type hint is '{type_hint}'",
                tag=_TypeHintsErrorTag.TYPE_HINT_MISMATCH)
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    container_is_immutable: bool = isinstance(obj, Immutable)
    new_parents = parents | {ValidationState(id(obj), type_hint, "iterable")}

    # Handle Iterable[T]
    if len(args) == 1:
        item_type_hint: Any = args[0]
    else:
        item_type_hint = Any
    for item in obj:
        is_valid, is_imm = _check_instance_of_typehint(item, item_type_hint, options,
                                                 new_parents, raise_on_error=False, context="iterable_item")
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Item '{item}' in Iterable does not match type hint '{item_type_hint}'.",
                    tag=_TypeHintsErrorTag.VALIDATION_FAILED)
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
        container_is_immutable = container_is_immutable and is_imm

    # If we reach here, all checks passed
    if container_is_immutable:
        _CACHE.add_cache_entry(type_hint, obj, True, options.noncachable_types)
    return CheckResult(_IS_VALID, container_is_immutable)

def _container_check_callable(
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
    from .type_hints import _is_subtype_of_typehint  # pylint: disable=import-outside-toplevel

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
        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

    # If no args, just being callable is enough. Callables are not immutable.
    if not args:
        return CheckResult(_IS_VALID, _NOT_IMMUTABLE)

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
                        return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
            except (ValueError, TypeError):
                pass  # Built-ins or C callables may not have signatures
        return CheckResult(_IS_VALID, _NOT_IMMUTABLE)

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
            return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

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
                    return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)

        # Check return type if possible
        if return_type is not None and sig.return_annotation is not inspect.Signature.empty:
            # Check if the actual return annotation is a subtype of the expected return type (covariance)
            if not _is_subtype_of_typehint(sig.return_annotation, return_type):
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Callable's annotated return type '{sig.return_annotation}' does not match "
                        f"expected type hint '{return_type}'.",
                        tag=_TypeHintsErrorTag.VALIDATION_FAILED)
                return CheckResult(_NOT_VALID, _NOT_IMMUTABLE)
    except (ValueError, TypeError):
        # Builtins or C callables may not have signatures; fallback to just callable
        return CheckResult(_IS_VALID, _NOT_IMMUTABLE)

    return CheckResult(_IS_VALID, _NOT_IMMUTABLE)
