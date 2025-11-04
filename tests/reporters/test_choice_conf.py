"""Tests for choices.py module."""
from argparse import Namespace
from functools import cache
from pathlib import Path
from typing import Sequence, Optional

import pytest

from tests.kwargs import ChoiceConfKWArgs
from tests.testspec import TestSpec, TestAction, TestGet, idspec, Assert

from simplebench.case import Case
from simplebench.exceptions import SimpleBenchValueError, SimpleBenchTypeError
from simplebench.session import Session
from simplebench.reporters.protocols import ReporterCallback
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.choice.choice_conf import ChoiceConf, ChoiceConfErrorTag


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
            default_targets={Target.CONSOLE},
            targets={Target.FILESYSTEM, Target.CALLBACK},
            subdir='mockreports',
            options_type=ReporterOptions,
            file_suffix='mock',
            file_unique=True,
            file_append=False,
            formats={Format.JSON},
            choices=[
                ChoiceConf(
                    flags=['--mock'],
                    flag_type=FlagType.BOOLEAN,
                    name='mock',
                    description='statistical results to mock',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    output_format=Format.JSON,
                    file_suffix='mock',
                    file_unique=True,
                    file_append=False,
                    options=ReporterOptions(),
                    extra=MockReporterExtras(full_data=False)),
            ])

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Mock implementation of run_report."""

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """Mock implementation of render."""
        return "mocked_rendered_output"


@cache
def sample_reporter() -> Reporter:
    """Factory function to return a sample MockReporter instance for testing."""
    return MockReporter()


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestAction(
            name="ChoiceConf with all parameters",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice', file_suffix='sample', file_unique=True, file_append=False,
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON, extra={'key': 'value'}),
            assertion=Assert.ISINSTANCE,
            expected=ChoiceConf,
        )),
        idspec("INIT_002", TestAction(
            name="ChoiceConf with no extra parameter",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            assertion=Assert.ISINSTANCE,
            expected=ChoiceConf,
        )),
        idspec("INIT_003", TestAction(
            name="ChoiceConf with missing formats argument - raises TypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE]),
            exception=TypeError,
        )),
        idspec("INIT_005", TestAction(
            name="ChoiceConf with wrong type output_format argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=''),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.OUTPUT_FORMAT_INVALID_ARG_TYPE,
        )),
        idspec("INIT_007", TestAction(
            name="ChoiceConf with missing targets argument - raises TypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], output_format=Format.JSON),
            exception=TypeError,
        )),
        idspec("INIT_008", TestAction(
            name="ChoiceConf with empty list targets argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets=[], output_format=Format.JSON),
            exception=SimpleBenchValueError,
            exception_tag=ChoiceConfErrorTag.TARGETS_INVALID_ARG_VALUE,
        )),
        idspec("INIT_009", TestAction(
            name="ChoiceConf with wrong type targets argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets="not_targets", output_format=Format.JSON),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.TARGETS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_010", TestAction(
            name="ChoiceConf with incorrect targets list item type - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets=['invalid_target'],  # type: ignore[list-item]
                output_format=Format.JSON),
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.TARGETS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_011", TestAction(
            name="ChoiceConf with missing sections argument - raises TypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=TypeError,
        )),
        idspec("INIT_012", TestAction(
            name="ChoiceConf with empty list sections argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchValueError,
            exception_tag=ChoiceConfErrorTag.SECTIONS_INVALID_ARG_VALUE,
        )),
        idspec("INIT_013", TestAction(
            name="ChoiceConf with wrong type sections argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections="not_sections", targets=[Target.CONSOLE], output_format=Format.JSON),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.SECTIONS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_014", TestAction(
            name="ChoiceConf with incorrect sections list item type - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=['invalid_section'], targets=[Target.CONSOLE],  # type: ignore[list-item]
                output_format=Format.JSON),
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.SECTIONS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_015", TestAction(
            name="ChoiceConf with missing description argument - raises TypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=TypeError,
        )),
        idspec("INIT_016", TestAction(
            name="ChoiceConf with blank string description argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='sample',
                description='   ',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchValueError,
            exception_tag=ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_VALUE,
        )),
        idspec("INIT_017", TestAction(
            name="ChoiceConf with wrong type description argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN,
                name='sample', description=123,  # type: ignore[arg-type]
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
        )),
        idspec("INIT_018", TestAction(
            name="ChoiceConf with missing name argument - raises TypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN,
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=TypeError,
        )),
        idspec("INIT_019", TestAction(
            name="ChoiceConf with blank string name argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN, name='   ',
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchValueError,
            exception_tag=ChoiceConfErrorTag.NAME_INVALID_ARG_VALUE,
        )),
        idspec("INIT_020", TestAction(
            name="ChoiceConf with wrong type name argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--sample'], flag_type=FlagType.BOOLEAN,
                name=123,  # type: ignore[arg-type]
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.NAME_INVALID_ARG_TYPE,
        )),
        idspec("INIT_021", TestAction(
            name="ChoiceConf with missing flags argument - raises TypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flag_type=FlagType.BOOLEAN, name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=TypeError,
        )),
        idspec("INIT_022", TestAction(
            name="ChoiceConf with empty list flags argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=[], flag_type=FlagType.BOOLEAN, name='sample',
                description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchValueError,
            exception_tag=ChoiceConfErrorTag.FLAGS_INVALID_ARGS_VALUE,
        )),
        idspec("INIT_023", TestAction(
            name="ChoiceConf with flag with whitespace - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags=['--valid', '--bad flag'], flag_type=FlagType.BOOLEAN,
                name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchValueError,
            exception_tag=ChoiceConfErrorTag.FLAGS_INVALID_ARGS_VALUE,
        )),
        idspec("INIT_024", TestAction(
            name="ChoiceConf with wrong type flags argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=ChoiceConfKWArgs(
                flags='--sample', flag_type=FlagType.BOOLEAN,  # type: ignore[arg-type]
                name='sample', description='A sample choice',
                sections=[Section.OPS], targets=[Target.CONSOLE], output_format=Format.JSON),
            exception=SimpleBenchTypeError,
            exception_tag=ChoiceConfErrorTag.FLAGS_INVALID_ARG_TYPE,
        )),
    ]
)
def test_initialization(testspec: TestSpec):
    """Test initializing Choice with various combinations of keyword arguments.

    This test verifies that the Choice class can be initialized correctly
    using different combinations of parameters provided through the
    ChoiceConfKWArgs class. It checks that the attributes of the Choice instance
    match the expected values based on the provided keyword arguments.
    """
    testspec.run()


@cache
def choice_conf_instance(cache_id: str = 'default', *,  # pylint: disable=unused-argument
                         name: str = 'mock', flags: Sequence[str] = ('--mock',)) -> ChoiceConf:
    """Factory function to return the same mock Choice instance for testing."""
    return ChoiceConf(
        flags=flags,
        flag_type=FlagType.BOOLEAN,
        name=name,
        description='A mock choice.',
        sections=[Section.OPS], targets=[Target.CONSOLE],
        output_format=Format.JSON,
        extra='mock_extra')


@pytest.mark.parametrize(
    "testspec", [
        idspec("PROPS_001", TestGet(
            name="ChoiceConf flags property",
            attribute="flags",
            obj=choice_conf_instance(),
            assertion=Assert.EQUAL,
            expected=frozenset(['--mock']),
        )),
        idspec("PROPS_002", TestGet(
            name="ChoiceConf name property",
            attribute="name",
            obj=choice_conf_instance(),
            assertion=Assert.EQUAL,
            expected='mock',
        )),
        idspec("PROPS_003", TestGet(
            name="ChoiceConf description property",
            attribute="description",
            obj=choice_conf_instance(),
            assertion=Assert.EQUAL,
            expected='A mock choice.',
        )),
        idspec("PROPS_004", TestGet(
            name="ChoiceConf sections property",
            attribute="sections",
            obj=choice_conf_instance(),
            assertion=Assert.EQUAL,
            expected=frozenset([Section.OPS]),
        )),
        idspec("PROPS_005", TestGet(
            name="ChoiceConf targets property",
            attribute="targets",
            obj=choice_conf_instance(),
            assertion=Assert.EQUAL,
            expected=frozenset([Target.CONSOLE]),
        )),
        idspec("PROPS_006", TestGet(
            name="ChoiceConf formats property",
            attribute="output_format",
            obj=choice_conf_instance(),
            assertion=Assert.EQUAL,
            expected=Format.JSON,
        )),
        idspec("PROPS_007", TestGet(
            name="ChoiceConf extra property",
            attribute="extra",
            obj=choice_conf_instance(),
            assertion=Assert.EQUAL,
            expected='mock_extra',
        )),
    ]
)
def test_choice_properties(testspec: TestSpec):
    """Test Choice properties return expected values."""
    testspec.run()
