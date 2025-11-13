"""Test the CaseType class."""

from simplebench.type_proxies import CaseTypeProxy, is_case

from ..factories import case_factory


def test_isinstance_with_lazy_case_type():
    """Test that isinstance works with the lazy CaseType.

    This test ensures that the CaseType proxy correctly identifies
    instances of the Case class without causing import issues.
    """
    case = case_factory()
    assert isinstance(case, CaseTypeProxy), "case should be an instance of CaseType"
    assert not isinstance(123, CaseTypeProxy), "integer should not be an instance of CaseType"


def validate_is_case_type(obj: object) -> None:
    """Validate that the is_case type guard works correctly."""
    if not is_case(obj):
        raise TypeError("Object is not of type Case")

    assert is_case(obj), "case instance should be recognized as Case"
    assert not is_case(123), "Integer should not be recognized as Case"
