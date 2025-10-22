# -*- coding: utf-8 -*-
"""Reporter for benchmark results using Rich tables on the console."""
from __future__ import annotations
from argparse import Namespace
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from rich.console import Console
from rich.table import Table

from ..defaults import DEFAULT_INTERVAL_SCALE
from ..enums import Section, Target, Format, FlagType
from ..exceptions import SimpleBenchValueError, ErrorTag
from ..results import Results
from ..si_units import si_scale_for_smallest
from ..utils import sanitize_filename, sigfigs
from ..validators import validate_sequence_of_type, validate_non_blank_string, validate_positive_int
from .choices import Choice, Choices, ChoiceOptions
from .interfaces import Reporter
from .protocols import ReporterCallback


if TYPE_CHECKING:
    from ..case import Case
    from ..session import Session


class RichTableChoiceOptions(ChoiceOptions):
    """Class for holding Rich table reporter specific options in a Choice.

    This class provides additional configuration options specific to the JSON reporter.
    It is accessed via the `options` attribute of a Choice instance.

    Attributes:
        default_targets (frozenset[Target]): The default targets for the Rich table reporter choice.
        subdir (str): The subdirectory to output Rich table files to.
        width (int, default=200): The width of the Rich table output when rendered to the filesystem or via callback.

    """
    def __init__(self,
                 default_targets: Iterable[Target],
                 subdir: str = 'rich',
                 width: int = 200) -> None:
        """Initialize RichTableChoiceOptions with default targets and subdirectory.

        Args:
            default_targets (Iterable[Target]): The default targets for the Rich table reporter choice.
            subdir (str, default='json'): The subdirectory to output Rich table files to.
        """
        if not isinstance(default_targets, Iterable):
            raise SimpleBenchValueError(
                'RichTableChoiceOptions.default_targets must be an iterable of Target values.',
                tag=ErrorTag.RICH_TABLE_REPORTER_CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE)
        default_targets = validate_sequence_of_type(
                list(default_targets), Target, 'RichTableChoiceOptions.default_targets',
                ErrorTag.RICH_TABLE_REPORTER_CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE,
                ErrorTag.RICH_TABLE_REPORTER_CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE,
                allow_empty=False)
        self._default_targets: frozenset[Target] = frozenset(default_targets)
        self._subdir: str = validate_non_blank_string(
                subdir, 'RichTableChoiceOptions.subdir',
                ErrorTag.RICH_TABLE_REPORTER_CHOICE_OPTIONS_INVALID_SUBDIR_TYPE,
                ErrorTag.RICH_TABLE_REPORTER_CHOICE_OPTIONS_INVALID_SUBDIR_VALUE)
        self._width: int = validate_positive_int(
                width, 'RichTableChoiceOptions.width',
                ErrorTag.RICH_TABLE_REPORTER_CHOICE_OPTIONS_INVALID_WIDTH_TYPE,
                ErrorTag.RICH_TABLE_REPORTER_CHOICE_OPTIONS_INVALID_WIDTH_VALUE)

    @property
    def default_targets(self) -> frozenset[Target]:
        """Return the default targets for the JSON reporter choice.

        Returns:
            frozenset[Target]: The default targets for the JSON reporter choice.
        """
        return self._default_targets

    @property
    def subdir(self) -> str:
        """Return the subdirectory to output JSON files to.

        Returns:
            str: The subdirectory to output JSON files to (default is 'rich').
        """
        return self._subdir

    @property
    def width(self) -> int:
        """Return the width of the Rich table output when rendered to the filesystem or via callback.

        Returns:
            int: The width of the Rich table output in characters (default is 200).
        """
        return self._width


