"""Mixin for orchestration-related functionality for the Reporter class."""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING

from rich.table import Table
from rich.text import Text

from simplebench.enums import Section, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.prioritized import Prioritized
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.type_proxies import is_case, is_choice, is_session
from simplebench.utils import sanitize_filename
from simplebench.validators import validate_type

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session


class _ReporterOrchestrationMixin:
    """Mixin for orchestration-related functionality for the Reporter class.

    It provides methods to orchestrate the rendering of reports by case or by section,
    handling the dispatching of outputs to various targets such as filesystem, console,
    or callback functions.

    This makes writing reporters easier by providing common orchestration logic that
    can be reused across different reporter implementations.

    Methods:
        render_by_case: Render the report for an entire case at once across all applicable sections.
        render_by_section: Render a report for each section and case individually and dispatch to targets.
    """

    def _validate_render_by_args(
        self: ReporterProtocol, *,
        renderer: ReportRenderer,
        args: Namespace,
        case: Case,
        choice: Choice,
        path: Path | None = None,
        session: Session | None = None,
        callback: ReporterCallback | None = None
    ) -> None:
        """Validate common arguments for render_by_case and render_by_section methods.

        Checks that the provided arguments are of the expected types. Raises exceptions
        if any argument is of an incorrect type.

        Args:
            renderer (ReportRenderer): The method to be used for actually rendering the report.
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[ReporterCallback]): A callback function for additional processing of the report.

        Returns:
            None

        Raises:
            SimpleBenchTypeError: If any of the provided arguments are not of the expected types.
        """
        if not isinstance(renderer, ReportRenderer):
            raise SimpleBenchTypeError(
                "renderer must be a callable ReportRenderer",
                tag=ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_RENDERER_ARG_TYPE)

        args = validate_type(
            args, Namespace, 'args',
            ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_ARGS_ARG_TYPE)
        # is_* checks handle deferred import runtime type checking for Case, Choice, and Session
        if not is_case(case):
            raise SimpleBenchTypeError(
                "Expected a Case instance for case argument",
                tag=ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CASE_ARG_TYPE)

        if not is_choice(choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance for choice argument",
                tag=ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CHOICE_ARG_TYPE)

        if not is_session(session) and session is not None:
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                tag=ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_SESSION_ARG_TYPE)

        if callback is not None and not isinstance(callback, ReporterCallback):
            raise SimpleBenchTypeError(
                "callback must be a callable ReporterCallback if provided",
                tag=ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CALLBACK_ARG_TYPE)

        if path is not None:
            path = validate_type(
                path, Path, 'path',
                ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_PATH_ARG_TYPE)

    def render_by_case(self: ReporterProtocol, *,
                       renderer: ReportRenderer,
                       args: Namespace,
                       case: Case,
                       choice: Choice,
                       path: Path | None = None,
                       session: Session | None = None,
                       callback: ReporterCallback | None = None) -> None:
        """Render the report for an entire case at once across all applicable sections.

        This method is called by the subclass's run_report() method to run one report per case
        that is then processed according to the specified targets.

        It calls the subclass's render() method to actually generate the report output.

        Usage of this method is appropriate when the report output encompasses
        all sections in a single output, such as a summary table or comprehensive report.

        Usage:

        ```python
        from typing import TYPE_CHECKING

        from simplebench.reporters.reporter.reporter import Reporter, ReporterOptions

        if TYPE_CHECKING:
            from simplebench.case import Case
            from simplebench.reporters.choice.choice import Choice
            from simplebench.session import Session

        class MyReporter(Reporter):
            def __init__(self, ...):
                ...

            def run_report(self, case: Case, choice: Choice, session: Session | None = None) -> None:
                self.render_by_case(renderer=self.render,
                                    args=self._args,
                                    case=case,
                                    choice=choice,
                                    path=self._path,
                                    session=session,
                                    callback=self._callback)

            def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
                '''Render the report output for the entire case across all sections.'''
                ...
        ```

        Args:
            renderer (ReportRenderer): The method to be used for actually rendering the report.
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[ReporterCallback]):
                A callback function for additional processing of the report.
                The function should accept two arguments: the Case instance and the CSV data as a string.
                Leave as None if no callback is needed.

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or if
                required arguments are missing. Also raised if the callback is not callable when
                provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
                target is specified.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        self._validate_render_by_args(
            renderer=renderer,
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback)

        prioritized = Prioritized(reporter=self, choice=choice, case=case)

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=prioritized.default_targets)
        output = renderer(case=case, section=Section.NULL, options=prioritized.options)
        output_as_text = output
        if isinstance(output, (Text, Table)):
            output_as_text = self.rich_text_to_plain_text(output)
        filename: str = sanitize_filename(case.title)
        if prioritized.file_suffix:
            filename += f'.{prioritized.file_suffix}'

        for output_target in targets:
            match output_target:
                case Target.FILESYSTEM:
                    self.target_filesystem(
                        path=path,
                        subdir=prioritized.subdir,
                        filename=filename,
                        output=output_as_text,
                        unique=prioritized.file_unique,
                        append=prioritized.file_append)

                case Target.CALLBACK:
                    self.target_callback(
                        callback=callback,
                        case=case,
                        section=Section.NULL,
                        output_format=choice.output_format,
                        output=output_as_text)

                case Target.CONSOLE:
                    self.target_console(session=session, output=output)

                case _:
                    raise SimpleBenchValueError(
                        f'Unsupported target for {type(self)}: {output_target}',
                        tag=ReporterErrorTag.RENDER_BY_CASE_UNSUPPORTED_TARGET)

    def render_by_section(
            self: ReporterProtocol,
            *,
            renderer: ReportRenderer,
            args: Namespace,
            case: Case,
            choice: Choice,
            path: Path | None = None,
            session: Session | None = None,
            callback: ReporterCallback | None = None) -> None:
        """Render a report for each section and dispatch to targets.

        This method is called by the subclass's run_report() method to run one report per section
        that is then processed according to the specified targets.

        It calls the subclass's render() method to actually generate the report output.

        Usage of this method is appropriate when the report output divides each case by
        section, such as separate files or outputs for each section of the report.

        Usage:

        ```python
        from simplebench.reporters.reporter.reporter import Reporter, ReporterOptions

        if TYPE_CHECKING:
            from simplebench.case import Case
            from simplebench.reporters.choice.choice import Choice
            from simplebench.session import Session


        class MyReporter(Reporter):
            def __init__(self, ...):
                ...

            def run_report(self, case: Case, choice: Choice, session: Session | None = None) -> None:
                self.render_by_section(
                                    renderer=self.render,
                                    args=self._args,
                                    case=case,
                                    choice=choice,
                                    path=self._path,
                                    session=session,
                                    callback=self._callback)

            def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
                '''Render the report output for the entire case across all sections.'''
                ...
        ```

        Args:
            renderer (ReportRenderer): The method to be used for actually rendering the report.
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[ReporterCallback]):
                A callback function for additional processing of the report.
                The function should accept two arguments: the Case instance and the CSV data as a string.
                Leave as None if no callback is needed.

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or if
                required arguments are missing. Also raised if the callback is not callable when
                provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
                target is specified.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        self._validate_render_by_args(
            renderer=renderer,
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback)

        prioritized = Prioritized(reporter=self, choice=choice, case=case)

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=prioritized.default_targets)
        for section in choice.sections:
            output = renderer(case=case, section=section, options=prioritized.options)
            output_as_text = output
            if isinstance(output, (Text, Table)):
                output_as_text = self.rich_text_to_plain_text(output)
            filename: str = sanitize_filename(section.value)
            if prioritized.file_suffix:
                filename += f'.{prioritized.file_suffix}'
            for output_target in targets:
                match output_target:
                    case Target.FILESYSTEM:
                        self.target_filesystem(
                            path=path,
                            subdir=prioritized.subdir,
                            filename=filename,
                            output=output_as_text,
                            unique=prioritized.file_unique,
                            append=prioritized.file_append)
                    case Target.CALLBACK:
                        self.target_callback(
                            callback=callback,
                            case=case,
                            section=section,
                            output_format=choice.output_format,
                            output=output_as_text)

                    case Target.CONSOLE:
                        self.target_console(session=session, output=output)

                    case _:
                        raise SimpleBenchValueError(
                            f'Unsupported target for {type(self)}: {output_target}',
                            tag=ReporterErrorTag.RENDER_BY_SECTION_UNSUPPORTED_TARGET)
