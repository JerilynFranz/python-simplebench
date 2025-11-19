"""ErrorTags for simplebench.tasks module."""
from ..enums import enum_docstrings
from ..exceptions import ErrorTag


@enum_docstrings
class _RichTaskErrorTag(ErrorTag):
    """Error tags for the RichTasks class."""
    INIT_INVALID_NAME_ARG = "INIT_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichTask() constructor"""
    INIT_INVALID_DESCRIPTION_ARG = "INIT_INVALID_DESCRIPTION_ARG"
    """Something other than a string or rich.Text was passed to the RichTask() constructor"""
    INIT_INVALID_PROGRESS_ARG = "INIT_INVALID_PROGRESS_ARG"
    """Something other than a Progress instance was passed to the RichTask() constructor"""
    INIT_EMPTY_STRING_NAME = "INIT_EMPTY_STRING_NAME"
    """The name arg cannot be an empty string"""
    INIT_EMPTY_STRING_DESCRIPTION = "INIT_EMPTY_STRING_DESCRIPTION"
    """The description arg cannot be an empty string"""
    UPDATE_INVALID_COMPLETED_ARG = "UPDATE_INVALID_COMPLETED_ARG"
    """Something other than an int was passed to the RichTask() update method"""
    UPDATE_INVALID_DESCRIPTION_ARG = "UPDATE_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the RichTask() update method"""
    UPDATE_INVALID_REFRESH_ARG = "UPDATE_INVALID_REFRESH_ARG"
    """Something other than a bool was passed to the RichTask() update method"""
    UPDATE_ALREADY_TERMINATED_TASK = "UPDATE_ALREADY_TERMINATED_TASK"
    """The task has already been terminated"""
    TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK = "TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK"
    """The task has already been terminated"""


@enum_docstrings
class _RichProgressTasksErrorTag(ErrorTag):
    """Error tags for the RichProgressTasks class."""
    DELITEM_INVALID_NAME_ARG = "DELITEM_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() __delitem__ method"""
    DELITEM_NOT_FOUND = "DELITEM_NOT_FOUND"
    """The requested task was not found"""
    GETITEM_INVALID_NAME_ARG = "GETITEM_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() __getitem__ method"""
    GETITEM_NOT_FOUND = "GETITEM_NOT_FOUND"
    """The requested task was not found"""
    INIT_INVALID_VERBOSITY_ARG = "INIT_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the RichProgressTasks()
    constructor as the verbosity arg"""
    INIT_INVALID_CONSOLE_ARG = "INIT_INVALID_CONSOLE_ARG"
    """Something other than a Console instance was passed to the RichProgressTasks() constructor as the console arg"""
    ADD_TASK_DUPLICATE_NAME = "ADD_TASK_DUPLICATE_NAME"
    """A task with the same name already exists"""
