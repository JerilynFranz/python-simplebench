"""ErrorTags for simplebench.cli related exceptions in SimpleBench."""

from enum import auto
from simplebench.doc_utils import enum_docstrings

from ..exceptions.error_tag import ErrorTag


@enum_docstrings
class _CLIErrorTag(ErrorTag):
    """ErrorTags for CLI-related exceptions."""

    CLI_INVALID_EXTRA_ARGS_TYPE = auto()
    """The 'extra_args' argument must either be None or a list of str."""
    CLI_INVALID_EXTRA_ARGS_ITEM_TYPE = auto()
    """A non-str item was found in the passed 'extra_args' list."""
    ARGUMENT_CONFLICT = auto()
    """Conflicting arguments were provided to the CLI."""
    NO_MATCHING_CASES = auto()
    """No matching benchmark cases were found for the specified --run options."""
    NO_REPORTERS_SPECIFIED = auto()
    """No reporters were specified for output generation."""
