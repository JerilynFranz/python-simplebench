"""Tests for the simplebench/utils.py module."""

import pytest

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from simplebench import utils
import simplebench.constants as constants

from .testspec import TestAction

constants.DEFAULT_SIGNIFICANT_FIGURES = 3  # Ensure default is as expected for tests


@pytest.mark.parametrize("testspec", [
    pytest.param(TestAction(
        name="Missing kwargs arg",
        kwargs={},
        action=utils.kwargs_variations,
        exception=TypeError),
        id="KWARGS_VARIATIONS_001"),
    pytest.param(TestAction(
        name="Empty kwargs",
        kwargs={'kwargs': {}},
        action=utils.kwargs_variations,
        expected=[{}]),
        id="KWARGS_VARIATIONS_002"),
    pytest.param(TestAction(
        name="One key with one value",
        kwargs={'kwargs': {"a": [1]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1}]),
        id="KWARGS_VARIATIONS_003"),
    pytest.param(TestAction(
        name="One key with multiple values",
        kwargs={'kwargs': {"a": [1, 2, 3]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1}, {"a": 2}, {"a": 3}]),
        id="KWARGS_VARIATIONS_004"),
    pytest.param(TestAction(
        name="Two keys with one value each",
        kwargs={'kwargs': {"a": [1], "b": [2]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1, "b": 2}]),
        id="KWARGS_VARIATIONS_005"),
    pytest.param(TestAction(
        name="invalid positional arg type (str)",
        args=["not_a_dict"],
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE),
        id="KWARGS_VARIATIONS_006"),
    pytest.param(TestAction(
        name="invalid kwargs value type (str)",
        kwargs={'kwargs': {"a": 1, "b": "not_"}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE),
        id="KWARGS_VARIATIONS_007"),
    pytest.param(TestAction(
        name="invalid kwargs value type (bytes)",
        kwargs={'kwargs': {"a": 1, "b": b"not_"}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE),
        id="KWARGS_VARIATIONS_008"),
    pytest.param(TestAction(
        name="Two keys with multiple values each",
        kwargs={'kwargs': {"a": [1, 2], "b": ['x', 'y']}},
        action=utils.kwargs_variations,
        expected=[{"a": 1, "b": 'x'},
                  {"a": 1, "b": 'y'},
                  {"a": 2, "b": 'x'},
                  {"a": 2, "b": 'y'}]),
        id="KWARGS_VARIATIONS_009"),
    pytest.param(TestAction(
        name="Invalid kwargs value type (int)",
        kwargs={'kwargs': {"a": 1, "b": 2}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE),
        id="KWARGS_VARIATIONS_010")
])
def test_kwargs_variations(testspec: TestAction) -> None:
    """Test utils.kwargs_variations() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    pytest.param(TestAction(
        name="Missing number arg",
        args=[],
        kwargs={'figures': 3},
        action=utils.sigfigs,
        exception=TypeError),
        id="SIGFIGS_001"),
    pytest.param(TestAction(
        name="Missing figures arg",
        kwargs={'number': 1.2345},
        action=utils.sigfigs,
        expected=1.23),
        id="SIGFIGS_002"),
    pytest.param(TestAction(
        name="Invalid number arg type (str)",
        kwargs={'number': 'not_a_float', 'figures': 3},
        action=utils.sigfigs,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SIGFIGS_INVALID_NUMBER_ARG_TYPE),
        id="SIGFIGS_003"),
    pytest.param(TestAction(
        name="Invalid figures arg type (str)",
        kwargs={'number': 1.2345, 'figures': 'not_an_int'},
        action=utils.sigfigs,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SIGFIGS_INVALID_FIGURES_ARG_TYPE),
        id="SIGFIGS_004"),
    pytest.param(TestAction(
        name="Invalid figures arg value (0 < 1)",
        kwargs={'number': 1.2345, 'figures': 0},
        action=utils.sigfigs,
        exception=ValueError),
        id="SIGFIGS_005"),
    pytest.param(TestAction(
        name="Valid number and figures args (kwargs, 3 figures)",
        kwargs={'number': 1.235, 'figures': 3},
        action=utils.sigfigs,
        expected=1.24),
        id="SIGFIGS_006"),
    pytest.param(TestAction(
        name="Valid number and figures args (positional args, 3 figures)",
        args=[1.235, 3],
        action=utils.sigfigs,
        expected=1.24),
        id="SIGFIGS_007"),
    pytest.param(TestAction(
        name="number arg is zero",
        kwargs={'number': 0.0, 'figures': 3},
        action=utils.sigfigs,
        expected=0.0),
        id="SIGFIGS_008"),
])
def test_sigfigs(testspec: TestAction) -> None:
    """Test utils.sigfigs() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    pytest.param(TestAction(
        name="Missing filename arg",
        args=[],
        action=utils.sanitize_filename,
        exception=TypeError),
        id="SANITIZE_FILENAME_001"),
    pytest.param(TestAction(
        name="Invalid filename arg type (int)",
        args=[1],
        action=utils.sanitize_filename,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE),
        id="SANITIZE_FILENAME_002"),
    pytest.param(TestAction(
        name="Filename with only valid characters",
        args=['valid_filename-123.txt'],
        action=utils.sanitize_filename,
        expected='valid_filename-123_txt'),
        id="SANITIZE_FILENAME_003"),
    pytest.param(TestAction(
        name="Filename with spaces",
        args=['file name with spaces.txt'],
        action=utils.sanitize_filename,
        expected='file_name_with_spaces_txt'),
        id="SANITIZE_FILENAME_004"),
    pytest.param(TestAction(
        name='Empty filename',
        args=[''],
        action=utils.sanitize_filename,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SANITIZE_FILENAME_EMPTY_NAME_ARG),
        id="SANITIZE_FILENAME_005"),
])
def test_sanitize_filename(testspec: TestAction) -> None:
    """Test utils.sanitize_filename() function."""
    testspec.run()
