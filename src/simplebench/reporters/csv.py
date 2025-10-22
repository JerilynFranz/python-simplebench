# -*- coding: utf-8 -*-
"""Reporter for benchmark results using CSV files."""
from __future__ import annotations
from argparse import Namespace
import csv
from io import StringIO
from pathlib import Path
from typing import Optional, Iterable, TYPE_CHECKING


from ..defaults import DEFAULT_INTERVAL_SCALE
from ..enums import Section, Target, Format, FlagType
from ..exceptions import SimpleBenchValueError, ErrorTag
from ..results import Results
from ..si_units import si_scale_for_smallest
from ..utils import sanitize_filename, sigfigs
from .choices import Choice, Choices, ChoiceOptions
from .interfaces import Reporter
from .protocols import ReporterCallback


if TYPE_CHECKING:
    from ..case import Case
    from ..session import Session


class CSVChoiceOptions(ChoiceOptions):
    """Class for holding CSV reporter specificoptions in a Choice.

    This class provides additional configuration options specific to the CSV reporter.
    It is accessed via the `options` attribute of a Choice instance.

    Attributes:
        default_targets (frozenset[Target]): The default targets for the CSV reporter choice.
        subdir (str): The subdirectory to output CSV files to.
    """
    def __init__(self, default_targets: Iterable[Target], subdir: str = 'str') -> None:
        """Initialize CSVChoiceOptions with default targets and subdirectory.

        Args:
            default_targets (Iterable[Target]): The default targets for the CSV reporter choice.
            subdir (str, default='csv'): The subdirectory to output CSV files to.
        """
        self._default_targets: frozenset[Target] = frozenset(default_targets)
        self._subdir: str = subdir

    @property
    def default_targets(self) -> frozenset[Target]:
        """Return the default targets for the CSV reporter choice."""
        return self._default_targets

    @property
    def subdir(self) -> str:
        """Return the subdirectory to output CSV files to."""
        return self._subdir


class CSVReporter(Reporter):
    """Class for outputting benchmark results to CSV files.

    It supports reporting operations per second and per round timing results,
    either separately or together, to the filesystem or via a callback function.

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
        choices (Choices): A collection of Choices instances defining
            the reporter instance, CLI flags, Choice name, supported Result Sections,
            supported output Targets, and supported output Formats for the reporter.
    """

    DEFAULT_TARGETS = [Target.FILESYSTEM]
    """Default targets for CSVReporter choices."""

    def __init__(self) -> None:
        super().__init__(
            name='csv',
            description='Outputs benchmark results to CSV files.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE},
            formats={Format.CSV},
            choices=Choices([
                Choice(
                    reporter=self,
                    flags=['--csv'],
                    flag_type=FlagType.TARGET_LIST,
                    name='csv',
                    description=(
                        'Output results to CSV (file, console, callback, default=file)'),
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    formats=[Format.CSV],
                    options=CSVChoiceOptions(default_targets=self.DEFAULT_TARGETS)),
            ])
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,  # pylint: disable=unused-argument
                   callback: Optional[ReporterCallback] = None  # pylint: disable=unused-argument
                   ) -> None:
        """Output the benchmark results to a file as tagged CSV if available.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid without a large amount of boilerplate code. The base class also handles lazy
        loading of the reporter classes, so subclasses can assume any required imports are available

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
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
        default_targets: frozenset[Target] = frozenset()
        subdir: str = 'csv'
        if isinstance(choice.options, CSVChoiceOptions):
            default_targets = choice.options.default_targets
            subdir = choice.options.subdir

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=default_targets)
        for section in choice.sections:
            base_unit: str = self.get_base_unit_for_section(section=section)
            csv_output = self._to_csv(case=case, section=section, base_unit=base_unit)

            for output_target in targets:
                match output_target:
                    case Target.FILESYSTEM:
                        filename: str = sanitize_filename(section.value) + '.csv'
                        self.target_filesystem(
                            path=path, subdir=subdir, filename=filename, output=csv_output)

                        # with file.open(mode='w', encoding='utf-8', newline='') as csvfile:
                        #     self._to_csv(case=case, section=section, csvfile=csvfile, base_unit=base_unit)
                    case Target.CALLBACK:
                        self.target_callback(
                            callback=callback, case=case, section=section, output_format=Format.CSV, output=csv_output)

                    case Target.CONSOLE:
                        output = f'[bold underline]CSV Report - {section.value}[/bold underline]\n\n{csv_output}'
                        self.target_console(session=session, output=output)

                    case _:
                        raise SimpleBenchValueError(
                            f'Unsupported target for CSVReporter: {output_target}',
                            tag=ErrorTag.REPORTER_RUN_REPORT_UNSUPPORTED_TARGET)

    def _to_csv(self, case: Case, section: Section, base_unit: str) -> str:
        """Return the benchmark results as tagged CSV data.

        Args:
            case: The Case instance representing the benchmarked code.
            section: The section to output (eg. Section.OPS or Section.TIMING).
            base_unit: The base unit for the measurements (e.g., 'seconds', 'operations').

        Returns:
            str: The benchmark results formatted as tagged CSV data.

        Raises:
            SimpleBenchValueError: If the specified section is unsupported.
        """
        results: list[Results] = case.results

        # Determine a common SI scale for the output values to improve readability
        all_numbers: list[float] = []
        all_numbers.extend([result.results_section(section).mean for result in results])
        all_numbers.extend([result.results_section(section).median for result in results])
        all_numbers.extend([result.results_section(section).minimum for result in results])
        all_numbers.extend([result.results_section(section).maximum for result in results])
        all_numbers.extend([result.results_section(section).percentiles[5] for result in results])
        all_numbers.extend([result.results_section(section).percentiles[95] for result in results])
        all_numbers.extend([result.results_section(section).standard_deviation for result in results])
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
