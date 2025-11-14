"""Tests for the simplebench.reporters.reporter._ReporterPrioritizationMixin mixin class."""
from dataclasses import dataclass

import pytest

from simplebench.case import Case
from simplebench.enums import Target
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.options import ReporterOptions

from ....factories import (
    FactoryReporter,
    FactoryReporterOptions,
    case_factory,
    case_kwargs_factory,
    choice_conf_kwargs_factory,
    choice_factory,
    reporter_factory,
    reporter_kwargs_factory,
    reporter_options_factory,
)
from ....testspec import Assert, TestAction, TestSpec, idspec


def test_factory_reporter_default_options() -> None:
    """Test the get_hardcoded_default_options class method with FactoryReporter."""
    FactoryReporter.set_default_options(None)
    hardcoded_default_options = FactoryReporter.get_hardcoded_default_options()
    hardcoded_default_options.tag = 'hardcoded_default_options'  # type: ignore[attr-defined]

    assert hardcoded_default_options is FactoryReporter.get_default_options(), (
        "FactoryReporter.get_default_options() should return the hardcoded default options"
        " when no default options are set."
    )

    default_options = FactoryReporterOptions()
    default_options.tag = 'default_options'
    FactoryReporter.set_default_options(default_options)

    assert default_options is FactoryReporter.get_default_options(), (
        "FactoryReporter.get_default_options() should return the set default options"
        " when they are set."
    )

    FactoryReporter.set_default_options(None)
    assert hardcoded_default_options is FactoryReporter.get_default_options(), (
        "FactoryReporter.get_default_options() should return the hardcoded default options"
        " after default options are cleared."
    )


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

    default_options_title = 'without' if reporter_default_options is None else 'with'

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
            action=get_prioritized_options_helper,
            kwargs={
                'reporter': reporter,
                'case': testcase.case,
                'choice': choice,
                'default_reporter_options': testcase.reporter_default_options,
            },
            assertion=Assert.IS,
            expected=testcase.expected,
        ))

    def get_prioritized_options_helper(
            reporter: FactoryReporter,
            case: Case,
            choice: Choice,
            default_reporter_options: ReporterOptions | None) -> ReporterOptions:
        """Helper function to call get_prioritized_options and handle failures."""
        FactoryReporter.set_default_options(default_reporter_options)
        return reporter.get_prioritized_options(
                case=case,
                choice=choice)

    # Prioritization tests with FactoryReporter default options set to reporter_default_options
    prioritization_testcases = [
        PrioritizeOptionsTest(
            test_id="PRIORITIZE_OPTIONS_001",
            name=(f"Case With Options, Choice With Options, Reporter {default_options_title} "
                  "Default Options -> (Case with Options)"),
            case=case_with_options,
            choices=choices_conf_with_options,
            reporter_default_options=reporter_default_options,
            expected=case_options,
        ),
        PrioritizeOptionsTest(
            test_id="PRIORITIZE_OPTIONS_002",
            name=(f"Case Without Options, Choice With Options, Reporter {default_options_title} "
                  "Default Options -> (Choice with Options)"),
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
                name=(f"(A) Case Without Options, Choice Without Options, Reporter {default_options_title} "
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
                name=(f"(B) Case Without Options, Choice Without Options, Reporter {default_options_title} "
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


def get_prioritized_default_targets_testspecs() -> list[TestSpec]:
    """Get test specifications for get_prioritized_default_targets method.

    Returns:
        list[TestSpec]: A list of TestSpec instances for testing.

    """
    testspecs: list[TestSpec] = []

    choice_default_targets = frozenset({Target.CONSOLE})
    choice_conf_kwargs_with_default_targets = choice_conf_kwargs_factory().replace(
                                            name='choice_with_default_targets',
                                            flags=['--choice-with-default-targets'],
                                            default_targets=choice_default_targets)
    choice_conf_with_default_targets = ChoiceConf(**choice_conf_kwargs_with_default_targets)

    choice_conf_kwargs_without_default_targets = choice_conf_kwargs_factory().replace(
                                            name='choice_without_default_targets',
                                            flags=['--choice-without-default-targets']) - ['default_targets']
    choice_conf_without_default_targets = ChoiceConf(**choice_conf_kwargs_without_default_targets)
    choices = ChoicesConf(choices=[choice_conf_with_default_targets,
                                   choice_conf_without_default_targets])

    reporter_default_targets = frozenset({Target.FILESYSTEM})
    reporter_kwargs = reporter_kwargs_factory().replace(
                            choices=choices,
                            default_targets=reporter_default_targets)
    reporter = FactoryReporter(**reporter_kwargs)

    choice_with_default_targets = reporter.choices['choice_with_default_targets']
    choice_without_default_targets = reporter.choices['choice_without_default_targets']

    testspecs.extend([
        idspec("PRIORITIZE_DEFAULT_TARGETS_001", TestAction(
            name="Choice with default targets -> (Choice default targets)",
            action=reporter.get_prioritized_default_targets,
            args=[choice_with_default_targets],
            assertion=Assert.EQUAL,
            expected=choice_default_targets,
        )),
        idspec("PRIORITIZE_DEFAULT_TARGETS_002", TestAction(
            name="Choice without default targets -> (Reporter default targets)",
            action=reporter.get_prioritized_default_targets,
            args=[choice_without_default_targets],
            assertion=Assert.EQUAL,
            expected=reporter_default_targets,
        )),
        idspec("PRIORITIZE_DEFAULT_TARGETS_003", TestAction(
            name="Invalid choice arg type raises SimpleBenchTypeError",
            action=reporter.get_prioritized_default_targets,
            args=['not_a_real_choice_instance'],
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.GET_PRIORITIZED_DEFAULT_TARGETS_INVALID_CHOICE_ARG_TYPE,)),
    ])
    return testspecs


@pytest.mark.parametrize("testspec",
                         get_prioritized_default_targets_testspecs())
def test_get_prioritized_default_targets(testspec: TestSpec) -> None:
    """Test the get_prioritized_default_targets method of PrioritizationMixin."""
    testspec.run()


def get_prioritized_subdir_testspecs() -> list[TestSpec]:
    """Get test specifications for get_prioritized_subdir method.

    Returns:
        list[TestSpec]: A list of TestSpec instances for testing.

    """
    testspecs: list[TestSpec] = []

    choice_subdir = 'choicesubdir'
    choice_conf_kwargs_with_subdir = choice_conf_kwargs_factory().replace(
                                            name='choice_with_subdir',
                                            flags=['--choice-with-subdir'],
                                            subdir=choice_subdir)
    choice_conf_with_subdir = ChoiceConf(**choice_conf_kwargs_with_subdir)

    choice_conf_kwargs_without_subdir = choice_conf_kwargs_factory().replace(
                                            name='choice_without_subdir',
                                            flags=['--choice-without-subdir']) - ['subdir']
    choice_conf_without_subdir = ChoiceConf(**choice_conf_kwargs_without_subdir)
    choices = ChoicesConf(choices=[choice_conf_with_subdir,
                                   choice_conf_without_subdir])

    reporter_default_subdir = 'reporterdefaultsubdir'
    reporter_kwargs = reporter_kwargs_factory().replace(
                            choices=choices,
                            subdir=reporter_default_subdir)
    reporter = FactoryReporter(**reporter_kwargs)

    choice_with_subdir = reporter.choices['choice_with_subdir']
    choice_without_subdir = reporter.choices['choice_without_subdir']

    testspecs.extend([
        idspec("PRIORITIZE_SUBDIR_001", TestAction(
            name="Choice with subdir -> (Choice subdir)",
            action=reporter.get_prioritized_subdir,
            args=[choice_with_subdir],
            assertion=Assert.EQUAL,
            expected=choice_subdir,
        )),
        idspec("PRIORITIZE_SUBDIR_002", TestAction(
            name="Choice without subdir -> (Reporter default subdir)",
            action=reporter.get_prioritized_subdir,
            args=[choice_without_subdir],
            assertion=Assert.EQUAL,
            expected=reporter_default_subdir,
        )),
        idspec("PRIORITIZE_SUBDIR_003", TestAction(
            name="Invalid choice arg type raises SimpleBenchTypeError",
            action=reporter.get_prioritized_subdir,
            args=['not_a_real_choice_instance'],
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.GET_PRIORITIZED_SUBDIR_INVALID_CHOICE_ARG_TYPE,)),
    ])
    return testspecs


@pytest.mark.parametrize("testspec",
                         get_prioritized_subdir_testspecs())
def test_get_prioritized_subdir(testspec: TestSpec) -> None:
    """Test the get_prioritized_subdir method of PrioritizationMixin."""
    testspec.run()


def get_prioritized_file_suffix_testspecs() -> list[TestSpec]:
    """Get test specifications for get_prioritized_file_suffix method.

    Returns:
        list[TestSpec]: A list of TestSpec instances for testing.
    """
    testspecs: list[TestSpec] = []

    reporter_kwargs = reporter_kwargs_factory()
    reporter = FactoryReporter(**reporter_kwargs)

    choice_suffix = ''
    choice_conf_kwargs_with_file_suffix = choice_conf_kwargs_factory().replace(
                                            name='choice_with_file_suffix',
                                            flags=['--choice-with-file-suffix'],
                                            file_suffix=choice_suffix)
    choice_conf_with_file_suffix = ChoiceConf(**choice_conf_kwargs_with_file_suffix)

    choice_conf_kwargs_without_file_suffix = choice_conf_kwargs_factory().replace(
                                            name='choice_without_file_suffix',
                                            flags=['--choice-without-file-suffix']) - ['file_suffix']
    choice_conf_without_file_suffix = ChoiceConf(**choice_conf_kwargs_without_file_suffix)
    choices = ChoicesConf(choices=[choice_conf_with_file_suffix,
                                   choice_conf_without_file_suffix])

    reporter_suffix = 'reporterfs'
    reporter_kwargs = reporter_kwargs_factory().replace(
                            choices=choices,
                            file_suffix=reporter_suffix)
    reporter = FactoryReporter(**reporter_kwargs)

    choice_with_file_suffix = reporter.choices['choice_with_file_suffix']
    choice_without_file_suffix = reporter.choices['choice_without_file_suffix']

    testspecs.extend([
        idspec("PRIORITIZE_FILE_SUFFIX_001", TestAction(
            name="Choice with file suffix -> (Choice file suffix)",
            action=reporter.get_prioritized_file_suffix,
            args=[choice_with_file_suffix],
            assertion=Assert.EQUAL,
            expected=choice_suffix,
        )),
        idspec("PRIORITIZE_FILE_SUFFIX_002", TestAction(
            name="Choice without file suffix -> (Reporter file suffix)",
            action=reporter.get_prioritized_file_suffix,
            args=[choice_without_file_suffix],
            assertion=Assert.EQUAL,
            expected=reporter_suffix,
        )),
    ])
    return testspecs


@pytest.mark.parametrize("testspec",
                         get_prioritized_file_suffix_testspecs())
def test_get_prioritized_file_suffix(testspec: TestSpec) -> None:
    """Test the get_prioritized_file_suffix method of PrioritizationMixin."""
    testspec.run()


def get_prioritized_file_append_and_unique_testspecs() -> list[TestSpec]:
    """Get test specifications for get_prioritized_file_append and
    get_prioritized_file_unique methods.

    These file_append and file_unique are tested together because they always
    have opposite boolean values making them complementary and so easily tested together
    with the same setup.

    Returns:
        list[TestSpec]: A list of TestSpec instances for testing.
    """
    testspecs: list[TestSpec] = []

    choice_file_append_true = True
    choice_file_append_false = False

    choice_file_unique_false = False
    choice_file_unique_true = True

    choice_name_with_file_append_true_unique_false = 'choice_with_file_append_true_unique_false'
    choice_name_with_file_append_false_unique_true = 'choice_with_file_append_false_unique_true'
    choice_name_without_file_append_or_unique = 'choice_without_file_append_or_unique'

    choice_conf_kwargs_with_file_append_true_unique_false = choice_conf_kwargs_factory().replace(
                                            name=choice_name_with_file_append_true_unique_false,
                                            flags=['--choice-with-file-append-true-unique-false'],
                                            file_append=choice_file_append_true,
                                            file_unique=choice_file_unique_false)
    choice_conf_with_file_append_true_unique_false = ChoiceConf(**choice_conf_kwargs_with_file_append_true_unique_false)

    choice_conf_kwargs_with_file_append_false_unique_true = choice_conf_kwargs_factory().replace(
                                            name=choice_name_with_file_append_false_unique_true,
                                            flags=['--choice-with-file-append-false-unique-true'],
                                            file_append=choice_file_append_false,
                                            file_unique=choice_file_unique_true)
    choice_conf_with_file_append_false_unique_true = ChoiceConf(**choice_conf_kwargs_with_file_append_false_unique_true)

    choice_conf_kwargs_without_file_append_or_unique = choice_conf_kwargs_factory().replace(
                                    name=choice_name_without_file_append_or_unique,
                                    flags=['--choice-without-file-append-or-unique']) - ['file_append', 'file_unique']
    choice_conf_without_file_append_or_unique = ChoiceConf(**choice_conf_kwargs_without_file_append_or_unique)

    choices = ChoicesConf(choices=[choice_conf_with_file_append_true_unique_false,
                                   choice_conf_with_file_append_false_unique_true,
                                   choice_conf_without_file_append_or_unique])

    reporter_kwargs_append_true = reporter_kwargs_factory().replace(choices=choices,
                                                                    file_append=True,
                                                                    file_unique=False)
    reporter_kwargs_append_false = reporter_kwargs_factory().replace(choices=choices,
                                                                     file_append=False,
                                                                     file_unique=True)

    reporter_append_false = FactoryReporter(**reporter_kwargs_append_false)
    reporter_append_true = FactoryReporter(**reporter_kwargs_append_true)

    choice_with_file_append_true_unique_false = reporter_append_false.choices[
                                                    choice_name_with_file_append_true_unique_false]
    choice_with_file_append_false_unique_true = reporter_append_false.choices[
                                                    choice_name_with_file_append_false_unique_true]
    choice_without_file_append_or_unique = reporter_append_false.choices[choice_name_without_file_append_or_unique]

    testspecs.extend([
        idspec("FILE_APPEND_001", TestAction(
            name="Reporter with file_append=True, Choice with file_append=True -> True (Choice file append)",
            action=reporter_append_true.get_prioritized_file_append,
            args=[choice_with_file_append_true_unique_false],
            assertion=Assert.EQUAL,
            expected=True,
        )),
        idspec("FILE_APPEND_002", TestAction(
            name="Reporter with file_append=False, Choice with file_append=True -> True (Choice file append)",
            action=reporter_append_false.get_prioritized_file_append,
            args=[choice_with_file_append_true_unique_false],
            assertion=Assert.EQUAL,
            expected=True,
        )),
        idspec("FILE_APPEND_003", TestAction(
            name="Reporter with file_append=True, Choice with file_append=False -> False (Choice file append)",
            action=reporter_append_true.get_prioritized_file_append,
            args=[choice_with_file_append_false_unique_true],
            assertion=Assert.EQUAL,
            expected=False,
        )),
        idspec("FILE_APPEND_004", TestAction(
            name="Reporter with file_append=False, Choice with file_append=False -> False (Choice file append)",
            action=reporter_append_false.get_prioritized_file_append,
            args=[choice_with_file_append_false_unique_true],
            assertion=Assert.EQUAL,
            expected=False,
        )),
        idspec("FILE_UNIQUE_001", TestAction(
            name="Reporter with file_unique=False, Choice with file_unique=False -> False (Choice file unique)",
            action=reporter_append_false.get_prioritized_file_unique,
            args=[choice_with_file_append_true_unique_false],
            assertion=Assert.EQUAL,
            expected=False,
        )),
        idspec("FILE_UNIQUE_002", TestAction(
            name="Reporter with file_unique=True, Choice with file_unique=False -> False (Choice file unique)",
            action=reporter_append_true.get_prioritized_file_unique,
            args=[choice_with_file_append_true_unique_false],
            assertion=Assert.EQUAL,
            expected=False,
        )),
        idspec("FILE_UNIQUE_003", TestAction(
            name="Reporter with file_unique=False, Choice with file_unique=True -> True (Choice file unique)",
            action=reporter_append_false.get_prioritized_file_unique,
            args=[choice_with_file_append_false_unique_true],
            assertion=Assert.EQUAL,
            expected=True,
        )),
        idspec("FILE_UNIQUE_004", TestAction(
            name="Reporter with file_unique=True, Choice with file_unique=True -> True (Choice file unique)",
            action=reporter_append_true.get_prioritized_file_unique,
            args=[choice_with_file_append_false_unique_true],
            assertion=Assert.EQUAL,
            expected=True,
        )),
        idspec("FILE_APPEND_AND_UNIQUE_NONE_001", TestAction(
            name="Reporter with file_append=True, Choice without file_append -> True (Reporter file append)",
            action=reporter_append_true.get_prioritized_file_append,
            args=[choice_without_file_append_or_unique],
            assertion=Assert.EQUAL,
            expected=True,
        )),
        idspec("FILE_APPEND_AND_UNIQUE_NONE_002", TestAction(
            name="Reporter with file_append=False, Choice without file_append -> False (Reporter file append)",
            action=reporter_append_false.get_prioritized_file_append,
            args=[choice_without_file_append_or_unique],
            assertion=Assert.EQUAL,
            expected=False,
        )),
        idspec("FILE_APPEND_AND_UNIQUE_NONE_003", TestAction(
            name="Reporter with file_unique=False, Choice without file_unique -> False (Reporter file unique)",
            action=reporter_append_false.get_prioritized_file_unique,  # file_append=False means file_unique=True
            args=[choice_without_file_append_or_unique],
            assertion=Assert.EQUAL,
            expected=True,
        )),
        idspec("FILE_APPEND_AND_UNIQUE_NONE_004", TestAction(
            name="Reporter with file_unique=True, Choice without file_unique -> True (Reporter file unique)",
            action=reporter_append_true.get_prioritized_file_unique,  # file_append=True means file_unique=False
            args=[choice_without_file_append_or_unique],
            assertion=Assert.EQUAL,
            expected=False,
        )),
    ])
    return testspecs


@pytest.mark.parametrize("testspec",
                         get_prioritized_file_append_and_unique_testspecs())
def test_get_prioritized_file_append_and_unique(testspec: TestSpec) -> None:
    """Test the get_prioritized_file_append and get_prioritized_file_unique methods of PrioritizationMixin.

    They are tested together because they always have opposite boolean values making them complementary
    and so easily tested.
    """
    testspec.run()
