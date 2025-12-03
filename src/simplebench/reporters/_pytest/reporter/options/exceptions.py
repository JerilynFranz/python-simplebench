"""ErrorTags for the pytest reporter Options() class."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _PytestOptionsErrorTag(ErrorTag):
    """ErrorTags for exceptions in the :class:`~.PytestOptions` class."""
    INVALID_VIRTUAL_WIDTH_TYPE = "INVALID_VIRTUAL_WIDTH_TYPE"
    """The ``virtual_width`` specified in the :class:`~.PytestOptions` must be an
    integer or ``None``.
    """
    INVALID_VIRTUAL_WIDTH_VALUE = "INVALID_VIRTUAL_WIDTH_VALUE"
    """The ``virtual_width`` specified in the :class:`~.PytestOptions` must be between
    80 and 10000 characters when specified.
    """
    INVALID_DEFAULT_FIELDS_TYPE = "INVALID_DEFAULT_FIELDS_TYPE"
    """The ``default_fields`` specified in the :class:`~.PytestOptions` must be a sequence
    of :class:`~.PytestField` instances.
    """
    INVALID_DEFAULT_FIELDS_VALUE = "INVALID_DEFAULT_FIELDS_VALUE"
    """The ``default_fields`` specified in the :class:`~.PytestOptions` must not be empty.
    """
    INVALID_VARIATION_COLS_LAST_TYPE = "INVALID_VARIATION_COLS_LAST_TYPE"
    """The ``variation_cols_last`` specified in the :class:`~.PytestOptions` must be a boolean.
    """
