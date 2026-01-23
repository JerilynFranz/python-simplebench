"""TestSpec testing framework - assertion operators."""

# pylint: disable=too-many-return-statements
import logging
from enum import Enum
from typing import Any

log = logging.getLogger(__name__)


class Assert(str, Enum):
    """Enumeration of supported assertion operators.

    :cvar EQUAL: Checks if two values are equal.
    :vartype EQUAL: str
    :cvar NOT_EQUAL: Checks if two values are not equal.
    :vartype NOT_EQUAL: str
    :cvar LESS_THAN: Checks if one value is less than another.
    :vartype LESS_THAN: str
    :cvar LESS_THAN_OR_EQUAL: Checks if one value is less than or equal to another.
    :vartype LESS_THAN_OR_EQUAL: str
    :cvar GREATER_THAN: Checks if one value is greater than another.
    :vartype GREATER_THAN: str
    :cvar GREATER_THAN_OR_EQUAL: Checks if one value is greater than or equal to another.
    :vartype GREATER_THAN_OR_EQUAL: str
    :cvar IN: Checks if a value is contained within another (e.g., a list or set).
    :vartype IN: str
    :cvar NOT_IN: Checks if a value is not contained within another (e.g., a list or set).
    :vartype NOT_IN: str
    :cvar IS: Checks if two references point to the same object.
    :vartype IS: str
    :cvar IS_NOT: Checks if two references do not point to the same object.
    :vartype IS_NOT: str
    :cvar IS_NONE: Checks if a reference is None.
    :vartype IS_NONE: str
    :cvar IS_NOT_NONE: Checks if a reference is not None.
    :vartype IS_NOT_NONE: str
    :cvar ISINSTANCE: Checks if an object is an instance of a specified class or tuple of classes.
    :vartype ISINSTANCE: str
    :cvar ISSUBCLASS: Checks if a class is a subclass of another class.
    :vartype ISSUBCLASS: str
    :cvar str LEN: Checks the length of a collection against an expected value.
    """

    EQUAL = '=='
    NOT_EQUAL = '!='
    LESS_THAN = '<'
    LESS_THAN_OR_EQUAL = '<='
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUAL = '>='
    IN = 'in'
    NOT_IN = 'not in'
    IS = 'is'
    IS_NOT = 'is not'
    IS_NONE = 'is None'
    IS_NOT_NONE = 'is not None'
    ISINSTANCE = 'isinstance'
    ISSUBCLASS = 'issubclass'
    LEN = 'len'
    TRUE = 'true'
    FALSE = 'false'


def expected_argument_required(assertion: Assert) -> bool:
    """Check if the given assertion operator requires an expected argument.

    :param Assert assertion: The assertion operator to check.
    :return bool: True if the assertion operator requires an expected argument, False otherwise.
    """
    if assertion in (Assert.IS_NONE, Assert.IS_NOT_NONE, Assert.TRUE, Assert.FALSE):
        return False
    else:
        return True


def validate_assertion(assertion: Assert, expected: Any, found: Any) -> str:
    """Helper function to perform an assertion check.

    This function takes an assertion operator, an expected value, and a found value,
    and performs the specified assertion check. If the assertion fails, it returns
    an error message; otherwise, it returns an empty string.

    :param Assert assertion: The assertion operator to use.
    :param Any expected: The expected value.
    :param Any found: The found value.
    :return str: An error message if the assertion fails, otherwise an empty string.
    :raises ValueError: If an unsupported assertion operator is provided.
    """
    if assertion == Assert.EQUAL:
        if not found == expected:
            return f'Assert.EQUAL failed: found={found}, expected={expected}'
    elif assertion == Assert.NOT_EQUAL:
        if not found != expected:
            return f'Assert.NOT_EQUAL failed: found={found}, expected={expected}'
    elif assertion == Assert.LESS_THAN:
        if not found < expected:
            return f'Assert.LESS_THAN failed: found={found}, expected={expected}'
    elif assertion == Assert.LESS_THAN_OR_EQUAL:
        if not found <= expected:
            return f'Assert.LESS_THAN_OR_EQUAL failed: found={found}, expected={expected}'
    elif assertion == Assert.GREATER_THAN:
        if not found > expected:
            return f'Assert.GREATER_THAN failed: found={found}, expected={expected}'
    elif assertion == Assert.GREATER_THAN_OR_EQUAL:
        if not found >= expected:
            return f'Assert.GREATER_THAN_OR_EQUAL failed: found={found}, expected={expected}'
    elif assertion == Assert.IN:
        if not (expected in found):  # noqa: E713  # Keep for readability
            return f'Assert.IN failed: found={found}, expected={expected}'
    elif assertion == Assert.NOT_IN:
        if not (expected not in found):
            return f'Assert.NOT_IN failed: found={found}, expected={expected}'
    elif assertion == Assert.IS:
        if not (found is expected):  # noqa: E714  # Keep for readability
            return f'Assert.IS failed: found={found}, expected={expected}'
    elif assertion == Assert.IS_NOT:
        if not (found is not expected):
            return f'Assert.IS_NOT failed: found={found}, expected={expected}'
    elif assertion == Assert.ISINSTANCE:
        try:
            if not isinstance(found, expected):
                return f'Assert.ISINSTANCE failed: found={type(found)}, expected={expected}'
        except TypeError as exc:
            return f"Assert.ISINSTANCE failed: invalid expected type '{expected}': {exc}"
    elif assertion == Assert.ISSUBCLASS:
        try:
            if not issubclass(found, expected):
                return f'Assert.ISSUBCLASS failed: found={found}, expected={expected}'
        except TypeError as exc:
            return f"Assert.ISSUBCLASS failed: invalid expected type '{expected}': {exc}"
    elif assertion == Assert.IS_NONE:
        if found is not None:
            return f'Assert.IS_NONE failed: found={found}'
    elif assertion == Assert.IS_NOT_NONE:
        if found is None:
            return f'Assert.IS_NOT_NONE failed: found={found}'
    elif assertion == Assert.TRUE:
        if not found:
            return f'Assert.TRUE failed: found={found}'
    elif assertion == Assert.FALSE:
        if found:
            return f'Assert.FALSE failed: found={found}'
    elif assertion == Assert.LEN:
        if not len(found) == expected:
            return f'Assert.LEN failed: found={len(found)}, expected={expected}'
    else:
        return f"Unsupported assertion operator '{assertion}'"
    return ''
