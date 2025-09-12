# -*- coding: utf-8 -*-
"""Reporter for benchmark results using JSON files."""
from __future__ import annotations
from argparse import ArgumentParser
import json
from io import StringIO
from pathlib import Path
from typing import Any, Callable, Optional, TYPE_CHECKING

from ..case import Case
from .interfaces import Reporter
from ..utils import sanitize_filename, get_machine_info
from .choices import Choice, Choices, Section, Target, Format
if TYPE_CHECKING:
    from ..session import Session


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
        choices: Choices = Choices()
        self._choices: Choices = choices
        choices.add(
            Choice(
                reporter=self,
                flags=['--json'],
                name='json',
                description='operations per second and per round timing results to JSON',
                sections=[Section.OPS, Section.TIMING],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.JSON],
                extra={'full_data': False})
        )
        choices.add(
            Choice(
                reporter=self,
                flags=['--json-ops'],
                name='json-ops',
                description='Save operations per second results to JSON',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.JSON],
                extra={'full_data': False})
        )
        choices.add(
            Choice(
                reporter=self,
                flags=['--json-timings'],
                name='json-timings',
                description='per round timing results to JSON',
                sections=[Section.TIMING],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.JSON],
                extra={'full_data': False})
        )
        choices.add(
            Choice(
                reporter=self,
                flags=['--json-data'],
                name='json-data',
                description='operations per second and per round timing results to JSON + full data',
                sections=[Section.OPS, Section.TIMING],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.JSON],
                extra={'full_data': True})
        )
        choices.add(
            Choice(
                reporter=self,
                flags=['--json-ops-data'],
                name='json-ops-data',
                description='Save operations per second results to JSON + full data',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.JSON],
                extra={'full_data': True})
        )
        choices.add(
            Choice(
                reporter=self,
                flags=['--json-timings-data'],
                name='json-timings-data',
                description='per round timing results to JSON + full data',
                sections=[Section.TIMING],
                targets=[Target.FILESYSTEM, Target.CALLBACK],
                formats=[Format.JSON],
                extra={'full_data': True})
        )

    def supported_formats(self):
        """Return the set of supported output formats for the reporter."""
        return set([Format.JSON])

    def supported_sections(self):
        """Return the set of supported result sections for the reporter."""
        return set([Section.OPS, Section.TIMING])

    def supported_targets(self):
        """Return the set of supported output targets for the reporter."""
        return set([Target.FILESYSTEM, Target.CALLBACK])

    @property
    def choices(self) -> Choices:
        """Return the Choices instance for the reporter, including sections,
        output targets, and formats.
        """
        return self._choices

    @property
    def name(self) -> str:
        """Return the unique identifying name of the reporter."""
        return 'json'

    @property
    def description(self) -> str:
        """Return a brief description of the reporter."""
        return 'Outputs benchmark results to JSON files.'

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        for choice in self.choices.values():
            for flag in choice.flags:
                parser.add_argument(flag, action='store_true', help=choice.description)

    def run_report(self,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,  # pylint: disable=unused-argument
                   callback: Optional[Callable[[Case, Section, Format, Any], None]
                                      ] = None  # pylint: disable=unused-argument
                   ) -> None:
        """Output the benchmark results to a file as tagged JSON if available.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid without a large amount of boilerplate code. The base class also handles lazy
        loading of the reporter classes, so subclasses can assume any required imports are available

        Args:
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the JSON file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[Callable[[Case, Section, Format, Any], None]]):
                A callback function for additional processing of the report.
                The function should accept two arguments: the Case instance and the JSON data as a string.
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
        directory = path / 'json'  # type: ignore[reportOptionalMemberAccess]
        directory.mkdir(parents=True, exist_ok=True)

        file = directory / sanitize_filename('meta.machine_info.json')
        if not file.exists() and Target.FILESYSTEM in choice.targets:
            machine_info = get_machine_info()
            with file.open('w', encoding='utf-8') as json_file:
                json.dump(machine_info, json_file, indent=4)

        for section in choice.sections:
            json_text: str = ''
            full_data: bool = choice.extra.get('full_data', False)
            with StringIO(newline='') as jsonfile:
                json.dump(case.as_dict(full_data=full_data), jsonfile, indent=4)
                jsonfile.seek(0)
                json_text = jsonfile.read()

            if Target.CALLBACK in choice.targets and case.callback is not None:
                case.callback(case, section, Format.JSON, json_text)

            if Target.FILESYSTEM in choice.targets:
                file_counter: int = 1
                safe_filename: str = sanitize_filename(section.value)
                file = directory / f'data.{safe_filename}_{file_counter:03d}.json'
                while file.exists():
                    file_counter += 1
                    file = directory / f'data.{safe_filename}_{file_counter:03d}.json'
                with file.open('w', encoding='utf-8') as json_file:
                    json_file.write(json_text)
