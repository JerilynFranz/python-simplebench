"""Reporter for benchmark results using CSV files.

This module provides the :class:`~.CSVReporter` class, which is responsible for
outputting benchmark results to CSV files.
"""
from __future__ import annotations

import csv
from io import StringIO
from typing import TYPE_CHECKING, Any, ClassVar

from simplebench.defaults import DEFAULT_INTERVAL_SCALE
from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError
# simplebench.reporters imports
from simplebench.reporters.reporter import Reporter
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.results import Results
from simplebench.si_units import si_scale_for_smallest
from simplebench.type_proxies import is_case
from simplebench.utils import sigfigs
from simplebench.validators import validate_type

from .config import CSVConfig
from .exceptions import CSVReporterErrorTag
from .options import CSVOptions

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
        :type case: :class:`~simplebench.case.Case`
        :param section: The section to output (eg. :attr:`~simplebench.enums.Section.OPS` or
                        :attr:`~simplebench.enums.Section.TIMING`).
        :type section: :class:`~simplebench.enums.Section`
        :param options: The options for the CSV report. (Currently unused.)
        :type options: :class:`~simplebench.reporters.reporter.options.ReporterOptions`
        :return: The benchmark results formatted as tagged CSV data.
        :rtype: str
        :raises SimpleBenchValueError: If the specified section is unsupported.
        """
        if not is_case(case):  # Handle deferred import type checking
            raise SimpleBenchTypeError(
                f"Invalid case argument: expected Case instance, got {type(case).__name__}",
                tag=CSVReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                CSVReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(options, self.options_type, 'options',
                                CSVReporterErrorTag.RENDER_INVALID_OPTIONS)

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
            header: list[str] = [
                'N',
                'Iterations',
                'Rounds',
                'Elapsed Seconds',
                f'mean ({common_unit})',
                f'median ({common_unit})',
                f'min ({common_unit})',
                f'max ({common_unit})',
                f'5th ({common_unit})',
                f'95th ({common_unit})',
                f'std dev ({common_unit})',
                'rsd (%)'
            ]
            for value in case.variation_cols.values():
                header.append(value)
            writer.writerow(header)
            for result in results:
                stats_target = result.results_section(section)
                row: list[str | float | int] = [
                    result.n,
                    len(result.iterations),
                    result.rounds,
                    result.total_elapsed * DEFAULT_INTERVAL_SCALE,
                    sigfigs(stats_target.mean * common_scale),
                    sigfigs(stats_target.median * common_scale),
                    sigfigs(stats_target.minimum * common_scale),
                    sigfigs(stats_target.maximum * common_scale),
                    sigfigs(stats_target.percentiles[5] * common_scale),
                    sigfigs(stats_target.percentiles[95] * common_scale),
                    sigfigs(stats_target.adjusted_standard_deviation * common_scale),
                    sigfigs(stats_target.adjusted_relative_standard_deviation)
                ]
                for value in result.variation_marks.values():
                    row.append(value)
                writer.writerow(row)

            csvfile.seek(0)
            return csvfile.read()
