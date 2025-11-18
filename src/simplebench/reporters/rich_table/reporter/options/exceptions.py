"""ErrorTags for the rich_table reporter Options() class."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class RichTableOptionsErrorTag(ErrorTag):
    """ErrorTags for exceptions in the :class:`~.RichTableOptions` class."""
    INVALID_VIRTUAL_WIDTH_TYPE = "INVALID_VIRTUAL_WIDTH_TYPE"
    """The ``virtual_width`` specified in the :class:`~.RichTableOptions` must be an
    integer or ``None``.
    """
    INVALID_VIRTUAL_WIDTH_VALUE = "INVALID_VIRTUAL_WIDTH_VALUE"
    """The ``virtual_width`` specified in the :class:`~.RichTableOptions` must be between
    80 and 10000 characters when specified.
    """
