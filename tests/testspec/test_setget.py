"""TestSpec framework - TestSetGet class"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import TracebackType
from typing import Any, Callable, NoReturn, Optional

from .assertions import Assert, validate_assertion
from .base import TestSpec
from .constants import NO_EXPECTED_VALUE, NO_OBJ_ASSIGNED
from .deferred import _resolve_deferred_value
from .helpers import _process_exception


@dataclass
class TestSetGet(TestSpec):
    """A class for testing setting and getting attributes.

    This class allows for testing the setting and getting of attributes on an object,
    including validation of the set value, expected exceptions, and custom validation functions.

    :param name: Identifying name for the test.
    :type name: str
    :param obj: The object whose attribute is to be tested. If not provided, the special sentinel value
                NO_OBJ_ASSIGNED is used. The object must not be None and must be an instance of object.
                It must be provided to run the test.
                Defaults to NO_OBJ_ASSIGNED.
    :type obj: Optional[object], optional
    :param attribute: The name of the attribute to be tested by setting.
    :type attribute: str
    :param value: Value to set the attribute to.
    :type value: Any
    :param expected: Expected value of attribute after setting the attribute. If a get_exception or
                     set_exception is set, the expected value is ignored. If there is no expected exception
                     and no expected value, use the special sentinel value NO_EXPECTED_VALUE to skip the
                     get step validation for the set value.
                     Defaults to NO_EXPECTED_VALUE.
    :type expected: Optional[Any], optional
    :param get_attribute: The name of the attribute to be retrieved for 'expected' validation.
                          If None, use the same as `attribute`.
                          Defaults to None.
    :type get_attribute: Optional[str], optional
    :param assertion: The assertion operator to use when comparing the expected and found values.
                      Defaults to Assert.EQUAL.
    :type assertion: Assert, optional
    :param exception: Expected exception type (if any) to be raised by setting the attribute.
                      Defaults to None.
    :type exception: Optional[type[Exception]], optional
    :param exception_tag: Expected tag (if any) to be found in the exception message.
                          Defaults to None.
    :type exception_tag: Optional[str | Enum], optional
    :param validate: Function to validate obj after setting the attribute.
                     It should return True if the object state is valid.
                     This is distinguished from the expected value check in that it can perform more complex validation
                     of the entire object state rather than just checking the value of a single attribute.
                     It is passed two arguments, the TestSetGet instance and the object being validated.
                     Defaults to None.
    :type validate: Optional[Callable[[TestSetGet, Any], bool]], optional
    :param on_fail: Function to call on test failure to raise an exception.
                    Defaults to pytest.fail.
    :type on_fail: Callable[[str], NoReturn], optional
    :param extra: Extra fields for use by test frameworks. It is not used by the TestSetGet class itself.
                  Defaults to None.
    :type extra: Any, optional
    """
    __test__ = False  # Prevent pytest from trying to collect this class as a test case

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
    assertion: Assert = Assert.EQUAL
    """The assertion operator to use when comparing the expected and found values. (default is Assert.EQUAL)"""
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
    if the object state is unexpected.

    This is distinguished from the expected value check in that it can perform more complex validation
    of the entire object state rather than just checking the value of a single attribute.

    It is passed two arguments, the TestSetGet instance and the object being validated.

    The validation function should call the `on_fail` method to raise an exception if the object is not
    in a valid state. None should be returned if the object is valid.
    """
    on_fail: Callable[[str], NoReturn] | None = None
    """Function to call on test failure. The function should raise an exception (default is _fail method)."""

    extra: Any = None
    """Extra data for use by test frameworks. It is not used by the TestSetGet class itself. Default is None."""

    _creation_traceback: Optional[TracebackType] = None
    """The traceback at the point where the TestAction was created."""

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
        super().__post_init__()

    def run(self) -> None:
        """Execute the attribute set/get test."""
        # disabled because we are using the __setattr__ and __getattribute__ dunder methods directly
        # for testing purposes because there is no other way to do get/set testing for attributes generically.
        # pylint: disable=unnecessary-dunder-call

        # hide traceback for this function in pytest output. Disabled for pylint because it is a pytest
        # feature that is just not understood by pylint.
        __tracebackhide__ = True  # pylint: disable=unused-variable

        test_description: str = f"{self.name}"

        # Errors found during the test
        errors: list[str] = []

        obj = _resolve_deferred_value(self.obj)
        if obj is NO_OBJ_ASSIGNED:
            if self.on_fail:
                self.on_fail(f"{self.name}: obj for test is not assigned")
            else:
                self._fail(f"{self.name}: obj for test is not assigned")
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from

        # Resolve any deferred values for obj
        expected = _resolve_deferred_value(self.expected)
        validate = _resolve_deferred_value(self.validate)

        # Set the attribute and check for exceptions as appropriate
        try:
            if not hasattr(obj, self.attribute):
                errors.append(f"obj has no attribute {self.attribute}")
            else:
                obj.__setattr__(self.attribute, self.value)
                if self.set_exception is not None:
                    errors.append("set operation returned instead of raising an expected exception")

        except BaseException as err:  # pylint: disable=broad-exception-caught
            new_errors = _process_exception(
                err=err,
                exception=self.set_exception,
                exception_tag=self.set_exception_tag,
                label=f"setting attribute {self.attribute}"
            )
            errors.extend(new_errors)

        # bail now if there was an error during the set operation
        if errors:
            if self.on_fail:
                self.on_fail(test_description + ": " + "\n".join(errors))
            else:
                self._fail(test_description + ": " + "\n".join(errors))
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from

        # If there is no get_exception or expected value or validate function, we can't do any validation
        # on the set value, so just return now. This amounts to a minimal test of just setting the attribute
        # it causing an exception.
        if (self.get_exception is None and
                expected is NO_EXPECTED_VALUE and
                validate is None):
            return

        # Perform post-set validations if requested. This is skipped if there was an exception
        # during the set operation.
        attribute_to_get = self.attribute if self.get_attribute is None else self.get_attribute
        try:
            if not hasattr(obj, attribute_to_get):
                errors.append(f"obj has no attribute {attribute_to_get}")
            else:
                if validate is not None:
                    validate(self, obj)  # Exception should be raised by validate if unexpected obj state

                if expected is NO_EXPECTED_VALUE:
                    return

                found: Any = obj.__getattribute__(attribute_to_get)
                assertion_error = validate_assertion(self.assertion, expected, found)
                if assertion_error:
                    errors.append(
                        f"{assertion_error} for attribute '{attribute_to_get}'")

        except BaseException as err:  # pylint: disable=broad-exception-caught
            new_errors = _process_exception(
                err=err,
                exception=self.get_exception,
                exception_tag=self.get_exception_tag,
                label=f"getting attribute {attribute_to_get}"
            )
            errors.extend(new_errors)

        # Report any errors found during the validate portion of the test
        if errors:
            if self.on_fail:
                self.on_fail(test_description + ": " + "\n".join(errors))
            else:
                self._fail(test_description + ": " + "\n".join(errors))
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from