class RichTableReporter(Reporter):
    """Class for outputting benchmark results as Rich Tables.

    It supports reporting operations per second and per round timing results,
    either separately or together, to the console, to files, and/or via a callback function.

    Defined command-line flags:
        --rich-table.console Outputs operations per second, per round timing, and memory usage results.
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
    DEFAULT_WIDTH: int = 200
    """Default width of Rich table output when rendered to filesystem or via callback."""

    def __init__(self) -> None:
        """Initialize the RichTableReporter."""
        super().__init__(
            name='rich-table',
            description='Displays benchmark results as a rich text table on the console.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK},
            formats={Format.RICH_TEXT},
            choices=Choices([
                 Choice(
                    reporter=self,
                    flags=['--rich-table'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table',
                    description=(
                        'All results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    formats=[Format.RICH_TEXT],
                    options=RichTableChoiceOptions(
                        default_targets=[Target.CONSOLE],
                        subdir='rich',
                        width=RichTableReporter.DEFAULT_WIDTH)),
                Choice(
                    reporter=self,
                    flags=['--rich-table.ops'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-ops',
                    description=(
                        'Ops/second results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.OPS],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    formats=[Format.RICH_TEXT],
                    options=RichTableChoiceOptions(
                        default_targets=[Target.CONSOLE],
                        subdir='rich',
                        width=RichTableReporter.DEFAULT_WIDTH)),
                Choice(
                    reporter=self,
                    flags=['--rich-table.timing'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-timing',
                    description=(
                        'Timing results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.TIMING],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    formats=[Format.RICH_TEXT],
                    options=RichTableChoiceOptions(
                        default_targets=[Target.CONSOLE],
                        subdir='rich',
                        width=RichTableReporter.DEFAULT_WIDTH)),
                Choice(
                    reporter=self,
                    flags=['--rich-table.memory'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-memory',
                    description=(
                        'Memory results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    formats=[Format.RICH_TEXT],
                    options=RichTableChoiceOptions(
                        default_targets=[Target.CONSOLE],
                        subdir='rich',
                        width=RichTableReporter.DEFAULT_WIDTH)),
            ])
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None
                   ) -> None:
        """Output the benchmark results to a file as tagged RichTable if available.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid without a large amount of boilerplate code. The base class also handles lazy
        loading of the reporter classes, so subclasses can assume any required imports are available

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Path | None): The path to the directory where the RichTable file(s) will be saved.
            session (Session | None): The Session instance containing benchmark results.
            callback (ReporterCallback | None):
                A callback function for additional processing of the report.
                The function should accept two arguments: the Case instance and the RichTable data as a string.
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
        default_targets: frozenset[Target] = frozenset()
        subdir: str = 'rich'
        if choice.options is not None and not isinstance(choice.options, RichTableChoiceOptions):
            raise SimpleBenchValueError(
                'RichTableReporter requires a RichTableChoiceOptions instance for its Choice().options if set.',
                tag=ErrorTag.REPORTER_RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE)
        if isinstance(choice.options, RichTableChoiceOptions):
            default_targets = choice.options.default_targets
            subdir = choice.options.subdir

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=default_targets)
        rich_output: Table
        text_output: str
        for section in choice.sections:
            base_unit: str = self.get_base_unit_for_section(section=section)
            rich_output, text_output = self._to_rich_table(
                case=case, options=choice.options, section=section, base_unit=base_unit)

            for output_target in targets:
                match output_target:
                    case Target.FILESYSTEM:
                        filename: str = sanitize_filename(section.value) + '.txt'
                        self.target_filesystem(
                            path=path, subdir=subdir, filename=filename, output=text_output, append=True)

                    case Target.CALLBACK:
                        self.target_callback(
                            callback=callback,
                            case=case,
                            section=section,
                            output_format=Format.PLAIN_TEXT, output=text_output)

                    case Target.CONSOLE:
                        self.target_console(session=session, output=rich_output)

                    case _:
                        raise SimpleBenchValueError(
                            f'Unsupported target for RichTableReporter: {output_target}',
                            tag=ErrorTag.REPORTER_RUN_REPORT_UNSUPPORTED_TARGET)

    def _to_rich_table(self,
                       case: Case,
                       options: RichTableChoiceOptions | None,
                       section: Section,
                       base_unit: str) -> tuple[Table, str]:
        """Prints the benchmark results in a rich table format if available.

        It creates a Rich Table instance and also captures its plain string representation
        as a width limited console output (default width is 200 characters if not specified
        in the choice options).

        Args:
            case (Case): The Case instance representing the benchmarked code.
            options (RichTableChoiceOptions | None): The options specifying the report configuration.
            section (Section): The Section enum value specifying the type of results to display.
            base_unit (str): The base unit for the results, e.g., 'ops/s' or 's'.

        Returns:
            Tuple[Table, str]: A tuple containing the Rich Table instance and its plain string representation.
        """
        results: list[Results] = case.results
        mean_unit, mean_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).mean for result in results],
            base_unit=base_unit)
        median_unit, median_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).median for result in results],
            base_unit=base_unit)
        min_unit, min_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).minimum for result in results],
            base_unit=base_unit)
        max_unit, max_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).maximum for result in results],
            base_unit=base_unit)
        p5_unit, p5_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[5] for result in results],
            base_unit=base_unit)
        p95_unit, p95_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[95] for result in results],
            base_unit=base_unit)
        stddev_unit, stddev_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).standard_deviation for result in results],
            base_unit=base_unit)

        table = Table(title=(case.title + f'\n{section.value}\n\n' + case.description),
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
            stats_target = result.results_section(section)
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

        # Capture the rich table output as a plain string with a width limited console
        width: int = RichTableReporter.DEFAULT_WIDTH if options is None else options.width
        output_io = StringIO()
        console = Console(file=output_io, no_color=True, width=width)
        console.print(table)
        text_output = output_io.getvalue()
        output_io.close()

        return (table, text_output)
