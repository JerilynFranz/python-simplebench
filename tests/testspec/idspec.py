"""TestSpec testing framework - idspec helper."""

from typing import Any

import pytest

from .base import TestSpec
from .context import Context


def idspec(id_base: str, testspec: TestSpec | tuple[Context, TestSpec]) -> Any:
    """Helper function to create a test case with a specific pytest id directly from a TestAction or TestProperty.

    This function generates a pytest parameter with a custom id based on the provided base
    string and the name of the TestAction or TestProperty instance. It is useful for organizing
    and identifying test cases in a clear and descriptive manner.

    Because the pytest ParameterSet class definition is hidden from the public API,
    we cannot use it directly in type annotations.

    :param id_base: The base string to use for the test case id.
    :type id_base: str
    :param testspec: The TestSpec instance containing the test configuration.
        TestSet, TestGet, TestSetGet, and TestAction are all subclasses of TestSpec.
        It can also be a tuple of (Context, TestSpec) to provide a context for the test.
    :type testspec: TestSpec | tuple[Context, TestSpec]
    :return: A pytest parameter with a custom id derived from the id_base string and the test specification name.
    :rtype: Any
    :raises TypeError: If testspec is not an instance of TestSpec or id_base is not a str.
    """
    if not isinstance(testspec, (TestSpec, tuple)):
        raise TypeError(f"testspec must be an instance of TestSpec or a type: got {type(testspec)}")
    if isinstance(testspec, tuple):
        if len(testspec) != 2 or not isinstance(testspec[0], Context) or not isinstance(testspec[1], TestSpec):
            raise TypeError("testspec tuple must be of the form (Context, TestSpec)")
        testspec = testspec[1]
    if not isinstance(id_base, str):
        raise TypeError("id_base must be a str")
    return pytest.param(testspec, id=f"{id_base} {testspec.name}")  # type: ignore[attr-defined]
