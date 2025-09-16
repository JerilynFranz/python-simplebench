"""TestSpec testing framework."""
from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import traceback
from typing import Any, Optional, Sequence, NoReturn

import pytest

# Sentinel value used to indicate that no expected value is set
NO_EXPECTED_VALUE = object()
"""A sentinel value used to indicate that no expected value is set."""
NO_OBJ_ASSIGNED = object()
"""A sentinel object used to indicate that no obj has been assigned."""


def no_assigned_action(*args: Any, **kwargs: Any) -> Any:
    """A placeholder function that raises a NotImplementedError when called.

    This function serves as a sentinel value to indicate that no action has been assigned.
    It can be used in scenarios where a callable is expected, but no specific implementation
    is provided during initialization.

    Args:
        *args: Positional arguments (not used).
        **kwargs: Keyword arguments (not used).

    Raises:
        NotImplementedError: Always raised to indicate that no action is assigned.
    """
    raise NotImplementedError("No action assigned for this test.")


def idspec(id_base: str, testspec: TestAction | TestSetGet) -> Any:
    """Helper function to create a test case with a specific pytest id directly from a TestAction or TestProperty.

    This function generates a pytest parameter with a custom id based on the provided base
    string and the name of the TestAction or TestProperty instance. It is useful for organizing
    and identifying test cases in a clear and descriptive manner.

    Because the pytest ParameterSet class definition is hidden from the public API,
    we cannot use it directly in type annotations.

    Args:
        id_base (str): The base string to use for the test case id.
        testspec (TestAction | TestProperty): The TestAction or TestProperty instance containing the test configuration.
    Returns:
        A pytest parameter with a custom id.
    Raises:
        TypeError: If testspec is not an instance of TestAction or TestProperty or id_base is not a str.
    """
    if not isinstance(testspec, (TestAction, TestSetGet)):
        raise TypeError("testspec must be an instance of TestAction or TestProperty")
    if not isinstance(id_base, str):
        raise TypeError("id_base must be a str")
    return pytest.param(testspec, id=f"{id_base} {testspec.name}")


class TestSpec():
    """Base class for test specifications."""

    def run(self) -> None:
        """Run the test based on the provided TestSpec entry.

        This function is intended to be overridden by subclasses to implement
        specific test execution logic.
        """
        raise NotImplementedError("Subclasses must implement the run method.")


