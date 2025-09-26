"""Tests for the simplebench/results.py module."""
from __future__ import annotations
from enum import Enum
from functools import cache

import pytest

from simplebench.constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from simplebench.iteration import Iteration
from simplebench.results import Results
from simplebench.enums import Section
from simplebench.stats import OperationsPerInterval, OperationTimings, MemoryUsage, PeakMemoryUsage, Stats

from .testspec import TestAction, TestSetGet, idspec


class Nonsense(str, Enum):
    """A nonsense enum value for testing."""
    NONESENSE = 'nonsense'


@pytest.mark.parametrize("testspec", [
    idspec("RESULTS_001", TestAction(
        name="Default Values",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1
        },
        validate_result=lambda result: (result.group == 'default_group' and
                                        result.title == 'default_title' and
                                        result.description == 'default_description' and
                                        result.n == 1 and
                                        result.variation_cols == {} and
                                        result.interval_unit == DEFAULT_INTERVAL_UNIT and
                                        result.interval_scale == DEFAULT_INTERVAL_SCALE and
                                        result.iterations == [] and
                                        isinstance(result.ops_per_second, OperationsPerInterval) and
                                        result.ops_per_second.data == [] and
                                        isinstance(result.per_round_timings, OperationTimings) and
                                        result.per_round_timings.data == [] and
                                        result.ops_per_interval_unit == DEFAULT_INTERVAL_UNIT and
                                        result.ops_per_interval_scale == DEFAULT_INTERVAL_SCALE and
                                        result.total_elapsed == 0 and
                                        result.variation_marks == {} and
                                        result.extra_info == {} and
                                        isinstance(result, Results)))),
    idspec("RESULTS_002", TestAction(
        name="negative n",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': -1
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_N_INVALID_ARG_VALUE)),
    idspec("RESULTS_003", TestAction(
        name="non-integer n",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1.5
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_N_INVALID_ARG_TYPE)),
    idspec("RESULTS_004", TestAction(
        name="non-string group",
        action=Results,
        args=[],
        kwargs={
            'group': 123,
            'title': 'default_title',
            'description': 'default_description',
            'n': 1
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_GROUP_INVALID_ARG_TYPE)),
    idspec("RESULTS_005", TestAction(
        name="non-string title",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 123,
            'description': 'default_description',
            'n': 1
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_TITLE_INVALID_ARG_TYPE)),
    idspec("RESULTS_006", TestAction(
        name="non-string description",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 123,
            'n': 1
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_DESCRIPTION_INVALID_ARG_TYPE)),
    idspec("RESULTS_007", TestAction(
        name="non-dict variation_cols",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'variation_cols': []
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_TYPE)),
    idspec("RESULTS_008", TestAction(
        name="non-string variation_cols key",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'variation_cols': {1: 'value'}
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_KEY_TYPE)),
    idspec("RESULTS_009", TestAction(
        name="non-string variation_cols value",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'variation_cols': {'key': 1}
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_VALUE_TYPE)),
    idspec("RESULTS_010", TestAction(
        name="non-string interval_unit",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'interval_unit': 123
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_INTERVAL_UNIT_INVALID_ARG_TYPE)),
    idspec("RESULTS_011", TestAction(
        name="non-float interval_scale",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'interval_scale': 'large'
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_INTERVAL_SCALE_INVALID_ARG_TYPE)),
    idspec("RESULTS_012", TestAction(
        name="non-list iterations with dict",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'iterations': {}
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_ITERATIONS_INVALID_ARG_TYPE)),
    idspec("RESULTS_013", TestAction(
        name="non-list iterations with string",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'iterations': 'not_a_list'
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_ITERATIONS_INVALID_ARG_TYPE)),
    idspec("RESULTS_014", TestAction(
        name="non-float iterations element",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'iterations': [1.0, 'two', 3.0]
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_ITERATIONS_INVALID_ARG_IN_SEQUENCE)),
    idspec("RESULTS_015", TestAction(
        name="non-OperationsPerInterval ops_per_second",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'ops_per_second': {}
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_OPS_PER_SECOND_INVALID_ARG_TYPE)),
    idspec("RESULTS_016", TestAction(
        name="non-OperationTimings per_round_timings",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'per_round_timings': []
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_PER_ROUND_TIMINGS_INVALID_ARG_TYPE)),
    idspec("RESULTS_017", TestAction(
        name="non-string ops_per_interval_unit",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'ops_per_interval_unit': 123
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_TYPE)),
    idspec("RESULTS_018", TestAction(
        name="non-number ops_per_interval_scale",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'ops_per_interval_scale': 'large'
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_TYPE)),
    idspec("RESULTS_019", TestAction(
        name="non-number total_elapsed",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'total_elapsed': 'fast'
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_TOTAL_ELAPSED_INVALID_ARG_TYPE)),
    idspec("RESULTS_020", TestAction(
        name="non-dict variation_marks",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'variation_marks': []
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_VARIATION_MARKS_INVALID_ARG_TYPE)),
    idspec("RESULTS_021", TestAction(
        name="non-string variation_marks key",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'variation_marks': {1: 'value'}
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_VARIATION_MARKS_INVALID_ARG_KEY_TYPE)),
    idspec("RESULTS_022", TestAction(
        name="non-dict variation_marks value",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'variation_marks': [('key', 1)]
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_VARIATION_MARKS_INVALID_ARG_TYPE)),
    idspec("RESULTS_023", TestAction(
        name="non-dict extra_info",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'extra_info': []
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.RESULTS_EXTRA_INFO_INVALID_ARG_TYPE)),
    idspec("RESULTS_024", TestAction(
        name="empty string group",
        action=Results,
        args=[],
        kwargs={
            'group': '',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_GROUP_INVALID_ARG_VALUE)),
    idspec("RESULTS_025", TestAction(
        name="empty string title",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': '',
            'description': 'default_description',
            'n': 1
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_TITLE_INVALID_ARG_VALUE)),
    idspec("RESULTS_026", TestAction(
        name="empty string variation_cols key",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'variation_cols': {'': 'value'}
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_KEY_VALUE)),
    idspec("RESULTS_027", TestAction(
        name="empty string interval_unit",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'interval_unit': ''
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_INTERVAL_UNIT_INVALID_ARG_VALUE)),
    idspec("RESULTS_028", TestAction(
        name="empty string ops_per_interval_unit",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'ops_per_interval_unit': ''
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_VALUE)),
    idspec("RESULTS_029", TestAction(
        name="negative interval_scale",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'interval_scale': -1.0
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_030", TestAction(
        name="zero interval_scale",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'interval_scale': 0.0
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_031", TestAction(
        name="negative ops_per_interval_scale",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'ops_per_interval_scale': -1.0
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_032", TestAction(
        name="zero ops_per_interval_scale",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'ops_per_interval_scale': 0.0
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_033", TestAction(
        name="negative total_elapsed",
        action=Results,
        args=[],
        kwargs={
            'group': 'default_group',
            'title': 'default_title',
            'description': 'default_description',
            'n': 1,
            'total_elapsed': -1.0
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.RESULTS_TOTAL_ELAPSED_INVALID_ARG_VALUE)),
])
def test_results_init(testspec: TestAction) -> None:
    """Test Results initialization."""
    testspec.run()


@cache
def base_results() -> Results:
    """Create a base Results instance for testing."""
    return Results(
        group='test_group',
        title='test_title',
        description='test_description',
        n=1
    )


@cache
def base_operations_per_interval() -> OperationsPerInterval:
    """Create a base OperationsPerInterval instance for testing."""
    return OperationsPerInterval(
        unit='ops/second',
        scale=1.0,
        data=[100.0, 200.0, 300.0]
    )


@cache
def base_per_round_timings() -> OperationTimings:
    """Create a base OperationTimings instance for testing."""
    return OperationTimings(
        unit='seconds',
        scale=1.0,
        data=[0.01, 0.02, 0.03]
    )


@pytest.mark.parametrize("testspec", [
    idspec("PROPERTIES_001", TestSetGet(
        name='set/get group',
        attribute='group',
        value='new_group',
        expected='new_group',
        obj=base_results())),
    idspec("PROPERTIES_002", TestSetGet(
        name='set/get title',
        attribute='title',
        value='new_title',
        expected='new_title',
        obj=base_results())),
    idspec("PROPERTIES_003", TestSetGet(
        name='set/get description',
        attribute='description',
        value='new_description',
        expected='new_description',
        obj=base_results())),
    idspec("PROPERTIES_004", TestSetGet(
        name='set/get n',
        attribute='n',
        value=5,
        expected=5,
        obj=base_results())),
    idspec("PROPERTIES_005", TestSetGet(
        name='set/get variation_cols',
        attribute='variation_cols',
        value={'key': 'value'},
        expected={'key': 'value'},
        obj=base_results())),
    idspec("PROPERTIES_006", TestSetGet(
        name='set/get interval_unit',
        attribute='interval_unit',
        value='minutes',
        expected='minutes',
        obj=base_results())),
    idspec("PROPERTIES_007", TestSetGet(
        name='set/get interval_scale',
        attribute='interval_scale',
        value=60.0,
        expected=60.0,
        obj=base_results())),
    idspec("PROPERTIES_008", TestSetGet(
        name='set/get iterations',
        attribute='iterations',
        value=[Iteration(n=1, elapsed=0.1), Iteration(n=2, elapsed=0.2), Iteration(n=3, elapsed=0.3)],
        expected=[Iteration(n=1, elapsed=0.1), Iteration(n=2, elapsed=0.2), Iteration(n=3, elapsed=0.3)],
        obj=base_results())),
    idspec("PROPERTIES_009", TestSetGet(
        name='set/get ops_per_second',
        attribute='ops_per_second',
        value=base_operations_per_interval(),
        expected=base_operations_per_interval(),
        obj=base_results())),
    idspec("PROPERTIES_010", TestSetGet(
        name='set/get per_round_timings',
        attribute='per_round_timings',
        value=base_per_round_timings(),
        expected=base_per_round_timings(),
        obj=base_results())),
    idspec("PROPERTIES_011", TestSetGet(
        name='set/get ops_per_interval_unit',
        attribute='ops_per_interval_unit',
        value='ops/minute',
        expected='ops/minute',
        obj=base_results())),
    idspec("PROPERTIES_012", TestSetGet(
        name='set/get ops_per_interval_scale',
        attribute='ops_per_interval_scale',
        value=60.0,
        expected=60.0,
        obj=base_results())),
    idspec("PROPERTIES_013", TestSetGet(
        name='set/get total_elapsed',
        attribute='total_elapsed',
        value=1.5,
        expected=1.5,
        obj=base_results())),
    idspec("PROPERTIES_014", TestSetGet(
        name='set/get variation_marks',
        attribute='variation_marks',
        value={'key': 'value'},
        expected={'key': 'value'},
        obj=base_results())),
    idspec("PROPERTIES_015", TestSetGet(
        name='set/get extra_info',
        attribute='extra_info',
        value={'key': 'value'},
        expected={'key': 'value'},
        obj=base_results())),
])
def test_results_getset_properties(testspec: TestSetGet) -> None:
    """Test Results get/set properties."""
    testspec.run()


@pytest.mark.parametrize("section", [
    pytest.param(Section.OPS, id="Section.OPS"),
    pytest.param(Section.TIMING, id="Section.TIMING"),
    pytest.param(Section.MEMORY, id="Section.MEMORY"),
    pytest.param(Section.PEAK_MEMORY, id="Section.PEAK_MEMORY"),
])
def test_results_sections(section: Section) -> None:
    """Test Results sections property."""
    results = base_results()
    section_value = results.results_section(section)
    assert isinstance(section_value, Stats), (
        f"results_section({section}) should be type Stats not {type(section_value)}")
