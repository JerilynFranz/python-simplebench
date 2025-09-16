"""Tests for the simplebench/utils.py module."""

import pytest

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from simplebench import utils
import simplebench.constants as constants

from .testspec import TestAction, idspec

constants.DEFAULT_SIGNIFICANT_FIGURES = 3  # Ensure default is as expected for tests


@pytest.mark.parametrize("testspec", [
    idspec("KWARGS_VARIATIONS_001", TestAction(
        name="Missing kwargs arg",
        kwargs={},
        action=utils.kwargs_variations,
        exception=TypeError)),
    idspec("KWARGS_VARIATIONS_002", TestAction(
        name="Empty kwargs",
        kwargs={'kwargs': {}},
        action=utils.kwargs_variations,
        expected=[{}])),
    idspec("KWARGS_VARIATIONS_003", TestAction(
        name="One key with one value",
        kwargs={'kwargs': {"a": [1]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1}])),
    idspec("KWARGS_VARIATIONS_004", TestAction(
        name="One key with multiple values",
        kwargs={'kwargs': {"a": [1, 2, 3]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1}, {"a": 2}, {"a": 3}])),
    idspec("KWARGS_VARIATIONS_005", TestAction(
        name="Two keys with one value each",
        kwargs={'kwargs': {"a": [1], "b": [2]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1, "b": 2}])),
    idspec("KWARGS_VARIATIONS_006", TestAction(
        name="invalid positional arg type (str)",
        args=["not_a_dict"],
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE)),
    idspec("KWARGS_VARIATIONS_007", TestAction(
        name="invalid kwargs value type (str)",
        kwargs={'kwargs': {"a": 1, "b": "not_"}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE)),
    idspec("KWARGS_VARIATIONS_008", TestAction(
        name="invalid kwargs value type (bytes)",
        kwargs={'kwargs': {"a": 1, "b": b"not_"}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE)),
    idspec("KWARGS_VARIATIONS_009", TestAction(
        name="Two keys with multiple values each",
        kwargs={'kwargs': {"a": [1, 2], "b": ['x', 'y']}},
        action=utils.kwargs_variations,
        expected=[{"a": 1, "b": 'x'},
                  {"a": 1, "b": 'y'},
                  {"a": 2, "b": 'x'},
                  {"a": 2, "b": 'y'}])),
    idspec("KWARGS_VARIATIONS_010", TestAction(
        name="Invalid kwargs value type (int)",
        kwargs={'kwargs': {"a": 1, "b": 2}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE)),
])
def test_kwargs_variations(testspec: TestAction) -> None:
    """Test utils.kwargs_variations() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("SIGFIGS_001", TestAction(
        name="Missing number arg",
        args=[],
        kwargs={'figures': 3},
        action=utils.sigfigs,
        exception=TypeError)),
    idspec("SIGFIGS_002", TestAction(
        name="Missing figures arg",
        kwargs={'number': 1.2345},
        action=utils.sigfigs,
        expected=1.23)),
    idspec("SIGFIGS_003", TestAction(
        name="Invalid number arg type (str)",
        kwargs={'number': 'not_a_float', 'figures': 3},
        action=utils.sigfigs,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SIGFIGS_INVALID_NUMBER_ARG_TYPE)),
    idspec("SIGFIGS_004", TestAction(
        name="Invalid figures arg type (str)",
        kwargs={'number': 1.2345, 'figures': 'not_an_int'},
        action=utils.sigfigs,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SIGFIGS_INVALID_FIGURES_ARG_TYPE)),
    idspec("SIGFIGS_005", TestAction(
        name="Invalid figures arg value (0 < 1)",
        kwargs={'number': 1.2345, 'figures': 0},
        action=utils.sigfigs,
        exception=SimpleBenchValueError)),
    idspec("SIGFIGS_006", TestAction(
        name="Valid number and figures args (kwargs, 3 figures)",
        kwargs={'number': 1.235, 'figures': 3},
        action=utils.sigfigs,
        expected=1.24)),
    idspec("SIGFIGS_007", TestAction(
        name="Valid number and figures args (positional args, 3 figures)",
        args=[1.235, 3],
        action=utils.sigfigs,
        expected=1.24)),
    idspec("SIGFIGS_008", TestAction(
        name="number arg is zero",
        kwargs={'number': 0.0, 'figures': 3},
        action=utils.sigfigs,
        expected=0.0)),
])
def test_sigfigs(testspec: TestAction) -> None:
    """Test utils.sigfigs() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("SANITIZE_FILENAME_001", TestAction(
        name="Missing filename arg",
        args=[],
        action=utils.sanitize_filename,
        exception=TypeError)),
    idspec("SANITIZE_FILENAME_002", TestAction(
        name="Invalid filename arg type (int)",
        args=[1],
        action=utils.sanitize_filename,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE)),
    idspec("SANITIZE_FILENAME_003", TestAction(
        name="Filename with only valid characters",
        args=['valid_filename-123.txt'],
        action=utils.sanitize_filename,
        expected='valid_filename-123_txt')),
    idspec("SANITIZE_FILENAME_004", TestAction(
        name="Filename with spaces",
        args=['file name with spaces.txt'],
        action=utils.sanitize_filename,
        expected='file_name_with_spaces_txt')),
    idspec("SANITIZE_FILENAME_005", TestAction(
        name='Empty filename',
        args=[''],
        action=utils.sanitize_filename,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SANITIZE_FILENAME_EMPTY_NAME_ARG)),
])
def test_sanitize_filename(testspec: TestAction) -> None:
    """Test utils.sanitize_filename() function."""
    testspec.run()
