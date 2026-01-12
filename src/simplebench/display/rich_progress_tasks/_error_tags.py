"""Error tags for the RichProgressTasks class."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _RichProgressTasksErrorTag(ErrorTag):
    """Error tags for the RichProgressTasks class."""

    DELITEM_INVALID_NAME_ARG = 'DELITEM_INVALID_NAME_ARG'
    """Something other than a string was passed to the RichProgressTask() __delitem__ method"""
    DELITEM_NOT_FOUND = 'DELITEM_NOT_FOUND'
    """The requested task was not found"""
    GETITEM_INVALID_NAME_ARG = 'GETITEM_INVALID_NAME_ARG'
    """Something other than a string was passed to the RichProgressTask() __getitem__ method"""
    GETITEM_NOT_FOUND = 'GETITEM_NOT_FOUND'
    """The requested task was not found"""
    INIT_INVALID_VERBOSITY_ARG = 'INIT_INVALID_VERBOSITY_ARG'
    """Something other than a Verbosity instance was passed to the RichProgressTasks()
    constructor as the verbosity arg"""
    INIT_INVALID_CONSOLE_ARG = 'INIT_INVALID_CONSOLE_ARG'
    """Something other than a Console instance was passed to the RichProgressTasks() constructor as the console arg"""
    ADD_TASK_DUPLICATE_NAME = 'ADD_TASK_DUPLICATE_NAME'
    """A task with the same name already exists"""
