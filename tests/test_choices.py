"""Tests for choices.py module."""


from functools import cache
import inspect
from pathlib import Path
from typing import Sequence, Any, Optional

import pytest

from simplebench.case import Case
from simplebench.exceptions import SimpleBenchValueError, SimpleBenchTypeError, ErrorTag
from simplebench.session import Session
from simplebench.reporters.interfaces import ReporterCallback
from simplebench.enums import Section, Target, Format
from simplebench.reporters import Reporter
from simplebench.reporters.choices import Choices, Choice

from .testspec import TestSpec, TestAction, idspec, Assert


class NoDefaultValue:
    """A sentinel class to indicate no default value is provided."""


class ChoiceKWArgs(dict):
    """A class to hold keyword arguments for initializing a Choice instance.

    This class is primarily used to facilitate testing of the Choice class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Choice class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self, *,
            reporter: Reporter | NoDefaultValue = NoDefaultValue(),
            flags: Sequence[str] | NoDefaultValue = NoDefaultValue(),
            name: str | NoDefaultValue = NoDefaultValue(),
            description: str | NoDefaultValue = NoDefaultValue(),
            sections: Sequence[Section] | NoDefaultValue = NoDefaultValue(),
            targets: Sequence[Target] | NoDefaultValue = NoDefaultValue(),
            formats: Sequence[Format] | NoDefaultValue = NoDefaultValue(),
            extra: Any | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ChoiceKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choice instance in tests.

        Args:
            reporter (Reporter| NoDefaultValue, default=NoDefaultValue()):
                An instance of a Reporter subclass.
            flags (Sequence[str] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of command-line flags associated with the choice.
            name (str | NoDefaultValue, default=NoDefaultValue()):
                A unique name for the choice.
            description (str | NoDefaultValue, default=NoDefaultValue()):
                A brief description of the choice.
            sections (Sequence[Section] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of Section enums to include in the report.
            targets (Sequence[Target] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of Target enums for output.
            formats (Sequence[Format] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of Format enums for output.
            extra (Any | NoDefaultValue, default=NoDefaultValue()):
                Any additional metadata associated with the choice. Defaults to None.
        """
        kwargs = {}
        for key in ('reporter', 'flags', 'name', 'description',
                    'sections', 'targets', 'formats', 'extra'):
            value = locals()[key]
            if not isinstance(value, NoDefaultValue):
                kwargs[key] = value
        super().__init__(**kwargs)


def test_choicekwargs_matches_choice_signature():
    """Verify ChoiceKWArgs signature matches Choice.__init__.

    This test ensures that the ChoiceKWArgs class has the same parameters as
    the Choice class's __init__ method. This prevents discrepancies between
    the two classes that could lead to errors in tests or misunderstandings
    about the parameters required to initialize a Choice instance.
    """
    choice_sig = inspect.signature(Choice.__init__)
    choicekwargs_sig = inspect.signature(ChoiceKWArgs.__init__)

    # Get parameter names (excluding 'self')
    choice_params = set(choice_sig.parameters.keys()) - {'self'}
    choicekwargs_params = set(choicekwargs_sig.parameters.keys()) - {'self'}

    assert choice_params == choicekwargs_params, \
        f"Mismatch: Choice has {choice_params - choicekwargs_params}, " \
        f"ChoiceKWArgs has {choicekwargs_params - choice_params}"


class ChoicesKWArgs(dict):
    """A class to hold keyword arguments for initializing a Choices instance.

    This class is primarily used to facilitate testing of the Choices class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Choices class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            choices: Sequence[Choice] | Choices | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ChoicesKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choices instance in tests.

        Args:
            choices (Sequence[Choice] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of Choice instances.
        """
        kwargs = {}
        for key in ('choices',):
            value = locals()[key]
            if not isinstance(value, NoDefaultValue):
                kwargs[key] = value
        super().__init__(**kwargs)


def test_choiceskwargs_matches_choices_signature():
    """Verify ChoicesKWArgs signature matches Choices.__init__.

    This test ensures that the ChoicesKWArgs class has the same parameters as
    the Choices class's __init__ method. This prevents discrepancies between
    the two classes that could lead to errors in tests or misunderstandings
    about the parameters required to initialize a Choices instance.
    """
    choices_sig = inspect.signature(Choices.__init__)
    choiceskwargs_sig = inspect.signature(ChoicesKWArgs.__init__)

    # Get parameter names (excluding 'self')
    choices_params = set(choices_sig.parameters.keys()) - {'self'}
    choiceskwargs_params = set(choiceskwargs_sig.parameters.keys()) - {'self'}

    assert choices_params == choiceskwargs_params, \
        f"Mismatch: Choices has {choices_params - choiceskwargs_params}, " \
        f"ChoicesKWArgs has {choiceskwargs_params - choices_params}"


class MockReporterExtras:
    """A mock ReporterExtras subclass for testing Choice initialization."""
    def __init__(self, full_data: bool = False) -> None:
        self.full_data = full_data


