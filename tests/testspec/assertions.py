"""TestSpec testing framework - assertion operators."""
from enum import Enum
from typing import Any


class Assert(str, Enum):
    """Enumeration of supported assertion operators.

    Supported operators include:
        - EQUAL ('=='): Checks if two values are equal.
        - NOT_EQUAL ('!='): Checks if two values are not equal.
        - LESS_THAN ('<'): Checks if one value is less than another.
        - LESS_THAN_OR_EQUAL ('<='): Checks if one value is less than or equal to another.
        - GREATER_THAN ('>'): Checks if one value is greater than another.
        - GREATER_THAN_OR_EQUAL ('>='): Checks if one value is greater than or equal to another.
        - IN ('in'): Checks if a value is contained within another (e.g., a list or set).
        - NOT_IN ('not in'): Checks if a value is not contained within another (e.g., a list or set).
        - IS ('is'): Checks if two references point to the same object.
        - IS_NOT ('is not'): Checks if two references do not point to the same object.
        - IS_NONE ('is None'): Checks if a reference is None.
        - IS_NOT_NONE ('is not None'): Checks if a reference is not None.
        - ISINSTANCE ('isinstance'): Checks if an object is an instance of a specified class or tuple of classes.
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


def validate_assertion(assertion: Assert, expected: Any, found: Any) -> str:
    """Helper function to perform an assertion check.

    This function takes an assertion operator, an expected value, and a found value,
    and performs the specified assertion check. If the assertion fails, it returns
    an error message; otherwise, it returns an empty string.

    Args:
        assertion (Assert): The assertion operator to use.
        expected (Any): The expected value.
        found (Any): The found value.
        on_fail (Callable[[str], None]): A callback function to call on failure. It should accept a single
            string argument containing the failure message and must not return (i.e., it should raise an exception).

    Returns:
        str: An error message if the assertion fails, otherwise an empty string.

    Raises:
        ValueError: If an unsupported assertion operator is provided.
    """
    match assertion:
        case Assert.EQUAL:
            if not found == expected:
                return f"assertion failed: (found={found}) == (expected={expected})"
        case Assert.NOT_EQUAL:
            if not found != expected:
                return f"assertion failed: (found={found}) != (expected={expected})"
        case Assert.LESS_THAN:
            if not found < expected:
                return f"assertion failed: (found={found}) < (expected={expected})"
        case Assert.LESS_THAN_OR_EQUAL:
            if not found <= expected:
                return f"assertion failed: (found={found}) <= (expected={expected})"
        case Assert.GREATER_THAN:
            if not found > expected:
                return f"assertion failed: (found={found}) > (expected={expected})"
        case Assert.GREATER_THAN_OR_EQUAL:
            if not found >= expected:
                return f"assertion failed: (found={found}) >= (expected={expected})"
        case Assert.IN:
            if not (found in expected):  # pylint: disable=superfluous-parens  # for clarity
                return f"assertion failed: (found={found}) in (expected={expected})"
        case Assert.NOT_IN:
            if not (found not in expected):  # pylint: disable=superfluous-parens  # for clarity
                return f"assertion failed: (found={found}) not in (expected={expected})"
        case Assert.IS:
            if not (found is expected):  # pylint: disable=superfluous-parens  # for clarity
                return f"assertion failed: (found={found}) is (expected={expected})"
        case Assert.IS_NOT:
            if not (found is not expected):  # pylint: disable=superfluous-parens  # for clarity
                return f"assertion failed: (found={found}) is not (expected={expected})"
        case Assert.ISINSTANCE:
            if not isinstance(found, expected):
                return f"assertion failed: (found={type(found)}) isinstance (expected={expected})"
        case Assert.IS_NONE:
            if found is not None:
                return f"assertion failed: (found={found}) is None"
        case Assert.IS_NOT_NONE:
            if found is None:
                return f"assertion failed: (found={found}) is not None"
        case _:
            return f"Unsupported assertion operator '{assertion}'"
    return ""
