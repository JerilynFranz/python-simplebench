"""ErrorTags for typed dict validation."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _TypedDictErrorTag(ErrorTag):
    """Error tags for type hints validation errors."""

    INVALID_CORE_DATA_MAPPING_TYPE_ARGS = auto()
    """The CoreDataMapping type does not have exactly one type argument."""
    DATA_DOES_NOT_CONFORM_TO_TYPEDDICT = auto()
    """The provided data does not conform to the expected TypedDict structure."""
    NOT_A_SET = auto()
    """The provided data is not a Set."""
    SET_ITEM_INVALID_TYPE = auto()
    """An item in the Set has an invalid type."""
    SET_ITEM_INVALID_VALUE = auto()
    """An item in the Set has an invalid value."""
    NOT_A_SEQUENCE = auto()
    """The provided data is not a Sequence."""
    NOT_A_MAPPING = auto()
    """The provided data is not a Mapping."""
    INVALID_MAPPING_TYPE_ARGS = auto()
    """The Mapping type does not have exactly two type arguments."""
    MISSING_REQUIRED_KEYS = auto()
    """One or more required keys are missing."""
    EXTRA_KEYS_PRESENT = auto()
    """One or more extra keys are present."""
    MAPPING_KEY_NOT_STRING = auto()
    """A key in the mapping is not a string."""
    MISCONFIGURED_TYPED_DICT = auto()
    """The TypedDict class is misconfigured."""
    UNABLE_TO_RESOLVE_TYPE_HINT = auto()
    """Unable to resolve the provided type hint."""
    MAX_CORE_DATA_DEPTH_EXCEEDED = auto()
    """The maximum core data depth has been exceeded during validation."""
    NOT_A_TYPED_DICT = auto()
    """The provided data is not a TypedDict."""
    INVALID_TYPEDDICT_VALUE_TYPE = auto()
    """The value type for a TypedDict key is invalid."""
    MISSING_REQUIRED_TYPEDDICT_KEY = auto()
    """A required key is missing from the TypedDict data."""
    EXTRA_TYPEDDICT_KEY = auto()
    """An extra key is present in the TypedDict data that is not defined in the TypedDict."""
    INVALID_TYPEDDICT_KEY_VALUE_TYPE = auto()
    """The value for a TypedDict key has an incorrect type."""
    CYCLIC_REFERENCE_DETECTED = auto()
    """A cyclic reference was detected during TypedDict validation."""
