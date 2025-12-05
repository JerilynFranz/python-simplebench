"""Reporter for benchmark results using Rich tables and pytest."""
from __future__ import annotations

import logging
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

from .config import PytestConfig
from .exceptions import _PytestReporterErrorTag
from .options import PytestField, PytestOptions

Options: TypeAlias = PytestOptions

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice import Choice


class PytestReporter(Reporter):
    """Class for outputting benchmark results as Rich Tables.

    It supports reporting operations per second and per round timing results,
    either separately or together.

    **Defined command-line flags:**

    * ``--pytest``: Outputs all results as rich text tables.
    * ``--pytest.ops``: Outputs operations per second results as rich text tables.
    * ``--pytest.timing``: Outputs timing results as rich text tables.
    * ``--pytest.memory``: Outputs memory usage results as rich text tables.
    * ``--pytest.peak_memory``: Outputs peak memory usage results as rich text tables

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
    _OPTIONS_TYPE: ClassVar[type[PytestOptions]] = PytestOptions  # pylint: disable=line-too-long # type: ignore[reportIncompatibleVariableOveride]  # noqa: E501
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}

    def __init__(self, config: PytestConfig | None = None) -> None:
        """Initialize the PytestReporter.

        .. note::

            The exception documentation below refers to validation of subclass configuration
            class variables ``_OPTIONS_TYPE`` and ``_OPTIONS_KWARGS``. These must be correctly
            defined in any subclass of :class:`~.PytestReporter` to ensure proper
            functionality.

            In simple use, these exceptions should never be raised, as
            :class:`~.PytestReporter` provides valid implementations. They are documented
            here for completeness.

        :param config: An optional configuration object to override default reporter settings.
                       If not provided, default settings will be used.
        :type config: PytestConfig | None

        :raises ~simplebench.exceptions.SimpleBenchTypeError: If the subclass configuration
            types are invalid.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If the subclass configuration
            values are invalid.
        """
        log.debug("PytestReporter created.")
        if config is None:
            config = PytestConfig()

        super().__init__(config)
        self.rendered_tables: list[Table] = []
        self.cases_by_section: dict[Section, list[Case]] = {}

    def run_report(  # pylint: disable=unused-argument
        self,
        *,
        case: Case,
        choice: Choice,
        **kwargs: Any  # Capture other args to satisfy the protocol
    ) -> None:
        """
        Overrides the default report orchestration.

        Instead of dispatching to targets (console, file), this method
        renders each report section into a Rich Table and stores it for
        later use by the pytest terminal summary hook.
        """
        log.debug("PytestReporter.run_report called for case '%s' with choice: %r", case.title, choice)
        options = self.get_prioritized_options(case=case, choice=choice)
        for section in choice.sections:
            table = self.render(case=case, section=section, options=options)
            if isinstance(table, Table):
                self.rendered_tables.append(table)
                self.cases_by_section.setdefault(section, []).append(case)
        log.debug("PytestReporter finished rendering. Total tables captured: %d", len(self.rendered_tables))

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
            (:class:`~.PytestOptions` is a subclass of :class:`~.ReporterOptions`.)
        :param section: The :class:`~simplebench.enums.Section` enum value specifying the
            type of results to display.
        :return: The :class:`~rich.table.Table` instance.
        """
        # is_* checks provide deferred import validation to avoid circular imports
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"'case' argument must be a Case instance, got {type(case)}",
                tag=_PytestReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                _PytestReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(options, Options, 'options',
                                _PytestReporterErrorTag.RENDER_INVALID_OPTIONS)
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
        p1_unit, p1_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[1] for result in results],
            base_unit=base_unit)
        p5_unit, p5_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[5] for result in results],
            base_unit=base_unit)
        p25_unit, p25_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[25] for result in results],
            base_unit=base_unit)
        p75_unit, p75_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[75] for result in results],
            base_unit=base_unit)
        p95_unit, p95_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[95] for result in results],
            base_unit=base_unit)
        p99_unit, p99_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).percentiles[99] for result in results],
            base_unit=base_unit)
        stddev_unit, stddev_scale = si_scale_for_smallest(
            numbers=[result.results_section(section).standard_deviation for result in results],
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
                case PytestField.N:
                    table.add_column('N', justify='center')
                case PytestField.ITERATIONS:
                    table.add_column('Iterations', justify='center')
                case PytestField.ROUNDS:
                    table.add_column('Rounds', justify='center')
                case PytestField.ELAPSED_SECONDS:
                    table.add_column('Elapsed Seconds', justify='center', max_width=7)
                case PytestField.MEAN:
                    table.add_column(f'mean {mean_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.MEDIAN:
                    table.add_column(f'median {median_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.MIN:
                    table.add_column(f'min {min_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.MAX:
                    table.add_column(f'max {max_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.P1:
                    table.add_column(f'1st {p1_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.P5:
                    table.add_column(f'5th {p5_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.P25:
                    table.add_column(f'25th {p25_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.P75:
                    table.add_column(f'75th {p75_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.P95:
                    table.add_column(f'95th {p95_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.P99:
                    table.add_column(f'99th {p99_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.STD_DEV:
                    table.add_column(f'std dev {stddev_unit}', justify='center', vertical='bottom', overflow='fold')
                case PytestField.RSD_PERCENT:
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
                    case PytestField.N:
                        row.append(f'{str(result.n):>6}')
                    case PytestField.ITERATIONS:
                        row.append(f'{len(result.iterations):>6d}')
                    case PytestField.ROUNDS:
                        row.append(f'{result.rounds:>6d}')
                    case PytestField.ELAPSED_SECONDS:
                        row.append(f'{result.total_elapsed * DEFAULT_INTERVAL_SCALE:>4.2f}')
                    case PytestField.MEAN:
                        row.append(f'{sigfigs(stats_target.mean * mean_scale):>8.2f}')
                    case PytestField.MEDIAN:
                        row.append(f'{sigfigs(stats_target.median * median_scale):>8.2f}')
                    case PytestField.MIN:
                        row.append(f'{sigfigs(stats_target.minimum * min_scale):>8.2f}')
                    case PytestField.MAX:
                        row.append(f'{sigfigs(stats_target.maximum * max_scale):>8.2f}')
                    case PytestField.P1:
                        row.append(f'{sigfigs(stats_target.percentiles[1] * p1_scale):>8.2f}')
                    case PytestField.P5:
                        row.append(f'{sigfigs(stats_target.percentiles[5] * p5_scale):>8.2f}')
                    case PytestField.P25:
                        row.append(f'{sigfigs(stats_target.percentiles[25] * p25_scale):>8.2f}')
                    case PytestField.P75:
                        row.append(f'{sigfigs(stats_target.percentiles[75] * p75_scale):>8.2f}')
                    case PytestField.P95:
                        row.append(f'{sigfigs(stats_target.percentiles[95] * p95_scale):>8.2f}')
                    case PytestField.P99:
                        row.append(f'{sigfigs(stats_target.percentiles[99] * p99_scale):>8.2f}')
                    case PytestField.STD_DEV:
                        row.append(f'{sigfigs(stats_target.standard_deviation * stddev_scale):>8.2f}')
                    case PytestField.RSD_PERCENT:
                        row.append(f'{sigfigs(stats_target.relative_standard_deviation):>5.2f}%')

            if options.variation_cols_last:
                for value in result.variation_marks.values():
                    row.append(f'{value!s}')

            table.add_row(*row)

        return table
