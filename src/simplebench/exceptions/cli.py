"""ErrorTags for simplebench.cli related exceptions in SimpleBench."""
from ..enums import enum_docstrings
from .base import ErrorTag


@enum_docstrings
class _CLIErrorTag(ErrorTag):
    """ErrorTags for CLI-related exceptions."""
    CLI_INVALID_EXTRA_ARGS_TYPE = "CLI_INVALID_EXTRA_ARGS_TYPE"
    """The 'extra_args' argument must either be None or a list of str."""
    CLI_INVALID_EXTRA_ARGS_ITEM_TYPE = "CLI_INVALID_EXTRA_ARGS_ITEM_TYPE"
    """A non-str item was found in the passed 'extra_args' list."""
