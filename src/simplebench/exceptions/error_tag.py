"""Base class for error tag enums."""

from enum import Enum

__all__: list[str] = []


class ErrorTag(str, Enum):
    """Base class for error tag enums.

    ErrorTags are used to identify specific error condition sources in the simplebench package.

    Tests use these tags to assert specific error condition paths at a much more granular level than
    just checking the exception type or message.

    By inheriting from both str and Enum, ErrorTag members are both enumerated constants and also
    behave like strings. This allows them to be used as unique identifiers for error conditions while
    also being easily comparable and usable in string contexts (e.g., as dictionary keys or in error messages).

    Each specific error tag enum (e.g., _MetricsErrorTag) will inherit from this base class and define its own set of
    error tags relevant to its context (e.g., Metrics-related errors).

    The _generate_next_value_ method is overridden to return the name of the member as its value, which
    allows for more readable and meaningful enum member values.
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> str:
        """Generate the next value for the enum member.

        This method is overridden to return the name of the member as its value, which
        allows for more readable and meaningful enum member values.
        :param name: The name of the enum member.
        :type name: str
        :param start: The initial value (not used in this implementation).
        :type start: int
        :param count: The number of existing members (not used in this implementation).
        :type count: int
        :param last_values: The list of existing member values (not used in this implementation).
        :type last_values: list
        :return: The name of the enum member as its value.
        :rtype: str
         """
        return name
