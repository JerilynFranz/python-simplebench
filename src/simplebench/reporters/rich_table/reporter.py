"""Reporter for benchmark results using Rich tables on the console."""
from __future__ import annotations
from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING

from rich.table import Table

from simplebench.defaults import DEFAULT_INTERVAL_SCALE
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.results import Results
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.si_units import si_scale_for_smallest
from simplebench.utils import sigfigs
from simplebench.validators import validate_type

# simplebench.reporters imports
from ..choices import Choices
from ..choice import Choice

# simplebench.reporters.rich_table imports
from .options import RichTableOptions
from .exceptions import RichTableReporterErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session

Options = RichTableOptions


class RichTableReporter(Reporter):
    """Class for outputting benchmark results as Rich Tables.

    It supports reporting operations per second and per round timing results,
    either separately or together, to the console, to files, and/or via a callback function.

    Defined command-line flags:
        --rich-table:               Outputs all results as rich text tables on the console.
        --rich-table.ops:           Outputs only operations per second results.
        --rich-table.timings:       Outputs only per round timing results.
        --rich-table.memory:        Outputs only memory usage results.
        --rich-table.peak-memory:   Outputs only peak memory usage results.

    Each flag supports multiple targets: console, filesystem, and callback with the default target
    being console.

    Attributes:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Choices): A collection of Choices instances defining
            the reporter instance, CLI flags, Choice name, supported Result Sections,
            supported output Targets, and supported output Formats for the reporter.
    """
    _HARDCODED_DEFAULT_OPTIONS = RichTableOptions()
    """Built-in default ReporterOptions instance for the reporter used if none is specified
    in a passed `Case`, `Choice`, or by `_DEFAULT_OPTIONS`. It forms the basis for the
    dynamic default options functionality provided by the `set_default_options()` and
    `get_default_options()` methods."""

    def __init__(self) -> None:
        """Initialize the RichTableReporter."""
        super().__init__(
            name='rich-table',
            description='Displays benchmark results as a rich text table on the console.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            options_type=Options,
            targets={Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK},
            formats={Format.RICH_TEXT},
            file_suffix='txt',
            file_unique=False,
            file_append=True,
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
                    output_format=Format.RICH_TEXT),
                Choice(
                    reporter=self,
                    flags=['--rich-table.ops'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-ops',
                    description=(
                        'Ops/second results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.OPS],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.RICH_TEXT),
                Choice(
                    reporter=self,
                    flags=['--rich-table.timing'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-timing',
                    description=(
                        'Timing results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.TIMING],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.RICH_TEXT),
                Choice(
                    reporter=self,
                    flags=['--rich-table.memory'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-memory',
                    description=(
                        'Memory results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.RICH_TEXT),
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
        loading of the reporter classes, so subclasses can assume any required imports are available.

        The run_report() method's main responsibility it to select the appropriate output method
        (render_by_case() in this case) based on the provided arguments.

        The actual rendering of the Rich Table data is handled by the render() method.

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
        self.render_by_case(
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> Table:
        """Prints the benchmark results in a rich table format if available.

        It creates a Rich Table instance containing the benchmark results for the specified section.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            options (RichTableOptions): The options specifying the report configuration.
                            (RichTableOptions is a subclass of ReporterOptions.)
            section (Section): The Section enum value specifying the type of results to display.

        Returns:
            Table: A tuple containing the Rich Table instance and its plain string representation.
        """
        case = validate_type(value=case, expected=Case, name='case',
                             error_tag=RichTableReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(value=section, expected=Section, name='section',
                                error_tag=RichTableReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(value=options, expected=Options, name='options',
                                error_tag=RichTableReporterErrorTag.RENDER_INVALID_OPTIONS)

        base_unit: str = self.get_base_unit_for_section(section=section)
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

        return table
