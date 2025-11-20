"""ErrorTags for Matplotlib :class:`~.Theme`."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ThemeErrorTag(ErrorTag):
    """ErrorTags for exceptions in the MatPlotLib :class:`~.Theme` class."""
    THEME_IMMUTABLE = "THEME_IMMUTABLE"
    """The Theme instance is immutable; modification of individual rcParams is not allowed after creation."""
