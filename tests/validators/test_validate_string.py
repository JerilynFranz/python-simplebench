"""Tests for simplebench.validators.validate_string()"""
import pytest

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_string, ValidatorsErrorTag

from ..testspec import TestSpec, Assert, idspec, TestAction


class GenericErrorTag(ErrorTag):
    """Error tags for string validator tests."""
    INVALID_ARG_TYPE = "INVALID_ARG_TYPE"
    INVALID_ARG_VALUE = "INVALID_ARG_VALUE"


@pytest.mark.parametrize("testspec", [
    idspec("PARAM_001", TestAction(
        name="No arguments - raises TypeError",
        action=validate_string,
        args=[],
        exception=TypeError)),
    idspec("PARAM_002", TestAction(
        name="Only value argument (positional) - raises TypeError",
        action=validate_string,
        args=["test_string"],
        exception=TypeError)),
    idspec("PARAM_003", TestAction(
        name="Value and field_name arguments (positional) - raises TypeError",
        action=validate_string,
        args=["test_string", "param_name"],
        exception=TypeError)),
    idspec("PARAM_004", TestAction(
        name="Value, field_name, type_error_tag arguments (positional) - raises TypeError",
        action=validate_string,
        args=["test_string", "param_name", GenericErrorTag.INVALID_ARG_TYPE],
        exception=TypeError)),
    idspec("PARAM_005", TestAction(
        name="All required arguments (positional) - returns 'test_string'",
        action=validate_string,
        args=[
            "test_string", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        assertion=Assert.EQUAL,
        expected="test_string")),
    idspec("PARAM_006", TestAction(
        name="All required arguments (kwargs) - returns 'test_string'",
        action=validate_string,
        kwargs={
            "value": "test_string",
            "field_name": "param_name",
            "type_error_tag": GenericErrorTag.INVALID_ARG_TYPE,
            "value_error_tag": GenericErrorTag.INVALID_ARG_VALUE},
        assertion=Assert.EQUAL,
        expected="test_string")),
    idspec("PARAM_007", TestAction(
        name="All required arguments (mixed positional and kwargs) - returns 'test_string'",
        action=validate_string,
        args=["test_string", "param_name"],
        kwargs={
            "type_error_tag": GenericErrorTag.INVALID_ARG_TYPE,
            "value_error_tag": GenericErrorTag.INVALID_ARG_VALUE},
        assertion=Assert.EQUAL,
        expected="test_string")),
    idspec("PARAM_008", TestAction(
        name="strip set positionally - raises TypeError",
        action=validate_string,
        args=["test_string", "param_name",
              GenericErrorTag.INVALID_ARG_TYPE,
              GenericErrorTag.INVALID_ARG_VALUE,
              True],  # strip is kwarg only
        exception=TypeError)),
    idspec("PARAM_009", TestAction(
        name="strip=True set as kwarg - returns a string",
        action=validate_string,
        args=[
            "", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'strip': True},
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec("PARAM_010", TestAction(
        name="strip=None set as kwarg - raises SimpleBenchTypeError with correct tag",
        action=validate_string,
        args=[
            "", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'strip': None},
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.INVALID_STRIP_ARG_TYPE)),
    idspec("PARAM_011", TestAction(
        name="allow_empty set to True - returns a string",
        action=validate_string,
        args=[
            "", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': True},
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec("PARAM_012", TestAction(
        name="allow_empty set to 'yes' - raises SimpleBenchTypeError with correct tag",
        action=validate_string,
        args=[
            "", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': 'yes'},
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.INVALID_ALLOW_EMPTY_ARG_TYPE)),
    idspec("PARAM_013", TestAction(
        name="allow_blank set to False - returns a string",
        action=validate_string,
        args=[
            "non_blank", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_blank': False},
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec("PARAM_014", TestAction(
        name="allow_blank set to 0 - raises SimpleBenchTypeError with correct tag",
        action=validate_string,
        args=[
            "non_blank", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_blank': 0},
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.INVALID_ALLOW_BLANK_ARG_TYPE)),
    idspec("PARAM_015", TestAction(
        name="alphanumeric_only set to True - returns a string",
        action=validate_string,
        args=[
            "Alpha123", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True},
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec("PARAM_016", TestAction(
        name="alphanumeric_only set to 'no' - raises SimpleBenchTypeError with correct tag",
        action=validate_string,
        args=[
            "Alpha123", "param_name",
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': 'no'},
        exception=SimpleBenchTypeError,
        exception_tag=ValidatorsErrorTag.INVALID_ALPHANUMERIC_ONLY_ARG_TYPE)),
])
def test_param(testspec: TestSpec):
    """Test validate_string calling parameters."""
    testspec.run()

# Lessons Learned: Combining too many interacting parameter options in a single
# function can lead to a combinatorial explosion of test cases even for an apparently
# simple function and it is harder than you might think to ensure correct functioning
# across the full parameter space.
#
# Here we have 4 boolean parameters (allow_empty, allow_blank, strip, alphanumeric_only)
# leading to 16 possible combinations of parameter settings. Each of these can
# interact with different input string values (valid strings, empty strings,
# blank strings, alphanumeric strings, non-alphanumeric strings, padded strings) leading
# to many possible test cases.
#
# Writing these tests directly revealed some issues in the original implementation
# of validate_string() which have now been fixed.


@pytest.mark.parametrize("testspec", [
    idspec("VALIDATE_001", TestAction(
        name="Default behavior valid string - returned value is type str",
        action=validate_string,
        args=[
            "valid_string", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE
        ],
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec("VALIDATE_002", TestAction(
        name="Default behavior valid string - returned value is 'valid_string'",
        action=validate_string,
        args=[
            "valid_string", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE
        ],
        assertion=Assert.EQUAL,
        expected="valid_string")),
    idspec("VALIDATE_003", TestAction(
        name="Default behavior invalid type (int) - raises SimpleBenchTypeError with correct tag",
        action=validate_string,
        args=[
            123, 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE
        ],
        exception=SimpleBenchTypeError,
        exception_tag=GenericErrorTag.INVALID_ARG_TYPE)),
    idspec("VALIDATE_004", TestAction(
        name="Default behavior 'non_empty_string' returns 'non_empty_string'",
        action=validate_string,
        args=[
            "non_empty_string", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={},
        assertion=Assert.EQUAL,
        expected="non_empty_string")),
    idspec("VALIDATE_005", TestAction(
        name="Default behavior '  non_empty_string  ' returns '  non_empty_string  '",
        action=validate_string,
        args=[
            "  non_empty_string  ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={},
        assertion=Assert.EQUAL,
        expected="  non_empty_string  ")),
    idspec("VALIDATE_006", TestAction(
        name="Default behavior empty string '' returns ''",
        action=validate_string,
        args=[
            "", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_007", TestAction(
        name="Default behavior blank string '   ' returns '   '",
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={},
        assertion=Assert.EQUAL,
        expected="   ")),
    idspec("VALIDATE_008", TestAction(
        name="strip=False: '  non_empty_string  ' returns '  non_empty_string  '",
        action=validate_string,
        args=[
            "  non_empty_string  ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'strip': False},
        assertion=Assert.EQUAL,
        expected="  non_empty_string  ")),
    idspec("VALIDATE_009", TestAction(
        name="strip=True: '  non_empty_string  ' returns 'non_empty_string'",
        action=validate_string,
        args=[
            "  non_empty_string  ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'strip': True},
        assertion=Assert.EQUAL,
        expected="non_empty_string")),
    idspec("VALIDATE_010", TestAction(
        name="allow_empty=False: empty string '' raises SimpleBenchValueError with correct tag",
        action=validate_string,
        args=[
            "", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': False},
        exception=SimpleBenchValueError,
        exception_tag=GenericErrorTag.INVALID_ARG_VALUE)),
    idspec("VALIDATE_011", TestAction(
        name="allow_blank=False, strip=False: blank string '   ' raises SimpleBenchValueError with correct tag",
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_blank': False, 'strip': False},
        exception=SimpleBenchValueError,
        exception_tag=GenericErrorTag.INVALID_ARG_VALUE)),
    idspec("VALIDATE_012", TestAction(  # allow_empty=True is default and overrides allow_blank=False when strip=True
        name="allow_blank=False, strip=True: blank string '   ' returns ''",
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_blank': False, 'strip': True},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_013", TestAction(
        name="allow_empty=False, allow_blank=True, strip=False: blank string '   ' returns '   '",
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': False, 'allow_blank': True, 'strip': False},
        assertion=Assert.EQUAL,
        expected="   ")),
    idspec("VALIDATE_014", TestAction(
        name=("allow_empty=False, allow_blank=True, strip=True: "
              "blank string '   ' raises SimpleBenchValueError with correct tag"),
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': False, 'allow_blank': True, 'strip': True},
        exception=SimpleBenchValueError,
        exception_tag=GenericErrorTag.INVALID_ARG_VALUE)),
    idspec("VALIDATE_015", TestAction(
        name="allow_empty=True, allow_blank=False, strip=False: empty string '' returns ''",
        action=validate_string,
        args=[
            "", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': True, 'allow_blank': False, 'strip': False},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_016", TestAction(
        name="allow_empty=True, allow_blank=False, strip=True: '   ' returns ''",
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': True, 'allow_blank': False, 'strip': True},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_017", TestAction(
        name="allow_empty=True, allow_blank=True, strip=False: string '' returns ''",
        action=validate_string,
        args=[
            "", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': True, 'allow_blank': True, 'strip': False},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_018", TestAction(
        name="allow_empty=True, allow_blank=True, strip=True: string '   ' returns ''",
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'allow_empty': True, 'allow_blank': True, 'strip': True},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_019", TestAction(
        name="alphanumeric_only=True: 'ValidString123' returns 'ValidString123'",
        action=validate_string,
        args=[
            "ValidString123", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True},
        assertion=Assert.EQUAL,
        expected="ValidString123")),
    idspec("VALIDATE_020", TestAction(
        name="alphanumeric_only=True: 'Invalid String!' raises SimpleBenchValueError with correct tag",
        action=validate_string,
        args=[
            "Invalid String!", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True},
        exception=SimpleBenchValueError,
        exception_tag=GenericErrorTag.INVALID_ARG_VALUE)),
    idspec("VALIDATE_021", TestAction(
        name="alphanumeric_only=True, allow_empty=True: empty string '' returns ''",
        action=validate_string,
        args=[
            "", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True, 'allow_empty': True},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_022", TestAction(
        name="alphanumeric_only=True, allow_empty=False: empty string '' raises SimpleBenchValueError with correct tag",
        action=validate_string,
        args=[
            "", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True, 'allow_empty': False},
        exception=SimpleBenchValueError,
        exception_tag=GenericErrorTag.INVALID_ARG_VALUE)),
    idspec("VALIDATE_023", TestAction(
        name=("alphanumeric_only=True, allow_blank=True, strip=False: "
              "blank string '   ' raises SimpleBenchValueError with correct tag"),
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True, 'allow_blank': True, 'strip': False},
        exception=SimpleBenchValueError,
        exception_tag=GenericErrorTag.INVALID_ARG_VALUE)),
    idspec("VALIDATE_024", TestAction(  # allow_empty=True is default and overrides allow_blank=False when strip=True
        name="alphanumeric_only=True, allow_blank=True, strip=True: blank string '   ' returns ''",
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True, 'allow_blank': True, 'strip': True},
        assertion=Assert.EQUAL,
        expected="")),
    idspec("VALIDATE_025", TestAction(
        name=("alphanumeric_only=True, allow_empty=False, allow_blank=True, strip=True: "
              "blank string raises SimpleBenchValueError with correct tag"),
        action=validate_string,
        args=[
            "   ", 'test_param',
            GenericErrorTag.INVALID_ARG_TYPE,
            GenericErrorTag.INVALID_ARG_VALUE],
        kwargs={'alphanumeric_only': True, 'allow_blank': True, 'strip': True},
        assertion=Assert.EQUAL,
        expected="")),
])
def test_validate_string(testspec: TestSpec):
    """Test validate_string function."""
    testspec.run()
