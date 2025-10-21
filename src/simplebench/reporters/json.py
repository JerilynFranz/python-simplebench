# -*- coding: utf-8 -*-
"""Reporter for benchmark results using JSON files."""
from __future__ import annotations
from argparse import Namespace
from dataclasses import dataclass
import json
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

from ..enums import Section, FlagType
from ..utils import sanitize_filename, get_machine_info, sigfigs
from .interfaces import Reporter
from .choices import Choice, Choices, Target, Format
from .protocols import ReporterCallback

if TYPE_CHECKING:
    from ..case import Case
    from ..session import Session


@dataclass
class JSONExtras:
    """Class for holding extra JSON reporter options in a Choice."""
    full_data: bool = False
    """ Whether to include full data in the JSON output, including all
    individual timing results and operation counts. Default is False, which
    includes only summary statistics."""


class JSONReporter(Reporter):
    """Class for outputting benchmark results to JSON files.

    It supports reporting operations per second and per round timing results,
    either separately or together, to the filesystem or via a callback function.

    The JSON files are tagged with metadata including the case title,
    description, and units for clarity.

    Defined command-line flags:
        --json: Outputs both operations per second and per round timing results to JSON.
        --json-ops: Outputs only operations per second results to JSON.
        --json-timings: Outputs only per round timing results to JSON.

    Attributes:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Choices): A collection of Choices instances defining
            the reporter instance, CLI flags, Choice name, supported Result Sections,
            supported output Targets, and supported output Formats for the reporter.
    """

    def __init__(self) -> None:
        super().__init__(
            name='json',
            description='Outputs benchmark results to JSON files.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.FILESYSTEM, Target.CALLBACK},
            formats={Format.JSON},
            choices=Choices([
                Choice(
                    reporter=self,
                    flags=['--json'],
                    flag_type=FlagType.BOOLEAN,
                    name='json',
                    description='statistical results to JSON',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    formats=[Format.JSON],
                    extra=JSONExtras(full_data=False)),
                Choice(
                    reporter=self,
                    flags=['--json-data'],
                    flag_type=FlagType.BOOLEAN,
                    name='json-data',
                    description='statistical results to JSON + full data',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    formats=[Format.JSON],
                    extra=JSONExtras(full_data=True)),
            ])
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,  # pylint: disable=unused-argument
                   callback: ReporterCallback | None = None,  # pylint: disable=unused-argument
                   ) -> None:
        """Output the benchmark results to a file as tagged JSON if available.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid without a large amount of boilerplate code. The base class also handles lazy
        loading of the reporter classes, so subclasses can assume any required imports are available

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Path | None, default=None): The path to the directory where the JSON file(s) will be saved.
            session (Session | None, default=None): The Session instance containing benchmark results.
            callback (ReporterCallback | None, default=None): A callback function for additional processing
                of the report.

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or if
                required arguments are missing. Also raised if the callback is not callable when
                provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
                target is specified.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        directory = path / 'json'  # type: ignore[reportOptionalMemberAccess]
        directory.mkdir(parents=True, exist_ok=True)

        file = directory / sanitize_filename('meta.machine_info.json')
        if not file.exists() and Target.FILESYSTEM in choice.targets:
            machine_info = get_machine_info()
            with file.open('w', encoding='utf-8') as json_file:
                json.dump(machine_info, json_file, indent=4)

        for section in choice.sections:
            json_text: str = ''
            full_data: bool = choice.extra.full_data if isinstance(choice.extra, JSONExtras) else False
            with StringIO(newline='') as jsonfile:
                json.dump(case.as_dict(full_data=full_data), jsonfile, indent=4)
                jsonfile.seek(0)
                json_text = jsonfile.read()

            if Target.CALLBACK in choice.targets and case.callback is not None:
                case.callback(case=case, section=section, output_format=Format.JSON, output=json_text)

            if Target.FILESYSTEM in choice.targets:
                file_counter: int = 1
                safe_filename: str = sanitize_filename(section.value)
                file = directory / f'data.{safe_filename}_{file_counter:03d}.json'
                while file.exists():
                    file_counter += 1
                    file = directory / f'data.{safe_filename}_{file_counter:03d}.json'
                with file.open('w', encoding='utf-8') as json_file:
                    json_file.write(json_text)

    def mean_change(self, first: Case, second: Case, section: Section) -> float | None:
        """Compare two Case instances for a given section and return the change as a float ratio.

        The float ratio is calculated as (value2 - value1) / value1, where value1 and value2
        are the mean values for the specified section in the first and second cases, respectively.

        A value of 0.0 indicates no change, a positive value indicates an increase,
        and a negative value indicates a decrease. If either case does not have data for the
        specified section, None is returned. The ratio is limited to 3 significant digits for
        clarity and to prevent a false sense of precision to the result.

        If first mean value is 0.0 and second mean value is also 0.0, the change is defined as 0.0.
        If first mean value is 0.0 and second mean value is non-zero, the change is defined as
        None to indicate incomparability.

        Args:
            first (Case): The first Case instance to compare.
            second (Case): The second Case instance to compare.
            section (Section): The Section to compare.

        Returns:
            float | None: The change between the mean for two cases for the specified section,
            or None if the section is not present in either case or the numbers are incomparable.
        """
        value1 = first.section_mean(section)
        value2 = second.section_mean(section)

        if value1 is None or value2 is None:
            return None

        if value1 == 0.0:
            if value2 == 0.0:
                return 0.0
            return None  # Infinite increase from zero to non-zero is not comparable
        if value1 == 0 and value2 == 0:
            return 0.0

        return sigfigs((value2 - value1) / value1, 3)
