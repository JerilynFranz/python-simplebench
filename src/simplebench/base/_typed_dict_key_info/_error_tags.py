"""
Docstring for simplebench.report.validate._error_tags
"""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__ = []


@enum_docstrings
class _TypedDictKeyInfoErrorTag(ErrorTag):
    NESTED_REQUIRED_NOTREQUIRED_READONLY = 'NESTED_REQUIRED_NOTREQUIRED_READONLY'
    """The TypedDict key has nested Required/NotRequired/ReadOnly wrappers that failed to unwrap."""
    UNEXPECTED_TYPEDDICT_KEY_WRAPPER_TYPE = 'UNEXPECTED_TYPEDDICT_KEY_WRAPPER_TYPE'
    """The TypedDict key wrapper type is neither Required nor NotRequired."""
    UNEXPECTED_TYPEDDICT_WRAPPER_MODULE = 'UNEXPECTED_TYPEDDICT_WRAPPER_MODULE'
    """The TypedDict key type wrapper module is not either typing or typing_extensions."""
