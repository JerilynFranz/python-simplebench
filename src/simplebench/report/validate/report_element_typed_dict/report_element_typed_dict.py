""""Validation utilities for report elements defined as TypedDicts.

Structural validation functions to check if a given mapping conforms to the schema
defined by a ReportElementTypedDict subclass.

ReportElementTypedDict is a specialized TypedDict subclass used to define
the expected structure of report elements in SimpleBench. They consist **ONLY**
of string keys, core type primitive values, and nested :class:`ReportElementTypedDict` instances.

This module provides functions to validate arbitrary mappings against
the structure defined by a ReportElementTypedDict subclass without needing
to create actual instances of the TypedDict. This allows for flexible and
efficient validation of report data structures.

It does not need to solve the general TypedDict mimic validation problem,
only the specific case of ReportElementTypedDicts used in SimpleBench reports.
"""

from typing import Any, Mapping, TypeGuard, TypeVar

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types.core import is_core_data_primitive, is_core_data_primitive_type

from . import _cache
from ._error_tags import _ReportElementValidationErrorTag
from ._typed_dict_key_info import _TypedDictKeyInfo

T = TypeVar("T", bound=ReportElementTypedDict)

"""Set of core data primitive types for quick membership testing."""

def is_report_element_typed_dict(obj: Any) -> TypeGuard[ReportElementTypedDict]:
    """TypeGuard function. Check if an object is actually a :class:`ReportElementTypedDict` subclass.
        
    :param Any obj: The object to check.
    :return bool: True if the object is a ReportElementTypedDict subclass, False otherwise.
    """
    return bool(isinstance(obj, type) and issubclass(obj, ReportElementTypedDict))  # type: ignore[reportArgumentType]

def report_element_typed_dict_mimic(data: Mapping[str, Any], td_cls: type[T]) -> T:
    """Validate a mapping against the ReportElementTypedDict.

    Raises an error if validation fails.

    This is a mimic function that behaves like a type cast to ReportElementTypedDict.

    Because it performs structural validation, the returned value is guaranteed to conform
    to the specified ReportElementTypedDict structure if no error is raised.

    This is a structural check and does not require an actual instance of ReportElementTypedDict.

    It validates that:
    - All required keys are present and of the correct type.
    - All optional keys, if present, are of the correct type.
    - No extra keys are present.

    For performance, it uses a size-limited cache to store previously validated
    results to avoid redundant validation. Only fully immutable core data type
    structures are cached positively (with validity of `True`) to ensure safety.
    Mutable structures can be validated but are not cached.

    :param Mapping[str, Any] data: The dictionary to validate.
    :param ReportElementTypedDict td_cls: The TypedDict subclass type to validate against.
    :return ReportElementTypedDict: The validated ReportElementTypedDict.
    :raise SimpleBenchValueError: If required keys are missing or extra keys are    present.
    :raise SimpleBenchTypeError: If any value has an incorrect type.
    """
    if not is_report_element_typed_dict_mimic(data, td_cls):
        raise SimpleBenchTypeError(
            f"Data does not conform to ReportElementTypedDict {td_cls.__name__}",
            tag=_ReportElementValidationErrorTag.NOT_A_REPORT_ELEMENT_TYPED_DICT)
    return data

def is_report_element_typed_dict_mimic(data: Mapping[str, Any],
                                       td_cls: type[T]) -> TypeGuard[T]:
    """TypeGuard function. Check if a mapping conforms to a ReportElementTypedDict subclass.

    It acts as a structural isinstance() check for mappings against the TypedDict subclass.

    It comprehensively checks that the mapping conforms to the structure defined
    by the ReportElementTypedDict subclass and recursively checks nested ReportElementTypedDicts.

    Static type checkers can use this to narrow types accordingly and will understand
    that after a successful check the mapping conforms to the ReportElementTypedDict structure.

    A Mapping[str, Any] is checked against the structure defined by the TypedDict subclass.

    It validates that:
    - All required keys are present and of the correct type.
    - All optional keys, if present, are of the correct type.
    - No extra keys are present.

    It **DOES NOT** require an actual instance of TypedDict and performs
    a structural check against the TypedDict subclass definition for a
    generic Mapping[str, Any]. This allows validating arbitrary dictionaries
    against the TypedDict structure without needing to create TypedDict instances.

    For performance, it uses a size-limited cache to store previous validation results.

    Also, if subtrees of the mapping have already been validated and cached,
    it reuses those cached results to avoid redundant validation.

    If subtrees are newly encountered, they are validated and their results
    are added to the cache for future reuse. Only fully immutable core data type
    structures are cached positively (with validity of `True`) to ensure safety.
    
    :param Mapping[str, Any] data: The dictionary to check.
    :param ReportElementTypedDict td_cls: The TypedDict subclass type to check against.
    :return bool: True if the dictionary conforms to the TypedDict subclass, False otherwise.
    :raise SimpleBenchTypeError: If the TypedDict subclass is misconfigured.
    """
    valid, _ = _validate_and_check_immutability_of_mimic(data, td_cls)
    return valid

