"""Test simplebench/reporters/interfaces.py module"""
from __future__ import annotations
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Optional, Sequence, Iterable

import pytest

from tests.kwargs import ChoicesKWArgs, ReporterKWArgs, ChoiceKWArgs

from tests.testspec import TestAction, TestSpec, idspec, NO_EXPECTED_VALUE, Assert

from simplebench.case import Case
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchValueError, SimpleBenchTypeError
from simplebench.iteration import Iteration
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.choice import Choice
from simplebench.reporters.choices import Choices
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.results import Results
from simplebench.runners import SimpleRunner
from simplebench.session import Session


def default_path() -> Path:
    """Return a default Path instance for testing purposes."""
    return Path('/tmp/mock_report.txt')  # pragma: no cover (path not actually used)


def benchcase(bench: SimpleRunner, **kwargs) -> Results:
    """A simple benchmark case function."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(10))  # Example operation to benchmark
    return bench.run(n=10, action=action, **kwargs)


def broken_benchcase_missing_bench(**kwargs: Any) -> Results:  # pylint: disable=unused-argument  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter.

    The function signature is intentionally incorrect for testing purposes.
    """
    # Nothing inside this actually runs since it's just for testing Reporter's
    # error handling for an invalid function type signature.
    return Results(  # made-up results for testing purposes
            group='test_case', title='Test Case',
            description='A test case for testing.',
            n=10, total_elapsed=3.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0)])


def broken_benchcase_missing_kwargs(
        bench: SimpleRunner) -> Results:  # pylint: disable=unused-argument  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter.

    The function signature is intentionally incorrect for testing purposes.
    """
    # Nothing inside this actually runs since it's just for testing Reporter's
    # error handling for an invalid function type signature.
    return Results(  # made-up results for testing purposes
            group='test_case', title='Test Case',
            description='A test case for testing.',
            n=10, total_elapsed=3.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0)])


def default_callback(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: Any) -> None:
    """A default callback function for testing purposes."""
    return None  # pragma: no cover


def default_sections_list() -> list[Section]:
    """Return a default list of Sections for testing purposes."""
    return [Section.OPS]


def default_targets_list() -> list[Target]:
    """Return a default list of Targets for testing purposes."""
    return [Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM]


def default_formats_list() -> list[Format]:
    """Return a default list of Formats for testing purposes."""
    return [Format.RICH_TEXT]


def default_output_format() -> Format:
    """Return a default Format for testing purposes."""
    return Format.RICH_TEXT


def default_description() -> str:
    """Return a default description string for testing purposes."""
    return "A default description for testing."


def default_name() -> str:
    """Return a default name string for testing purposes."""
    return "default_name"


def default_flags() -> list[str]:
    """Return a default list of flags for testing purposes."""
    return ['--default']


def default_flag_type() -> FlagType:
    """Return a default FlagType for testing purposes."""
    return FlagType.TARGET_LIST


def default_file_suffix() -> str:
    """Return a default file suffix string for testing purposes."""
    return "default"


def default_file_unique() -> bool:
    """Return a default file unique boolean for testing purposes."""
    return True


def default_file_append() -> bool:
    """Return a default file append boolean for testing purposes."""
    return False


def default_choice_instance(reporter: Reporter) -> Choice:
    """Return a default Choice instance for testing purposes.

    This has to be called from inside a Reporter init method to pass the reporter instance.
    """
    return Choice(
        reporter=reporter,
        flags=default_flags(),
        flag_type=default_flag_type(),
        name=default_name(),
        description=default_description(),
        sections=default_sections_list(),
        targets=default_targets_list(),
        output_format=default_output_format())


def default_choices_instance(reporter: Reporter) -> Choices:
    """Return a default Choices instance for testing purposes.

    This has to be called from inside a Reporter init method to pass the reporter instance.
    """
    choices = Choices()
    choices.add(default_choice_instance(reporter=reporter))
    return choices


def default_report_output() -> str:
    """Return the default report output string for testing purposes."""
    return "Rendered Report"


def default_action() -> list[str]:
    """Return a default list of actions for testing purposes."""
    return ['--default-action']


def default_report_parameters() -> dict[str, Any]:
    """Return default report parameters for testing purposes."""
    return {
        'args': namespace_instance(),
        'case': ConfiguredCase(),
        'choice': ConfiguredChoice(),
        'path': default_path(),
        'session': ConfiguredSession(),
        'callback': default_callback
    }


def namespace_instance() -> Namespace:
    """Return an ArgumentParser instance for testing purposes."""
    arg_parser = ArgumentParser(prog='simplebench')
    args = arg_parser.parse_args([])
    return args


class UnconfiguredReporterOptions(ReporterOptions):
    """A dummy ReporterOptions subclass for testing purposes.

    The UnconfiguredReporter is preconfigured with no options so all
    parameters are must be provided at runtime (unless defaults are set elsewhere).
    """


USE_SELF_FOR_REPORTER = object()
"""Sentinel value to indicate that the reporter parameter should be set to self.

