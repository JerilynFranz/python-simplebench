# -*- coding: utf-8 -*-
"""Reporter for benchmark results using CSV files."""
from __future__ import annotations
import csv
from io import TextIOWrapper, StringIO
from pathlib import Path
from typing import Any, Callable, Optional, TYPE_CHECKING


from ..constants import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE
from ..enums import Section, Target, Format
from ..exceptions import SimpleBenchValueError, ErrorTag
from .interfaces import Reporter
from ..results import Results
from ..si_units import si_scale_for_smallest
from ..utils import sanitize_filename, sigfigs
from .choices import Choice, Choices

if TYPE_CHECKING:
    from ..case import Case
    from ..session import Session


class CSVReporter(Reporter):
    """Class for outputting benchmark results to CSV files.

    It supports reporting operations per second and per round timing results,
    either separately or together, to the filesystem or via a callback function.

    The CSV files are tagged with metadata comments including the case title,
    description, and units for clarity.

    Defined command-line flags:
        --csv: Outputs both operations per second and per round timing results to CSV.
        --csv-ops: Outputs only operations per second results to CSV.
        --csv-timings: Outputs only per round timing results to CSV.

    Attributes:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Choices): A collection of Choices instances defining
            the reporter instance, CLI flags, Choice name, supported Result Sections,
            supported output Targets, and supported output Formats for the reporter.
    """

    def __init__(self) -> None:
        super().__init__(
            name='csv',
            description='Outputs benchmark results to CSV files.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.FILESYSTEM, Target.CALLBACK},
            formats={Format.CSV},
            choices=self._load_choices()
        )

    def _load_choices(self) -> Choices:
        """Load the Choices instance for the reporter, including sections, output targets, and formats."""
        choices: Choices = Choices()
        self._choices: Choices = choices
        choices.add(
            Choice(
                reporter=self,
                flags=['--csv'],
                name='csv',
                description='operations per second and per round timing results to CSV',
                sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.CSV]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--csv-ops'],
                name='csv-ops',
                description='Save operations per second results to CSV',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.CSV]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--csv-timings'],
                name='csv-timings',
                description='per round timing results to CSV',
                sections=[Section.TIMING],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.CSV]))
        choices.add(
            Choice(
                reporter=self,
                flags=['--csv-memory'],
                name='csv-memory',
                description='memory usage results to CSV',
                sections=[Section.MEMORY, Section.PEAK_MEMORY],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.CSV]))
        return choices

    def run_report(self,
                   *,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,  # pylint: disable=unused-argument
                   callback: Optional[Callable[[Case, Section, Format, Any], None]
                                      ] = None  # pylint: disable=unused-argument
                   ) -> None:
        """Output the benchmark results to a file as tagged CSV if available.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid without a large amount of boilerplate code. The base class also handles lazy
        loading of the reporter classes, so subclasses can assume any required imports are available

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
                    f"Unsupported section: {section} (this should never happen)",
                    tag=ErrorTag.CSV_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION)

            filename: str = sanitize_filename(section.value)
            if Target.FILESYSTEM in choice.targets:
                file = path.joinpath('csv', f'{filename}.csv')  # type: ignore[reportOptionalMemberAccess]
                file.parent.mkdir(parents=True, exist_ok=True)
                with file.open(mode='w', encoding='utf-8', newline='') as csvfile:
                    self._to_csv(case=case, section=section, csvfile=csvfile, base_unit=base_unit)
            if Target.CALLBACK in choice.targets and case.callback is not None:
                with StringIO(newline='') as csvfile:
                    self._to_csv(case=case, section=section, csvfile=csvfile, base_unit=base_unit)
                    csvfile.seek(0)
                    case.callback(case, section, Format.CSV, csvfile.read())

    def _to_csv(self, case: Case, section: Section, csvfile: TextIOWrapper | StringIO, base_unit: str) -> None:
        """Output the benchmark results as tagged CSV to the csvfile.

        Args:
            case: The Case instance representing the benchmarked code.
            section: The section to output (eg. Section.OPS or Section.TIMING).
            csvfile: The file-like object to write the CSV data to.
            base_unit: The base unit for the measurements (e.g., 'seconds', 'operations').

        Returns:
            None
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
