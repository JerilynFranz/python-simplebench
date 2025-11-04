"""Tests for simplebench.validators validate_iterable_of_type() function."""
import pytest

from tests.testspec import TestSpec, idspec, TestAction

from simplebench.exceptions import ErrorTag
from simplebench.validators import validate_iterable_of_type


class GenericErrorTag(ErrorTag):
    """Error tags for string validator tests."""
    INVALID_ARG_TYPE = "INVALID_ARG_TYPE"
    INVALID_ARG_VALUE = "INVALID_ARG_VALUE"


@pytest.mark.parametrize("testspec", [
        idspec("PARAM_001", TestAction(
            name="Valid list of strings",
            action=validate_iterable_of_type,
            kwargs={
                "value": ["a", "b", "c"],
                "types": str,
                "field_name": "test_field",
                "type_tag": GenericErrorTag.INVALID_ARG_TYPE,
                "value_tag": GenericErrorTag.INVALID_ARG_VALUE,
                "allow_empty": False,
                "exact_type": False,
            },
            expected=["a", "b", "c"],
        )),
        idspec("PARAM_002", TestAction(
            name="Valid tuple of integers",
            action=validate_iterable_of_type,
            kwargs={
                "value": (1, 2, 3),
                "types": int,
                "field_name": "test_field",
                "type_tag": GenericErrorTag.INVALID_ARG_TYPE,
                "value_tag": GenericErrorTag.INVALID_ARG_VALUE,
                "allow_empty": False,
                "exact_type": True,
            },
            expected=[1, 2, 3],
        )),
        idspec("PARAM_003", TestAction(
            name="Valid list of mixed types with tuple of expected types",
            action=validate_iterable_of_type,
            kwargs={
                "value": [1, "two", 3.0],
                "types": (int, str, float),
                "field_name": "test_field",
                "type_tag": GenericErrorTag.INVALID_ARG_TYPE,
                "value_tag": GenericErrorTag.INVALID_ARG_VALUE,
                "allow_empty": False,
                "exact_type": False,
            },
            expected=[1, "two", 3.0],
        )),
    ])
def test_validate_iterable_of_type_valid_cases(testspec: TestSpec) -> None:
    """Test cases for validate_iterable_of_type()."""
    testspec.run()
