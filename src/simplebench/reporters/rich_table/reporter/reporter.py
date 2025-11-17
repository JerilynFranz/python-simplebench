"""Reporter for benchmark results using Rich tables on the console."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias

from rich.table import Table

from simplebench.defaults import DEFAULT_INTERVAL_SCALE
from simplebench.enums import FlagType, Format, Section, Target
from simplebench.exceptions import SimpleBenchTypeError
# simplebench.reporters imports
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter import Reporter, ReporterOptions
# simplebench.reporters.rich_table imports
from simplebench.reporters.rich_table.reporter.exceptions import RichTableReporterErrorTag
from simplebench.reporters.rich_table.reporter.options import RichTableOptions
from simplebench.results import Results
from simplebench.si_units import si_scale_for_smallest
from simplebench.type_proxies import is_case
from simplebench.utils import sigfigs
from simplebench.validators import validate_type

Options: TypeAlias = RichTableOptions

if TYPE_CHECKING:
    from simplebench.case import Case


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
    _OPTIONS_TYPE: ClassVar[type[RichTableOptions]] = RichTableOptions  # pylint: disable=line-too-long # type: ignore[reportIncompatibleVariableOveride]  # noqa: E501
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}

    def __init__(self) -> None:
        """Initialize the RichTableReporter.

        Note:

        The exception documentation below refers to validation of subclass configuration
        class variables `_OPTIONS_TYPE` and `_OPTIONS_KWARGS`. These must be correctly defined
        in any subclass of `RichTableReporter` to ensure proper functionality.

        In simple use, these exceptions should never be raised, as `RichTableReporter` provides
        valid implementations. They are documented here for completeness.

         Raises:
            SimpleBenchTypeError: If the subclass configuration types are invalid.
            SimpleBenchValueError: If the subclass configuration values are invalid.
        """
        super().__init__(
            name='rich-table',
            description='Displays benchmark results as a rich text table on the console.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK},
            default_targets={Target.CONSOLE},
            formats={Format.RICH_TEXT},
            file_suffix='txt',
            file_unique=False,
            file_append=True,
            choices=ChoicesConf([
                 ChoiceConf(
                    flags=['--rich-table'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table',
                    description=(
                        'All results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.RICH_TEXT),
                ChoiceConf(
                    flags=['--rich-table.ops'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-ops',
                    description=(
                        'Ops/second results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.OPS],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.RICH_TEXT),
                ChoiceConf(
                    flags=['--rich-table.timing'],
                    flag_type=FlagType.TARGET_LIST,
                    name='rich-table-timing',
                    description=(
                        'Timing results as rich text tables (filesystem, console, callback, default=console)'),
                    sections=[Section.TIMING],
                    targets=[Target.CONSOLE, Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.RICH_TEXT),
                ChoiceConf(
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

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> Table:
        """Prints the benchmark results in a rich table format if available.

        It creates a Rich Table instance containing the benchmark results for the specified section.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            options (RichTableOptions): The options specifying the report configuration.
                            (RichTableOptions is a subclass of ReporterOptions.)
            section (Section): The Section enum value specifying the type of results to display.

        Returns:
            Table: The Rich Table instance.
        """
        # is_* checks provide deferred import validation to avoid circular imports
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"'case' argument must be a Case instance, got {type(case)}",
                tag=RichTableReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                RichTableReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(options, Options, 'options',
                                RichTableReporterErrorTag.RENDER_INVALID_OPTIONS)

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
            numbers=[result.results_section(section).adjusted_standard_deviation for result in results],
            base_unit=base_unit)

        table = Table(title=(case.title + f'\n{section.value}\n\n' + case.description),
                      show_header=True,
                      title_style='bold green1',
                      header_style='bold magenta')
        table.add_column('N', justify='center')
        table.add_column('Iterations', justify='center')
        table.add_column('Rounds', justify='center')
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
                f'{result.rounds:>6d}',
                f'{result.total_elapsed * DEFAULT_INTERVAL_SCALE:>4.2f}',
                f'{sigfigs(stats_target.mean * mean_scale):>8.2f}',
                f'{sigfigs(stats_target.median * median_scale):>8.2f}',
                f'{sigfigs(stats_target.minimum * min_scale):>8.2f}',
                f'{sigfigs(stats_target.maximum * max_scale):>8.2f}',
                f'{sigfigs(stats_target.percentiles[5] * p5_scale):>8.2f}',
                f'{sigfigs(stats_target.percentiles[95] * p95_scale):>8.2f}',
                f'{sigfigs(stats_target.adjusted_standard_deviation * stddev_scale):>8.2f}',
                f'{sigfigs(stats_target.adjusted_relative_standard_deviation):>5.2f}%'
            ]
            for value in result.variation_marks.values():
                row.append(f'{value!s}')
            table.add_row(*row)

        return table
