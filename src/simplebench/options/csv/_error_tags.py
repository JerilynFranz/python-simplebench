"""ErrorTags for :class:`~.CSVOptions` class related exceptions."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _CSVOptionsErrorTag(ErrorTag):
    """ErrorTags for :class:`~.CSVOptions` class related exceptions."""

    INVALID_DEFAULT_FIELDS_TYPE = auto()
    """The ``fields`` specified in the :class:`~.CSVOptions` must be a sequence
    of :class:`~.CSVField` instances.
    """
    INVALID_DEFAULT_FIELDS_VALUE = auto()
    """The ``fields`` specified in the :class:`~.CSVOptions` must not be empty.
    """
    INVALID_VARIATION_COLS_LAST_TYPE = auto()
    """The ``variation_cols_last`` specified in the :class:`~.CSVOptions` must be a boolean.
    """
