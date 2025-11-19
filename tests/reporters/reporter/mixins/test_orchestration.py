"""Tests for the simplebench.reporters.reporter.mixins._OrchestrationMixin mixin class."""
from typing import TypeAlias, TypeVar

import pytest
from rich.table import Table
from rich.text import Text

from simplebench.case import Case
from simplebench.enums import Section, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.exceptions import _ReporterErrorTag
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
    reporter_config_factory,
    session_factory,
)
from ....factories.reporter.reporter_methods import (
    CallbackSpy,
    ConsoleSpy,
    FileSystemSpy,
    RenderSpy,
    dispatch_to_targets_kwargs_factory,
    render_by_case_kwargs_factory,
    render_by_section_kwargs_factory,
)
from ....kwargs.reporters.reporter import RenderByCaseMethodKWArgs, RenderBySectionMethodKWArgs
from ....testspec import Assert, TestAction, TestGet, TestSpec, idspec

Output: TypeAlias = str | bytes | Text | Table


class RenderOrchestrationReporterFactoryOptions(FactoryReporterOptions):
    """Factory reporter options for orchestration tests."""


class FactoryReporterForOrchestration(FactoryReporter):
    """Factory reporter with mock methods for testing orchestration methods.

    Overrides:
        render(): Uses a `RenderSpy` to record calls to `render()`.
        target_console(): Uses a `ConsoleSpy` to record calls to `target_console()`.
        target_callback(): Uses a `CallbackSpy` to record calls to `target_callback()`.
        target_filesystem(): Uses a `FileSystemSpy` to record calls to `target_filesystem()`.
    """
    _OPTIONS_TYPE = RenderOrchestrationReporterFactoryOptions
    _OPTIONS_KWARGS = {}

    def __init__(self, choices: ChoicesConf) -> None:
        """Initialize the FactoryReporterForOrchestration with mock method spies.

        :param choices: The choices configuration for the reporter.
        :type choices: ChoicesConf
        """
        reporter_options = reporter_config_factory(
            choices=choices,
            targets={Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK, Target.INVALID},)
        super().__init__(reporter_options)
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

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: The rendered output.
        :rtype: Output
        """
        return self.render_spy(case=case, section=section, options=options)


def _orchestration_reporter_factory(choice_name: str,
                                    sections: set[Section] | None = None,
                                    targets: set[Target] | None = None,
                                    default_targets: set[Target] | None = None) -> FactoryReporterForOrchestration:
    """Generate a FactoryReporterForOrchestration testing instance.

    :param choice_name: The name of the choice.
    :type choice_name: str
    :param sections: The sections to include.
    :type sections: set[Section] | None
    :param targets: The targets to include.
    :type targets: set[Target] | None
    :param default_targets: The default targets.
    :type default_targets: set[Target] | None
    :return: A factory reporter for orchestration.
    :rtype: FactoryReporterForOrchestration
    """
    sections = sections or {Section.MEMORY, Section.OPS, Section.TIMING, Section.PEAK_MEMORY}
    default_targets = default_targets or {Target.CONSOLE}
    targets = targets or {Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK}
    choice_conf_kwargs = choice_conf_kwargs_factory(cache_id=None).replace(
        name=choice_name,
        sections=sections,
        targets=targets,
        default_targets=default_targets,
        options=RenderOrchestrationReporterFactoryOptions(),
    )
    choices_conf = ChoicesConf([ChoiceConf(**choice_conf_kwargs)])
    reporter = FactoryReporterForOrchestration(choices=choices_conf)
    return reporter


T = TypeVar("T", RenderByCaseMethodKWArgs, RenderBySectionMethodKWArgs)


def _setup_good_path(
    kwargs_class: type[T],
    choice_name: str,
    sections: set[Section] | None = None
) -> tuple[FactoryReporterForOrchestration, T]:
    """Generic helper to arrange a 'good path' test scenario.

    :param kwargs_class: The kwargs class.
    :type kwargs_class: type[T]
    :param choice_name: The name of the choice.
    :type choice_name: str
    :param sections: The sections to include.
    :type sections: set[Section] | None
    :return: A tuple containing the reporter and the kwargs.
    :rtype: tuple[FactoryReporterForOrchestration, T]
    """
    reporter = _orchestration_reporter_factory(choice_name=choice_name, sections=sections)
    choice = reporter.choices[choice_name]
    flag_name: str = next(iter(choice.flags))
    target_values: list[str] = [Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value]
    args = argument_parser_factory(
        arguments=[list_of_strings_flag_factory(flag=flag_name, choices=target_values)]
    ).parse_args([flag_name, *target_values])
    kwargs = kwargs_class(
        renderer=reporter.render,
        args=args,
        case=case_factory(),
        choice=choice,
        path=path_factory(),
        session=session_factory(),
        callback=default_reporter_callback
    )
    return reporter, kwargs


def _setup_bad_target_path(
    kwargs_class: type[T],
    choice_name: str,
    sections: set[Section] | None = None
) -> tuple[FactoryReporterForOrchestration, T]:
    """Generic helper to arrange a 'bad target' test scenario.

    :param kwargs_class: The kwargs class.
    :type kwargs_class: type[T]
    :param choice_name: The name of the choice.
    :type choice_name: str
    :param sections: The sections to include.
    :type sections: set[Section] | None
    :return: A tuple containing the reporter and the kwargs.
    :rtype: tuple[FactoryReporterForOrchestration, T]
    """
    reporter = _orchestration_reporter_factory(
        choice_name=choice_name,
        sections=sections,
        targets={Target.INVALID, Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK},
        default_targets={Target.INVALID}
    )
    choice = reporter.choices[choice_name]
    flag_name = next(iter(choice.flags))
    target_values = [Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value, Target.INVALID.value]
    args = argument_parser_factory(
        arguments=[list_of_strings_flag_factory(flag=flag_name, choices=target_values)]
    ).parse_args([flag_name, Target.INVALID.value])
    kwargs = kwargs_class(
        renderer=reporter.render,
        args=args,
        case=case_factory(),
        choice=choice,
        path=path_factory(),
        session=session_factory(),
        callback=default_reporter_callback
    )
    return reporter, kwargs


def _setup_render_by_case_good_path() -> tuple[FactoryReporterForOrchestration, RenderByCaseMethodKWArgs]:
    """Helper to arrange the 'good path' test scenario for render_by_case.

    :return: A tuple containing the reporter and the kwargs.
    :rtype: tuple[FactoryReporterForOrchestration, RenderByCaseMethodKWArgs]
    """
    return _setup_good_path(  # type: ignore[return-value]
        kwargs_class=RenderByCaseMethodKWArgs,
        choice_name="test_choice"
    )


def _setup_render_by_section_good_path() -> tuple[FactoryReporterForOrchestration, RenderBySectionMethodKWArgs]:
    """Helper to arrange the 'good path' test scenario for render_by_section.

    :return: A tuple containing the reporter and the kwargs.
    :rtype: tuple[FactoryReporterForOrchestration, RenderBySectionMethodKWArgs]
    """
    return _setup_good_path(  # type: ignore[return-value]
        kwargs_class=RenderBySectionMethodKWArgs,
        choice_name="test_choice_by_section",
        sections={Section.MEMORY, Section.OPS, Section.TIMING}
    )


def _setup_render_by_case_bad_target_path() -> tuple[FactoryReporterForOrchestration, RenderByCaseMethodKWArgs]:
    """Helper to arrange the 'bad target' test scenario for render_by_case.

    :return: A tuple containing the reporter and the kwargs.
    :rtype: tuple[FactoryReporterForOrchestration, RenderByCaseMethodKWArgs]
    """
    return _setup_bad_target_path(  # type: ignore[return-value]
        kwargs_class=RenderByCaseMethodKWArgs,
        choice_name="bad_target_choice"
    )


def _setup_render_by_section_bad_target_path() -> tuple[FactoryReporterForOrchestration, RenderBySectionMethodKWArgs]:
    """Helper to arrange the 'bad target' test scenario for render_by_section.

    :return: A tuple containing the reporter and the kwargs.
    :rtype: tuple[FactoryReporterForOrchestration, RenderBySectionMethodKWArgs]
    """
    return _setup_bad_target_path(  # type: ignore[return-value]
        kwargs_class=RenderBySectionMethodKWArgs,
        choice_name="bad_target_choice_by_section"
    )


def render_by_case_testspecs() -> list[TestSpec]:
    """Generate test specifications for the render_by_case method tests.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    # --- Good Path Test Group ---
    good_reporter, good_kwargs = _setup_render_by_case_good_path()
    good_reporter.render_by_case(**good_kwargs)
    testspecs.extend([
        idspec("BY_CASE_001", TestGet(
            name="Verify exactly one render call was made",
            obj=good_reporter.render_spy,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
        idspec("BY_CASE_002", TestGet(
            name="Verify exactly one console target call was made",
            obj=good_reporter.target_console,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
        idspec("BY_CASE_003", TestGet(
            name="Verify exactly one filesystem target call was made",
            obj=good_reporter.target_filesystem,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
        idspec("BY_CASE_004", TestGet(
            name="Verify exactly one callback target call was made",
            obj=good_reporter.target_callback,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=1)),
    ])

    # --- Bad Path Test ---
    bad_target_reporter, bad_target_kwargs = _setup_render_by_case_bad_target_path()
    testspecs.append(idspec("BY_CASE_005", TestAction(
        name=("Verify that specifying an unsupported target raises "
              "a SimpleBenchValueError/RENDER_BY_CASE_UNSUPPORTED_TARGET"),
        action=bad_target_reporter.render_by_case,
        kwargs=bad_target_kwargs,
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_UNSUPPORTED_TARGET)))

    # --- Parameter Validation Tests ---
    render_by_case_kwargs = render_by_case_kwargs_factory(cache_id=None)
    testspecs.extend([
        idspec("BY_CASE_006", TestAction(
            name="Verify that invalid 'renderer' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_case,
            kwargs=render_by_case_kwargs.replace(renderer="invalid_renderer"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_RENDERER_ARG_TYPE)),
        idspec("BY_CASE_007", TestAction(
            name="Verify that invalid 'args' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_case,
            kwargs=render_by_case_kwargs.replace(args="invalid_args"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_ARGS_ARG_TYPE)),
        idspec("BY_CASE_008", TestAction(
            name="Verify that invalid 'case' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_case,
            kwargs=render_by_case_kwargs.replace(case="invalid_case"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CASE_ARG_TYPE)),
        idspec("BY_CASE_009", TestAction(
            name="Verify that invalid 'choice' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_case,
            kwargs=render_by_case_kwargs.replace(choice="invalid_choice"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CHOICE_ARG_TYPE)),
        idspec("BY_CASE_010", TestAction(
            name="Verify that invalid 'path' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_case,
            kwargs=render_by_case_kwargs.replace(path="invalid_path"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_PATH_ARG_TYPE)),
        idspec("BY_CASE_011", TestAction(
            name="Verify that invalid 'session' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_case,
            kwargs=render_by_case_kwargs.replace(session="invalid_session"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_SESSION_ARG_TYPE)),
        idspec("BY_CASE_012", TestAction(
            name="Verify that invalid 'callback' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_case,
            kwargs=render_by_case_kwargs.replace(callback="invalid_callback"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CALLBACK_ARG_TYPE)),
    ])

    return testspecs


def render_by_section_testspecs() -> list[TestSpec]:
    """Generate test specifications for the render_by_section method tests.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    # --- Good Path Test Group ---
    good_reporter, good_kwargs = _setup_render_by_section_good_path()
    # The number of sections determines how many times the spies should be called.
    num_sections = len(good_kwargs['choice'].sections)
    good_reporter.render_by_section(**good_kwargs)

    testspecs.extend([
        idspec("BY_SECTION_001", TestGet(
            name="Verify render is called once per section",
            obj=good_reporter.render_spy,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=num_sections)),
        idspec("BY_SECTION_002", TestGet(
            name="Verify console target is called once per section",
            obj=good_reporter.target_console,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=num_sections)),
        idspec("BY_SECTION_003", TestGet(
            name="Verify filesystem target is called once per section",
            obj=good_reporter.target_filesystem,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=num_sections)),
        idspec("BY_SECTION_004", TestGet(
            name="Verify callback target is called once per section",
            obj=good_reporter.target_callback,
            attribute="count",
            assertion=Assert.EQUAL,
            expected=num_sections)),
    ])

    # --- Bad Path Test ---
    bad_target_reporter, bad_target_kwargs = _setup_render_by_section_bad_target_path()
    testspecs.append(idspec("BY_SECTION_005", TestAction(
        name=("Verify that specifying an unsupported target raises "
              "a SimpleBenchValueError/RENDER_BY_SECTION_UNSUPPORTED_TARGET"),
        action=bad_target_reporter.render_by_section,
        kwargs=bad_target_kwargs,
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_UNSUPPORTED_TARGET)))

    # --- Parameter Validation Tests ---
    render_by_section_kwargs = render_by_section_kwargs_factory(cache_id=None)
    testspecs.extend([
        idspec("BY_SECTION_006", TestAction(
            name="Verify that invalid 'renderer' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_section,
            kwargs=render_by_section_kwargs.replace(renderer="invalid_renderer"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_RENDERER_ARG_TYPE)),
        idspec("BY_SECTION_007", TestAction(
            name="Verify that invalid 'args' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_section,
            kwargs=render_by_section_kwargs.replace(args="invalid_args"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_ARGS_ARG_TYPE)),
        idspec("BY_SECTION_008", TestAction(
            name="Verify that invalid 'case' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_section,
            kwargs=render_by_section_kwargs.replace(case="invalid_case"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CASE_ARG_TYPE)),
        idspec("BY_SECTION_009", TestAction(
            name="Verify that invalid 'choice' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_section,
            kwargs=render_by_section_kwargs.replace(choice="invalid_choice"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CHOICE_ARG_TYPE)),
        idspec("BY_SECTION_010", TestAction(
            name="Verify that invalid 'path' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_section,
            kwargs=render_by_section_kwargs.replace(path="invalid_path"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_PATH_ARG_TYPE)),
        idspec("BY_SECTION_011", TestAction(
            name="Verify that invalid 'session' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_section,
            kwargs=render_by_section_kwargs.replace(session="invalid_session"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_SESSION_ARG_TYPE)),
        idspec("BY_SECTION_012", TestAction(
            name="Verify that invalid 'callback' argument raises SimpleBenchTypeError",
            action=good_reporter.render_by_section,
            kwargs=render_by_section_kwargs.replace(callback="invalid_callback"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CALLBACK_ARG_TYPE)),
    ])

    return testspecs


@pytest.mark.parametrize("testspec", render_by_case_testspecs())
def test_render_by_case(testspec: TestSpec) -> None:
    """Test the render_by_case method of the OrchestrationMixin.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize("testspec", render_by_section_testspecs())
def test_render_by_section(testspec: TestSpec) -> None:
    """Test the render_by_section method of the OrchestrationMixin.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def dispatch_to_targets_params_testspecs() -> list[TestSpec]:
    """Generate test specifications for the dispatch_to_targets method tests.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    reporter = _orchestration_reporter_factory(choice_name="dispatch_test_choice")
    kwargs = dispatch_to_targets_kwargs_factory(cache_id=None)

    testspecs.extend([
        idspec("DISPATCH_001", TestAction(
            name="Verify that valid parameters do not raise an exception",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs)),
        idspec("DISPATCH_002", TestAction(
            name="Verify that invalid 'args' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(args="invalid_args"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_ARGS_ARG_TYPE)),
        idspec("DISPATCH_003", TestAction(
            name="Verify that invalid 'case' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(case="invalid_case"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_CASE_ARG_TYPE)),
        idspec("DISPATCH_004", TestAction(
            name="Verify that invalid 'choice' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(choice="invalid_choice"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_CHOICE_ARG_TYPE)),
        idspec("DISPATCH_005", TestAction(
            name="Verify that invalid 'path' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(path="invalid_path"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_PATH_ARG_TYPE)),
        idspec("DISPATCH_006", TestAction(
            name="Verify that invalid 'session' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(session="invalid_session"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_SESSION_ARG_TYPE)),
        idspec("DISPATCH_007", TestAction(
            name="Verify that invalid 'callback' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(callback="invalid_callback"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_CALLBACK_ARG_TYPE)),
        idspec("DISPATCH_008", TestAction(
            name="Verify that invalid 'output' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(output=123),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_OUTPUT_ARG_TYPE)),
        idspec("DISPATCH_009", TestAction(
            name="Verify that invalide 'filename_base' argument raises SimpleBenchTypeError",
            action=reporter.dispatch_to_targets,
            kwargs=kwargs.replace(filename_base=456),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_FILENAME_BASE_ARG_TYPE)),
    ])

    return testspecs


@pytest.mark.parametrize("testspec", dispatch_to_targets_params_testspecs())
def test_dispatch_to_targets_params(testspec: TestSpec):
    """Tests for parameter validation of the dispatch_to_targets method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()

# We don't need to explicitly test the individual targets for dispatch_to_targets
# because they are already implicitly tested as part of the render_by_case and
# render_by_section tests.
