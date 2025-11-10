"""Mixin for orchestration-related functionality for the Reporter class."""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING

from rich.table import Table
from rich.text import Text

from simplebench.enums import Section, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metaclasses import ICase, ISession
from simplebench.reporters.choice.choice import Choice, IChoice
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.reporters.validators import (validate_report_renderer,
                                              validate_reporter_callback)
from simplebench.utils import sanitize_filename
from simplebench.validators import validate_type

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session


class _ReporterOrchestrationMixin:
    """Mixin for orchestration-related functionality for the Reporter class."""

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
        renderer = validate_report_renderer(renderer)

        args = validate_type(
            args, Namespace, 'args',
            ReporterErrorTag.RENDER_BY_CASE_INVALID_ARGS_ARG_TYPE)

        # We validate for Case using ICase to prevent circular import issues
        if not isinstance(case, ICase):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                tag=ReporterErrorTag.RENDER_BY_CASE_INVALID_CASE_ARG)

        # We validate for Choice using IChoice to prevent circular import issues
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ReporterErrorTag.RENDER_BY_CASE_INVALID_CHOICE_ARG_TYPE)

        if path is not None:
            path = validate_type(
                path, Path, 'path',
                ReporterErrorTag.RENDER_BY_CASE_INVALID_PATH_ARG_TYPE)

        # We validate for Session using ISession to prevent circular import issues
        if not isinstance(session, ISession) and session is not None:
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                tag=ReporterErrorTag.RENDER_BY_CASE_INVALID_SESSION_ARG_TYPE)

        callback = validate_reporter_callback(callback, allow_none=True)

        default_targets = self.get_prioritized_default_targets(choice=choice)
        subdir = self.get_prioritized_subdir(choice=choice)
        file_suffix = self.get_prioritized_file_suffix(choice=choice)
        file_unique = self.get_prioritized_file_unique(choice=choice)
        file_append = self.get_prioritized_file_append(choice=choice)
        options = self.get_prioritized_options(case=case, choice=choice)

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=default_targets)
        output = renderer(case=case, section=Section.NULL, options=options)

        for output_target in targets:
            match output_target:
                case Target.FILESYSTEM:
                    filename: str = sanitize_filename(case.title)
                    if file_suffix:
                        filename += f'.{file_suffix}'
                    if isinstance(output, (Text, Table)):
                        output = self.rich_text_to_plain_text(output)
                    self.target_filesystem(
                        path=path,
                        subdir=subdir,
                        filename=filename,
                        output=output,
                        unique=file_unique,
                        append=file_append)

                case Target.CALLBACK:
                    if isinstance(output, (Text, Table)):
                        output = self.rich_text_to_plain_text(output)
                    self.target_callback(
                        callback=callback,
                        case=case,
                        section=Section.NULL,
                        output_format=choice.output_format,
                        output=output)

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
        renderer = validate_report_renderer(renderer)

        args = validate_type(
            args, Namespace, 'args',
            ReporterErrorTag.RENDER_BY_SECTION_INVALID_ARGS_ARG_TYPE)

        # We validate for Case using ICase to prevent circular import issues
        if not isinstance(case, ICase):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                tag=ReporterErrorTag.RENDER_BY_SECTION_INVALID_CASE_ARG)

        # We validate for Choice using IChoice to prevent circular import issues
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ReporterErrorTag.RENDER_BY_SECTION_INVALID_CHOICE_ARG_TYPE)

        if path is not None:
            path = validate_type(
                path, Path, 'path',
                ReporterErrorTag.RENDER_BY_SECTION_INVALID_PATH_ARG_TYPE)

        # We validate for Session using ISession to prevent circular import issues
        if not isinstance(session, ISession) and session is not None:
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                tag=ReporterErrorTag.RENDER_BY_SECTION_INVALID_SESSION_ARG_TYPE)

        callback = validate_reporter_callback(callback, allow_none=True)

        default_targets = self.get_prioritized_default_targets(choice=choice)
        subdir = self.get_prioritized_subdir(choice=choice)
        options = self.get_prioritized_options(case=case, choice=choice)

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=default_targets)
        for section in choice.sections:
            output = renderer(case=case, section=section, options=options)

            for output_target in targets:
                match output_target:
                    case Target.FILESYSTEM:
                        filename: str = sanitize_filename(section.value)
                        if self._file_suffix:
                            filename += f'.{self._file_suffix}'
                        if isinstance(output, (Text, Table)):
                            output = self.rich_text_to_plain_text(output)
                        self.target_filesystem(
                            path=path,
                            subdir=subdir,
                            filename=filename,
                            output=output,
                            unique=self._file_unique,
                            append=self._file_append)

                    case Target.CALLBACK:
                        if isinstance(output, (Text, Table)):
                            output = self.rich_text_to_plain_text(output)
                        self.target_callback(
                            callback=callback,
                            case=case,
                            section=section,
                            output_format=choice.output_format,
                            output=output)

                    case Target.CONSOLE:
                        self.target_console(session=session, output=output)

                    case _:
                        raise SimpleBenchValueError(
                            f'Unsupported target for {type(self)}: {output_target}',
                            tag=ReporterErrorTag.RENDER_BY_SECTION_UNSUPPORTED_TARGET)
