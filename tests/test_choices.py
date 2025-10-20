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

from .testspec import TestSpec, TestAction, TestGet, idspec, Assert, NO_EXPECTED_VALUE


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
            name="Choice with missing formats argument - raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE]),
            exception=TypeError,
        )),
        idspec("INIT_004", TestAction(
            name="Choice with empty list formats argument - raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_FORMATS_ARG_VALUE,
        )),
        idspec("INIT_005", TestAction(
            name="Choice with wrong type formats argument - raises SimpleBenchTypeError",
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
            name="Choice with missing targets argument - raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_008", TestAction(
            name="Choice with empty list targets argument - raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_TARGETS_ARG_VALUE,
        )),
        idspec("INIT_009", TestAction(
            name="Choice with wrong type targets argument - raises SimpleBenchTypeError",
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
            name="Choice with missing sections argument - raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_012", TestAction(
            name="Choice with empty list sections argument - raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='A sample choice',
                sections=[], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_SECTIONS_ARG_VALUE,
        )),
        idspec("INIT_013", TestAction(
            name="Choice with wrong type sections argument - raises SimpleBenchTypeError",
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
            name="Choice with missing description argument - raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_016", TestAction(
            name="Choice with blank string description argument - raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description='   ',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_DESCRIPTION_ARG_VALUE,
        )),
        idspec("INIT_017", TestAction(
            name="Choice with wrong type description argument - raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='sample', description=123,  # type: ignore[arg-type]
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_DESCRIPTION_ARG_TYPE,
        )),
        idspec("INIT_018", TestAction(
            name="Choice with missing name argument - raises TypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=TypeError,
        )),
        idspec("INIT_019", TestAction(
            name="Choice with blank string name argument - raises SimpleBenchValueError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name='   ', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICE_EMPTY_NAME_ARG_VALUE,
        )),
        idspec("INIT_020", TestAction(
            name="Choice with wrong type name argument - raises SimpleBenchTypeError",
            action=Choice,
            kwargs=ChoiceKWArgs(
                reporter=MockReporter(), flags=['--sample'], name=123,  # type: ignore[arg-type]
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON]),
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICE_INVALID_NAME_ARG_TYPE,
        )),
        idspec("INIT_021", TestAction(
            name="Choice with missing flags argument - raises TypeError",
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


@cache
def choice_instance(cache_id: str = 'default', *,  # pylint: disable=unused-argument
                    name: str = 'mock', flags: Sequence[str] = ('--mock',)) -> Choice:
    """Factory function to return the same mock Choice instance for testing."""
    return Choice(
        reporter=sample_reporter(),
        flags=flags,
        name=name,
        description='A mock choice.',
        sections=[Section.OPS], targets=[Target.CONSOLE], formats=[Format.JSON],
        extra='mock_extra')


@pytest.mark.parametrize(
    "testspec", [
        idspec("PROPS_001", TestGet(
            name="Choice reporter property",
            attribute="reporter",
            obj=choice_instance(),
            assertion=Assert.IS,
            expected=sample_reporter(),
        )),
        idspec("PROPS_002", TestGet(
            name="Choice flags property",
            attribute="flags",
            obj=choice_instance(),
            assertion=Assert.EQUAL,
            expected=frozenset(['--mock']),
        )),
        idspec("PROPS_003", TestGet(
            name="Choice name property",
            attribute="name",
            obj=choice_instance(),
            assertion=Assert.EQUAL,
            expected='mock',
        )),
        idspec("PROPS_004", TestGet(
            name="Choice description property",
            attribute="description",
            obj=choice_instance(),
            assertion=Assert.EQUAL,
            expected='A mock choice.',
        )),
        idspec("PROPS_005", TestGet(
            name="Choice sections property",
            attribute="sections",
            obj=choice_instance(),
            assertion=Assert.EQUAL,
            expected=frozenset([Section.OPS]),
        )),
        idspec("PROPS_006", TestGet(
            name="Choice targets property",
            attribute="targets",
            obj=choice_instance(),
            assertion=Assert.EQUAL,
            expected=frozenset([Target.CONSOLE]),
        )),
        idspec("PROPS_007", TestGet(
            name="Choice formats property",
            attribute="formats",
            obj=choice_instance(),
            assertion=Assert.EQUAL,
            expected=frozenset([Format.JSON]),
        )),
        idspec("PROPS_008", TestGet(
            name="Choice extra property",
            attribute="extra",
            obj=choice_instance(),
            assertion=Assert.EQUAL,
            expected='mock_extra',
        )),
    ]
)
def test_choice_properties(testspec: TestSpec):
    """Test Choice properties return expected values."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestAction(
            name="Choices with a list of Choice instances",
            action=Choices,
            kwargs=ChoicesKWArgs(
                choices=[
                    choice_instance(),
                ]),
            validate_result=lambda result: len(result) == 1 and result['mock'] is choice_instance(),
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_002', TestAction(
            name="Missing choices argument - creates default empty Choices",
            action=Choices,
            kwargs=ChoicesKWArgs(),
            validate_result=lambda result: len(result) == 0,
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_003', TestAction(
            name="Choices initialized using a different Choices instance",
            action=Choices,
            kwargs=ChoicesKWArgs(choices=Choices(choices=[choice_instance()])),
            validate_result=lambda result: len(result) == 1 and result['mock'] is choice_instance(),
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_004', TestAction(
            name="Choices with invalid choices argument type - raises SimpleBenchTypeError",
            action=Choices,
            kwargs=ChoicesKWArgs(choices='not_a_sequence'),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICES_INVALID_CHOICES_ARG_TYPE,
        )),
    ]
)
def test_choices_init(testspec: TestSpec):
    """Test initializing Choices with various combinations of keyword arguments.

    This test verifies that the Choices class can be initialized correctly
    using different combinations of parameters provided through the
    ChoicesKWArgs class. It checks that the attributes of the Choices instance
    match the expected values based on the provided keyword arguments.
    """
    testspec.run()


@cache
def choices_instance(cache_id: str = "default", *,  # pylint: disable=unused-argument
                     choices: Sequence[Choice] | Choices | None = None) -> Choices:
    """Factory function to return a cached Choices instance for testing.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Choices instances if needed.
        choices (Sequence[Choice] | Choices | None, default=None):
            A sequence of Choice instances or a Choices instance to initialize the Choices instance.
    """
    return Choices() if choices is None else Choices(choices=choices)


@pytest.mark.parametrize(
    "testspec", [
        idspec("ADD_001", TestAction(
            name="Add valid Choice instance to Choices via choices.add(<keyword-argument>)",
            obj=choices_instance('ADD_001'),
            action=choices_instance('ADD_001').add,
            kwargs={'choice': choice_instance()},
            validate_obj=lambda choices: len(choices) == 1 and choices['mock'] is choice_instance(),
            expected=NO_EXPECTED_VALUE,
        )),
        idspec("ADD_002", TestAction(
            name="Add valid Choice instance to Choices via choices.add(<positional-argument>)",
            obj=choices_instance('ADD_002'),
            action=choices_instance('ADD_002').add,
            args=[choice_instance()],
            validate_obj=lambda choices: len(choices) == 1 and choices['mock'] is choice_instance(),
            expected=NO_EXPECTED_VALUE,
        )),
        idspec("ADD_003", TestAction(
            name="Add invalid type of object to Choices - raises SimpleBenchTypeError",
            obj=choices_instance('ADD_003'),
            action=choices_instance('ADD_003').add,
            args=['not_a_choice'],  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICES_ADD_INVALID_CHOICE_ARG_TYPE,
        )),
        idspec("ADD_004", TestAction(
            name="Add different Choice name to Choices",
            obj=choices_instance("ADD_004", choices=(choice_instance(
                "ADD_004", name='unique_choice', flags=('--unique-choice',)),)),
            action=choices_instance("ADD_004", choices=(choice_instance(
                "ADD_004", name='unique_choice', flags=('--unique-choice',)),)).add,
            args=[choice_instance(
                "ADD_004", name='another_unique_choice', flags=('--another-unique-choice',))],
            validate_obj=lambda choices: (
                len(choices) == 2 and
                choices['unique_choice'] is choice_instance(
                    "ADD_004", name='unique_choice', flags=('--unique-choice',)) and
                choices['another_unique_choice'] is choice_instance(
                    "ADD_004", name='another_unique_choice', flags=('--another-unique-choice',))),
            expected=NO_EXPECTED_VALUE,
        )),
        idspec("ADD_005", TestAction(
            name="Add duplicate Choice to Choices - raises SimpleBenchValueError",
            obj=choices_instance('ADD_005', choices=(choice_instance(),)),
            action=choices_instance('ADD_005', choices=(choice_instance(),)).add,
            args=[choice_instance()],
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.CHOICES_SETITEM_DUPLICATE_CHOICE_NAME)
        ),
    ]
)
def test_choices_add_method(testspec: TestSpec) -> None:
    """Test the Choices.add() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("ALL_CHOICE_ARGS_001", TestAction(
            name="Get all Choice args from Choices with no choices (expect empty set)",
            action=Choices().all_choice_args,
            assertion=Assert.EQUAL,
            expected=set(),
        )),
        idspec("ALL_CHOICE_ARGS_002", TestAction(
            name="Get all Choice args from Choices with multiple choices",
            action=Choices(choices=[
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_one', flags=('--one',)),
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_two', flags=('--two', '--deux')),
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_three', flags=('--three',)),
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_four', flags=('--fourth-item',)),
            ]).all_choice_args,
            assertion=Assert.EQUAL,
            expected={'one', 'two', 'deux', 'three', 'fourth_item'},
        )),
    ])
def test_choices_all_choice_args_method(testspec: TestSpec) -> None:
    """Test the Choices.all_choice_args() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("ALL_CHOICE_FLAGS_001", TestAction(
            name="Get all Choice flags from Choices with no choices (expect empty set)",
            action=Choices().all_choice_flags,
            assertion=Assert.EQUAL,
            expected=set(),
        )),
        idspec("ALL_CHOICE_FLAGS_002", TestAction(
            name="Get all Choice flags from Choices with multiple choices",
            action=Choices(choices=[
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_one', flags=('--one',)),
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_two', flags=('--two', '--deux')),
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_three', flags=('--three',)),
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_four', flags=('--fourth-item',)),
            ]).all_choice_flags,
            assertion=Assert.EQUAL,
            expected={'--one', '--two', '--deux', '--three', '--fourth-item'},
        )),
    ])
def test_choices_all_choice_flags_method(testspec: TestSpec) -> None:
    """Test the Choices.all_choice_flags() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("GET_CHOICE_FOR_ARG_001", TestAction(
            name="Get Choice for existing arg",
            action=Choices(choices=[
                choice_instance('GET_CHOICE_FOR_ARG_001', name='choice_one', flags=('--one',)),
                choice_instance('GET_CHOICE_FOR_ARG_001', name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=['one'],
            assertion=Assert.IS,
            expected=choice_instance('GET_CHOICE_FOR_ARG_001', name='choice_one', flags=('--one',)),
        )),
        idspec("GET_CHOICE_FOR_ARG_002", TestAction(
            name="Get non-existing Choice arg (expect None)",
            action=Choices(choices=[
                choice_instance('GET_CHOICE_FOR_ARG_002', name='choice_one', flags=('--one',)),
                choice_instance('GET_CHOICE_FOR_ARG_002', name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=['nonexistent'],
            assertion=Assert.IS,
            expected=None,
        )),
        idspec("GET_CHOICE_FOR_ARG_003", TestAction(
            name="Get Choice with wrong type arg (raises SimpleBenchTypeError)",
            action=Choices(choices=[
                choice_instance('GET_CHOICE_FOR_ARG_003', name='choice_one', flags=('--one',)),
                choice_instance('GET_CHOICE_FOR_ARG_003', name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=[123],  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.CHOICES_GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE,
        )),
    ])
def test_choices_get_choice_for_arg_method(testspec: TestSpec) -> None:
    """Test the Choices.get_choice_for_arg() method."""
    testspec.run()