def _validate_and_check_immutability_of_mimic(
        data: Mapping[str, Any], td_cls: type[ReportElementTypedDict]) -> tuple[bool, bool]:
    """Validate a mapping against a ReportElementTypedDict subclass
    and check if it consists only of fully immutable core data types.

    It recursively checks the structure and types of the mapping against the TypedDict subclass
    and returns whether it conforms to the TypedDict subclass and whether the structure
    is fully immutable core data types.

    :param Mapping[str, Any] data: The dictionary to check.
    :param ReportElementTypedDict td_cls: The TypedDict subclass type to check against.
    :return tuple[bool, bool]: A tuple where the first element indicates if the dictionary
        conforms to the TypedDict subclass, and the second element indicates if the
        data consists only of fully immutable core data types.
    :raise SimpleBenchTypeError: If the TypedDict subclass is misconfigured.
    """
    cached_state: bool | None = _cache.valid_in_cache(td_cls, data)
    if cached_state is not None:
        # Cached results are always immutable core data types and thus safe to reuse.
        # Mutable structures can be validated but they are not cached because their
        # state can change.
        return (cached_state, cached_state)

    _validate_report_element_typed_dict_subclass(td_cls)
    _validate_is_mapping_of_string_to_any(data)
    _validate_has_required_and_no_extra_keys(data, td_cls)

    keys_to_check: set[str] = set(data.keys())

    # Check value types
    immutable_children: bool = True
    while keys_to_check:
        key = keys_to_check.pop()
        value = data[key]
        key_info = _TypedDictKeyInfo(key, td_cls)
        expected_type = key_info.value_type

        if is_core_data_primitive_type(expected_type):
            if not is_core_data_primitive(value):
                _cache.add_cache_entry(td_cls, data, False)
                return (False, False) # Value type mismatch and we cannot determine immutability
            continue

        # Nested ReportElementTypedDict subclasses
        if isinstance(expected_type, type) and issubclass(
            expected_type, ReportElementTypedDict):  # type: ignore[reportArgumentType]
            valid, immutable_tree = _validate_and_check_immutability_of_mimic(
                                        value, expected_type)
            if immutable_tree:
                _cache.add_cache_entry(td_cls, data, valid)
            else:
                immutable_children = False  # at least one child is mutable
            if not valid:
                _cache.add_cache_entry(td_cls, data, False)
                return (False, False)
            continue

        # Unsupported type - fails to be a nested ReportElementTypedDict or core data primitive
        # This probably indicates a misconfiguration of the TypedDict subclass
        raise SimpleBenchTypeError(
            f"Key '{key}' in ReportElementTypedDict '{td_cls.__name__}' has unsupported type {expected_type}",
            tag=_ReportElementValidationErrorTag.MISCONFIGURED_REPORT_ELEMENT_TYPED_DICT)

    if immutable_children:  # All children are immutable core data types and so we can cache positively
        _cache.add_cache_entry(td_cls, data, True)
    return (True, immutable_children)  # All keys validated successfully, propagate immutability status

def _validate_report_element_typed_dict_subclass(td_cls: type[ReportElementTypedDict]) -> None:
    """Validate a ReportElementTypedDict subclass schema.

    This is not a runtime instance validation, but a static schema validation.

    This function checks that the provided TypedDict subclass is declared correctly
    and consistently. It ensures that all keys in the TypedDict's annotations
    are accounted for in either the `__required_keys__` or `__optional_keys__` sets.
    It raises an error if there are any discrepancies.

    :param ReportElementTypedDict td_cls: The TypedDict subclass to validate
    :raise SimpleBenchTypeError: If the TypedDict subclass is misconfigured.
    """
    annotations = td_cls.__annotations__
    required: set[str] = getattr(td_cls, '__required_keys__', set(annotations))
    optional: set[str] = getattr(td_cls, '__optional_keys__', set())
    annotation_set = set(annotations.keys())

    if annotation_set != required.union(optional):
        missing_from_annotations = (required.union(optional)) - annotation_set
        extra_in_annotations = annotation_set - (required.union(optional))
        output = []
        if extra_in_annotations:
            output.append(
                f"Keys {extra_in_annotations} are in annotations but not marked as required/optional "
                f"for class {td_cls.__name__}")
        if missing_from_annotations:
            output.append(
                f"Keys {missing_from_annotations} are marked as required/optional but "
                f"missing from annotations for class {td_cls.__name__}")
        message = "; ".join(output)
        raise SimpleBenchTypeError(
            message,
            tag=_ReportElementValidationErrorTag.MISCONFIGURED_REPORT_ELEMENT_TYPED_DICT)

def _validate_is_mapping_of_string_to_any(data: Mapping[str, Any]) -> None:
    """Validate that data is a Mapping[str, Any].

    :param Mapping[str, Any] data: The data to validate.
    :raise SimpleBenchTypeError: If data is not a Mapping[str, Any].
    """
    if not isinstance(data, Mapping):
        raise SimpleBenchTypeError(
            f"Data must be a Mapping, got {type(data)}",
            tag=_ReportElementValidationErrorTag.NOT_A_MAPPING)
    for key in data.keys():
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                f"All keys in data must be strings, found key of type {type(key)}",
                tag=_ReportElementValidationErrorTag.MAPPING_KEY_NOT_STRING)

def _validate_has_required_and_no_extra_keys(data: Mapping[str, Any],
                                             td_cls: type[ReportElementTypedDict]) -> None:
    """Validate that data has all required keys and no extra keys.

    :param Mapping[str, Any] data: The data to validate.
    :param ReportElementTypedDict td_cls: The TypedDict subclass to validate against.
    :raise SimpleBenchTypeError: If required keys are missing or extra keys are present.
    """
    annotations = td_cls.__annotations__
    required: set[str] = getattr(td_cls, '__required_keys__', set(annotations))

    missing = required - data.keys()
    if missing:
        raise SimpleBenchTypeError(
            f"Missing required keys: {missing}",
            tag=_ReportElementValidationErrorTag.MISSING_REQUIRED_KEYS)

    extra = data.keys() - annotations.keys()
    if extra:
        raise SimpleBenchTypeError(
            f"Extra keys not allowed: {extra}",
            tag=_ReportElementValidationErrorTag.EXTRA_KEYS_PRESENT)
