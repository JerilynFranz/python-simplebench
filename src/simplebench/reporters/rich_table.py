# -*- coding: utf-8 -*-
"""Reporter for benchmark results using Rich tables on the console."""
from __future__ import annotations
from pathlib import Path
from typing import Optional, Any, Callable

from rich.console import Console
from rich.table import Table

from ..constants import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE
from ..exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from ..session import Session
from ..case import Case
from ..results import Results
from ..utils import sanitize_filename, sigfigs, si_scale_for_smallest
from .choices import Choice, Choices, Section, Format, Target
from .interfaces import Reporter


class RichTableReporter(Reporter):
    """Class for outputting benchmark results as Rich Tables.

    It supports reporting operations per second and per round timing results,
    either separately or together, to the console, to files, and/or via a callback function.

    Defined command-line flags:
        --rich-table-console Outputs both operations per second and per round timing results.
        --rich-table-ops-console: Outputs only operations per second results.
        --rich-table-timings-console: Outputs only per round timing results.
        --rich-table-file: Saves both operations per second and per round timing results to files.
        --rich-table-ops-file: Saves only operations per second results to a file.
        --rich-table-timings-file: Saves only per round timing results to a file.
        --rich-table-callback: Outputs both operations per second and per round timing results via a callback function.
        --rich-table-ops-callback: Outputs only operations per second results via a callback function.
        --rich-table-timings-callback: Outputs only per round timing results via a callback function.

    Attributes:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Choices): A collection of Choices instances defining
            the reporter instance, CLI flags, Choice name, supported Result Sections,
            supported output Targets, and supported output Formats for the reporter.
    """
    def __init__(self) -> None:
        """Initialize the RichTableReporter with Choice."""
        self._choices: Choices = Choices()
        self._choices.add(
             Choice(
                reporter=self,
                flags=['--rich-table'],
                name='rich-table',
                description=('Display operations per second and per round timing results '
                             'as a rich text table on the console'),
                sections=[Section.OPS],
                targets=[Target.CONSOLE, Target.CALLBACK],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-ops'],
                name='rich-table-ops',
                description='Display operations per second results as a rich text table on the console',
                sections=[Section.OPS],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-timings'],
                name='rich-table-timings',
                description='Display timing results as a rich text table on the console',
                sections=[Section.TIMING],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT])
        )
        self._choices.add(
             Choice(
                reporter=self,
                flags=['--rich-table-file'],
                name='rich-table-file',
                description=('Save operations per second and per round timing results '
                             'as rich text tables in files'),
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-ops-file'],
                name='rich-table-ops-file',
                description='Save operations per second results as a rich text table in a file',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-timings-file'],
                name='rich-table-timings-file',
                description='Save timing results as a rich text table in a file',
                sections=[Section.TIMING],
                targets=[Target.FILESYSTEM],
                formats=[Format.RICH_TEXT])
        )
        self._choices.add(
             Choice(
                reporter=self,
                flags=['--rich-table-callback'],
                name='rich-table-callback',
                description=('Returns operations per second and per round timing results '
                             'via callback function as a rich text table'),
                sections=[Section.OPS],
                targets=[Target.CALLBACK],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-ops-callback'],
                name='rich-table-ops-callback',
                description=('Returns operations per second results via callback function as a rich text table'),
                sections=[Section.OPS],
                targets=[Target.CALLBACK],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-timings-callback'],
                name='rich-table-timings-callback',
                description=('Returns timing results via callback function as a rich text table'),
                sections=[Section.TIMING],
                targets=[Target.CALLBACK],
                formats=[Format.RICH_TEXT])
        )

    @property
    def choices(self) -> Choices:
        """Return the Choices instance for the reporter, including sections,
        output targets, and formats.
        """
        return self._choices

    @property
    def name(self) -> str:
        """Return the unique identifying name of the reporter."""
        return 'rich-table'

    @property
    def description(self) -> str:
        """Return a brief description of the reporter."""
        return 'Displays benchmark results as a rich text table on the console.'

    def report(self,
               case: Case,
               choice: Choice,
               path: Optional[Path] = None,
               session: Optional[Session] = None,
               callback: Optional[Callable[[Case, Section, Format, Any], None]] = None) -> None:
        """Output the benchmark results to the console and/or a callback if available.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the Rich Table file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[Callable[[Case, Section, Format, Any], None]]):
                A callback function for additional processing of the report.
                The function should accept three arguments:
                 - the Case instance
                 - the Format instance
                 - the rich.table.Table data.
                Leave as None if no callback is needed.

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.RICH_TABLE_REPORTER_INIT_INVALID_CASE_ARG)
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                ErrorTag.RICH_TABLE_REPORTER_REPORT_INVALID_CHOICE_ARG)
        for section in choice.sections:
            if section not in (Section.OPS, Section.TIMING):
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    ErrorTag.RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in (Target.FILESYSTEM, Target.CALLBACK):
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    ErrorTag.RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_TARGET)
        if path is not None and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "path must be a pathlib.Path instance if provided",
                ErrorTag.RICH_TABLE_REPORTER_REPORT_INVALID_PATH_ARG)
        if Target.CALLBACK in choice.targets:
            if callback is not None and not callable(callback):
                raise SimpleBenchTypeError(
                    "Callback function must be callable if provided",
                    ErrorTag.RICH_TABLE_REPORTER_REPORT_INVALID_CALLBACK_ARG)
        if Target.FILESYSTEM in choice.targets and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "Path must be a pathlib.Path instance when using FILESYSTEM target",
                ErrorTag.RICH_TABLE_REPORTER_REPORT_INVALID_PATH_ARG)
        for output_format in choice.formats:
            if output_format is not Format.CSV:
                raise SimpleBenchValueError(
                    f"Unsupported Format in Choice: {output_format}",
                    ErrorTag.RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_FORMAT)
        if session is not None and not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                ErrorTag.RICH_TABLE_REPORTER_REPORT_INVALID_SESSION_ARG)

        # Only proceed if there are results to report
        results = case.results
        if not results:
            return

        for section in choice.sections:
            base_unit: str = ''
            if section is Section.OPS:
                base_unit = BASE_OPS_PER_INTERVAL_UNIT
            elif section is Section.TIMING:
                base_unit = BASE_INTERVAL_UNIT
            else:  # This should never happen due to earlier validation
                raise SimpleBenchValueError(
                    f"Unsupported section: {section} (this should not happen)",
                    ErrorTag.RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_SECTION)

            table = self.to_rich_table(case=case, target=section.value, base_unit=base_unit)
            console: Console
            if Target.FILESYSTEM in choice.targets and path is not None:
                filename: str = sanitize_filename(section.name)
                file = path.joinpath('rich', f'{filename}.rich.txt')
                file.parent.mkdir(parents=True, exist_ok=True)
                with file.open(mode='w', encoding='utf-8', newline='') as f:
                    console = Console(no_color=True, width=120, file=f)
                    console.print(table)
                    console.file.flush()
                    console.file.close()
            if Target.CALLBACK in choice.targets and case.callback is not None:
                console = Console(record=True, no_color=True, width=120)
                console.begin_capture()
                console.print(table)
                console.end_capture()
                text: str = console.export_text()
                case.callback(case, section, Format.RICH_TEXT, text)
            if Target.CONSOLE in choice.targets:
                console = session.console if session is not None else Console()
                console.print(table)

    def to_rich_table(self,
                      case: Case,
                      target: str,
                      base_unit: str) -> Table:
        """Prints the benchmark results in a rich table format if available.
        """
        results: list[Results] = case.results
        mean_unit, mean_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).mean for result in results],
            base_unit=base_unit)
        median_unit, median_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).median for result in results],
            base_unit=base_unit)
        min_unit, min_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).minimum for result in results],
            base_unit=base_unit)
        max_unit, max_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).maximum for result in results],
            base_unit=base_unit)
        p5_unit, p5_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).percentiles[5] for result in results],
            base_unit=base_unit)
        p95_unit, p95_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).percentiles[95] for result in results],
            base_unit=base_unit)
        stddev_unit, stddev_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).standard_deviation for result in results],
            base_unit=base_unit)

        table = Table(title=(case.title + '\n\n' + case.description),
                      show_header=True,
                      title_style='bold green1',
                      header_style='bold magenta')
        table.add_column('N', justify='center')
        table.add_column('Iterations', justify='center')
        table.add_column('Elapsed Seconds', justify='center', max_width=7)
        table.add_column(f'mean {mean_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'median {median_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'min {min_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'max {max_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'5th {p5_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'95th {p95_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'std dev {stddev_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column('rsd%', justify='center', vertical='bottom', overflow='fold')
        for value in case.variation_cols.values():
            table.add_column(value, justify='center', vertical='bottom', overflow='fold')
        for result in results:
            stats_target = getattr(result, target)
            row: list[str] = [
                f'{result.n:>6d}',
                f'{len(result.iterations):>6d}',
                f'{result.total_elapsed * DEFAULT_INTERVAL_SCALE:>4.2f}',
                f'{sigfigs(stats_target.mean * mean_scale):>8.2f}',
                f'{sigfigs(stats_target.median * median_scale):>8.2f}',
                f'{sigfigs(stats_target.minimum * min_scale):>8.2f}',
                f'{sigfigs(stats_target.maximum * max_scale):>8.2f}',
                f'{sigfigs(stats_target.percentiles[5] * p5_scale):>8.2f}',
                f'{sigfigs(stats_target.percentiles[95] * p95_scale):>8.2f}',
                f'{sigfigs(stats_target.standard_deviation * stddev_scale):>8.2f}',
                f'{sigfigs(stats_target.relative_standard_deviation):>5.2f}%'
            ]
            for value in result.variation_marks.values():
                row.append(f'{value!s}')
            table.add_row(*row)
        return table
