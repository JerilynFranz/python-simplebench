"""TestSpec testing framework - Pytest shim for TestSet attribute set tests.

This module provides a PytestSet class that serves as a bridge between
the TestSet class and the pytest testing framework. It allows for the
declarative specification of attribute-set tests while assigning unique
identifiers to each test case for Pytest.
"""

from collections.abc import Callable
from typing import Any, NoReturn

from .constants import NO_OBJ_ASSIGNED
from .idspec import idspec
from .test_set import TestSet


class PytestSet(TestSet):
    """A generic unit test specification class for pytest attribute-set tests.

    This is a thin wrapper around :class:`TestSet` that adds pytest-specific
    functionality, such as assigning unique ids to each test case.

    They are intended to be used with pytest's parameterized testing features.

    :param str ident: Id for the test.
    :param str name: Identifying name for the test.
    :param str attribute: The name of the attribute to be tested by setting.
    :param Any value: Value to set the attribute to.
    :param Optional[object] obj: The object whose attribute is to be tested. Defaults to NO_OBJ_ASSIGNED.
    :param Optional[type[BaseException]] exception: Expected exception type (if any) to be
        raised by setting the attribute.
    :param Optional[str | Enum] exception_tag: Expected tag (if any) to be found in the exception message.
    :param Optional[Callable[[TestSet, Any], None | NoReturn]] validate: Function to validate obj after
        setting attribute.
    :param Callable[[str], NoReturn] on_fail: Function to call on test failure.
    :param Any extra: Extra fields for use by test frameworks.
    """

    __test__ = False  # Prevent pytest from collecting this class as a test case

    def __new__(
        cls,
        ident: str,
        *,
        name: str = '',
        attribute: str = '',
        value: Any = None,
        obj: object | None = NO_OBJ_ASSIGNED,
        exception: type[BaseException] | None = None,
        exception_tag: str | None = None,
        validate: Callable[[TestSet, Any], None | NoReturn] | None = None,
        on_fail: Callable[[str], NoReturn] | None = None,
        extra: Any = None,
    ) -> Any:
        """Create a PytestSet test case with a unique id.

        :param str ident: Id for the test.
        :param str name: Identifying name for the test.
        :param str attribute: The name of the attribute to be tested by setting.
        :param Any value: Value to set the attribute to.
        :param Optional[object] obj: The object whose attribute is to be tested.
        :param Optional[type[BaseException]] exception: Expected exception type (if any).
        :param Optional[str | Enum] exception_tag: Expected tag (if any) in the exception message.
        :param Optional[Callable[[TestSet, Any], None | NoReturn]] validate: Function to validate obj after
            setting attribute.
        :param Callable[[str], NoReturn] on_fail: Function to call on test failure.
        :param Any extra: Extra fields for use by test frameworks.
        """
        return idspec(
            ident,
            TestSet(
                name=name,
                attribute=attribute,
                value=value,
                obj=obj,
                exception=exception,
                exception_tag=exception_tag,
                validate=validate,
                on_fail=on_fail,
                extra=extra,
            ),
        )

    def run(self) -> Any:
        """Run the test set action using pytest.

        :return: The result of the test set action.
        :rtype: Any
        """
        raise NotImplementedError(
            'PytestSet instances are not meant to be run directly. '
            'pytest will "unwrap" them and run the underlying TestSet instances.'
        )
