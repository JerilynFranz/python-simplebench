"""ErrorTags for RichTask module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _RichTaskErrorTag(ErrorTag):
    """Error tags for the RichTasks class."""

    INIT_INVALID_NAME_ARG = auto()
    """Something other than a string was passed to the RichTask() constructor"""
    INIT_INVALID_DESCRIPTION_ARG = auto()
    """Something other than a string or rich.Text was passed to the RichTask() constructor"""
    INIT_INVALID_PROGRESS_ARG = auto()
    """Something other than a Progress instance was passed to the RichTask() constructor"""
    INIT_EMPTY_STRING_NAME = auto()
    """The name arg cannot be an empty string"""
    INIT_EMPTY_STRING_DESCRIPTION = auto()
    """The description arg cannot be an empty string"""
    UPDATE_INVALID_COMPLETED_ARG = auto()
    """Something other than an int was passed to the RichTask() update method"""
    UPDATE_INVALID_DESCRIPTION_ARG = auto()
    """Something other than a string was passed to the RichTask() update method"""
    UPDATE_INVALID_REFRESH_ARG = auto()
    """Something other than a bool was passed to the RichTask() update method"""
    UPDATE_ALREADY_TERMINATED_TASK = auto()
    """The task has already been terminated"""
    TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK = auto()
    """The task has already been terminated"""
