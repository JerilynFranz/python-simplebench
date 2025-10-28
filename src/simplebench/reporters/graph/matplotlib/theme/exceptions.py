"""ErrorTags for Matplotlib themes."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class ThemeErrorTag(ErrorTag):
    """ErrorTags for exceptions in the MatPlotLib Theme class."""
    THEME_IMMUTABLE = "THEME_IMMUTABLE"
    """The Theme instance is immutable; modification of individual rcParams is not allowed after creation."""
