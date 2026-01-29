"""TestSpec testing framework - Pytest shim for TestGet attribute tests.

This module provides a PytestGet class that serves as a bridge between
the TestGet class and the pytest testing framework. It allows for the
declarative specification of attribute-get tests while assigning unique
identifiers to each test case for Pytest.
"""

from collections.abc import Callable
from typing import Any, NoReturn

from .assertions import Assert
from .base import TestSpec
from .constants import NO_EXPECTED_VALUE, NO_OBJ_ASSIGNED
from .idspec import idspec
from .test_get import TestGet


class PytestGet(TestSpec):
    """A generic unit test specification class for pytest attribute-get tests.

    This is a thin wrapper around :class:`TestGet` that adds pytest-specific
    functionality, such as assigning unique ids to each test case.

    They are intended to be used with pytest's parameterized testing features.

    :param str ident: Id for the test.
    :param str name: Identifying name for the test.
    :param str attribute: The name of the attribute to be tested by getting.
    :param Optional[object] obj: The object whose attribute is to be tested. Defaults to NO_OBJ_ASSIGNED.
    :param Optional[Assert] assertion: The assertion operator to use when comparing the expected and
        found values.
    :param Any expected: Expected value of attribute after getting. If a get_exception is set,
        the expected value is ignored.
    :param Optional[type[BaseException]] exception: Expected exception type (if any) to be raised
        by getting the attribute.
    :param Optional[str | Enum] exception_tag: Expected tag (if any) to be found in the exception message.
    :param Optional[Callable[[TestGet, Any], None | NoReturn]] validate: Function to validate obj
        after getting attribute.
    :param str | Callable[[], str] display_on_fail: Message to display on test failure.
    :param Optional[Callable[[str], NoReturn]] on_fail: Function to call on test failure.
    :param Any extra: Extra fields for use by test frameworks.
    """

    __test__ = False  # Prevent pytest from collecting this class as a test case

    def __new__(
        cls,
        ident: str,
        *,
        name: str = '',
        attribute: str = '',
        obj: object | None = NO_OBJ_ASSIGNED,
        assertion: Assert = Assert.EQUAL,
        expected: Any = NO_EXPECTED_VALUE,
        exception: type[BaseException] | None = None,
        exception_tag: str | None = None,
        validate: Callable[[TestGet, Any], None | NoReturn] | None = None,
        display_on_fail: str | Callable[[], str] = '',
        on_fail: Callable[[str], NoReturn] | None = None,
        extra: Any = None,
    ) -> Any:
        """Create a PytestGet test case with a unique id.

        :param str ident: Id for the test.
        :param str name: Identifying name for the test.
        :param str attribute: The name of the attribute to be tested by getting.
        :param Optional[object] obj: The object whose attribute is to be tested.
        :param Optional[Assert] assertion: The assertion operator to use.
        :param Any expected: Expected value of attribute after getting.
        :param Optional[type[BaseException]] exception: Expected exception type (if any).
        :param Optional[str | Enum] exception_tag: Expected tag (if any) in the exception message.
        :param Optional[Callable[[TestGet, Any], None | NoReturn]] validate: Function to validate obj
            after getting attribute.
        :param str | Callable[[], str] display_on_fail: Message to display on test failure.
        :param Optional[Callable[[str], NoReturn]] on_fail: Function to call on test failure.
        :param Any extra: Extra fields for use by test frameworks.
        """
        return idspec(
            ident,
            TestGet(
                name=name,
                attribute=attribute,
                obj=obj,
                assertion=assertion,
                expected=expected,
                exception=exception,
                exception_tag=exception_tag,
                validate=validate,
                display_on_fail=display_on_fail,
                on_fail=on_fail,
                extra=extra,
            ),
        )

    def run(self) -> Any:
        """Run the test get action using pytest.

        :return: The result of the test get action.
        :rtype: Any
        """
        raise NotImplementedError(
            'PytestGet instances are not meant to be run directly. '
            'pytest will "unwrap" them and run the underlying TestGet instances.'
        )
