"""ErrorTags for Matplotlib :class:`~.Theme`."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ThemeErrorTag(ErrorTag):
    """ErrorTags for exceptions in the MatPlotLib :class:`~.Theme` class."""

    THEME_IMMUTABLE = auto()
    """The Theme instance is immutable; modification of individual rcParams is not allowed after creation."""
