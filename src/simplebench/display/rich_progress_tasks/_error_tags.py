"""Error tags for the RichProgressTasks class."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _RichProgressTasksErrorTag(ErrorTag):
    """Error tags for the RichProgressTasks class."""

    DELITEM_INVALID_NAME_ARG = auto()
    """Something other than a string was passed to the RichProgressTask() __delitem__ method"""
    DELITEM_NOT_FOUND = auto()
    """The requested task was not found"""
    GETITEM_INVALID_NAME_ARG = auto()
    """Something other than a string was passed to the RichProgressTask() __getitem__ method"""
    GETITEM_NOT_FOUND = auto()
    """The requested task was not found"""
    INIT_INVALID_VERBOSITY_ARG = auto()
    """Something other than a Verbosity instance was passed to the RichProgressTasks()
    constructor as the verbosity arg"""
    INIT_INVALID_CONSOLE_ARG = auto()
    """Something other than a Console instance was passed to the RichProgressTasks() constructor as the console arg"""
    ADD_TASK_DUPLICATE_NAME = auto()
    """A task with the same name already exists"""
