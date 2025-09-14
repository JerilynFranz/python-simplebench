"""Tests for the simplebench/utils.py module."""

import pytest

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from simplebench import utils
import simplebench.constants as constants

from .testspec import TestSpec

constants.DEFAULT_SIGNIFICANT_FIGURES = 3  # Ensure default is as expected for tests


@pytest.mark.parametrize("testspec", [
    pytest.param(TestSpec(
        name="Missing kwargs arg",
        kwargs={},
        action=utils.kwargs_variations,
        exception=TypeError),
        id="KWARGS_VARIATIONS_001"),
    pytest.param(TestSpec(
        name="Empty kwargs",
        kwargs={'kwargs': {}},
        action=utils.kwargs_variations,
        expected=[{}]),
        id="KWARGS_VARIATIONS_002"),
    pytest.param(TestSpec(
        name="One key with one value",
        kwargs={'kwargs': {"a": [1]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1}]),
        id="KWARGS_VARIATIONS_003"),
    pytest.param(TestSpec(
        name="One key with multiple values",
        kwargs={'kwargs': {"a": [1, 2, 3]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1}, {"a": 2}, {"a": 3}]),
        id="KWARGS_VARIATIONS_004"),
    pytest.param(TestSpec(
        name="Two keys with one value each",
        kwargs={'kwargs': {"a": [1], "b": [2]}},
        action=utils.kwargs_variations,
        expected=[{"a": 1, "b": 2}]),
        id="KWARGS_VARIATIONS_005"),
    pytest.param(TestSpec(
        name="invalid positional arg type (str)",
        args=["not_a_dict"],
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE),
        id="KWARGS_VARIATIONS_006"),
    pytest.param(TestSpec(
        name="invalid kwargs value type (str)",
        kwargs={'kwargs': {"a": 1, "b": "not_"}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE),
        id="KWARGS_VARIATIONS_007"),
    pytest.param(TestSpec(
        name="invalid kwargs value type (bytes)",
        kwargs={'kwargs': {"a": 1, "b": b"not_"}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE),
        id="KWARGS_VARIATIONS_008"),
    pytest.param(TestSpec(
        name="Two keys with multiple values each",
        kwargs={'kwargs': {"a": [1, 2], "b": ['x', 'y']}},
        action=utils.kwargs_variations,
        expected=[{"a": 1, "b": 'x'},
                  {"a": 1, "b": 'y'},
                  {"a": 2, "b": 'x'},
                  {"a": 2, "b": 'y'}]),
        id="KWARGS_VARIATIONS_009"),
    pytest.param(TestSpec(
        name="Invalid kwargs value type (int)",
        kwargs={'kwargs': {"a": 1, "b": 2}},
        action=utils.kwargs_variations,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE),
        id="KWARGS_VARIATIONS_010")
])
def test_kwargs_variations(testspec: TestSpec) -> None:
    """Test utils.kwargs_variations() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    pytest.param(TestSpec(
        name="Missing number arg",
        args=[],
        kwargs={'figures': 3},
        action=utils.sigfigs,
        exception=TypeError),
        id="SIGFIGS_001"),
    pytest.param(TestSpec(
        name="Missing figures arg",
        kwargs={'number': 1.2345},
        action=utils.sigfigs,
        expected=1.23),
        id="SIGFIGS_002"),
    pytest.param(TestSpec(
        name="Invalid number arg type (str)",
        kwargs={'number': 'not_a_float', 'figures': 3},
        action=utils.sigfigs,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SIGFIGS_INVALID_NUMBER_ARG_TYPE),
        id="SIGFIGS_003"),
    pytest.param(TestSpec(
        name="Invalid figures arg type (str)",
        kwargs={'number': 1.2345, 'figures': 'not_an_int'},
        action=utils.sigfigs,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SIGFIGS_INVALID_FIGURES_ARG_TYPE),
        id="SIGFIGS_004"),
    pytest.param(TestSpec(
        name="Invalid figures arg value (0 < 1)",
        kwargs={'number': 1.2345, 'figures': 0},
        action=utils.sigfigs,
        exception=ValueError),
        id="SIGFIGS_005"),
    pytest.param(TestSpec(
        name="Valid number and figures args (kwargs, 3 figures)",
        kwargs={'number': 1.235, 'figures': 3},
        action=utils.sigfigs,
        expected=1.24),
        id="SIGFIGS_006"),
    pytest.param(TestSpec(
        name="Valid number and figures args (positional args, 3 figures)",
        args=[1.235, 3],
        action=utils.sigfigs,
        expected=1.24),
        id="SIGFIGS_007"),
    pytest.param(TestSpec(
        name="number arg is zero",
        kwargs={'number': 0.0, 'figures': 3},
        action=utils.sigfigs,
        expected=0.0),
        id="SIGFIGS_008"),
])
def test_sigfigs(testspec: TestSpec) -> None:
    """Test utils.sigfigs() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    pytest.param(TestSpec(
        name="Missing unit arg",
        args=[],
        kwargs={'base_unit': 's'},
        action=utils.si_scale,
        exception=TypeError),
        id="SI_SCALE_001"),
    pytest.param(TestSpec(
        name="Missing base_unit arg",
        args=[],
        kwargs={'unit': 's'},
        action=utils.si_scale,
        exception=TypeError),
        id="SI_SCALE_002"),
    pytest.param(TestSpec(
        name="Invalid unit arg type (int)",
        args=[],
        kwargs={'unit': 1, 'base_unit': 's'},
        action=utils.si_scale,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_INVALID_UNIT_ARG_TYPE),
        id="SI_SCALE_003"),
    pytest.param(TestSpec(
        name="Invalid base_unit arg type (int)",
        args=[],
        kwargs={'unit': 's', 'base_unit': 1},
        action=utils.si_scale,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE),
        id="SI_SCALE_004"),
    pytest.param(TestSpec(
        name="Empty base_unit arg",
        args=[],
        kwargs={'unit': 's', 'base_unit': ''},
        action=utils.si_scale,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_EMPTY_BASE_UNIT_ARG),
        id="SI_SCALE_005"),
    pytest.param(TestSpec(
        name="unit does not end with base_unit",
        args=[],
        kwargs={'unit': 'ms', 'base_unit': 'm'},
        action=utils.si_scale,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT),
        id="SI_SCALE_006"),
    pytest.param(TestSpec(
        name="Unknown prefix in unit",
        args=[],
        kwargs={'unit': 'xs', 'base_unit': 's'},
        action=utils.si_scale,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_UNKNOWN_SI_UNIT_PREFIX),
        id="SI_SCALE_007"),
    pytest.param(TestSpec(
        name="Valid unit 's'",
        action=utils.si_scale,
        args=['s', 's'],
        kwargs={},
        expected=1.0),
        id="SI_SCALE_008"),
    pytest.param(TestSpec(
        name="Valid unit 'Ts'",
        action=utils.si_scale,
        args=['Ts', 's'],
        kwargs={},
        expected=1e12),
        id="SI_SCALE_009"),
    pytest.param(TestSpec(
        name="Valid unit 'Gs'",
        action=utils.si_scale,
        args=['Gs', 's'],
        kwargs={},
        expected=1e9),
        id="SI_SCALE_010"),
    pytest.param(TestSpec(
        name="Valid unit 'Ms'",
        action=utils.si_scale,
        args=['Ms', 's'],
        kwargs={},
        expected=1e6),
        id="SI_SCALE_011"),
    pytest.param(TestSpec(
        name="Valid unit 'ks'",
        action=utils.si_scale,
        args=['ks', 's'],
        kwargs={},
        expected=1e3),
        id="SI_SCALE_012"),
    pytest.param(TestSpec(
        name="Valid unit ''",
        action=utils.si_scale,
        args=['s', 's'],
        kwargs={},
        expected=1.0),
        id="SI_SCALE_013"),
    pytest.param(TestSpec(
        name="Valid unit 'ms'",
        action=utils.si_scale,
        args=['ms', 's'],
        kwargs={},
        expected=1e-3),
        id="SI_SCALE_014"),
    pytest.param(TestSpec(
        name="Valid unit 'μs'",
        action=utils.si_scale,
        args=['μs', 's'],  # '\u03bc' Greek Small Letter Mu (SI standard)
        kwargs={},
        expected=1e-6),
        id="SI_SCALE_015"),
    pytest.param(TestSpec(
        name="Valid unit 'µs'",
        action=utils.si_scale,
        args=['µs', 's'],  # '\u00b5' Micro Sign (legacy Unicode compatibility)
        kwargs={},
        expected=1e-6),
        id="SI_SCALE_016"),
    pytest.param(TestSpec(
        name="Valid unit 'ns'",
        action=utils.si_scale,
        args=['ns', 's'],
        kwargs={},
        expected=1e-9),
        id="SI_SCALE_017"),
    pytest.param(TestSpec(
        name="Valid unit 'ps'",
        action=utils.si_scale,
        args=['ps', 's'],
        kwargs={},
        expected=1e-12),
        id="SI_SCALE_018"),
])
def test_si_scale(testspec: TestSpec) -> None:
    """Test utils.si_scale() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    pytest.param(TestSpec(
        name="missing base_unit arg",
        args=[],
        kwargs={'current_unit': 's', 'target_unit': 's'},
        action=utils.si_scale_to_unit,
        exception=TypeError),
        id="SI_SCALE_TO_UNIT_001"),
    pytest.param(TestSpec(
        name="missing current_unit arg",
        args=[],
        kwargs={'base_unit': 's', 'target_unit': 's'},
        action=utils.si_scale_to_unit,
        exception=TypeError),
        id="SI_SCALE_TO_UNIT_002"),
    pytest.param(TestSpec(
        name="missing target_unit arg",
        args=[],
        kwargs={'base_unit': 's', 'current_unit': 's'},
        action=utils.si_scale_to_unit,
        exception=TypeError),
        id="SI_SCALE_TO_UNIT_003"),
    pytest.param(TestSpec(
        name="invalid base_unit arg type (int)",
        args=[],
        kwargs={'base_unit': 1, 'current_unit': 's', 'target_unit': 's'},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE),
        id="SI_SCALE_TO_UNIT_004"),
    pytest.param(TestSpec(
        name="invalid current_unit arg type (int)",
        args=[],
        kwargs={'base_unit': 's', 'current_unit': 1, 'target_unit': 's'},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE),
        id="SI_SCALE_TO_UNIT_005"),
    pytest.param(TestSpec(
        name="invalid target_unit arg type (int)",
        args=[],
        kwargs={'base_unit': 's', 'current_unit': 's', 'target_unit': 1},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE),
        id="SI_SCALE_TO_UNIT_006"),
    pytest.param(TestSpec(
        name="empty base_unit arg",
        args=[],
        kwargs={'base_unit': '', 'current_unit': 's', 'target_unit': 's'},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG),
        id="SI_SCALE_TO_UNIT_007"),
    pytest.param(TestSpec(
        name="empty current_unit arg",
        args=[],
        kwargs={'base_unit': 's', 'current_unit': '', 'target_unit': 's'},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG),
        id="SI_SCALE_TO_UNIT_008"),
    pytest.param(TestSpec(
        name="empty target_unit arg",
        args=[],
        kwargs={'base_unit': 's', 'current_unit': 's', 'target_unit': ''},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG),
        id="SI_SCALE_TO_UNIT_009"),
    pytest.param(TestSpec(
        name="base_unit does not match other units",
        args=[],
        kwargs={'base_unit': 'm', 'current_unit': 'ms', 'target_unit': 'ms'},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS),
        id="SI_SCALE_TO_UNIT_010"),
    pytest.param(TestSpec(
        name="current_unit does not match other units",
        args=[],
        kwargs={'base_unit': 'ms', 'current_unit': 'm', 'target_unit': 'ms'},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS),
        id="SI_SCALE_TO_UNIT_011"),
    pytest.param(TestSpec(
        name="target_unit does not match other units",
        args=[],
        kwargs={'base_unit': 'ms', 'current_unit': 'ms', 'target_unit': 'm'},
        action=utils.si_scale_to_unit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS),
        id="SI_SCALE_TO_UNIT_012"),
    pytest.param(TestSpec(
        name="valid args, no scaling (s to s)",
        args=['s', 's', 's'],
        kwargs={},
        action=utils.si_scale_to_unit,
        expected=1.0),
        id="SI_SCALE_TO_UNIT_013"),
    pytest.param(TestSpec(
        name="valid args, scaling up (ms to s)",
        args=['s', 'ms', 's'],
        kwargs={},
        action=utils.si_scale_to_unit,
        expected=1e3),
        id="SI_SCALE_TO_UNIT_014"),
    pytest.param(TestSpec(
        name="valid args, scaling down (s to ms)",
        args=['s', 's', 'ms'],
        kwargs={},
        action=utils.si_scale_to_unit,
        expected=1e-3),
        id="SI_SCALE_TO_UNIT_015"),
])
def test_si_scale_to_unit(testspec: TestSpec) -> None:
    """Test utils.si_scale_to_unit() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    pytest.param(TestSpec(
        name="Missing unit arg",
        args=[],
        action=utils.si_unit_base,
        exception=TypeError),
        id="SI_UNIT_BASE_001"),
    pytest.param(TestSpec(
        name="Invalid unit arg type (int)",
        args=[1],
        action=utils.si_unit_base,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE),
        id="SI_UNIT_BASE_002"),
    pytest.param(TestSpec(
        name="Empty unit arg",
        args=[''],
        action=utils.si_unit_base,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_UNIT_BASE_EMPTY_UNIT_ARG),
        id="SI_UNIT_BASE_003"),
    pytest.param(TestSpec(
        name="Unknown prefix in unit",
        args=['xs'],
        action=utils.si_unit_base,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.UTILS_SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX),
        id="SI_UNIT_BASE_004"),
])
def test_si_unit_base(testspec: TestSpec) -> None:
    """Test utils.si_unit_base() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    pytest.param(TestSpec(
        name="Missing arguments",
        kwargs={},
        action=utils.si_scale_for_smallest,
        exception=TypeError),
        id="SI_SCALE_FOR_SMALLEST_001"),
    pytest.param(TestSpec(
        name="Invalid numbers arg type (int)",
        kwargs={'numbers': 1, 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE),
        id="SI_SCALE_FOR_SMALLEST_002"),
    pytest.param(TestSpec(
        name="Invalid numbers arg type (str)",
        kwargs={'numbers': 'not_a_list_of_numbers', 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE),
        id="SI_SCALE_FOR_SMALLEST_003"),
    pytest.param(TestSpec(
        name="Invalid numbers arg type (bytes)",
        kwargs={'numbers': b'not_a_list_of_numbers', 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE),
        id="SI_SCALE_FOR_SMALLEST_004"),
    pytest.param(TestSpec(
        name="Invalid numbers arg value type (list with str)",
        kwargs={'numbers': [1, 2, 'not_a_number'], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.UTILS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_VALUES_TYPE),
        id="SI_SCALE_FOR_SMALLEST_005"),
    pytest.param(TestSpec(
        name="Empty numbers list",
        kwargs={'numbers': [], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('s', 1.0)),
        id="SI_SCALE_FOR_SMALLEST_006"),
    pytest.param(TestSpec(
        name="List with one number",
        kwargs={'numbers': [0.01234], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('ms', 1e3)),
        id="SI_SCALE_FOR_SMALLEST_007"),
    pytest.param(TestSpec(
        name="List with multiple numbers",
        kwargs={'numbers': [0.01234, 0.0005678, 0.000009], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('μs', 1e6)),
        id="SI_SCALE_FOR_SMALLEST_008"),
    pytest.param(TestSpec(
        name="List with zero and positive numbers",
        kwargs={'numbers': [0.0, 0.01234, 0.0005678, 0.000009], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('μs', 1e6)),
        id="SI_SCALE_FOR_SMALLEST_009"),
    pytest.param(TestSpec(
        name="List with negative and positive numbers",
        kwargs={'numbers': [-0.01234, 0.0005678, -0.000009], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('μs', 1e6)),
        id="SI_SCALE_FOR_SMALLEST_010"),
    pytest.param(TestSpec(
        name="List with all zeros",
        kwargs={'numbers': [0.0, 0.0, 0.0], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('s', 1.0)),
        id="SI_SCALE_FOR_SMALLEST_011"),
    pytest.param(TestSpec(
        name="List with all zeros and negative zeros",
        kwargs={'numbers': [0.0, -0.0, 0.0], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('s', 1.0)),
        id="SI_SCALE_FOR_SMALLEST_012"),
    pytest.param(TestSpec(
        name="List with very large and very small numbers",
        kwargs={'numbers': [1e12, 1e-12, 1e6, 1e-6], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('ps', 1e12)),
        id="SI_SCALE_FOR_SMALLEST_013"),
    pytest.param(TestSpec(
        name="List with one very large number",
        kwargs={'numbers': [1e12], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('Ts', 1e-12)),
        id="SI_SCALE_FOR_SMALLEST_014"),
    pytest.param(TestSpec(
        name="List with one very small number",
        kwargs={'numbers': [1e-12], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('ps', 1e12)),
        id="SI_SCALE_FOR_SMALLEST_015"),
    pytest.param(TestSpec(
        name="List with mixed int and float numbers",
        kwargs={'numbers': [1234, 0.5678, -9], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('ms', 1e3)),
        id="SI_SCALE_FOR_SMALLEST_016"),
    pytest.param(TestSpec(
        name="List with EXTREMELY small numbers",
        kwargs={'numbers': [1e-30, 1e-25, 1e-32], 'base_unit': 's'},
        action=utils.si_scale_for_smallest,
        expected=('fs', 1e15)),
        id="SI_SCALE_FOR_SMALLEST_017"),
])
def test_si_scale_for_smallest(testspec: TestSpec) -> None:
    """Test utils.si_scale_for_smallest() function."""
    testspec.run()
