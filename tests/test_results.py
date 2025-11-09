"""Tests for the simplebench/results.py module."""
from __future__ import annotations
from enum import Enum
from functools import cache

import pytest

from simplebench.defaults import (DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT,
                                  DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT)
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ResultsErrorTag
from simplebench.iteration import Iteration
from simplebench.results import Results
from simplebench.enums import Section
from simplebench.stats import OperationsPerInterval, OperationTimings, MemoryUsage, PeakMemoryUsage, Stats

from .kwargs import ResultsKWArgs
from .testspec import TestAction, TestGet, idspec, Assert


class Nonsense(str, Enum):
    """A nonsense enum value for testing."""
    NONSENSE = 'nonsense'


@cache
def base_iterations() -> list[Iteration]:
    """Create a base list of Iteration instances for testing."""
    return [
        Iteration(n=1, unit='s', elapsed=1.0, scale=1.0, memory=100, peak_memory=150)
    ]


@pytest.mark.parametrize("testspec", [
    idspec("RESULTS_000", TestAction(
        name="Minimal Args",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group',
            title='default_title',
            description='default_description',
            n=1,
            rounds=1,
            total_elapsed=1.0,
            iterations=base_iterations()),
        assertion=Assert.ISINSTANCE,
        expected=Results,
    )),
    idspec("RESULTS_001", TestAction(
        name="Default Values",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group',
            title='default_title',
            description='default_description',
            n=1,
            rounds=1,
            total_elapsed=1.0,
            iterations=base_iterations()),
        validate_result=lambda result: (result.group == 'default_group' and
                                        result.title == 'default_title' and
                                        result.description == 'default_description' and
                                        result.n == 1 and
                                        result.rounds == 1 and
                                        result.variation_cols == {} and
                                        result.interval_unit == DEFAULT_INTERVAL_UNIT and
                                        result.interval_scale == DEFAULT_INTERVAL_SCALE and
                                        len(result.iterations) == 1 and
                                        isinstance(result.ops_per_second, OperationsPerInterval) and
                                        result.ops_per_second.data == (1.0,) and
                                        isinstance(result.per_round_timings, OperationTimings) and
                                        result.per_round_timings.data == (1.0,) and
                                        isinstance(result.memory, MemoryUsage) and
                                        result.memory.data == (100,) and
                                        isinstance(result.peak_memory, PeakMemoryUsage) and
                                        result.peak_memory.data == (150,) and
                                        result.ops_per_interval_unit == DEFAULT_INTERVAL_UNIT and
                                        result.ops_per_interval_scale == DEFAULT_INTERVAL_SCALE and
                                        result.memory_unit == DEFAULT_MEMORY_UNIT and
                                        result.memory_scale == DEFAULT_MEMORY_SCALE and
                                        result.total_elapsed == 1.0 and
                                        result.variation_marks == {} and
                                        result.extra_info == {} and
                                        isinstance(result, Results)))),
    idspec("RESULTS_002", TestAction(
        name="negative n",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group',
            title='default_title',
            description='default_description',
            n=-1,
            rounds=1,
            total_elapsed=1.0,
            iterations=base_iterations()
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.N_INVALID_ARG_VALUE)),
    idspec("RESULTS_003", TestAction(
        name="non-integer n",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group',
            title='default_title',
            description='default_description',
            n=1.5,  # type: ignore[arg-type]
            rounds=1,
            total_elapsed=1.0,
            iterations=base_iterations()
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.N_INVALID_ARG_TYPE)),
    idspec("RESULTS_004", TestAction(
        name="non-string group",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group=123,  # type: ignore[arg-type]
            title='default_title',
            description='default_description',
            n=1,
            rounds=1,
            total_elapsed=1.0,
            iterations=base_iterations()
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.GROUP_INVALID_ARG_TYPE)),
    idspec("RESULTS_005", TestAction(
        name="non-string title",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group',
            title=123,  # type: ignore[arg-type]
            description='default_description',
            n=1,
            rounds=1,
            total_elapsed=1.0,
            iterations=base_iterations()
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.TITLE_INVALID_ARG_TYPE)),
    idspec("RESULTS_006", TestAction(
        name="non-string description",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group',
            title='default_title',
            description=123,  # type: ignore[arg-type]
            n=1,
            rounds=1,
            total_elapsed=1.0,
            iterations=base_iterations()
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.DESCRIPTION_INVALID_ARG_TYPE)),
    idspec("RESULTS_007", TestAction(
        name="non-dict variation_cols",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_cols=[]  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE)),
    idspec("RESULTS_008", TestAction(
        name="non-string variation_cols key",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_cols={1: 'value'}  # type: ignore[dict-item]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_TYPE)),
    idspec("RESULTS_009", TestAction(
        name="non-string variation_cols value",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_cols={'key': 1}  # type: ignore[dict-item]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_VALUE_TYPE)),
    idspec("RESULTS_010", TestAction(
        name="non-string interval_unit",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            interval_unit=123  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.INTERVAL_UNIT_INVALID_ARG_TYPE)),
    idspec("RESULTS_011", TestAction(
        name="non-float interval_scale",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            interval_scale='large'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.INTERVAL_SCALE_INVALID_ARG_TYPE)),
    idspec("RESULTS_012", TestAction(
        name="non-list iterations with dict",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0,
            iterations={}  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.ITERATIONS_INVALID_ARG_TYPE)),
    idspec("RESULTS_013", TestAction(
        name="non-list iterations with string",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0,
            iterations='not_a_list'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.ITERATIONS_INVALID_ARG_IN_SEQUENCE)),
    idspec("RESULTS_014", TestAction(
        name="non-Iteration iterations elements",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0,
            iterations=[1.0, 3.0]  # type: ignore[list-item]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.ITERATIONS_INVALID_ARG_IN_SEQUENCE)),
    idspec("RESULTS_015", TestAction(
        name="non-OperationsPerInterval ops_per_second",
        action=Results,
        args=[],
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_second={}  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.OPS_PER_SECOND_INVALID_ARG_TYPE)),
    idspec("RESULTS_016", TestAction(
        name="non-OperationTimings per_round_timings",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            per_round_timings=[]  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.PER_ROUND_TIMINGS_INVALID_ARG_TYPE)),
    idspec("RESULTS_017", TestAction(
        name="non-string ops_per_interval_unit",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_interval_unit=123  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.OPS_PER_INTERVAL_UNIT_INVALID_ARG_TYPE)),
    idspec("RESULTS_018", TestAction(
        name="non-number ops_per_interval_scale",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_interval_scale='large'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.OPS_PER_INTERVAL_SCALE_INVALID_ARG_TYPE)),
    idspec("RESULTS_019", TestAction(
        name="non-number total_elapsed",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, iterations=base_iterations(),
            total_elapsed='fast'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.TOTAL_ELAPSED_INVALID_ARG_TYPE)),
    idspec("RESULTS_020", TestAction(
        name="non-dict variation_marks",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_marks=[]  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE)),
    idspec("RESULTS_021", TestAction(
        name="non-string variation_marks key",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_marks={1: 'value'}  # type: ignore[dict-item]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_TYPE)),
    idspec("RESULTS_022", TestAction(
        name="non-dict variation_marks value",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_marks=[('key', 1)]  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE)),
    idspec("RESULTS_023", TestAction(
        name="non-dict extra_info",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            extra_info=[]  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.EXTRA_INFO_INVALID_ARG_TYPE)),
    idspec("RESULTS_024", TestAction(
        name="empty string group",
        action=Results,
        kwargs=ResultsKWArgs(
            title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            group=''  # invalid empty string
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.GROUP_INVALID_ARG_VALUE)),
    idspec("RESULTS_025", TestAction(
        name="empty string title",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            title='',  # invalid empty string
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.TITLE_INVALID_ARG_VALUE)),
    idspec("RESULTS_026", TestAction(
        name="empty string variation_cols key",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_cols={'': 'value'}  # invalid empty string key
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_VALUE)),
    idspec("RESULTS_027", TestAction(
        name="empty string interval_unit",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            interval_unit=''  # invalid empty string
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.INTERVAL_UNIT_INVALID_ARG_VALUE)),
    idspec("RESULTS_028", TestAction(
        name="empty string ops_per_interval_unit",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_interval_unit=''  # invalid empty string
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.OPS_PER_INTERVAL_UNIT_INVALID_ARG_VALUE)),
    idspec("RESULTS_029", TestAction(
        name="negative interval_scale",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            interval_scale=-1.0  # invalid negative value
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_030", TestAction(
        name="zero interval_scale",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            interval_scale=0.0  # invalid zero value
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_031", TestAction(
        name="negative ops_per_interval_scale",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_interval_scale=-1.0  # invalid negative value
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_032", TestAction(
        name="zero ops_per_interval_scale",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_interval_scale=0.0  # invalid zero value
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE)),
    idspec("RESULTS_033", TestAction(
        name="negative total_elapsed",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, iterations=base_iterations(),
            total_elapsed=-1.0  # invalid negative value
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.TOTAL_ELAPSED_INVALID_ARG_VALUE)),
    idspec("RESULTS_034", TestAction(
        name="blank string variation_marks key",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            variation_marks={' ': 'value'}),  # invalid blank string key
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_VALUE)),
    idspec("RESULTS_035", TestAction(
        name="Wrong type for peak_memory argument (str instead of PeakMemoryUsage)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            peak_memory='invalid_type'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.PEAK_MEMORY_INVALID_ARG_TYPE)),
    idspec("RESULTS_036", TestAction(
        name="Correct type for peak_memory argument (PeakMemoryUsage)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            peak_memory=PeakMemoryUsage(unit='bytes', scale=1.0, data=[150])),
        assertion=Assert.ISINSTANCE,
        expected=Results)),
    idspec("RESULTS_037", TestAction(
        name="Wrong type for memory argument (str instead of MemoryUsage)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            memory='invalid_type'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.MEMORY_INVALID_ARG_TYPE)),
    idspec("RESULTS_038", TestAction(
        name="Correct type for memory argument (MemoryUsage)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            memory=MemoryUsage(unit='bytes', scale=1.0, data=[150])
        ),
        assertion=Assert.ISINSTANCE,
        expected=Results)),
    idspec("RESULTS_039", TestAction(
        name="Wrong type for per_round_timings argument (str instead of OperationTimings)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            per_round_timings='invalid_type'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.PER_ROUND_TIMINGS_INVALID_ARG_TYPE)),
    idspec("RESULTS_040", TestAction(
        name="Correct type for per_round_timings argument (OperationTimings)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            per_round_timings=OperationTimings(unit='s', scale=1.0, data=[1.0])
        ),
        assertion=Assert.ISINSTANCE,
        expected=Results)),
    idspec("RESULTS_041", TestAction(
        name="Wrong type for ops_per_second argument (str instead of OperationsPerInterval)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_second='invalid_type'  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.OPS_PER_SECOND_INVALID_ARG_TYPE)),
    idspec("RESULTS_042", TestAction(
        name="Correct type for ops_per_second argument (OperationsPerInterval)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations(),
            ops_per_second=OperationsPerInterval(unit='ops/s', scale=1.0, data=[1.0])
        ),
        assertion=Assert.ISINSTANCE,
        expected=Results)),
    idspec("RESULTS_043", TestAction(
        name="Correct type for rounds argument (int)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=1, total_elapsed=1.0, iterations=base_iterations()
        ),
        assertion=Assert.ISINSTANCE,
        expected=Results)),
    idspec("RESULTS_044", TestAction(
        name="Wrong type for rounds argument (str instead of int)",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds='invalid_type', total_elapsed=1.0, iterations=base_iterations()  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ResultsErrorTag.ROUNDS_INVALID_ARG_TYPE)),
    idspec("RESULTS_045", TestAction(
        name="Negative value for rounds argument",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=-1, total_elapsed=1.0, iterations=base_iterations()
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.ROUNDS_INVALID_ARG_VALUE)),
    idspec("RESULTS_046", TestAction(
        name="Zero value for rounds argument",
        action=Results,
        kwargs=ResultsKWArgs(
            group='default_group', title='default_title', description='default_description',
            n=1, rounds=0, total_elapsed=1.0, iterations=base_iterations()
        ),
        exception=SimpleBenchValueError,
        exception_tag=ResultsErrorTag.ROUNDS_INVALID_ARG_VALUE)),
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
        n=1,
        rounds=1,
        total_elapsed=1.0,
        iterations=[Iteration(n=1, elapsed=0.1), Iteration(n=2, elapsed=0.2), Iteration(n=3, elapsed=0.3)],
    )


@cache
def getattribute_results() -> Results:
    """Create a Results instance for testing getting attributes."""
    return Results(
        group='test_group',
        title='test_title',
        description='test_description',
        n=1,
        rounds=1,
        total_elapsed=1.0,
        iterations=[Iteration(n=1, elapsed=0.1), Iteration(n=2, elapsed=0.2), Iteration(n=3, elapsed=0.3)],
        variation_cols={'size': 'N', 'type': 'test'},
        variation_marks={'size': 1, 'type': 'A'},
    )


@pytest.mark.parametrize("testspec", [
    idspec("GET_001", TestGet(
        name="Get non-existent attribute",
        attribute='non_existent_attr',
        obj=getattribute_results(),
        exception=AttributeError)),
    idspec("GET_002", TestGet(
        name="Get 'group' attribute",
        attribute='group',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected='test_group')),
    idspec("GET_003", TestGet(
        name="Get 'title' attribute",
        attribute='title',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected='test_title')),
    idspec("GET_004", TestGet(
        name="Get 'description' attribute",
        attribute='description',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected='test_description')),
    idspec("GET_005", TestGet(
        name="Get 'n' attribute",
        attribute='n',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=1)),
    idspec("GET_006", TestGet(
        name="Get 'total_elapsed' attribute",
        attribute='total_elapsed',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=1.0)),
    idspec("GET_007", TestGet(
        name="Get 'iterations' attribute",
        attribute='iterations',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=(Iteration(n=1, elapsed=0.1), Iteration(n=2, elapsed=0.2), Iteration(n=3, elapsed=0.3)))),
    idspec("GET_008", TestGet(
        name="Get 'variation_cols' attribute",
        attribute='variation_cols',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected={'size': 'N', 'type': 'test'})),
    idspec("GET_009", TestGet(
        name="Get 'variation_marks' attribute",
        attribute='variation_marks',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected={'size': 1, 'type': 'A'})),
    idspec("GET_010", TestGet(
        name="Get 'interval_unit' attribute",
        attribute='interval_unit',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=DEFAULT_INTERVAL_UNIT)),
    idspec("GET_011", TestGet(
        name="Get 'interval_scale' attribute",
        attribute='interval_scale',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=DEFAULT_INTERVAL_SCALE)),
    idspec("GET_012", TestGet(
        name="Get 'ops_per_second' attribute",
        attribute='ops_per_second',
        assertion=Assert.ISINSTANCE,
        obj=getattribute_results(),
        expected=OperationsPerInterval)),
    idspec("GET_013", TestGet(
        name="Get 'per_round_timings' attribute",
        attribute='per_round_timings',
        assertion=Assert.ISINSTANCE,
        obj=getattribute_results(),
        expected=OperationTimings)),
    idspec("GET_014", TestGet(
        name="Get 'memory' attribute",
        attribute='memory',
        assertion=Assert.ISINSTANCE,
        obj=getattribute_results(),
        expected=MemoryUsage)),
    idspec("GET_015", TestGet(
        name="Get 'peak_memory' attribute",
        attribute='peak_memory',
        assertion=Assert.ISINSTANCE,
        obj=getattribute_results(),
        expected=PeakMemoryUsage)),
    idspec("GET_016", TestGet(
        name="Get 'ops_per_interval_unit' attribute",
        attribute='ops_per_interval_unit',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=DEFAULT_INTERVAL_UNIT)),
    idspec("GET_017", TestGet(
        name="Get 'ops_per_interval_scale' attribute",
        attribute='ops_per_interval_scale',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=DEFAULT_INTERVAL_SCALE)),
    idspec("GET_018", TestGet(
        name="Get 'memory_unit' attribute",
        attribute='memory_unit',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=DEFAULT_MEMORY_UNIT)),
    idspec("GET_019", TestGet(
        name="Get 'memory_scale' attribute",
        attribute='memory_scale',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected=DEFAULT_MEMORY_SCALE)),
    idspec("GET_020", TestGet(
        name="Get 'extra_info' attribute",
        attribute='extra_info',
        assertion=Assert.EQUAL,
        obj=getattribute_results(),
        expected={})),
])
def test_getattribute(testspec: TestGet) -> None:
    """Test getting attributes from Results."""
    testspec.run()


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


def test_results_sections_invalid() -> None:
    """Test Results sections property with unsupported or invalid sections."""
    results = base_results()
    with pytest.raises(SimpleBenchValueError) as excinfo:
        results.results_section(Section.NULL)
    assert excinfo.value.tag_code == ResultsErrorTag.RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE, (
        f"Expected SimpleBenchValueError for unsupported section {Section.NULL}"
    )

    with pytest.raises(SimpleBenchTypeError) as excinfo1:
        results.results_section(Nonsense.NONSENSE)  # type: ignore[arg-type]
    assert excinfo1.value.tag_code == ResultsErrorTag.RESULTS_SECTION_INVALID_SECTION_ARG_TYPE, (
        f"Expected SimpleBenchTypeError for invalid section type {type(Nonsense.NONSENSE)}"
    )
