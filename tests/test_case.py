"""Tests for the case.py module."""
from __future__ import annotations
from argparse import ArgumentParser
from functools import cache
from typing import Any

import pytest

from simplebench import Case, SimpleRunner, Results, Session, Verbosity
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag

from .testspec import TestAction, idspec, Assert


def benchcase(bench: SimpleRunner, **kwargs: Any) -> Results:
    """A simple benchmark case function."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


def broken_benchcase_missing_bench(**kwargs: Any) -> Results:
    """A broken benchmark case function that is missing the required 'bench' parameter."""
    bench = SimpleRunner(
        case=Case(
            group='example',
            title='benchcase',
            action=benchcase,
            description='A simple benchmark case.'),
        kwargs={})

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


def broken_benchcase_missing_kwargs(bench: SimpleRunner) -> Results:
    """A broken benchmark case function that is missing the required '**kwargs' parameter."""
    kwargs: dict[str, Any] = {}

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


def broken_benchcase_wrong_kwargs_kind(bench: SimpleRunner, kwargs: dict[str, Any]) -> Results:
    """A broken benchmark case function that has the wrong kind of kwargs parameter (should be '**kwargs')."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


@cache
def postrun_benchmark_case() -> Case:
    """Creates and runs a benchmark Case, returning the Case instance."""
    case = Case(
        group='example',
        title='benchcase',
        action=benchcase,
        description='A simple benchmark case.',
        variation_cols={},
        kwargs_variations={},
        options=[]
    )

    argparse = ArgumentParser()
    session = Session(args_parser=argparse, cases=[case], verbosity=Verbosity.QUIET, progress=False)
    session.run()

    return case


@pytest.mark.parametrize("testspec", [
    idspec("INIT_001", TestAction(
        name="Minimal good path initialization",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
        },
        assertion=Assert.ISINSTANCE,
        expected=Case,
    )),
    idspec("INIT_002", TestAction(
        name="Maximal good path initialization",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'iterations': 100,
            'warmup_iterations': 10,
            'min_time': 0.1,
            'max_time': 10.0,
            'variation_cols': {},
            'kwargs_variations': {},
            'options': []
        },
        assertion=Assert.ISINSTANCE,
        expected=Case,
    )),
    idspec("INIT_003", TestAction(
        name="Missing group parameter",
        action=Case,
        kwargs={
            'title': 'benchcase',
            'description': 'A simple benchmark case',
            'action': benchcase,
        },
        exception=TypeError,
    )),
    idspec("INIT_004", TestAction(
        name="Missing title parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'description': 'A simple benchmark case.',
            'action': benchcase,
        },
        exception=TypeError)),
    idspec("INIT_005", TestAction(
        name="Missing description parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'action': benchcase,
        },
        exception=TypeError)),
    idspec("INIT_006", TestAction(
        name="Missing action parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
        },
        exception=TypeError)),
    idspec("INIT_007", TestAction(
        name="Wrong type for group parameter",
        action=Case,
        kwargs={
            'group': 123,  # type: ignore[arg-type]
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_GROUP_TYPE)),
    idspec("INIT_008", TestAction(
        name="Invalid (blank) value for group parameter",
        action=Case,
        kwargs={
            'group': ' ',  # Invalid blank string
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_GROUP_VALUE)),
    idspec("INIT_009", TestAction(
        name="Wrong type for title parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 123,  # type: ignore[arg-type]
            'description': 'A simple benchmark case.',
            'action': benchcase,
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_TITLE_TYPE)),
    idspec("INIT_010", TestAction(
        name="Invalid (blank) value for title parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': ' ',  # Invalid blank string
            'description': 'A simple benchmark case.',
            'action': benchcase,
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_TITLE_VALUE)),
    idspec("INIT_011", TestAction(
        name="Wrong type for description parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 123,  # type: ignore[arg-type]
            'action': benchcase,
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_DESCRIPTION_TYPE)),
    idspec("INIT_012", TestAction(
        name="Invalid (blank) value for description parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': ' ',  # Invalid blank string
            'action': benchcase,
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_DESCRIPTION_VALUE)),
    idspec("INIT_013", TestAction(
        name="Wrong type for 'action' parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': 'not_a_function',  # type: ignore[arg-type]
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_NOT_CALLABLE)),
    idspec("INIT_014", TestAction(
        name="'action' function does not accept required argument 'bench'",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': broken_benchcase_missing_bench  # does not accept (bench)
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_MISSING_BENCH_PARAMETER)),
    idspec("INIT_015", TestAction(
        name="'action' function does not accept required argument '**kwargs'",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': broken_benchcase_missing_kwargs  # does not accept any kwargs
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_MISSING_KWARGS_PARAMETER)),
    idspec("INIT_016", TestAction(
        name="'action' function is using wrong form for kwargs: Should specifically be '**kwargs'",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': broken_benchcase_wrong_kwargs_kind  # does not specifically accept **kwargs
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_MISSING_KWARGS_PARAMETER)),
    idspec("INIT_017", TestAction(
        name="Wrong type for iterations parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'iterations': 'not_an_int',  # type: ignore[arg-type]
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ITERATIONS_TYPE)),
    idspec("INIT_018", TestAction(
        name="Invalid (non-positive) value for iterations parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'iterations': 0,  # Invalid non-positive value
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_ITERATIONS_VALUE)),
    idspec("INIT_019", TestAction(
        name="Wrong type for warmup_iterations parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'warmup_iterations': 'not_an_int',  # type: ignore[arg-type]
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_TYPE)),
    idspec("INIT_020", TestAction(
        name="Invalid (negative) value for warmup_iterations parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'warmup_iterations': -1,  # Invalid negative value
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_VALUE)),
    idspec("INIT_021", TestAction(
        name="Wrong type for min_time parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'min_time': 'not_a_float',  # type: ignore[arg-type]
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_MIN_TIME_TYPE)),
    idspec("INIT_022", TestAction(
        name="Invalid (non-positive) value for min_time parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'min_time': 0.0,  # Invalid non-positive value
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_MIN_TIME_VALUE)),
    idspec("INIT_023", TestAction(
        name="Wrong type for max_time parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'max_time': 'not_a_float',  # type: ignore[arg-type]
        },
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_MAX_TIME_TYPE)),
    idspec("INIT_024", TestAction(
        name="Invalid (non-positive) value for max_time parameter",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'max_time': 0.0,  # Invalid non-positive value
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_MAX_TIME_VALUE)),
    idspec("INIT_025", TestAction(
        name="Invalid (max_time < min_time) values for time parameters",
        action=Case,
        kwargs={
            'group': 'example',
            'title': 'benchcase',
            'description': 'A simple benchmark case.',
            'action': benchcase,
            'min_time': 5.0,
            'max_time': 1.0,  # Invalid: max_time < min_time
        },
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_TIME_RANGE)),

])
def test_case_init(testspec: TestAction) -> None:
    """Test the initialization of the Case class."""
    testspec.run()
