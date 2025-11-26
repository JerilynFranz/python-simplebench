"""FlagType enums for SimpleBench.

Types of command-line flags for reporters.

    Available FlagTypes are:
      - BOOLEAN: Boolean flag type.
      - TARGET_LIST: List of output targets
      - INVALID: Invalid flag type. This is a testing placeholder and should not be used.
"""

from enum import Enum

from .decorators import enum_docstrings


@enum_docstrings
class FlagType(str, Enum):
    """Types of command-line flags for reporters.

    Available FlagTypes are:
      - BOOLEAN: Boolean flag type.
      - TARGET_LIST: List of output targets
      - INVALID: Invalid flag type. This is a testing placeholder and should not be used.
    """
    BOOLEAN = 'boolean'
    """Boolean flag type.

    This flag type represents a simple on/off or true/false option.

    Example: --verbose / --no-verbose
    """
    TARGET_LIST = 'target_list'
    """List of output targets

    This flag type represents a list of output targets for the reporter.

    This allows specifying multiple targets for the reporter to output to.

    The targets are specified as a list of strings and validated against
    the allowed Target enum values. It support passing NO targets as well,
    in which case the reporter will use the default targets.

    Example: --json console filesystem callback
    """

    INVALID = 'invalid'
    """Invalid flag type.

    This is a testing placeholder and should not be used. It is included
    to test error handling for unsupported flag types.
    """
