"""ErrorTags for typed dict validation."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _TypedDictErrorTag(ErrorTag):
    """Error tags for type hints validation errors."""

    NOT_A_SET = 'NOT_A_SET'
    """The provided data is not a Set."""
    SET_ITEM_INVALID_TYPE = 'SET_ITEM_INVALID_TYPE'
    """An item in the Set has an invalid type."""
    SET_ITEM_INVALID_VALUE = 'SET_ITEM_INVALID_VALUE'
    """An item in the Set has an invalid value."""
    NOT_A_SEQUENCE = 'NOT_A_SEQUENCE'
    """The provided data is not a Sequence."""
    NOT_A_MAPPING = 'NOT_A_MAPPING'
    """The provided data is not a Mapping."""
    INVALID_MAPPING_TYPE_ARGS = 'INVALID_MAPPING_TYPE_ARGS'
    """The Mapping type does not have exactly two type arguments."""
    MISSING_REQUIRED_KEYS = 'MISSING_REQUIRED_KEYS'
    """One or more required keys are missing."""
    EXTRA_KEYS_PRESENT = 'EXTRA_KEYS_PRESENT'
    """One or more extra keys are present."""
    MAPPING_KEY_NOT_STRING = 'MAPPING_KEY_NOT_STRING'
    """A key in the mapping is not a string."""
    MISCONFIGURED_TYPED_DICT = 'MISCONFIGURED_TYPED_DICT'
    """The TypedDict class is misconfigured."""
    UNABLE_TO_RESOLVE_TYPE_HINT = 'UNABLE_TO_RESOLVE_TYPE_HINT'
    """Unable to resolve the provided type hint."""
    MAX_CORE_DATA_DEPTH_EXCEEDED = 'MAX_CORE_DATA_DEPTH_EXCEEDED'
    """The maximum core data depth has been exceeded during validation."""
    NOT_A_TYPED_DICT = 'NOT_A_TYPED_DICT'
    """The provided data is not a TypedDict."""
    INVALID_TYPEDDICT_VALUE_TYPE = 'INVALID_TYPEDDICT_VALUE_TYPE'
    """The value type for a TypedDict key is invalid."""
    MISSING_REQUIRED_TYPEDDICT_KEY = 'MISSING_REQUIRED_TYPEDDICT_KEY'
    """A required key is missing from the TypedDict data."""
    EXTRA_TYPEDDICT_KEY = 'EXTRA_TYPEDDICT_KEY'
    """An extra key is present in the TypedDict data that is not defined in the TypedDict."""
    INVALID_TYPEDDICT_KEY_VALUE_TYPE = 'INVALID_TYPEDDICT_KEY_VALUE_TYPE'
    """The value for a TypedDict key has an incorrect type."""
    CYCLIC_REFERENCE_DETECTED = 'CYCLIC_REFERENCE_DETECTED'
    """A cyclic reference was detected during TypedDict validation."""
