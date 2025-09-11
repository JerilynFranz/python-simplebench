# -*- coding: utf-8 -*-
"""Reporter for benchmark results using CSV files."""
from __future__ import annotations
from argparse import ArgumentParser
import csv
from io import TextIOWrapper, StringIO
from pathlib import Path
from typing import Any, Callable, Optional, TYPE_CHECKING


from ..case import Case
from ..constants import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE
from ..exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from .interfaces import Reporter
from ..results import Results
from ..utils import sanitize_filename, sigfigs, si_scale_for_smallest
from .choices import Choice, Choices, Section, Target, Format


if TYPE_CHECKING:
    from ..session import Session

_lazy_classes_loaded: bool = False


def _lazy_load_classes() -> None:
    """Lazily load any classes or modules that cannot be loaded during initial setup."""
    global _lazy_classes_loaded  # pylint: disable=global-statement
    global Session  # pylint: disable=global-statement
    if not _lazy_classes_loaded:
        from ..session import Session  # pylint: disable=import-outside-toplevel
        _lazy_classes_loaded = True


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
        choices: Choices = Choices()
        self._choices: Choices = choices
        choices.add(
            Choice(
                reporter=self,
                flags=['--csv'],
                name='csv',
                description='operations per second and per round timing results to CSV',
                sections=[Section.OPS, Section.TIMING],
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

    @property
    def choices(self) -> Choices:
        """Return the Choices instance for the reporter, including sections,
        output targets, and formats.
        """
        return self._choices

    @property
    def name(self) -> str:
        """Return the unique identifying name of the reporter."""
        return 'csv'

    @property
    def description(self) -> str:
        """Return a brief description of the reporter."""
        return 'Outputs benchmark results to CSV files.'

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        for choice in self.choices.values():
            for flag in choice.flags:
                parser.add_argument(flag, action='store_true', help=choice.description)

    def report(self,
               case: Case,
               choice: Choice,
               path: Optional[Path] = None,
               session: Optional[Session] = None,
               callback: Optional[Callable[[Case, Section, Format, Any], None]] = None) -> None:
        """Output the benchmark results to a file as tagged CSV if available.

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
        _lazy_load_classes()
        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.CSV_REPORTER_REPORT_INVALID_CASE_ARG)
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                ErrorTag.CSV_REPORTER_REPORT_INVALID_CHOICE_ARG)
        for section in choice.sections:
            if section not in (Section.OPS, Section.TIMING):
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    ErrorTag.CSV_REPORTER_REPORT_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in (Target.FILESYSTEM, Target.CALLBACK):
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    ErrorTag.CSV_REPORTER_REPORT_UNSUPPORTED_TARGET)
        if Target.CALLBACK in choice.targets:
            if callback is not None and not callable(callback):
                raise SimpleBenchTypeError(
                    "Callback function must be callable if provided",
                    ErrorTag.CSV_REPORTER_REPORT_INVALID_CALLBACK_ARG)
        if Target.FILESYSTEM in choice.targets and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "Path must be a pathlib.Path instance when using FILESYSTEM target",
                ErrorTag.CSV_REPORTER_REPORT_INVALID_PATH_ARG)
        for output_format in choice.formats:
            if output_format is not Format.CSV:
                raise SimpleBenchValueError(
                    f"Unsupported Format in Choice: {output_format}",
                    ErrorTag.CSV_REPORTER_REPORT_UNSUPPORTED_FORMAT)

        if session is not None and not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                ErrorTag.CSV_REPORTER_REPORT_INVALID_SESSION_ARG)

        # Only proceed if there are results to report
        results = case.results
        if not results:
            return

        for section in choice.sections:
            base_unit: str = ''
            if section is Section.OPS:
                base_unit = BASE_OPS_PER_INTERVAL_UNIT
            elif section is Section.TIMING:
                base_unit = BASE_INTERVAL_UNIT
            else:  # This should never happen due to earlier validation
                raise SimpleBenchValueError(
                    f"Unsupported section: {section} (this should not happen)",
                    ErrorTag.CSV_REPORTER_REPORT_UNSUPPORTED_SECTION)

            filename: str = sanitize_filename(section.value)
            if Target.FILESYSTEM in choice.targets:
                file = path.joinpath('csv', f'{filename}.csv')  # type: ignore[reportOptionalMemberAccess]
                file.parent.mkdir(parents=True, exist_ok=True)
                with file.open(mode='w', encoding='utf-8', newline='') as csvfile:
                    self.to_csv(case=case, target=section.value, csvfile=csvfile, base_unit=base_unit)
            if Target.CALLBACK in choice.targets and case.callback is not None:
                with StringIO(newline='') as csvfile:
                    self.to_csv(case=case, target=section.value, csvfile=csvfile, base_unit=base_unit)
                    csvfile.seek(0)
                    case.callback(case, section, Format.CSV, csvfile.read())

    def to_csv(self, case: Case, csvfile: TextIOWrapper | StringIO, base_unit: str, target: str) -> None:
        """Output the benchmark results as tagged CSV to the csvfile.

        Args:
            case: The Case instance representing the benchmarked code.
            csvfile: The file-like object to write the CSV data to.
            base_unit: The base unit for the measurements (e.g., 'seconds', 'operations').
            target: The target section to output (eg. 'ops_per_second' or 'per_round_timing').

        Returns:
            None
        """
        all_numbers: list[float] = []
        results: list[Results] = case.results
        all_numbers.extend([getattr(result, target).mean for result in results])
        all_numbers.extend([getattr(result, target).median for result in results])
        all_numbers.extend([getattr(result, target).minimum for result in results])
        all_numbers.extend([getattr(result, target).maximum for result in results])
        all_numbers.extend([getattr(result, target).percentiles[5] for result in results])
        all_numbers.extend([getattr(result, target).percentiles[95] for result in results])
        all_numbers.extend([getattr(result, target).standard_deviation for result in results])
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
            stats_target = getattr(result, target)
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
