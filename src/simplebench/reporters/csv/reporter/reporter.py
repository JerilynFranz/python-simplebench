# -*- coding: utf-8 -*-
"""Reporter for benchmark results using CSV files."""
from __future__ import annotations
from argparse import Namespace
import csv
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

from simplebench.defaults import DEFAULT_INTERVAL_SCALE
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.results import Results
from simplebench.si_units import si_scale_for_smallest
from simplebench.utils import sigfigs
from simplebench.validators import validate_type

# simplebench.reporters imports
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter

# simplebench.reporters.csv imports
from .options import CSVOptions
from .exceptions import CSVReporterErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.session import Session


class CSVReporter(Reporter):
    """Class for outputting benchmark results to CSV files.

    It supports reporting statistics for various sections,
    either separately or together, to the filesystem, via a callback function,
    or to the console in CSV format.

    The CSV files are tagged with metadata comments including the case title,
    description, and units for clarity.

    Defined command-line flags:
        --csv: {file, console, callback} (default=file) Outputs results to CSV.

    Example usage:
        program.py --csv               # Outputs results to CSV files in the filesystem (default).
        program.py --csv filesystem    # Outputs results to CSV files in the filesystem.
        program.py --csv console       # Outputs results to the console in CSV format.
        program.py --csv callback      # Outputs results via a callback function in CSV format.
        program.py --csv filesystem console  # Outputs results to both CSV files and the console.

    Attributes:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Iterable[ChoicesConf]): Iterable of ChoicesConf instances defining
            the reporter instance, CLI flags, ChoiceConf  name, supported Result Sections,
            supported output Targets, and supported output Formats for the reporter.
        targets (set[Target]): The supported output targets for the reporter.
        formats (set[Format]): The supported output formats for the reporter.
    """
    _HARDCODED_DEFAULT_OPTIONS = CSVOptions()
    """Built-in default CSVOptions instance for the reporter used if none is specified
    in a passed `Case`, `Choice`, or by `_DEFAULT_OPTIONS`. It forms the basis for the
    dynamic default options functionality provided by the `set_default_options()` and
    `get_default_options()` methods."""

    def __init__(self) -> None:
        """Initialize the CSVReporter with its name, description, choices, targets, and formats."""
        super().__init__(
            name='csv',
            description='Outputs benchmark results to CSV files.',
            options_type=CSVOptions,
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE},
            formats={Format.CSV},
            file_suffix='csv',
            file_unique=True,
            file_append=False,
            choices=ChoicesConf([
                ChoiceConf(
                    flags=['--csv'],
                    flag_type=FlagType.TARGET_LIST,
                    name='csv',
                    description=(
                        'Output all results to CSV (filesystem, console, callback, default=filesystem)'),
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV,
                ),
                ChoiceConf(
                    flags=['--csv.ops'],
                    flag_type=FlagType.TARGET_LIST,
                    name='csv-ops',
                    description=(
                        'Output ops/second results to CSV (filesystem, console, callback, default=filesystem)'),
                    sections=[Section.OPS],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV,
                ),
                ChoiceConf(
                    flags=['--csv.timing'],
                    flag_type=FlagType.TARGET_LIST,
                    name='csv-timing',
                    description=(
                        'Output timing results to CSV (filesystem, console, callback, default=filesystem)'),
                    sections=[Section.TIMING],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV,
                ),
                ChoiceConf(
                    flags=['--csv.memory'],
                    flag_type=FlagType.TARGET_LIST,
                    name='csv-memory',
                    description=(
                        'Output memory results to CSV (filesystem, console, callback, default=filesystem)'),
                    sections=[Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV,
                ),
            ])
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,  # pylint: disable=unused-argument
                   callback: ReporterCallback | None = None  # pylint: disable=unused-argument
                   ) -> None:
        """Output the benchmark results to a file as tagged CSV if available.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid without a large amount of boilerplate code. The base class also handles lazy
        loading of the reporter classes, so subclasses can assume any required imports are available.

        It calls the Reporter.render_by_section() method to generate the report output.

        It passes the actual method to be used for rendering in the renderer parameter and that
        rendering method must conform with the ReportRenderer protocol.

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The ChoiceConf  instance specifying the report configuration.
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
        self.render_by_section(
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
        """Renders the benchmark results as tagged CSV data and returns it as a string.

        Args:
            case: The Case instance representing the benchmarked code.
            section: The section to output (eg. Section.OPS or Section.TIMING).
            options: The options for the CSV report. (Currently unused.)

        Returns:
            str: The benchmark results formatted as tagged CSV data.

        Raises:
            SimpleBenchValueError: If the specified section is unsupported.
        """
        case = validate_type(case, Case, 'case',
                             CSVReporterErrorTag.RENDER_INVALID_CASE)
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
                    sigfigs(stats_target.standard_deviation * common_scale),
                    sigfigs(stats_target.relative_standard_deviation)
                ]
                for value in result.variation_marks.values():
                    row.append(value)
                writer.writerow(row)

            csvfile.seek(0)
            return csvfile.read()
