"""Error tags for SimpleBench CoreData types."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _CoreDataErrorTag(ErrorTag):
    """Error tags for core type errors."""

    INVALID_CACHE_TYPE = 'INVALID_CACHE_TYPE'
    """The provided cache size is not an integer."""
    INVALID_CACHE_SIZE = 'INVALID_CACHE_SIZE'
    """The provided cache size is less than 1."""
    CORE_DATA_SET_NOT_ELEMENT_COLLECTION = 'CORE_DATA_SET_NOT_ELEMENT_COLLECTION'
    """The provided iterable to CoreDataSet is not an ElementCollection."""
    CORE_DATA_SET_INVALID_ITEM_TYPE = 'CORE_DATA_SET_INVALID_ITEM_TYPE'
    """An invalid item type was passed to CoreDataSet."""
    CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE = 'CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE'
    """An invalid item type was passed to CoreDataSequence."""
    CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION = 'CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION'
    """The provided iterable to CoreDataSequence is not an ElementCollection."""
    CORE_DATA_MAPPING_INVALID_ARG_TYPE = 'CORE_DATA_MAPPING_INVALID_ARG_TYPE'
    """The provided argument to CoreDataMapping is not a Mapping."""
    CORE_DATA_MAPPING_INVALID_KEY_TYPE = 'CORE_DATA_MAPPING_INVALID_KEY_TYPE'
    """A key in the provided Mapping to CoreDataMapping is not a str."""
    CORE_DATA_MAPPING_INVALID_KEY_VALUE = 'CORE_DATA_MAPPING_INVALID_KEY_VALUE'
    """A key in the provided Mapping to CoreDataMapping is not a valid identifier string."""
    CORE_DATA_MAPPING_INVALID_VALUE_TYPE = 'CORE_DATA_MAPPING_INVALID_VALUE_TYPE'
    """An invalid value type was passed to CoreDataMapping."""
    CORE_DATA_MAPPING_KEY_ERROR = 'CORE_DATA_MAPPING_KEY_ERROR'
    """A key error occurred when accessing CoreDataMapping."""
    CORE_DATA_MAPPING_IMMUTABLE = 'CORE_DATA_MAPPING_IMMUTABLE'
    """An attempt was made to modify an immutable CoreDataMapping."""
    CORE_DATA_COMPARISON_UNSUPPORTED_TYPE = 'CORE_DATA_COMPARISON_UNSUPPORTED_TYPE'
    """An unsupported CoreData type was used in comparison."""