This is used to avoid circular references when initializing UnconfiguredReporter
while still allowing the testing of reporter parameter handling of the Reporter base class.
"""


class UnconfiguredReporter(Reporter):
    """A dummy reporter subclass for testing purposes.

    No parameters are preset for this reporter.

    Provides a shim implementation of run_report() and render() methods to allow
    instantiation and testing of the Reporter base class functionality with
    both good and bad parameters.

    """
    def __init__(
            self,
            name: str | None = None,
            description: str | None = None,
            options_type: ReporterOptions | None = None,
            sections: Iterable[Section] | None = None,
            targets: Iterable[Target] | None = None,
            formats: Iterable[Format] | None = None,
            choices: Choices | None = None,
            file_suffix: str | None = None,
            file_unique: str | None = None,
            file_append: str | None = None) -> None:
        """Initialize UnconfiguredReporter with provided kwargs.

        Args:
            name (str | None): Name of the reporter.
            description (str | None): Description of the reporter.
            options_type (ReporterOptions | None): Options type for the reporter.
            sections (Iterable[Section] | None): Supported sections for the reporter.
            targets (Iterable[Target] | None): Supported targets for the reporter.
            formats (Iterable[Format] | None): Supported formats for the reporter.
            choices (Choices | None): Choices for the reporter.
            file_suffix (str | None): File suffix for the reporter.
            file_unique (str | None): File unique flag for the reporter.
            file_append (str | None): File append flag for the reporter.
        """
        # Types don't match because we are TESTING the base class parameter validation code.
        # This is expected and intentional.
        super().__init__(
            name=name,  # type: ignore[arg-type,reportArgumentType]
            description=description,  # type: ignore[arg-type,reportArgumentType]
            options_type=options_type,  # type: ignore[arg-type,reportArgumentType]
            sections=sections,  # type: ignore[arg-type,reportArgumentType]
            targets=targets,  # type: ignore[arg-type,reportArgumentType]
            formats=formats,  # type: ignore[arg-type,reportArgumentType]
            choices=choices,  # type: ignore[arg-type,reportArgumentType]
            file_suffix=file_suffix,  # type: ignore[arg-type,reportArgumentType]
            file_unique=file_unique,  # type: ignore[arg-type,reportArgumentType]
            file_append=file_append  # type: ignore[arg-type,reportArgumentType]
        )

    def run_report(self, *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Run the report with the given arguments, case, and choice."""
        self.render_by_case(
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """Render the report for the given case, section, and options."""
        return default_report_output()


class ConfiguredReporterOptions(ReporterOptions):
    """A mock ReporterOptions subclass for testing purposes."""


def default_options_type() -> type[ConfiguredReporterOptions]:
    """Return a default ReporterOptions instance for testing purposes."""
    return ConfiguredReporterOptions


class ConfiguredReporter(Reporter):
    """A mock reporter subclass with default options already set for testing purposes.

    Creates a Reporter with default parameters for testing that can be overridden as needed.

        - name=default_name(),
        - description=default_description(),
        - options_type=ConfiguredReporterOptions,
        - sections=default_sections_list(),
        - targets=default_targets_list(),
        - formats=default_formats_list(),
        - choices=default_choices_instance(reporter=self),
        - file_suffix=default_file_suffix(),
        - file_unique=default_file_unique(),
        -file_append=default_file_append()

    """
    def __init__(self) -> None:
        """Preconfigured Reporter for testing purposes.
            - name=default_name(),
            - description=default_description(),
            - options_type=ConfiguredReporterOptions,
            - sections=default_sections_list(),
            - targets=default_targets_list(),
            - formats=default_formats_list(),
            - choices=default_choices_instance(reporter=self),
            - file_suffix=default_file_suffix(),
            - file_unique=default_file_unique(),
            - file_append=default_file_append()
        """

        super().__init__(
            name=default_name(),
            description=default_description(),
            options_type=default_options_type(),
            sections=default_sections_list(),
            targets=default_targets_list(),
            formats=default_formats_list(),
            choices=default_choices_instance(reporter=self),
            file_suffix=default_file_suffix(),
            file_unique=default_file_unique(),
            file_append=default_file_append())

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Run the report with the given arguments, case, and choice."""
        self.render_by_case(
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """Render the report for the given case, section, and options."""
        return default_report_output()


def reporter_kwargs() -> ReporterKWArgs:
    """A preconfigured ReporterKWArgs instance for testing purposes.

    ReporterKWArgs(
        name=default_name(),
        description=default_description(),
        sections=default_sections_list(),
        targets=default_targets_list(),
        formats=default_formats_list(),
        choices=default_choices_instance(reporter=ConfiguredReporter()),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )

    Returns:
        ReporterKWArgs: A preconfigured instance with default values for testing.
    """
    return ReporterKWArgs(
        name=default_name(),
        description=default_description(),
        options_type=default_options_type(),
        sections=default_sections_list(),
        targets=default_targets_list(),
        formats=default_formats_list(),
        choices=default_choices_instance(reporter=ConfiguredReporter()),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )


reporter_kwargs_instance = reporter_kwargs()


class ConfiguredChoice(Choice):
    """A dummy Choice subclass for testing purposes.

    Creates a Choice with default parameters for testing that can be overridden as needed.

    """
    def __init__(
            self, *,
            reporter: Reporter | None = None,
            flags: list[str] | None = None,
            name: str = 'dummy',
            description: str = 'A dummy choice for testing.',
            flag_type: FlagType = FlagType.BOOLEAN,
            sections: Sequence[Section] | None = None,
            targets: Sequence[Target] | None = None,
            output_format: Format | None = None) -> None:
        super().__init__(
            reporter=reporter or ConfiguredReporter(),
            flags=flags if flags is not None else ['--dummy'],
            flag_type=flag_type,
            name=name,
            description=description,
            sections=sections if sections is not None else default_sections_list(),
            targets=targets if targets is not None else default_targets_list(),
            output_format=output_format if output_format is not None else default_output_format())


choice_instance = ConfiguredChoice()
"""A preconfigured ConfiguredChoice instance for testing purposes

Used to avoid re-instantiating multiple times in tests in
test that need multiple access to the same Choice instance."""


def default_choice_kwargs() -> ChoiceKWArgs:
    """Return default ChoiceKWArgs for testing purposes."""
    return ChoiceKWArgs(
        reporter=ConfiguredReporter(),
        flags=['--dummy'],
        flag_type=FlagType.BOOLEAN,
        name='dummy',
        description='A dummy choice for testing.',
        sections=default_sections_list(),
        targets=default_targets_list(),
        output_format=default_output_format()
    )


default_choice_kwargs_instance = default_choice_kwargs()


def default_choices_kwargs() -> ChoicesKWArgs:
    """Return default ChoicesKWArgs for testing purposes."""
    return ChoicesKWArgs(
        choices=[ConfiguredChoice()]
    )


class ConfiguredChoices(Choices):
    """A dummy Choices subclass for testing purposes."""
    def __init__(self) -> None:
        super().__init__()
        self.add(ConfiguredChoice())


choices_instance = ConfiguredChoices()
"""A preconfigured ConfiguredChoices instance for testing purposes.

Used to avoid re-instantiating multiple times in tests
that need multiple access to the same Choices instance."""


class ConfiguredCase(Case):
    """A dummy Case subclass for testing purposes."""
    def __init__(self) -> None:
        super().__init__(
            group='test_case',
            title='Test Case',
            description='A test case for testing.',
            action=benchcase)
        self._results.append(Results(  # made-up results for testing purposes
            group='test_case', title='Test Case', description='A test case for testing.',
            n=10, total_elapsed=6.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0), Iteration(elapsed=3.0)]))


case_instance = ConfiguredCase()
"""A preconfigured ConfiguredCase instance for testing purposes.

Used to avoid re-instantiating multiple times in tests that
need multiple access to the same Case instance.
"""


class ConfiguredSession(Session):
    """A dummy Session subclass for testing purposes."""
    def __init__(self) -> None:

        super().__init__(cases=[case_instance])


session_instance = ConfiguredSession()
"""A preconfigured ConfiguredSession instance for testing purposes.

Used to avoid re-instantiating multiple times in tests
that need multiple access to the same Session instance.
"""


class BadSuperConfiguredReporter(Reporter):
    """A dummy Reporter subclass for testing purposes.

    This class incorrectly calls super().run_report(), which should raise NotImplementedError
    when run() is called.
    """
    def __init__(self) -> None:
        super().__init__(**reporter_kwargs())

    def run_report(self,  # pylint: disable=useless-parent-delegation
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Incorrectly calls super().run_report(), which should raise NotImplementedError."""
        return super().run_report(
                                  args=args,
                                  case=case,
                                  choice=choice,
                                  path=path,
                                  session=session,
                                  callback=callback)


reporter_instance = ConfiguredReporter()
"""A preconfigured ConfiguredReporter instance for testing purposes.

Used to avoid re-instantiating multiple times in tests
that need multiple access to the same Reporter instance.
"""


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_001', TestAction(
        name="abstract base class Reporter() cannot be instantiated directly",
        action=Reporter,
        exception=TypeError)),
    idspec('REPORTER_002', TestAction(
        name="configured subclass of BadSuperConfiguredReporter() can be instantiated",
        action=BadSuperConfiguredReporter,
        assertion=Assert.ISINSTANCE,
        expected=BadSuperConfiguredReporter)),
    idspec('REPORTER_003', TestAction(
        name=("calling run_report() on BadSuperConfiguredReporter with bad run_report() super() delegation "
              "raises SimpleBenchNotImplementedError"),
        action=BadSuperConfiguredReporter().run_report,
        kwargs={'args': namespace_instance(), 'case': ConfiguredCase(), 'choice': ConfiguredChoice()},
        exception=SimpleBenchNotImplementedError,
        exception_tag=ReporterErrorTag.RUN_REPORT_NOT_IMPLEMENTED)),
    idspec('REPORTER_004', TestAction(
        name="configured subclass of ConfiguredReporter() can be instantiated",
        action=ConfiguredReporter,
        assertion=Assert.ISINSTANCE,
        expected=ConfiguredReporter)),
    idspec('REPORTER_005', TestAction(
        name="Correctly configured subclass of ConfiguredReporter() can call report() successfully",
        action=ConfiguredReporter().report,
        kwargs=default_report_parameters(),
        validate_result=lambda result: result is None)),
    idspec('REPORTER_006', TestAction(
        name="Correctly configured UnconfiguredReporter() can be instantated",
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=UnconfiguredReporter)),
    idspec('REPORTER_007', TestAction(
        name="Correctly configured UnconfiguredReporter() can call report() successfully",
        action=UnconfiguredReporter(**reporter_kwargs()).report,
        kwargs=default_report_parameters(),
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_008', TestAction(
        name=("Init of UnconfiguredReporter with missing name raises "
              "SimpleBenchTypeError/NAME_INVALID_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs() - ['name'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.NAME_INVALID_ARG_TYPE)),
    idspec('REPORTER_009', TestAction(
        name=("Init of UnconfiguredReporter with missing description raises "
              "SimpleBenchTypeError/DESCRIPTION_INVALID_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs() - ['description'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.DESCRIPTION_INVALID_ARG_TYPE)),
    idspec('REPORTER_010', TestAction(
        name=("Init of UnconfiguredReporter with missing sections raises "
              "SimpleBenchTypeError/SECTIONS_INVALID_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs() - ['sections'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SECTIONS_INVALID_ARG_TYPE)),
    idspec('REPORTER_011', TestAction(
        name=("Init of UnconfiguredReporter with empty targets raises "
              "SimpleBenchValueError/TARGETS_INVALID_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(targets=set()),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.TARGETS_ITEMS_ARG_VALUE)),
    idspec('REPORTER_012', TestAction(
        name=("Init of UnconfiguredReporter with empty formats raises "
              "SimpleBenchValueError/SECTIONS_ITEMS_ARG_VALUE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(formats=set()),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.FORMATS_ITEMS_ARG_VALUE)),
    idspec('REPORTER_013', TestAction(
        name=("Init of UnconfiguredReporter with missing choices raises "
              "SimpleBenchTypeError/CHOICES_INVALID_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs() - ['choices'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.CHOICES_INVALID_ARG_TYPE)),
    idspec('REPORTER_014', TestAction(
        name=("Init of UnconfiguredReporter with choices not being a Choices instance raises "
              "SimpleBenchTypeError/INVALID_CHOICES_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(choices="not_a_choices_instance"),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.CHOICES_INVALID_ARG_TYPE)),
    idspec('REPORTER_015', TestAction(
        name=("Init of UnconfiguredReporter with sections containing a non-Section enum raises "
              "SimpleBenchTypeError/SECTION_INVALID_ENTRY_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(sections={Section.OPS, "not_a_section_enum"}),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SECTIONS_INVALID_ARG_TYPE)),
    idspec('REPORTER_016', TestAction(
        name=("Init of UnconfiguredReporter with targets containing non-Target enum raises "
              "SimpleBenchTypeError/TARGETS_INVALID_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(targets={Target.CONSOLE, "not_a_target_enum"}),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.TARGETS_INVALID_ARG_TYPE)),
    idspec('REPORTER_017', TestAction(
        name=("Init of UnconfiguredReporter with formats containing non-Format enum raises "
              "SimpleBenchTypeError/FORMATS_INVALID_ARG_TYPE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(formats={Format.RICH_TEXT, "not_a_format_enum"}),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.FORMATS_INVALID_ARG_TYPE)),
    idspec('REPORTER_018', TestAction(
        name=("Init of UnconfiguredReporter with empty name raises "
              "SimpleBenchValueError/NAME_INVALID_ARG_VALUE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(name=''),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.NAME_INVALID_ARG_VALUE)),
    idspec('REPORTER_019', TestAction(
        name=("Init of UnconfiguredReporter with blank name raises "
              "SimpleBenchValueError/NAME_INVALID_ARGVALUE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(name='  '),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.NAME_INVALID_ARG_VALUE)),
    idspec('REPORTER_020', TestAction(
        name=("Init of UnconfiguredReporter with empty description raises "
              "SimpleBenchValueError/DESCRIPTION_INVALID_ARG_VALUE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(description=''),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.DESCRIPTION_INVALID_ARG_VALUE)),
    idspec('REPORTER_021', TestAction(
        name=("Init of UnconfiguredReporter with blank description raises "
              "SimpleBenchValueError/DESCRIPTION_INVALID_ARG_VALUE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(description='   '),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.DESCRIPTION_INVALID_ARG_VALUE)),
    idspec('REPORTER_022', TestAction(
        name=("Init of UnconfiguredReporter with no defined Choices raises "
              "SimpleBenchNotImplementedError/CHOICES_INVALID_ARG_VALUE"),
        action=UnconfiguredReporter,
        kwargs=reporter_kwargs().replace(choices=Choices()),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.CHOICES_INVALID_ARG_VALUE)),
])
def test_reporter_init(testspec: TestSpec) -> None:
    """Test Reporter init parameters."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('REPORT_001', TestAction(
        name=("report() with non-Case arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CASE_ARG"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': "not_a_case_instance",
                'choice': ConfiguredChoice()},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CASE_ARG)),
    idspec('REPORT_002', TestAction(
        name=("report() with non-Choice arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': "not_a_choice_instance"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_003', TestAction(
        name=("report() with non-Choice choice arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choices()},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_004', TestAction(
        name=("report() with Section not in Reporter's sections raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_SECTION"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(
                    **default_choice_kwargs_instance.replace(sections=[Section.NULL]))},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.REPORT_UNSUPPORTED_SECTION)),
    idspec('REPORT_005', TestAction(
        name=("report() with Target not in Reporter's targets raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_TARGET"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(
                    **default_choice_kwargs().replace(targets=[Target.CUSTOM]))},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.REPORT_UNSUPPORTED_TARGET)),
    idspec('REPORT_006', TestAction(
        name=("report() with Format not in Reporter's formats raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_FORMAT"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(
                    **default_choice_kwargs().replace(output_format=Format.CUSTOM))},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.REPORT_UNSUPPORTED_FORMAT)),
    idspec('REPORT_007', TestAction(
        name="report() with valid Case and Choice runs successfully",
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(**default_choice_kwargs()),
                'path': default_path()},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_008', TestAction(
        name="report() with valid callback runs successfully",
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(
                    **default_choice_kwargs().replace(targets=[Target.CALLBACK])),
                'callback': default_callback},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_009', TestAction(
        name=("report() with invalid callback raises"
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CALLBACK_ARG"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(**default_choice_kwargs().replace(targets=[Target.CALLBACK])),
                'callback': "not_a_callback"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CALLBACK_ARG)),
    idspec('REPORT_010', TestAction(
        name="report() with valid path runs successfully",
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(**default_choice_kwargs()),
                'path': default_path()},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_011', TestAction(
        name=("report() with invalid path raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_PATH_ARG"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(**default_choice_kwargs()),
                'path': "not_a_path"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_PATH_ARG)),
    idspec('REPORT_012', TestAction(
        name=("report() with valid session runs successfully"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(**default_choice_kwargs()),
                'path': default_path(),
                'session': ConfiguredSession()},
        expected=NO_EXPECTED_VALUE)),  # pragma: no cover (session not actually used),
    idspec('REPORT_013', TestAction(
        name=("report() with invalid session raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_SESSION_ARG"),
        action=ConfiguredReporter().report,
        kwargs={'args': namespace_instance(),
                'case': ConfiguredCase(),
                'choice': Choice(**default_choice_kwargs()),
                'path': default_path(),
                'session': "not_a_session"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_SESSION_ARG)),
])
def test_reporter_report(testspec: TestSpec) -> None:
    """Test Reporter.report() method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_ADD_CHOICE_001', TestAction(
        name="Adding a valid Choice to a Reporter works",
        action=ConfiguredReporter().add_choice,
        args=[Choice(**default_choice_kwargs().replace(name='dummy2', flags=['--dummy2']))],
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_ADD_CHOICE_002', TestAction(
        name=("Passing wrong type object to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_CHOICE_ARG"),
        action=ConfiguredReporter().add_choice,
        args=["not_a_choice_instance"],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_INVALID_ARG_TYPE)),
    idspec('REPORTER_ADD_CHOICE_003', TestAction(
        name=("Passing Choice with a section not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_SECTION_ARG"),
        action=ConfiguredReporter().add_choice,
        args=[Choice(**default_choice_kwargs().replace(
            name='dummy2', flags=['--dummy2'], sections=[Section.NULL]))],
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_SECTION)),
    idspec('REPORTER_ADD_CHOICE_004', TestAction(
        name=("Passing Choice with a target not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_TARGET_ARG"),
        action=ConfiguredReporter().add_choice,
        args=[Choice(**default_choice_kwargs().replace(
            name='dummy2', flags=['--dummy2'], targets=[Target.CUSTOM]))],
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_TARGET)),
    idspec('REPORTER_ADD_CHOICE_005', TestAction(
        name=("Passing Choice with a output_format not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/ADD_FORMAT_UNSUPPORTED_FORMAT"),
        action=ConfiguredReporter().add_choice,
        args=[Choice(**default_choice_kwargs().replace(
            name='dummy2', flags=['--dummy2'], output_format=Format.CUSTOM))],
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_FORMAT)),
])
def test_add_choice(testspec: TestSpec) -> None:
    """Test Reporter.add_choice() method."""
    testspec.run()


'''
class ConfiguredReporterForChoices(ConfiguredReporterInit):
    """A dummy Reporter subclass for testing add_flags_to_argparse()."""
    def __init__(self, *, choices: Choices) -> None:
        super().__init__(
            name='dummy',
            description='A dummy reporter for testing.',
            sections={Section.OPS},
            targets={Target.CONSOLE},
            formats={Format.RICH_TEXT},
            choices=choices)


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_ADD_FLAGS_001', TestAction(
        name="Adding a valid flag to an ArgumentParser",
        action=lambda: ConfiguredReporterForChoices(
            choices=Choices(choices=[ConfiguredChoice()])).add_flags_to_argparse(ArgumentParser()),
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_ADD_FLAGS_002', TestAction(
        name=("Passing a non-ArgumentParser to add_flags_to_argparse raises "
              "SimpleBenchTypeError/REPORTER_ADD_FLAGS_INVALID_PARSER_ARG"),
        action=lambda: ConfiguredReporterForChoices(
            choices=Choices(choices=[
                ConfiguredChoice(),
            ])).add_flags_to_argparse("not_an_argument_parser"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE)),
])
def test_reporter_add_flags_to_argparse(testspec: TestSpec) -> None:
    """Test Reporter.add_flags_to_argparse() method."""
    testspec.run()
'''


def test_attributes() -> None:
    """Test Reporter attributes.

    Verify that Reporter attributes are correctly set and immutable.
    """
    reporter: ConfiguredReporter = ConfiguredReporter()
    assert reporter.name == default_name(), "Failed to get Reporter.name"
    assert reporter.description == default_description(), "Failed to get Reporter.description"
    choices = reporter.choices
    assert isinstance(choices, Choices), "Failed to get Reporter.choices"
    with pytest.raises(AttributeError):
        reporter.name = "new_name"  # type: ignore[assignment,misc]
    with pytest.raises(AttributeError):
        reporter.description = "new_description"  # type: ignore[assignment,misc]
    with pytest.raises(AttributeError):
        reporter.choices = Choices(choices=[ConfiguredChoice()])  # type: ignore[assignment,misc]
