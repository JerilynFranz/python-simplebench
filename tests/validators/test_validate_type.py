"""Tests for simplebench.validators validate_type() function."""
import pytest

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError
from simplebench.validators import validate_type, ValidatorsErrorTag

from ..testspec import TestSpec, Assert, idspec, TestAction


class GenericErrorTag(ErrorTag):
    """Error tags for string validator tests."""
    INVALID_ARG_TYPE = "INVALID_ARG_TYPE"
    INVALID_ARG_VALUE = "INVALID_ARG_VALUE"


TEST_STRING: str = 'asbc'


@pytest.mark.parametrize('testspec', [
    idspec("PARAM_001", TestAction(
        name="Attempt to pass expected as NOT a type or tuple of types raises correct SimpleBenchTypeError",
        action=validate_type,
        kwargs={
            "value": TEST_STRING,
            "types": "not_a_type",
            "field_name": "test_field",
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.VALIDATE_TYPE_INVALID_EXPECTED_ARG_TYPE)),
    idspec("PARAM_002", TestAction(
        name="Attempt to pass expected as a tuple with a non-type item raises correct SimpleBenchTypeError",
        action=validate_type,
        kwargs={
            "value": TEST_STRING,
            "types": (str, 123),
            "field_name": "test_field",
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.VALIDATE_TYPE_INVALID_EXPECTED_ARG_ITEM_TYPE)),
    idspec("PARAM_003", TestAction(
        name="Attempt to pass name as non-str raises correct SimpleBenchTypeError",
        action=validate_type,
        kwargs={
            "value": TEST_STRING,
            "types": str,
            "field_name": 123,
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.VALIDATE_TYPE_INVALID_NAME_ARG_TYPE)),
    idspec("PARAM_004", TestAction(
        name="Attempt to pass error_tag as non-ErrorTag raises correct SimpleBenchTypeError",
        action=validate_type,
        kwargs={
            "value": TEST_STRING,
            "types": str,
            "field_name": "test_field",
            "error_tag": "not_an_errortag",
        },
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.VALIDATE_TYPE_INVALID_ERROR_TAG_TYPE)),
])
def test_param(testspec: TestSpec):
    """Tests for validate_string parameters validation."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec("TYPE_001", TestAction(
        name="Simple type for str - 'a string' returns type str value",
        action=validate_type,
        kwargs={
            "value": "a string",
            "types": str,
            "field_name": "test_field",
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec("TYPE_002", TestAction(
        name="Simple type for str - '123' raises SimpleBenchTypeError",
        action=validate_type,
        kwargs={
            "value": 123,
            "types": str,
            "field_name": "test_field",
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        exception=SimpleBenchTypeError,
        exception_tag=GenericErrorTag.INVALID_ARG_TYPE)),
    idspec("TYPE_003", TestAction(
        name="Expected as tuple - 123 for (str, int) returns type int value",
        action=validate_type,
        kwargs={
            "value": 123,
            "types": (str, int),
            "field_name": "test_field",
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        assertion=Assert.ISINSTANCE,
        expected=int)),
    idspec("TYPE_004", TestAction(
        name="Expected as tuple, wrong type value - 12.3 for (str, int) raises SimpleBenchTypeError",
        action=validate_type,
        kwargs={
            "value": 12.3,
            "types": (str, int),
            "field_name": "test_field",
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        exception=SimpleBenchTypeError,
        exception_tag=GenericErrorTag.INVALID_ARG_TYPE)),
    idspec("TYPE_005", TestAction(
        name="Successfuly validated value object is returned (not a new object)",
        action=validate_type,
        kwargs={
            "value": TEST_STRING,
            "types": str,
            "field_name": "test_field",
            "error_tag": GenericErrorTag.INVALID_ARG_TYPE,
        },
        assertion=Assert.IS,
        expected=TEST_STRING)),
])
def test_validate_type(testspec: TestSpec):
    """Tests for validate_type validation."""
    testspec.run()
