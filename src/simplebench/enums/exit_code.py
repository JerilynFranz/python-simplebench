"""Exit codes used by SimpleBench."""
from enum import Enum

from .decorators import enum_docstrings


@enum_docstrings
class ExitCode(int, Enum):
    """Exit codes for SimpleBench CLI.

    Defined Exit Codes are:
      - SUCCESS: Successful execution.
      - RUNTIME_ERROR: General runtime error during execution.
      - CLI_ARGUMENTS_ERROR: Error while processing command line arguments.
      - KEYBOARD_INTERRUPT: Keyboard interrupt occurred.

    """
    SUCCESS = 0
    """Successful execution."""
    RUNTIME_ERROR = 1
    """Runtime error during execution."""
    CLI_ARGUMENTS_ERROR = 2
    """Error while processing command line arguments."""
    KEYBOARD_INTERRUPT = 3
    """Keyboard interrupt occurred."""
