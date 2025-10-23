"""ErrorTags for simplebench.cli related exceptions in SimpleBench."""
from .base import ErrorTag
from ..enums import enum_docstrings


@enum_docstrings
class CLIErrorTag(ErrorTag):
    """ErrorTags for CLI-related exceptions."""
    CLI_INVALID_EXTRA_ARGS_TYPE = "CLI_INVALID_EXTRA_ARGS_TYPE"
    """The 'extra_args' argument must either be None or a list of str."""
    CLI_INVALID_EXTRA_ARGS_ITEM_TYPE = "CLI_INVALID_EXTRA_ARGS_ITEM_TYPE"
    """A non-str item was found in the passed 'extra_args' list."""
