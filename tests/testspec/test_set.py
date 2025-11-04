"""TestSpec framework - TestSet class."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, NoReturn, Optional

import pytest

from .base import TestSpec
from .constants import NO_OBJ_ASSIGNED
from .deferred import Deferred, _resolve_deferred_value
from .helpers import _process_exception


@dataclass
class TestSet(TestSpec):
    """A class for testing setting attributes.

    This class allows for testing the setting of attributes on an object. It does not
    perform any validation of the set value, but it can check for expected exceptions
    during the set operation and can call a custom validation function after setting
    the attribute.

    Args:
        name (str):
            Identifying name for the test.
        obj (Optional[object] | Deferred, default=NO_OBJ_ASSIGNED):
            The object whose attribute is to be tested. If not provided, the special sentinel value
            NO_OBJ_ASSIGNED is used. The object must not be None and must be an instance of object.
            It must be provided to run the test.
        attribute (str):
            The name of the attribute to be tested by setting.
        value (Any):
            Value to set the attribute to.
        exception (Optional[type[Exception]], default=None):
            Expected exception type (if any) to be raised by setting the attribute.
        exception_tag (Optional[str | Enum], default=None):
            Expected tag (if any) to be found in the exception message.
        validate (Optional[Callable[[TestSet, Any], bool] | Deferred], default=None):
            Function to validate obj after setting the attribute. It should return True if the object state is valid.

            This provides a way to perform post-set validation of the entire object state.

            It is passed two arguments, the TestSet instance and the object being validated.
        on_fail (Callable[[str], NoReturn], default=pytest.fail):
            Function to call on test failure to raise an exception
        extra (Any):
            Extra fields for use by test frameworks. It is not used by the TestSet class itself.
            Default is None.
    """
    __test__ = False  # Prevent pytest from trying to collect this class as a test case

    name: str
    """Identifying name for the test."""
    attribute: str
    """The name of the attribute to be tested by setting."""
    value: Any
    """Value to set the attribute to."""
    obj: Optional[object] = NO_OBJ_ASSIGNED
    """The object whose attribute is to be tested.

    It cannot be None, and must be an instance of object. If not provided during construction,
    the special sentinel value NO_OBJ_ASSIGNED is used. This must be replaced with a valid object
    before running the test."""
    exception: Optional[type[BaseException]] = None
    """Expected exception type (if any) to be raised by setting the attribute."""
    exception_tag: Optional[str | Enum] = None
    """Expected tag (if any) to be found in an exception message raised by setting the attribute."""
    validate: Optional[Callable[[TestSet, Any], None | NoReturn] | Deferred] = None
    """Function to validate obj state after setting the attribute. It should raise an exception
    if the object state is unexpected.

    It is passed two arguments, the TestSet instance and the object being validated.

    The validation function should call the `on_fail` method to raise an exception if the object is not
    in an expected state. None should be returned if the object state is as expected.
    """
    on_fail: Callable[[str], NoReturn] = pytest.fail
    """Function to call on test failure. The function should raise an exception (default is pytest.fail)."""
    extra: Any = None
    """Extra data for use by test frameworks. It is not used by the TestSet class itself. Default is None."""

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
        if self.exception is not None and not issubclass(self.exception, Exception):
            raise TypeError("exception must be an Exception type if provided")
        if self.exception_tag is not None and not isinstance(self.exception_tag, (str, Enum)):
            raise TypeError("exception_tag must be a str or Enum if provided")
        if not callable(self.on_fail):
            raise TypeError("on_fail must be callable")

    def run(self) -> None:
        """Execute the attribute set test.

        A failure during the set operation is defined as:
        - An unexpected exception is raised during the set operation.
        - An expected exception is not raised during the set operation.
        - An expected exception is raised, but the exception type does not match the expected type.
        - An expected exception is raised, but the exception tag does not match the expected tag.
        - The validate function raises an exception indicating the object is not in a valid state.

        Raises:
            pytest Fail: If the test fails.
            RuntimeError: If the obj attribute is not assigned to a valid object.
            RuntimeError: If the test fails and the on_fail function does not raise an exception.
        """
        # disabled because we are using the __setattr__ dunder method directly
        # for testing purposes because there is no other way to set testing for
        # attributes generically.
        # pylint: disable=unnecessary-dunder-call

        # hide traceback for this function in pytest output. Disabled for pylint because it is a pytest
        # feature that is just not understood by pylint.
        __tracebackhide__ = True  # pylint: disable=unused-variable

        # Errors found during the test
        errors: list[str] = []

        obj = _resolve_deferred_value(self.obj)
        if obj is NO_OBJ_ASSIGNED:
            self.on_fail(f"{self.name}: obj for test is not assigned")
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from
        # Set the attribute and check for exceptions as appropriate
        validate = _resolve_deferred_value(self.validate)
        if validate is not None and not callable(validate):
            raise TypeError("validate must be callable if provided")
        try:
            if not hasattr(obj, self.attribute):
                errors.append(f"obj has no attribute {self.attribute}")
            else:
                obj.__setattr__(self.attribute, self.value)
                if self.exception is not None:
                    errors.append("set operation returned instead of raising an expected exception")

        except BaseException as err:  # pylint: disable=broad-exception-caught
            new_errors = _process_exception(
                err=err,
                exception=self.exception,
                exception_tag=self.exception_tag,
                label=f"setting attribute {self.attribute}")
            errors.extend(new_errors)

        # bail now if there was an error during the set operation
        if errors:
            self.on_fail(self.name + ": " + "\n".join(errors))
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from

        # If there is no validate function, we can't do any validation on the set value, so just return.
        # This amounts to a minimal test of just setting the attribute it causes a specified exception or
        # not causing an exception.
        if validate is None:
            return

        # Perform post-set validations if requested. This is skipped if there was an exception
        # already raised during the set operation.
        try:
            validate(self, obj)  # Exception should be raised by validate if unexpected obj state

        except BaseException as err:  # pylint: disable=broad-exception-caught
            new_errors = _process_exception(
                err=err,
                exception=self.exception,
                exception_tag=self.exception_tag,
                label="validating attribute value")
            errors.extend(new_errors)

        # Report any errors found during the validate portion of the test
        if errors:
            self.on_fail(self.name + ": " + "\n".join(errors))
            raise RuntimeError("unreachable code after on_fail call")  # pylint: disable=raise-missing-from
