"""Tests for the simplebench/results.py module."""
# ruff: noqa: F401

from enum import Enum

import pytest
from testspec import Assert, PytestAction, TestAction

from simplebench.case.results import Results, _ResultsErrorTag
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench_tests import factories
from simplebench_tests.kwargs import ResultsKWArgs


@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="Full valid args",
        action=Results, kwargs=factories.results_kwargs_factory(),
        assertion=Assert.ISINSTANCE,
        expected=Results),
    PytestAction("INIT_002",
        name="negative n",
        action=Results, kwargs=factories.results_kwargs_factory().replace(n=-1),
        exception=SimpleBenchValueError,
        exception_tag=_ResultsErrorTag.N_INVALID_ARG_VALUE),
    PytestAction("INIT_003",
        name="non-string group",
        action=Results, kwargs=factories.results_kwargs_factory().replace(group=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsErrorTag.GROUP_INVALID_ARG_TYPE),
    PytestAction("INIT_004",
        name="non-string title",
        action=Results, kwargs=factories.results_kwargs_factory().replace(title=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsErrorTag.TITLE_INVALID_ARG_TYPE),
    PytestAction("INIT_005",
        name="non-string description",
        action=Results, kwargs=factories.results_kwargs_factory().replace(description=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsErrorTag.DESCRIPTION_INVALID_ARG_TYPE),
    PytestAction("INIT_006",
        name="non-VariationMarks variation_marks argument",
        action=Results, kwargs=factories.results_kwargs_factory().replace(variation_marks=[]),
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE),
    PytestAction("INIT_007",
        name="non-Iteration iterations with dict",
        action=Results, kwargs=factories.results_kwargs_factory().replace(iterations={'not': 'Interations'}),
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsErrorTag.ITERATIONS_INVALID_ARG_TYPE),
    PytestAction("INIT_008",
        name="non-Extras extra_info",
        action=Results, kwargs=factories.results_kwargs_factory().replace(extra_info='not an Extras instance'),
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsErrorTag.EXTRA_INFO_INVALID_ARG_TYPE),
    PytestAction("INIT_009",
        name="empty string group",
        action=Results, kwargs=factories.results_kwargs_factory().replace(group=''),
        exception=SimpleBenchValueError,
        exception_tag=_ResultsErrorTag.GROUP_INVALID_ARG_VALUE),
    PytestAction("INIT_010",
        name="empty string title",
        action=Results, kwargs=factories.results_kwargs_factory().replace(title=''),
        exception=SimpleBenchValueError,
        exception_tag=_ResultsErrorTag.TITLE_INVALID_ARG_VALUE),
    PytestAction("INIT_011",
        name="Wrong type for rounds argument (str instead of int)",
        action=Results, kwargs=factories.results_kwargs_factory().replace(rounds='invalid_type'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsErrorTag.ROUNDS_INVALID_ARG_TYPE),
    PytestAction("INIT_012",
        name="Negative value for rounds argument",
        action=Results, kwargs=factories.results_kwargs_factory().replace(rounds=-1),
        exception=SimpleBenchValueError,
        exception_tag=_ResultsErrorTag.ROUNDS_INVALID_ARG_VALUE),
    PytestAction("INIT_013",
        name="Zero value for rounds argument",
        action=Results, kwargs=factories.results_kwargs_factory().replace(rounds=0),
        exception=SimpleBenchValueError,
        exception_tag=_ResultsErrorTag.ROUNDS_INVALID_ARG_VALUE),
])
def test_results_init(testspec: TestAction) -> None:
    """Test Results initialization.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="Get non-existent attribute",
        action=lambda: factories.results_factory(),
        validate_attr='non_existent_attr',
        exception=AttributeError),
    PytestAction("PROP_002",
        name="Get 'group' attribute",
        action=lambda: factories.results_factory(),
        validate_attr='group',
        assertion=Assert.EQUAL,
        expected=factories.results_kwargs_factory()['group']),
    PytestAction("PROP_003",
        name="Get 'title' attribute",
        action=lambda: factories.results_factory(),
        validate_attr='title',
        assertion=Assert.EQUAL,
        expected=factories.results_kwargs_factory()['title']),
    PytestAction("PROP_004",
        name="Get 'description' attribute",
        action=lambda: factories.results_factory(),
        validate_attr='description',
        assertion=Assert.EQUAL,
        expected=factories.results_kwargs_factory()['description']),
    PytestAction("PROP_005",
        name="Get 'n' attribute",
        action=lambda: factories.results_factory(),
        validate_attr='n',
        assertion=Assert.EQUAL,
        expected=factories.results_kwargs_factory()['n']),
    PytestAction("PROP_006",
        name="Get 'iterations' attribute",
        action=lambda: factories.results_factory(),
        validate_attr='iterations',
        assertion=Assert.EQUAL,
        expected=factories.results_kwargs_factory()['iterations']),
    PytestAction("PROP_007",
        name="Get 'variation_marks' attribute",
        action=lambda: factories.results_factory(),
        validate_attr='variation_marks',
        assertion=Assert.EQUAL,
        expected=factories.results_kwargs_factory()['variation_marks']),
    PytestAction("PROP_008",
        name="Get 'extra_info' attribute",
        action=lambda: factories.results_factory(),
        validate_attr='extra_info',
        assertion=Assert.EQUAL,
        expected=factories.results_kwargs_factory()['extra_info']),
])
def test_get_property(testspec: TestAction) -> None:
    """Test getting attributes from Results.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
