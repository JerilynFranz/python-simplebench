# -*- coding: utf-8 -*-
"""Reporter for benchmark results using Rich tables on the console."""
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Any, Callable, TYPE_CHECKING

from rich.console import Console
from rich.table import Table

from ..case import Case
from ..constants import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE
from ..exceptions import SimpleBenchValueError, ErrorTag
from ..results import Results
from ..utils import sanitize_filename, sigfigs, si_scale_for_smallest
from .choices import Choice, Choices, Section, Format, Target
from .interfaces import Reporter


if TYPE_CHECKING:
    from ..session import Session

_lazy_classes_loaded: bool = False


def _lazy_load_classes() -> None:
    """Lazily load any classes or modules that cannot be loaded during initial setup."""
    global _lazy_classes_loaded  # pylint: disable=global-statement
    global Session  # pylint: disable=global-statement
    if not _lazy_classes_loaded:
        from ..session import Session  # pylint: disable=import-outside-toplevel
        _lazy_classes_loaded = True


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
        choices: Choices = Choices()
        self._choices: Choices = choices
        choices.add(
             Choice(
                reporter=self,
                flags=['--rich-table-console'],
                name='rich-table',
                description=('Display operations per second and per round timing results '
                             'as a rich text table on the console'),
                sections=[Section.OPS],
                targets=[Target.CONSOLE, Target.CALLBACK],
                formats=[Format.RICH_TEXT]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-ops-console'],
                name='rich-table-ops',
                description='Display operations per second results as a rich text table on the console',
                sections=[Section.OPS],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-timings-console'],
                name='rich-table-timings',
                description='Display timing results as a rich text table on the console',
                sections=[Section.TIMING],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT])
        )
        choices.add(
             Choice(
                reporter=self,
                flags=['--rich-table-file'],
                name='rich-table-file',
                description=('Save operations per second and per round timing results '
                             'as rich text tables in files'),
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM],
                formats=[Format.RICH_TEXT]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-ops-file'],
                name='rich-table-ops-file',
                description='Save operations per second results as a rich text table in a file',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM],
                formats=[Format.RICH_TEXT]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-timings-file'],
                name='rich-table-timings-file',
                description='Save timing results as a rich text table in a file',
                sections=[Section.TIMING],
                targets=[Target.FILESYSTEM],
                formats=[Format.RICH_TEXT])
        )
        choices.add(
             Choice(
                reporter=self,
                flags=['--rich-table-callback'],
                name='rich-table-callback',
                description=('Returns operations per second and per round timing results '
                             'via callback function as a rich text table'),
                sections=[Section.OPS],
                targets=[Target.CALLBACK],
                formats=[Format.RICH_TEXT]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-ops-callback'],
                name='rich-table-ops-callback',
                description=('Returns operations per second results via callback function as a rich text table'),
                sections=[Section.OPS],
                targets=[Target.CALLBACK],
                formats=[Format.RICH_TEXT]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--rich-table-timings-callback'],
                name='rich-table-timings-callback',
                description=('Returns timing results via callback function as a rich text table'),
                sections=[Section.TIMING],
                targets=[Target.CALLBACK],
                formats=[Format.RICH_TEXT])
        )

    def supported_formats(self):
        """Return the set of supported output formats for the reporter."""
        return set([Format.RICH_TEXT])

    def supported_sections(self):
        """Return the set of supported result sections for the reporter."""
        return set([Section.OPS, Section.TIMING])

    def supported_targets(self):
        """Return the set of supported output targets for the reporter."""
        return set([Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK])

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

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        for choice in self.choices.values():
            for flag in choice.flags:
                parser.add_argument(flag, action='store_true', help=choice.description)

    def run_report(self,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,  # pylint: disable=unused-argument
                   callback: Optional[Callable[[Case, Section, Format, Any], None]
                                      ] = None  # pylint: disable=unused-argument
                   ) -> None:
        """Output the benchmark results as rich text if available.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid. The base class also handles lazy loading of the reporter classes, so subclasses
        can assume any required imports are available

        Args:
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[Callable[[Case, Section, Format, Any], None]]):
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

            table = self._to_rich_table(case=case, target=section.value, base_unit=base_unit)
            console: Console
            if Target.FILESYSTEM in choice.targets and path is not None:
                filename: str = sanitize_filename(section.value)
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

    def _to_rich_table(self,
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
