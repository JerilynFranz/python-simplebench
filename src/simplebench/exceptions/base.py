"""Base class for error tag enums."""
from enum import Enum


class ErrorTag(str, Enum):
    """Base class for error tag enums.

    ErrorTags are used to identify specific error condition sources in the simplebench package.

    Tests use these tags to assert specific error condition paths.
    """
