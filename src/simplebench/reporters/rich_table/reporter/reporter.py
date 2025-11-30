"""Reporter for benchmark results using Rich tables on the console."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias

from rich.table import Table

from simplebench.defaults import DEFAULT_INTERVAL_SCALE
from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.results import Results
from simplebench.si_units import si_scale_for_smallest
from simplebench.type_proxies import is_case
from simplebench.utils import sigfigs
from simplebench.validators import validate_type

from .config import RichTableConfig
from .exceptions import _RichTableReporterErrorTag
from .options import RichTableField, RichTableOptions

Options: TypeAlias = RichTableOptions

if TYPE_CHECKING:
    from simplebench.case import Case


class RichTableReporter(Reporter):
    """Class for outputting benchmark results as Rich Tables.

    It supports reporting operations per second and per round timing results,
    either separately or together, to the console, to files, and/or via a callback function.

    **Defined command-line flags:**

    * ``--rich-table``: Outputs all results as rich text tables on the console.
    * ``--rich-table.ops``: Outputs only operations per second results.
    * ``--rich-table.timings``: Outputs only per round timing results.
    * ``--rich-table.memory``: Outputs only memory usage results.
    * ``--rich-table.peak-memory``: Outputs only peak memory usage results.

    Each flag supports multiple targets: ``console``, ``filesystem``, and ``callback`` with
    the default target being ``console``.

    :ivar name: The unique identifying name of the reporter.
    :vartype name: str
    :ivar description: A brief description of the reporter.
    :vartype description: str
    :ivar choices: A collection of :class:`~simplebench.reporters.choices.Choices` instances
        defining the reporter instance, CLI flags,
        :class:`~simplebench.reporters.choice.Choice` name, supported
        :class:`~simplebench.enums.Section` objects, supported output
        :class:`~simplebench.enums.Target` objects, and supported output
        :class:`~simplebench.enums.Format` objects for the reporter.
    :vartype choices: ~simplebench.reporters.choices.Choices
    """
    _OPTIONS_TYPE: ClassVar[type[RichTableOptions]] = RichTableOptions  # pylint: disable=line-too-long # type: ignore[reportIncompatibleVariableOveride]  # noqa: E501
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}

    def __init__(self, config: RichTableConfig | None = None) -> None:
        """Initialize the RichTableReporter.

        .. note::

            The exception documentation below refers to validation of subclass configuration
            class variables ``_OPTIONS_TYPE`` and ``_OPTIONS_KWARGS``. These must be correctly
            defined in any subclass of :class:`~.RichTableReporter` to ensure proper
            functionality.

            In simple use, these exceptions should never be raised, as
            :class:`~.RichTableReporter` provides valid implementations. They are documented
            here for completeness.

        :param config: An optional configuration object to override default reporter settings.
                       If not provided, default settings will be used.
        :type config: RichTableConfig | None

        :raises ~simplebench.exceptions.SimpleBenchTypeError: If the subclass configuration
            types are invalid.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If the subclass configuration
            values are invalid.
        """
        if config is None:
            config = RichTableConfig()

        super().__init__(config)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> Table:
        """Prints the benchmark results in a rich table format if available.

        It creates a :class:`~rich.table.Table` instance containing the benchmark results
        for the specified section.

        The table includes the fields specified in the `options` argument, formatted
        appropriately based on the results data.

        Depending on the `options`, variation columns can be placed at the start or end of the rows.

        :param case: The :class:`~simplebench.case.Case` instance representing the
            benchmarked code.
        :param options: The options specifying the report configuration.
            (:class:`~.RichTableOptions` is a subclass of :class:`~.ReporterOptions`.)
        :param section: The :class:`~simplebench.enums.Section` enum value specifying the
            type of results to display.
        :return: The :class:`~rich.table.Table` instance.
        """
        # is_* checks provide deferred import validation to avoid circular imports
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"'case' argument must be a Case instance, got {type(case)}",
                tag=_RichTableReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                _RichTableReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(options, Options, 'options',
                                _RichTableReporterErrorTag.RENDER_INVALID_OPTIONS)
        included_fields = options.fields

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

        if not options.variation_cols_last:
            for value in case.variation_cols.values():
                table.add_column(value, justify='center', vertical='bottom', overflow='fold')

        for field in included_fields:
            match field:
                case RichTableField.N:
                    table.add_column('N', justify='center')
                case RichTableField.ITERATIONS:
                    table.add_column('Iterations', justify='center')
                case RichTableField.ROUNDS:
                    table.add_column('Rounds', justify='center')
                case RichTableField.ELAPSED_SECONDS:
                    table.add_column('Elapsed Seconds', justify='center', max_width=7)
                case RichTableField.MEAN:
                    table.add_column(f'mean {mean_unit}', justify='center', vertical='bottom', overflow='fold')
                case RichTableField.MEDIAN:
                    table.add_column(f'median {median_unit}', justify='center', vertical='bottom', overflow='fold')
                case RichTableField.MIN:
                    table.add_column(f'min {min_unit}', justify='center', vertical='bottom', overflow='fold')
                case RichTableField.MAX:
                    table.add_column(f'max {max_unit}', justify='center', vertical='bottom', overflow='fold')
                case RichTableField.P5:
                    table.add_column(f'5th {p5_unit}', justify='center', vertical='bottom', overflow='fold')
                case RichTableField.P95:
                    table.add_column(f'95th {p95_unit}', justify='center', vertical='bottom', overflow='fold')
                case RichTableField.STD_DEV:
                    table.add_column(f'std dev {stddev_unit}', justify='center', vertical='bottom', overflow='fold')
                case RichTableField.RSD_PERCENT:
                    table.add_column('rsd%', justify='center', vertical='bottom', overflow='fold')

        if options.variation_cols_last:
            for value in case.variation_cols.values():
                table.add_column(value, justify='center', vertical='bottom', overflow='fold')

        for result in results:
            stats_target = result.results_section(section)
            row: list[str] = []

            if not options.variation_cols_last:
                for value in result.variation_marks.values():
                    row.append(f'{value!s}')

            # Add main fields
            for field in included_fields:
                match field:
                    case RichTableField.N:
                        row.append(f'{str(result.n):>6}')
                    case RichTableField.ITERATIONS:
                        row.append(f'{len(result.iterations):>6d}')
                    case RichTableField.ROUNDS:
                        row.append(f'{result.rounds:>6d}')
                    case RichTableField.ELAPSED_SECONDS:
                        row.append(f'{result.total_elapsed * DEFAULT_INTERVAL_SCALE:>4.2f}')
                    case RichTableField.MEAN:
                        row.append(f'{sigfigs(stats_target.mean * mean_scale):>8.2f}')
                    case RichTableField.MEDIAN:
                        row.append(f'{sigfigs(stats_target.median * median_scale):>8.2f}')
                    case RichTableField.MIN:
                        row.append(f'{sigfigs(stats_target.minimum * min_scale):>8.2f}')
                    case RichTableField.MAX:
                        row.append(f'{sigfigs(stats_target.maximum * max_scale):>8.2f}')
                    case RichTableField.P5:
                        row.append(f'{sigfigs(stats_target.percentiles[5] * p5_scale):>8.2f}')
                    case RichTableField.P95:
                        row.append(f'{sigfigs(stats_target.percentiles[95] * p95_scale):>8.2f}')
                    case RichTableField.STD_DEV:
                        row.append(f'{sigfigs(stats_target.adjusted_standard_deviation * stddev_scale):>8.2f}')
                    case RichTableField.RSD_PERCENT:
                        row.append(f'{sigfigs(stats_target.adjusted_relative_standard_deviation):>5.2f}%')

            if options.variation_cols_last:
                for value in result.variation_marks.values():
                    row.append(f'{value!s}')

            table.add_row(*row)

        return table
