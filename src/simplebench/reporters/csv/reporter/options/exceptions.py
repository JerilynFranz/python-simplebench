"""ErrorTags for :class:`~.CSVOptions` class related exceptions."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _CSVOptionsErrorTag(ErrorTag):
    """ErrorTags for :class:`~.CSVOptions` class related exceptions."""
    INVALID_DEFAULT_FIELDS_TYPE = "INVALID_DEFAULT_FIELDS_TYPE"
    """The ``fields`` specified in the :class:`~.CSVOptions` must be a sequence
    of :class:`~.CSVField` instances.
    """
    INVALID_DEFAULT_FIELDS_VALUE = "INVALID_DEFAULT_FIELDS_VALUE"
    """The ``fields`` specified in the :class:`~.CSVOptions` must not be empty.
    """
    INVALID_VARIATION_COLS_LAST_TYPE = "INVALID_VARIATION_COLS_LAST_TYPE"
    """The ``variation_cols_last`` specified in the :class:`~.CSVOptions` must be a boolean.
    """
