"""Test the CaseType class."""
import pytest

from simplebench.type_proxies import CaseTypeProxy, is_case

from ..factories import case_factory
from ..testspec import Assert, TestAction, TestSpec, idspec


@pytest.mark.parametrize("testspec", [
    idspec("IS_CASE_001", TestAction(
        name="Validate is_case with Case instance",
        action=isinstance,
        args=[case_factory(), CaseTypeProxy],
        assertion=Assert.EQUAL,
        expected=True,
    )),
    idspec("IS_CASE_002", TestAction(
        name="Validate is_case with non-Case instance",
        action=isinstance,
        args=[123, CaseTypeProxy],
        assertion=Assert.EQUAL,
        expected=False,
    )),
])
def test_isinstance_with_case_type_proxy(testspec: TestSpec) -> None:
    """Validate that isinstance works correctly with CaseTypeProxy."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("IS_CASE_TYPE_001", TestAction(
        name="Validate is_case with Case instance",
        action=is_case,
        args=[case_factory()],
        assertion=Assert.EQUAL,
        expected=True,
    )),
    idspec("IS_CASE_TYPE_002", TestAction(
        name="Validate is_case with non-Case instance",
        action=is_case,
        args=[123],
        assertion=Assert.EQUAL,
        expected=False,
    )),
])
def test_validate_is_case_type(testspec: TestSpec) -> None:
    """Validate that the is_case type guard works correctly."""
    testspec.run()
