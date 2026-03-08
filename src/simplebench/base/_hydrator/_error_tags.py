"""Builder exception ErrorTags for JSON report objects."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _HydratorErrorTag(ErrorTag):
    """Builder exception ErrorTags for JSON report objects."""

    UNSUPPORTED_TYPEDDICT_VALUE_TYPE = auto()
    """Unsupported TypedDict value type encountered during unwrapping to core type."""
    INVALID_PROCESS_AS_TYPE = auto()
    """Invalid `process_as` type. Must be a `dict`."""
    INVALID_PROCESS_AS_KEY = auto()
    """Invalid `process_as` key. Not listed in `allowed` keys."""
    INVALID_PROCESS_AS_NOT_CALLABLE = auto()
    """Invalid `process_as` value. Not callable."""
    INVALID_PROCESS_AS_TOO_MANY_PARAMETERS = auto()
    """Invalid `process_as` value. Cannot have more than one parameter."""
    INVALID_PROCESS_AS_NOT_POSITIONAL = auto()
    """Invalid `process_as` value. Must take positional-only or positional-or-keyword parameters."""
    INVALID_PROCESS_AS_NO_RETURN_ANNOTATION = auto()
    """Invalid `process_as` value. Must have a return type annotation."""
    INVALID_MATCH_ON_TYPE = auto()
    """Invalid `match_on` type. Must be a `dict`."""
    INVALID_MATCH_ON_KEY = auto()
    """Invalid `match_on` key. Not listed in `allowed` keys."""
    INVALID_DEFAULT_TYPE = auto()
    """Invalid `default` value type. Must be a `dict`."""
    INVALID_DEFAULT_KEY = auto()
    """Invalid `default` key. Not listed in `optional` keys."""
    INVALID_DATA_VALUE_TYPE = auto()
    """Invalid `data` value type. Did not match the `allowed` type."""
    INVALID_DATA_KEY = auto()
    """Invalid `data` key. Not listed in `allowed` keys."""
    INVALID_MATCH_ON_VALUE = auto()
    """Invalid `match_on` value. Not listed in `allowed` keys."""
    INVALID_ALLOWED_EMPTY = auto()
    """Invalid `allowed` value. The dictionary cannot be empty."""
    INVALID_SKIP_VALUE = auto()
    """Invalid `skip` value. Not listed in `allowed` keys."""
    INVALID_ALLOWED_VALUE_TYPE = auto()
    """Invalid `allowed` value. Expected a `type`."""
    INVALID_SKIP_TYPE = auto()
    """Invalid `skip` type: Must be an Iterable of str."""
    INVALID_SKIP_ITEM_TYPE = auto()
    """Invalid type for an item in the `skip` parameter. Expected `str`."""
    INVALID_ALLOWED_TYPE = auto()
    """Invalid `allowed` type: Must be a dict."""
    INVALID_OPTIONAL_TYPE = auto()
    """Invalid `optional` type: Must be an Iterable of str."""
    INVALID_OPTIONAL_ITEM_TYPE = auto()
    """Invalid type for an item in the `optional` parameter. Expected `str`."""
    INVALID_OPTIONAL_ITEM_VALUE = auto()
    """Invalid value for an item in the `optional` parameter. Not listed in `allowed` keys."""
    INVALID_ERROR_TAG_TYPE = auto()
    """Invalid type for the `error_tag` parameter. Expected type `ErrorTag`."""
    INVALID_DATA_TYPE = auto()
    """Invalid type for the `data` parameter. Expected type `dict`."""
    INVALID_DATA_KEY_TYPE = auto()
    """Invalid key type in the `data` parameter. Expected type `str`."""
    INVALID_OPTIONAL_FIELDS_TYPE = auto()
    """Invalid type for the `optional_fields` parameter. Expected Iterable of `str`."""
    INVALID_OPTIONAL_FIELDS_ITEM_TYPE = auto()
    """Invalid type for an item in the `optional_fields` parameter. Expected `str`."""
