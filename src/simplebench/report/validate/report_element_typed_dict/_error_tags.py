"""
Docstring for simplebench.report.validate._error_tags
"""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReportElementValidationErrorTag(ErrorTag):
    """Error tags for report element validation errors."""
    UNSUPPORTED_TYPEDDICT_KEY_TYPE = "UNSUPPORTED_TYPEDDICT_KEY_TYPE"
    """The TypedDict key has an unsupported type."""
    UNEXPECTED_TYPEDDICT_KEY_WRAPPER_TYPE = "UNEXPECTED_TYPEDDICT_KEY_WRAPPER_TYPE"
    """The TypedDict key wrapper type is neither Required nor NotRequired."""
    UNEXPECTED_TYPEDDICT_WRAPPER_MODULE = "UNEXPECTED_TYPEDDICT_WRAPPER_MODULE"
    """The TypedDict key type wrapper module is not either typing or typing_extensions."""
    MISCONFIGURED_REPORT_ELEMENT_TYPED_DICT = "MISCONFIGURED_REPORT_ELEMENT_TYPED_DICT"
    """The ReportElementTypedDict TypedDict subclass is misconfigured."""
    MISSING_REQUIRED_KEYS = "MISSING_REQUIRED_KEYS"
    """The provided data is missing required keys."""
    EXTRA_KEYS_PRESENT = "EXTRA_KEYS_PRESENT"
    """The provided data contains extra keys not defined in the TypedDict."""
    NOT_A_MAPPING = "NOT_A_MAPPING"
    """The provided data is not a mapping type."""
    MAPPING_KEY_NOT_STRING = "MAPPING_KEY_NOT_STRING"
    """A key for the provided mapping was not of type :class:`str`."""
    NOT_A_REPORT_ELEMENT_TYPED_DICT = "NOT_A_REPORT_ELEMENT_TYPED_DICT"
    """The provided TypedDict class is not a ReportElementTypedDict subclass."""
    INVALID_CACHE_SIZE = "INVALID_CACHE_SIZE"
    """The provided cache size is invalid."""
    INVALID_CACHE_SIZE_TYPE = "INVALID_CACHE_SIZE_TYPE"
    """The provided cache size is not an integer."""