@dataclass
class TestSetGet(TestSpec):
    """A class for testing setting and getting attributes.

    This class allows for testing the setting and getting of attributes on an object,
    including validation of the set value, expected exceptions, and custom validation functions.

    Args:
        name (str):
            Identifying name for the test.
        obj (Optional[object], default=NO_OBJ_ASSIGNED):
            The object whose attribute is to be tested. If not provided, the special sentinel value
            NO_OBJ_ASSIGNED is used. The object must not be None and must be an instance of object.
            It must be provided to run the test.
        attribute (str):
            The name of the attribute to be tested by setting.
        value (Any):
            Value to set the attribute to.
        expected Optional(Any):
            Expected value of attribute after setting the attribute. If a get_exception or
            set_exception is set, the expected value is ignored. If there is no expected exception
            and no expected value, use the special sentinel value NO_EXPECTED_VALUE to skip the
            get step validation for the set value.
        get_attribute (Optional[str], default=None):
            The name of the attribute to be retrieved for 'expected' validation. If None, use the same as `attribute`.
        exception (Optional[type[Exception]], default=None):
            Expected exception type (if any) to be raised by setting the attribute.
        exception_tag (Optional[str | Enum], default=None):
            Expected tag (if any) to be found in the exception message.
        validate (Optional[Callable[[TestSetGet, Any], bool]], default=None):
            Function to validate obj after setting the attribute. It should return True if the object state is valid.

            This is distinguished from the expected value check in that it can perform more complex validation
            of the entire object state rather than just checking the value of a single attribute.

            It is passed two arguments, the TestSetGet instance and the object being validated.
        on_fail (Callable[[str], NoReturn], default=pytest.fail):
            Function to call on test failure to raise an exception
    """
    name: str
    """Identifying name for the test."""
    attribute: str
    """The name of the attribute to be tested by setting."""
    value: Any
    """Value to set the attribute to."""
    obj: Optional[object] = NO_OBJ_ASSIGNED
    """The object whose attribute is to be tested. It cannot be None, and must be an instance of object.
    If not provided during construction, the special sentinel value NO_OBJ_ASSIGNED is used. This must be
    replaced with a valid object before running the test."""
    expected: Optional[Any] = NO_EXPECTED_VALUE
    """Expected value of attribute after setting the attribute. If a get_exception or
    set_exception is set, the expected value is ignored. If there is no expected exception
    and no expected value, use the special sentinel value NO_EXPECTED_VALUE to skip the
    get step validation for the set value. Omitting this field is equivalent to setting it to NO_EXPECTED_VALUE."""
    get_attribute: Optional[str] = None
    """The name of the attribute to be retrieved for 'expected' validation. If None, use the same as `attribute`."""
    set_exception: Optional[type[Exception]] = None
    """Expected exception type (if any) to be raised by setting the attribute."""
    set_exception_tag: Optional[str | Enum] = None
    """Expected tag (if any) to be found in an exception message raised by setting the attribute."""
    get_exception: Optional[type[Exception]] = None
    """Expected exception type (if any) to be raised by getting the attribute."""
    get_exception_tag: Optional[str | Enum] = None
    """Expected tag (if any) to be found in an exception message raised by getting the attribute."""
    validate: Optional[Callable[[TestSetGet, Any], None | NoReturn]] = None
    """Function to validate obj state after setting the attribute. It should raise an exception
    if the object state is invalid.

    This is distinguished from the expected value check in that it can perform more complex validation
    of the entire object state rather than just checking the value of a single attribute.

    It is passed two arguments, the TestSetGet instance and the object being validated.

    The validation function should call the `on_fail` method to raise an exception if the object is not
    in a valid state. None should be returned if the object is valid.
    """
    on_fail: Callable[[str], NoReturn] = pytest.fail
    """Function to call on test failure. The function should raise an exception (default is pytest.fail)."""

    def __post_init__(self) -> None:
        """Post-initialization validation checks."""
        if not isinstance(self.name, str):
            raise TypeError("name must be a str")
        if not isinstance(self.attribute, str):
            raise TypeError("attribute must be a str")
        if self.obj is None:
            raise TypeError("obj cannot be None")
        if not isinstance(self.obj, object):
            raise TypeError("obj must be an object")
        if self.attribute == "":
            raise ValueError("attribute cannot be an empty string")
        if self.validate is not None and not callable(self.validate):
            raise TypeError("validate must be callable if provided")
        if self.set_exception is not None and not issubclass(self.set_exception, Exception):
            raise TypeError("set_exception must be an Exception type if provided")
        if self.set_exception_tag is not None and not isinstance(self.set_exception_tag, (str, Enum)):
            raise TypeError("set_exception_tag must be a str or Enum if provided")
        if not callable(self.on_fail):
            raise TypeError("on_fail must be callable")

    def run(self) -> None:
        """Execute the attribute set/get test."""
        # disabled because we are using the __setattr__ and __getattribute__ dunder methods directly
        # for testing purposes because there is no other way to do get/set testing for attributes generically.
        # pylint: disable=unnecessary-dunder-call

        # hide traceback for this function in pytest output. Disabled for pylint because it is a pytest
        # feature that is just not understood by pylint.
        __tracebackhide__ = True  # pylint: disable=unused-variable

        # Errors found during the test
        errors: list[str] = []

        if self.obj is NO_OBJ_ASSIGNED:
            self.on_fail(f"{self.name}: obj for test is not assigned")
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from
        # Set the attribute and check for exceptions as appropriate
        try:
            self.obj.__setattr__(self.attribute, self.value)
            if self.set_exception is not None:
                errors.append("set operation returned instead of raising an expected exception")

        except Exception as err:  # pylint: disable=broad-exception-caught
            if self.set_exception is None:
                errors.append(f'Unexpected Exception raised while setting attribute {self.attribute}: {repr(err)}')
            elif not isinstance(err, self.set_exception):
                errors.append(f'Unexpected exception type: expected={self.set_exception}, found = {type(err)}')
            elif self.set_exception_tag:
                # Case 1: The expected tag is an Enum member.
                # This requires the exception object to have a 'tag_code' attribute.
                if isinstance(self.set_exception_tag, Enum):
                    if not hasattr(err, 'tag_code'):
                        errors.append(
                            f"Exception {type(err)} is missing the 'tag_code' attribute "
                            "required for Enum tag validation.")
                    else:
                        actual_tag = getattr(err, 'tag_code')
                        if actual_tag != self.set_exception_tag:
                            errors.append(f"Unexpected exception tag: expected={self.set_exception_tag}, "
                                          f"found={actual_tag}")
                # Case 2: The expected tag is a string.
                # This performs a substring search in the exception's string representation.
                else:
                    if str(self.set_exception_tag) not in str(err):
                        errors.append(
                            f"Correct exception type, but tag '{self.set_exception_tag}' "
                            f"not found in exception message: {repr(err)}"
                        )
        # bail now if there was an error during the set operation
        if errors:
            self.on_fail(self.name + ": " + "\n".join(errors))
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from

        # If there is no get_exception or expected value or validate function, we can't do any validation
        # on the set value, so just return now. This amounts to a minimal test of just setting the attribute
        # it causing an exception.
        if (self.get_exception is None and
                self.expected is NO_EXPECTED_VALUE and
                self.validate is None):
            return

        # Perform post-set validations if requested. This is skipped if there was an exception
        # during the set operation.
        attribute_to_get = self.attribute if self.get_attribute is None else self.get_attribute
        try:
            if self.validate is not None:
                self.validate(self, self.obj)  # Exception should be raised by validate if invalid obj state

            if self.expected is NO_EXPECTED_VALUE:
                return

            found: Any = self.obj.__getattribute__(attribute_to_get)
            if self.expected != found:
                errors.append(
                    f"expected={self.expected}, found={found} for attribute '{attribute_to_get}'")

        except Exception as err:  # pylint: disable=broad-exception-caught
            if self.get_exception is None:
                errors.append(f'Unexpected Exception raised while validating attribute value: {repr(err)}')
            elif not isinstance(err, self.get_exception):
                errors.append(
                    f'Unexpected exception type while validating attribute value: '
                    f'expected={self.get_exception}, found = {type(err)}')
            elif self.get_exception_tag:
                # Case 1: The expected tag is an Enum member.
                # This requires the exception object to have a 'tag_code' attribute.
                if isinstance(self.get_exception_tag, Enum):
                    if not hasattr(err, 'tag_code'):
                        errors.append(
                            f"Exception {type(err)} is missing the 'tag_code' attribute "
                            "required for Enum tag validation.")
                    else:
                        actual_tag = getattr(err, 'tag_code')
                        if actual_tag != self.get_exception_tag:
                            errors.append(f"Unexpected exception tag: expected={self.get_exception_tag}, "
                                          f"found={actual_tag}")
                # Case 2: The expected tag is a string.
                # This performs a substring search in the exception's string representation.
                else:
                    if str(self.get_exception_tag) not in str(err):
                        errors.append(
                            f"Correct exception type, but tag '{self.get_exception_tag}' "
                            f"not found in exception message: {repr(err)}"
                        )

        # Report any errors found during the get portion of the test
        if errors:
            self.on_fail(self.name + ": " + "\n".join(errors))
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from