class MockReporter(Reporter):
    """A mock Reporter subclass for testing Choice initialization."""
    def __init__(self) -> None:  # pylint: disable=useless-parent-delegation
        super().__init__(
            name='mock',
            description='Mock reporter.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.FILESYSTEM, Target.CALLBACK},
            formats={Format.JSON},
            choices=Choices([
                Choice(
                    reporter=self,
                    flags=['--mock'],
                    name='mock',
                    description='statistical results to mock',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    formats=[Format.JSON],
                    extra=MockReporterExtras(full_data=False)),
            ]))

    def run_report(self,
                   *,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Mock implementation of run_report."""


@cache
def sample_reporter() -> Reporter:
    """Factory function to return a sample MockReporter instance for testing."""
    return MockReporter()


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestAction(
            name="Choice with all parameters",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON], extra={'key': 'value'}),
            assertion=Assert.ISINSTANCE,
            expected=Choice,
        )),
        idspec("INIT_002", TestAction(
            name="Choice with no extra parameter",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            assertion=Assert.ISINSTANCE,
            expected=Choice,
        )),
        idspec("INIT_003", TestAction(
            name="Choice with missing formats argument- raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE]),
            exception=TypeError,
        )),
        idspec("INIT_004", TestAction(
            name="Choice with empty list formats argument- raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_FORMATS_ARG_VALUE,
        )),
        idspec("INIT_005", TestAction(
            name="Choice with wrong type formats argument- raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats={}),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_FORMATS_ARG_TYPE,
        )),
        idspec("INIT_006", TestAction(
            name="Choice with incorrect formats list item type - raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE],
                formats=['invalid_format']),  # type: ignore[list-item]
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_FORMATS_ARG_TYPE,
        )),
        idspec("INIT_007", TestAction(
            name="Choice with missing targets argument- raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_008", TestAction(
            name="Choice with empty list targets argument- raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_TARGETS_ARG_VALUE,
        )),
        idspec("INIT_009", TestAction(
            name="Choice with wrong type targets argument- raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets={}, formats=[Format.JSON]),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_TARGETS_ARG_TYPE,
        )),
        idspec("INIT_010", TestAction(
            name="Choice with incorrect targets list item type - raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=['invalid_target'],  # type: ignore[list-item]
                formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_TARGETS_ARG_TYPE,
        )),
        idspec("INIT_011", TestAction(
            name="Choice with missing sections argument- raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_012", TestAction(
            name="Choice with empty list sections argument- raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_SECTIONS_ARG_VALUE,
        )),
        idspec("INIT_013", TestAction(
            name="Choice with wrong type sections argument- raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections={}, targets=[Target.CONSOLE], formats=[Format.JSON]),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_SECTIONS_ARG_TYPE,
        )),
        idspec("INIT_014", TestAction(
            name="Choice with incorrect sections list item type - raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=['invalid_section'], targets=[Target.CONSOLE],  # type: ignore[list-item]
                formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_SECTIONS_ARG_TYPE,
        )),
        idspec("INIT_015", TestAction(
            name="Choice with missing description argument- raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_016", TestAction(
            name="Choice with blank string description argument- raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='   ',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_DESCRIPTION_ARG_VALUE,
        )),
        idspec("INIT_017", TestAction(
            name="Choice with wrong type description argument- raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description=123,  # type: ignore[arg-type]
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_DESCRIPTION_ARG_TYPE,
        )),
        idspec("INIT_018", TestAction(
            name="Choice with missing name argument- raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_019", TestAction(
            name="Choice with blank string name argument- raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='   ', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_NAME_ARG_VALUE,
        )),
        idspec("INIT_020", TestAction(
            name="Choice with wrong type name argument- raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name=123,  # type: ignore[arg-type]
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_NAME_ARG_TYPE,
        )),
        idspec("INIT_021", TestAction(
            name="Choice with missing flags argument- raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_022", TestAction(
            name="Choice with empty list flags argument - raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=[], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_INVALID_FLAGS_ARGS_VALUE,
        )),
        idspec("INIT_023", TestAction(
            name="Choice with flag with whitespace - raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--valid', '--bad flag'], name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_INVALID_FLAGS_ARGS_VALUE,
        )),
        idspec("INIT_024", TestAction(
            name="Choice with wrong type flags argument - raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags='--sample',  # type: ignore[arg-type]
                name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_FLAGS_ARG_TYPE,
        )),
        idspec("INIT_025", TestAction(
            name="Choice with missing reporter argument - raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_026", TestAction(
            name="Choice with wrong type reporter argument - raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter='not_a_reporter',  # type: ignore[arg-type]
                flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_REPORTER_ARG_TYPE,
        )),
    ]
)
def test_choice_initialization_with_kwargs(testspec: TestSpec):
    """Test initializing Choice with various combinations of keyword arguments.

    This test verifies that the Choice class can be initialized correctly
    using different combinations of parameters provided through the
    ChoiceKWArgs class. It checks that the attributes of the Choice instance
    match the expected values based on the provided keyword arguments.
    """
    testspec.run()
