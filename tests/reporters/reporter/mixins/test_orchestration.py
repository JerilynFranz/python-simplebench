"""Tests for the simplebench.reporters.reporter.mixins._OrchestrationMixin mixin class."""
from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias

import pytest
from rich.table import Table
from rich.text import Text

from simplebench.case import Case
from simplebench.enums import Section, Target
from simplebench.exceptions import SimpleBenchValueError
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.protocols import ReportRenderer
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.options import ReporterOptions

from ....factories import (
    FactoryReporter,
    FactoryReporterOptions,
    argument_parser_factory,
    case_factory,
    choice_conf_kwargs_factory,
    default_reporter_callback,
    list_of_strings_flag_factory,
    path_factory,
    reporter_kwargs_factory,
    session_factory,
)
from ....factories.reporter.reporter_methods import CallbackSpy, ConsoleSpy, FileSystemSpy, RenderSpy
from ....kwargs.reporters.reporter import RenderByCaseMethodKWArgs
from ....testspec import Assert, TestAction, TestGet, TestSpec, idspec

if TYPE_CHECKING:
    from simplebench.reporters.choice.choice import Choice
    from simplebench.reporters.reporter.protocols import ReporterCallback
    from simplebench.session import Session

Output: TypeAlias = str | bytes | Text | Table


class RenderByCaseReporterFactoryOptions(FactoryReporterOptions):
    """Factory reporter options for render_by_case tests."""


class FactoryReporterRenderByCase(FactoryReporter):
    """Factory reporter with mock methods for testing the `render_by_case()` method.

    Overrides:
        render(): Uses a `RenderSpy` to record calls to `render()`.
        target_console(): Uses a `ConsoleSpy` to record calls to `target_console()`.
        target_callback(): Uses a `CallbackSpy` to record calls to `target_callback()`.
        target_filesystem(): Uses a `FileSystemSpy` to record calls to `target_filesystem()`.
    """
    _OPTIONS_TYPE = RenderByCaseReporterFactoryOptions
    _OPTIONS_KWARGS = {}

    def __init__(self, choices: ChoicesConf) -> None:
        """Initialize the FactoryReporterRenderByCase with mock method spies.

        Args:
            choices (ChoicesConf): The choices configuration for the reporter.
        """

        reporter_kwargs = reporter_kwargs_factory().replace(
            choices=choices,
            targets={Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK, Target.INVALID},)
        super().__init__(**reporter_kwargs)
        self.render_spy: RenderSpy = RenderSpy()
        self.target_console = ConsoleSpy()  # type: ignore[method-assign,assignment,reporterAttributeAccessIssue]
        """Spy for console target method calls."""
        self.target_callback = CallbackSpy()  # type: ignore[method-assign,assignment,reporterAttributeAccessIssue]
        """Spy for callback target method calls."""
        self.target_filesystem = FileSystemSpy()  # type: ignore[method-assign,assignment,reporterAttributeAccessIssue]
        """Spy for filesystem target method calls."""

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> Output:
        """Render the report for the given case, section, and options.

        Unlike the base FactoryReporter, this method uses a RenderSpy
        to record calls for testing purposes.
        """
        return self.render_spy(case=case, section=section, options=options)


def render_by_case_reporter_factory(choice_name: str,
                                    sections: set[Section] | None = None,
                                    targets: set[Target] | None = None,
                                    default_targets: set[Target] | None = None) -> FactoryReporterRenderByCase:
    """Generate a FactoryReporterRenderByCase testing instance.

    It is created with a single choice configured for render_by_case tests
    with all sections and targets enabled, a console default target, and
    using RenderByCaseReporterFactoryOptions for options.

    Default Options:
    - name = `choice_name`
    - sections = `{Section.MEMORY, Section.OPS, Section.TIMING, Section.PEAK_MEMORY}`
    - targets = `{Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK}`
    - default_targets = `{Target.CONSOLE}`
    - options = `RenderByCaseReporterFactoryOptions()`

    Args:
        choice_name (str): The name of the choice to create.
        sections (set[Section] | None): The set of sections for the reporter.
            If `None`, sections will default to
            `{Section.MEMORY, Section.OPS, Section.TIMING, Section.PEAK_MEMORY}`.
        targets (set[Target] | None): The set of targets for the reporter.
            If `None`, targets will default to
            `{Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK}`.
        default_targets (set[Target] | None): The set of default targets for the reporter.
            If `None`, default_targets will default to `{Target.CONSOLE}`.
    Returns:
        FactoryReporterRenderByCase: The testing reporter instance.

    """
    sections = sections or {Section.MEMORY, Section.OPS, Section.TIMING, Section.PEAK_MEMORY}
    default_targets = default_targets or {Target.CONSOLE}
    targets = targets or {Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK}
    choice_conf_kwargs = choice_conf_kwargs_factory(cache_id=None).replace(
        name=choice_name,
        sections=sections,
        targets=targets,
        default_targets=default_targets,
        options=RenderByCaseReporterFactoryOptions(),
    )
    choices_conf = ChoicesConf([ChoiceConf(**choice_conf_kwargs)])
    reporter = FactoryReporterRenderByCase(choices=choices_conf)
    return reporter


