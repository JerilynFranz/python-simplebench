"""Error tags for SimpleBench CoreData types."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _CoreDataErrorTag(ErrorTag):
    """Error tags for core type errors."""

    CORE_DATA_SET_GENERIC_TYPE_MISMATCH = auto()
    """A value in a CoreDataSet does not match the expected generic type for that set."""
    CORE_DATA_MAPPING_GENERIC_TYPE_MISMATCH = auto()
    """A value in a CoreDataMapping does not match the expected generic type for that mapping."""
    CORE_DATA_SET_INVALID_BYTES = auto()
    """Bytes were provided to CoreDataSet, which does not support bytes."""
    INVALID_CACHE_TYPE = auto()
    """The provided cache size is not an integer."""
    INVALID_CACHE_SIZE = auto()
    """The provided cache size is less than 1."""
    CORE_DATA_SET_NOT_ELEMENT_COLLECTION = auto()
    """The provided iterable to CoreDataSet is not an ElementCollection."""
    CORE_DATA_SET_INVALID_ITEM_TYPE = auto()
    """An invalid item type was passed to CoreDataSet."""
    CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE = auto()
    """An invalid item type was passed to CoreDataSequence."""
    CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION = auto()
    """The provided iterable to CoreDataSequence is not an ElementCollection."""
    CORE_DATA_MAPPING_INVALID_ARG_TYPE = auto()
    """The provided argument to CoreDataMapping is not a Mapping."""
    CORE_DATA_MAPPING_INVALID_KEY_TYPE = auto()
    """A key in the provided Mapping to CoreDataMapping is not a str."""
    CORE_DATA_MAPPING_INVALID_KEY_VALUE = auto()
    """A key in the provided Mapping to CoreDataMapping is not a valid identifier string."""
    CORE_DATA_MAPPING_INVALID_VALUE_TYPE = auto()
    """An invalid value type was passed to CoreDataMapping."""
    CORE_DATA_MAPPING_KEY_ERROR = auto()
    """A key error occurred when accessing CoreDataMapping."""
    CORE_DATA_MAPPING_IMMUTABLE = auto()
    """An attempt was made to modify an immutable CoreDataMapping."""
    CORE_DATA_COMPARISON_UNSUPPORTED_TYPE = auto()
    """An unsupported CoreData type was used in comparison."""
    CORE_DATA_SEQUENCE_UNSUPPORTED_PICKLE_VERSION = auto()
    """An unsupported pickle version was encountered when unpickling CoreDataSequence."""
    CORE_DATA_SET_UNSUPPORTED_PICKLE_VERSION = auto()
    """An unsupported pickle version was encountered when unpickling CoreDataSet."""
    CORE_DATA_MAPPING_UNSUPPORTED_PICKLE_VERSION = auto()
    """An unsupported pickle version was encountered when unpickling CoreDataMapping."""
    CORE_DATA_SEQUENCE_INVALID_INDEX_SLICE = auto()
    """An invalid index or slice was used to access CoreDataSequence."""
    CORE_DATA_SEQUENCE_INVALID_INDEX_TYPE = auto()
    """An invalid index type was used to access CoreDataSequence."""
