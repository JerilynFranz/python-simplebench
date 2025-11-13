"""Tests for the simplebench.reporters.reporter._ReporterPrioritizationMixin mixin class."""
from dataclasses import dataclass
from typing import NoReturn

import pytest

from simplebench.case import Case
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.options import ReporterOptions

from ....factories import (FactoryReporter, FactoryReporterOptions,
                           case_factory, case_kwargs_factory,
                           choice_conf_kwargs_factory, choice_factory,
                           reporter_factory, reporter_kwargs_factory,
                           reporter_options_factory)
from ....testspec import Assert, TestAction, TestSpec, idspec


def get_prioritized_options_testspecs(reporter_default_options: ReporterOptions | None) -> list[TestSpec]:
    """Get test specifications for get_prioritized_options method.

    Because the default reporter options can affect the prioritization logic and are
    globally set on the FactoryReporter class, we need to run two separate sets of
    tests: one with default options set and one without.

    They can't be in the same set because the global state would interfere with each other.

    Args:
        reporter_default_options (ReporterOptions | None):
            The default ReporterOptions to use in the FactoryReporter.
    Returns:
        list[TestSpec]: A list of TestSpec instances for testing.

    """

    # Each of the ReporterOptions() instances must be different to allow
    # distinguishing their source in the tests.
    case_options = reporter_options_factory(cache_id=None)
    case_options.tag = 'case_options'

    case_kwargs_with_options = case_kwargs_factory(cache_id=None).replace(options=[case_options])
    case_with_options = Case(**case_kwargs_with_options)

    case_kwargs_without_options = case_kwargs_factory(cache_id=None).replace(options=[])
    case_without_options = Case(**case_kwargs_without_options)

    choice_options = reporter_options_factory(cache_id=None)
    choice_options.tag = 'choice_options'

    choice_conf_kwargs_with_options = choice_conf_kwargs_factory().replace(options=choice_options)
    choice_conf_with_options = ChoiceConf(**choice_conf_kwargs_with_options)
    choices_conf_with_options = ChoicesConf(choices=[choice_conf_with_options])

    choice_conf_kwargs_without_options = choice_conf_kwargs_factory() - ['options']
    choice_conf_without_options = ChoiceConf(**choice_conf_kwargs_without_options)
    choices_conf_without_options = ChoicesConf(choices=[choice_conf_without_options])

    reporter_hardcoded_default_options = FactoryReporter.get_hardcoded_default_options()
    reporter_hardcoded_default_options.tag = 'reporter_hardcoded_default_options'  # type: ignore[attr-defined]

    if reporter_default_options is not None:
        reporter_default_options.tag = 'reporter_default_options'  # type: ignore[attr-defined]

    testspecs: list[TestSpec] = []

    @dataclass(frozen=True)
    class PrioritizeOptionsTest:
        """A test case for prioritizing reporter options."""
        test_id: str
        """The unique identifier for the test case."""
        name: str
        """The name of the test case."""
        case: Case
        """The Case instance to use in the test."""
        choices: ChoicesConf
        """The ChoicesConf instance to use in the test."""
        reporter_default_options: ReporterOptions | None
        """The default ReporterOptions to use in the FactoryReporter."""
        expected: ReporterOptions
        """The expected result value."""

    def prioritize_options_testspec(testcase: PrioritizeOptionsTest) -> TestSpec:
        """Create a TestSpec for a prioritization test case.

        Args:
            testcase (PrioritizeOptionsTest): The test case to create a TestSpec for.

        Returns:
            TestSpec: The created TestSpec.
        """
        reporter_kwargs = reporter_kwargs_factory().replace(choices=testcase.choices)
        reporter = FactoryReporter(**reporter_kwargs)
        reporter.set_default_options(testcase.reporter_default_options)
        choice = next(iter(reporter.choices.values()))
        return idspec(testcase.test_id, TestAction(
            name=testcase.name,
            action=reporter.get_prioritized_options,
            kwargs={
                'case': testcase.case,
                'choice': choice,
            },
            assertion=Assert.IS,
            expected=testcase.expected,
            on_fail=prioritize_fail
        ))

    def prioritize_fail(msg: str) -> NoReturn:
        """Helper function to raise an AssertionError with a message."""
        default_options = FactoryReporter._DEFAULT_OPTIONS  # pylint: disable=protected-access
        hardcoded_default_options = FactoryReporter.get_hardcoded_default_options()
        raise AssertionError(
            f"{msg} FactoryReporter._DEFAULT_OPTIONS = {default_options}\n"
            f"FactoryReporter.get_hardcoded_default_options() = {hardcoded_default_options}"
            )

    # Prioritization tests with FactoryReporter default options set to reporter_default_options
    prioritization_testcases = [
        PrioritizeOptionsTest(
            test_id="PRIORITIZE_OPTIONS_001",
            name="Case With Options, Choice With Options, Reporter With Default Options -> (Case with Options)",
            case=case_with_options,
            choices=choices_conf_with_options,
            reporter_default_options=reporter_default_options,
            expected=case_options,
        ),
        PrioritizeOptionsTest(
            test_id="PRIORITIZE_OPTIONS_002",
            name="Case Without Options, Choice With Options, Reporter With Default Options -> (Choice with Options)",
            case=case_without_options,
            choices=choices_conf_with_options,
            reporter_default_options=reporter_default_options,
            expected=choice_options,
        ),
    ]

    if reporter_default_options is None:
        prioritization_testcases.append(
            PrioritizeOptionsTest(
                test_id="PRIORITIZE_OPTIONS_003",
                name=("Case Without Options, Choice Without Options, Reporter With Without "
                      "Default Options -> (Reporter Hardcoded Default Options)"),
                case=case_without_options,
                choices=choices_conf_without_options,
                reporter_default_options=reporter_default_options,
                expected=reporter_hardcoded_default_options,
            )
        )
    else:
        prioritization_testcases.append(
            PrioritizeOptionsTest(
                test_id="PRIORITIZE_OPTIONS_003",
                name=("Case Without Options, Choice Without Options, Reporter With "
                      "Default Options -> (Reporter Default Options)"),
                case=case_without_options,
                choices=choices_conf_without_options,
                reporter_default_options=reporter_default_options,
                expected=reporter_default_options,
            )
        )

    for testcase in prioritization_testcases:
        testspecs.append(prioritize_options_testspec(testcase))

    testspecs.extend([
        idspec("PRIORITIZE_OPTIONS_004", TestAction(
            name="Invalid case arg type raises SimpleBenchTypeError",
            action=reporter_factory().get_prioritized_options,
            kwargs={
                'case': 'not_a_real_case_instance',
                'choice': choice_factory(),
            },
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.GET_PRIORITIZED_OPTIONS_INVALID_CASE_ARG_TYPE)),
        idspec("PRIORITIZE_OPTIONS_005", TestAction(
            name="Invalid choice arg type raises SimpleBenchTypeError",
            action=reporter_factory().get_prioritized_options,
            kwargs={
                'case': case_factory(),
                'choice': 'not_a_real_choice_instance',
            },
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.GET_PRIORITIZED_OPTIONS_INVALID_CHOICE_ARG_TYPE)),
        idspec("PRIORITIZE_OPTIONS_007", TestAction(
            name="Missing case arg raises TypeError",
            action=reporter_factory().get_prioritized_options,
            kwargs={
                'choice': choice_factory(),
            },
            exception=TypeError)),
        idspec("PRIORITIZE_OPTIONS_008", TestAction(
            name="Missing choice arg raises TypeError",
            action=reporter_factory().get_prioritized_options,
            kwargs={
                'case': case_factory(),
            },
            exception=TypeError)),
    ])

    return testspecs


@pytest.mark.parametrize("testspec",
                         get_prioritized_options_testspecs(
                             reporter_default_options=FactoryReporterOptions()))
def test_get_prioritized_options_with_reporter_default_options(testspec: TestSpec) -> None:
    """Test the get_prioritized_options method of PrioritizationMixin.

    Tested with FactoryReporter default options set.
    """
    testspec.run()


@pytest.mark.parametrize("testspec",
                         get_prioritized_options_testspecs(
                             reporter_default_options=None))
def test_get_prioritized_options_without_reporter_default_options(testspec: TestSpec) -> None:
    """Test the get_prioritized_options method of PrioritizationMixin.

    Tested without FactoryReporter default options set.
    """
    testspec.run()