def render_by_case_testspecs() -> list[TestSpec]:
    """Generate test specifications for the render_by_case method tests."""
    testspecs: list[TestSpec] = []

    choice_name: str = "test_choice"
    reporter: FactoryReporterRenderByCase = render_by_case_reporter_factory(choice_name=choice_name)
    renderer: ReportRenderer = reporter.render
    choice: Choice = reporter.choices[choice_name]
    path: Path = path_factory(cache_id=None)
    case: Case = case_factory(cache_id=None)
    session: Session = session_factory(cache_id=None)
    callback: ReporterCallback = default_reporter_callback
    flag_name: str = next(iter(choice.flags))  # Use the first flag of the choice (only one exists)
    args: Namespace = argument_parser_factory(
            arguments=[
                list_of_strings_flag_factory(
                    flag=flag_name, choices=[
                        Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value])]
        ).parse_args([flag_name,
                      Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value])
    render_by_case_kwargs = RenderByCaseMethodKWArgs(
                                renderer=renderer,
                                args=args,
                                case=case,
                                choice=choice,
                                path=path,
                                session=session,
                                callback=callback)
    reporter.render_by_case(**render_by_case_kwargs)

    testspecs.extend([
        idspec("BY_CASE_001", TestGet(
            name="Verify exactly one render call was made",
            obj=reporter.render_spy,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
        idspec("BY_CASE_002", TestGet(
            name="Verify exactly one console target call was made",
            obj=reporter.target_console,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
        idspec("BY_CASE_003", TestGet(
            name="Verify exactly one filesystem target call was made",
            obj=reporter.target_filesystem,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
        idspec("BY_CASE_004", TestGet(
            name="Verify exactly one callback target call was made",
            obj=reporter.target_callback,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
    ])

    bad_target_reporter: FactoryReporterRenderByCase = render_by_case_reporter_factory(
        choice_name=choice_name,
        targets={Target.INVALID, Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK},
        default_targets={Target.INVALID})
    renderer = bad_target_reporter.render
    choice = bad_target_reporter.choices[choice_name]
    args = argument_parser_factory(
                arguments=[
                    list_of_strings_flag_factory(
                        flag=flag_name, choices=[
                            Target.CONSOLE.value, Target.FILESYSTEM.value,
                            Target.CALLBACK.value, Target.INVALID.value])]
        ).parse_args([flag_name, Target.INVALID.value])
    render_by_case_kwargs = RenderByCaseMethodKWArgs(
                                renderer=renderer,
                                args=args,
                                case=case,
                                choice=choice,
                                path=path,
                                session=session,
                                callback=callback)
    testspecs.append(idspec("BY_CASE_005", TestAction(
        name=("Verify that specifying an unsupported target raises "
              "a SimpleBenchValueError/RENDER_BY_CASE_UNSUPPORTED_TARGET"),
        action=bad_target_reporter.render_by_case,
        kwargs=render_by_case_kwargs,
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.RENDER_BY_CASE_UNSUPPORTED_TARGET)))

    return testspecs


@pytest.mark.parametrize("testspec", render_by_case_testspecs())
def test_render_by_case(testspec: TestSpec) -> None:
    """Test the render_by_case method of the OrchestrationMixin."""
    testspec.run()