@dataclass
class TestAction(TestSpec):
    """A generic unit test specification class.

    It allow tests to be specified declaratively while providing a large amount
    of flexibility.

    Args:
        name (str):
            Identifying name for the test.
        action (Callable[..., Any], default = no_assigned_action):
            A reference to a callable function or method to be invoked for the test. If no
            action is assigned, the special function `no_assigned_action` is used which
            raises NotImplementedError when called.
        args (Sequence[Any], default = []):
            Sequence of positional arguments to be passed to the `action` function or method.
        kwargs (dict[str, Any], default = {}):
            Dictionary containing keyword arguments to be passed to the `action` function or method.
        expected (Any, default=NO_EXPECTED_VALUE ):
            Expected value (if any) that is expected to be returned by the `action` function or method.
            If there is no expected value, the special class NoExpectedValue is used to flag it.
            This is used so that the specific return value of None can be distinguished from no
            particular value or any value at all is expected to be returned from the function or method.
        obj: Optional[Any] = None
        validate_obj: Optional[Callable[[Any], bool]] = None
        validate_result: Optional[Callable[[Any], bool]] = None
        exception: Optional[type[Exception]] = None
        exception_tag: Optional[str] = None
        on_fail: Callable[[str], NoReturn] = pytest.fail
            Function to call on test failure. (default is pytest.fail)
    """
    name: str
    """Identifying name for the test."""
    action: Callable[..., Any] = no_assigned_action
    """A reference to a callable function or method to be invoked for the test."""
    args: Optional[list[Any]] = None
    """Sequence of positional arguments to be passed to the `action` function or method."""
    kwargs: Optional[dict[str, Any]] = None
    """Dictionary containing keyword arguments to be passed to the `action` function or method."""
    expected: Any = NO_EXPECTED_VALUE
    """Expected value (if any) that is expected to be returned by the `action` function or method."""
    obj: Optional[Any] = None
    """Optional object to be validated."""
    validate_obj: Optional[Callable[[Any], bool]] = None
    """Function to validate the optional object."""
    validate_result: Optional[Callable[[Any], bool]] = None
    """Function to validate the result of the action."""
    exception: Optional[type[Exception]] = None
    """Expected exception type (if any) to be raised by the action."""
    exception_tag: Optional[str | Enum] = None
    """Expected tag (if any) to be found in the exception message."""
    display_on_fail: str | Callable[[], str] = ""
    """String or function to display additional information on test failure."""
    on_fail: Callable[[str], NoReturn] = pytest.fail
    """Function to call on test failure. (default is pytest.fail)

    The function must accept a single string argument containing the failure message
    and must not return (i.e., it should raise an exception or terminate the test).
    """

    def run(self) -> None:  # pylint: disable=too-many-branches
        """Run the test based on the provided TestSpec entry.

        This function executes the action specified in the entry, checks the result against
        the expected value, and reports any errors.

        Args:
            self (TestSpec): The test configuration entry containing all necessary information for the test.
        """
        # hide traceback for this function in pytest output
        __tracebackhide__ = True  # pylint: disable=unused-variable
        test_description: str = f"{self.name}"
        errors: list[str] = []
        try:
            # Use empty list/dict if the self field is None
            pos_args = self.args if self.args is not None else []
            kw_args = self.kwargs if self.kwargs is not None else {}
            found: Any = self.action(*pos_args, **kw_args)
            if self.exception:
                errors.append("returned result instead of raising exception")

            else:
                if self.validate_result and not self.validate_result(found):
                    errors.append(f"failed result validation: found={found}")
                if self.validate_obj and not self.validate_obj(self.obj):
                    errors.append(f"failed object validation: obj={self.obj}")
                if self.expected is not NO_EXPECTED_VALUE and self.expected != found:
                    errors.append(f"expected={self.expected}, found={found}")
                    if callable(self.display_on_fail):
                        errors.append(self.display_on_fail())
                    elif isinstance(self.display_on_fail, str):
                        errors.append(self.display_on_fail)
        except Exception as err:  # pylint: disable=broad-exception-caught
            if self.exception is None:
                errors.append(f"Did not expect exception. Caught exception {repr(err)}")
                errors.append("stacktrace = ")
                errors.append("\n".join(traceback.format_tb(tb=err.__traceback__)))

            elif not isinstance(err, self.exception):
                errors.append(
                    f"Unexpected exception type: expected={self.exception}, "
                    f"found = {type(err)}"
                )
            elif self.exception_tag:
                # Case 1: The expected tag is an Enum member.
                # This requires the exception object to have a 'tag_code' attribute.
                if isinstance(self.exception_tag, Enum):
                    if not hasattr(err, 'tag_code'):
                        errors.append(
                            "Exception is missing the 'tag_code' attribute required for Enum tag validation.")
                    else:
                        actual_tag = getattr(err, 'tag_code')
                        if actual_tag != self.exception_tag:
                            errors.append(f"Unexpected exception tag: expected={self.exception_tag}, "
                                          f"found={actual_tag}")
                # Case 2: The expected tag is a string.
                # This performs a substring search in the exception's string representation.
                else:
                    if str(self.exception_tag) not in str(err):
                        errors.append(
                            f"Correct exception type, but tag '{self.exception_tag}' "
                            f"not found in exception message: {repr(err)}"
                        )
        if errors:
            self.on_fail(test_description + ": " + "\n".join(errors))


def run_tests_list(test_specs: Sequence[TestSpec]) -> None:
    """Run a list of tests based on the provided TestSpec subclasses.

    This function iterates over the list of entries and runs each test using
    the `run` function. It allows for a clean and organized way to execute multiple tests.

    Args:
        test_specs (Sequence[TestSpec]): A list of TestSpec subclasses, each representing a test to be run.
    """
    for spec in test_specs:
        spec.run()
