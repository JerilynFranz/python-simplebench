"""Reporter for benchmark results using CSV files.

This module provides the :class:`~.CSVReporter` class, which is responsible for
outputting benchmark results to CSV files.
"""
from __future__ import annotations

import csv
from io import StringIO
from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias

from simplebench.defaults import DEFAULT_INTERVAL_SCALE
from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.reporter import Reporter
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.results import Results
from simplebench.si_units import si_scale_for_smallest
from simplebench.type_proxies import is_case
from simplebench.utils import sigfigs
from simplebench.validators import validate_type

from .config import CSVConfig
from .exceptions import _CSVReporterErrorTag
from .options import CSVField, CSVOptions

Options: TypeAlias = CSVOptions

if TYPE_CHECKING:
    from simplebench.case import Case


class CSVReporter(Reporter):
    """Class for outputting benchmark results to CSV files.

    It supports reporting statistics for various sections,
    either separately or together, to the filesystem, via a callback function,
    or to the console in CSV format.

    The CSV files are tagged with metadata comments including the case title,
    description, and units for clarity.

    Defined command-line flags:
        --csv: {file, console, callback} (default=file) Outputs results to CSV.

    .. code-block:: bash

        program.py --csv               # Outputs results to CSV files in the filesystem (default).
        program.py --csv filesystem    # Outputs results to CSV files in the filesystem.
        program.py --csv console       # Outputs results to the console in CSV format.
        program.py --csv callback      # Outputs results via a callback function in CSV format.
        program.py --csv filesystem console  # Outputs results to both CSV files and the console.

    :ivar name: The unique identifying name of the reporter.
    :vartype name: str
    :ivar description: A brief description of the reporter.
    :vartype description: str
    :ivar choices: Iterable of :class:`~.ChoicesConf` instances defining
        the reporter instance, CLI flags, :class:`~.ChoiceConf` name, supported
        :class:`~simplebench.enums.Section` objects, supported output
        :class:`~simplebench.enums.Target` objects, and supported output
        :class:`~simplebench.enums.Format` for the reporter.
    :vartype choices: Iterable[:class:`~.ChoicesConf`]
    :ivar targets: The supported output targets for the reporter.
    :vartype targets: set[:class:`~simplebench.enums.Target`]
    :ivar formats: The supported output formats for the reporter.
    :vartype formats: set[:class:`~simplebench.enums.Format`]
    """
    _OPTIONS_TYPE: ClassVar[type[CSVOptions]] = CSVOptions  # pylint: disable=line-too-long  # type: ignore[reportInvalidVariableOverride]  # noqa: E501
    """:meta private:"""
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}
    """:meta private:"""

    def __init__(self, config: CSVConfig | None = None) -> None:
        """Initialize the :class:`~.CSVReporter`.

        .. note::

            The exception documentation below refers to validation of subclass configuration
            class variables :attr:`~._OPTIONS_TYPE` and :attr:`~._OPTIONS_KWARGS`. These must be
            correctly defined in any subclass of :class:`~.CSVReporter` to ensure proper
            functionality.

        :param config: An optional configuration object to override default reporter settings.
                       If not provided, default settings will be used.
        :type config: CSVConfig | None

        :raises SimpleBenchTypeError: If the subclass configuration types are invalid.
        :raises SimpleBenchValueError: If the subclass configuration values are invalid.
        """
        if config is None:
            config = CSVConfig()

        super().__init__(config)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
        """Renders the benchmark results as tagged CSV data and returns it as a string.

        :param case: The :class:`~simplebench.case.Case` instance representing the
                     benchmarked code.
        :param section: The section to output (eg. :attr:`~simplebench.enums.Section.OPS` or
                        :attr:`~simplebench.enums.Section.TIMING`).
        :param options: The options for the CSV report.
        :return: The benchmark results formatted as tagged CSV data.
        :raises SimpleBenchValueError: If the specified section is unsupported.
        """
        if not is_case(case):  # Handle deferred import type checking
            raise SimpleBenchTypeError(
                f"Invalid case argument: expected Case instance, got {type(case).__name__}",
                tag=_CSVReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                _CSVReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(options, Options, 'options',
                                _CSVReporterErrorTag.RENDER_INVALID_OPTIONS)

        included_fields = options.fields

        base_unit: str = self.get_base_unit_for_section(section=section)
        results: list[Results] = case.results

        # Determine a common SI scale for the output values to improve readability
        all_numbers: list[float] = self.get_all_stats_values(results=results, section=section)
        common_unit, common_scale = si_scale_for_smallest(numbers=all_numbers, base_unit=base_unit)

        with StringIO() as csvfile:
            csvfile.seek(0)

            writer = csv.writer(csvfile)
            writer.writerow([f'# title: {case.title}'])
            writer.writerow([f'# description: {case.description}'])
            writer.writerow([f'# unit: {common_unit}'])
            header: list[str] = []

            if not options.variation_cols_last:
                for value in case.variation_cols.values():
                    header.append(value)

            for field in included_fields:
                match field:
                    case CSVField.N:
                        header.append('N')
                    case CSVField.ITERATIONS:
                        header.append('Iterations')
                    case CSVField.ROUNDS:
                        header.append('Rounds')
                    case CSVField.ELAPSED_SECONDS:
                        header.append('Elapsed Seconds')
                    case CSVField.MEAN:
                        header.append(f'mean ({common_unit})')
                    case CSVField.MEDIAN:
                        header.append(f'median ({common_unit})')
                    case CSVField.MIN:
                        header.append(f'min ({common_unit})')
                    case CSVField.MAX:
                        header.append(f'max ({common_unit})')
                    case CSVField.P5:
                        header.append(f'5th ({common_unit})')
                    case CSVField.P95:
                        header.append(f'95th ({common_unit})')
                    case CSVField.STD_DEV:
                        header.append(f'std dev ({common_unit})')
                    case CSVField.RSD_PERCENT:
                        header.append('rsd (%)')

            if options.variation_cols_last:
                for value in case.variation_cols.values():
                    header.append(value)

            writer.writerow(header)
            for result in results:
                stats_target = result.results_section(section)
                row: list[str | float | int] = []

                if not options.variation_cols_last:
                    for value in result.variation_marks.values():
                        row.append(value)

                    for field in included_fields:
                        match field:
                            case CSVField.N:
                                row.append(result.n)
                            case CSVField.ITERATIONS:
                                row.append(len(result.iterations))
                            case CSVField.ROUNDS:
                                row.append(result.rounds)
                            case CSVField.ELAPSED_SECONDS:
                                row.append(sigfigs(result.total_elapsed * DEFAULT_INTERVAL_SCALE, 10))
                            case CSVField.MEAN:
                                row.append(sigfigs(stats_target.mean * common_scale))
                            case CSVField.MEDIAN:
                                row.append(sigfigs(stats_target.median * common_scale))
                            case CSVField.MIN:
                                row.append(sigfigs(stats_target.minimum * common_scale))
                            case CSVField.MAX:
                                row.append(sigfigs(stats_target.maximum * common_scale))
                            case CSVField.P5:
                                row.append(sigfigs(stats_target.percentiles[5] * common_scale))
                            case CSVField.P95:
                                row.append(sigfigs(stats_target.percentiles[95] * common_scale))
                            case CSVField.STD_DEV:
                                row.append(sigfigs(stats_target.standard_deviation * common_scale))
                            case CSVField.RSD_PERCENT:
                                row.append(sigfigs(stats_target.relative_standard_deviation))

                if options.variation_cols_last:
                    for value in result.variation_marks.values():
                        row.append(value)

                writer.writerow(row)

            csvfile.seek(0)
            return csvfile.read()
