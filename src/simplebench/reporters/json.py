# -*- coding: utf-8 -*-
"""Reporter for benchmark results using JSON files."""
from __future__ import annotations
from argparse import Namespace
import json
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from ..enums import Section, FlagType
from ..exceptions import SimpleBenchValueError, SimpleBenchTypeError, ErrorTag
from ..utils import sanitize_filename, get_machine_info, sigfigs
from .interfaces import Reporter
from .choices import Choice, Choices, ChoiceOptions, Target, Format
from .protocols import ReporterCallback

if TYPE_CHECKING:
    from ..case import Case
    from ..session import Session


class JSONChoiceOptions(ChoiceOptions):
    """Class for holding JSON reporter specific options in a Choice.

    This class provides additional configuration options specific to the JSON reporter.
    It is accessed via the `options` attribute of a Choice instance.

    Attributes:
        default_targets (frozenset[Target]): The default targets for the JSON reporter choice.
        subdir (str): The subdirectory to output JSON files to.
        full_data (bool): Whether to include full data in the JSON output.

    """
    def __init__(self,
                 default_targets: Iterable[Target],
                 subdir: str = 'json',
                 full_data: bool = False) -> None:
        """Initialize JSONChoiceOptions with default targets and subdirectory.

        Args:
            default_targets (Iterable[Target]): The default targets for the JSON reporter choice.
            subdir (str, default='json'): The subdirectory to output JSON files to.
            full_data (bool, default=False): Whether to include full data in the JSON output.
        """
        self._default_targets: frozenset[Target] = frozenset(default_targets)
        self._subdir: str = subdir
        self._full_data: bool = full_data

    @property
    def default_targets(self) -> frozenset[Target]:
        """Return the default targets for the JSON reporter choice.

        Returns:
            frozenset[Target]: The default targets for the JSON reporter choice.
        """
        return self._default_targets

    @property
    def subdir(self) -> str:
        """Return the subdirectory to output JSON files to.

        Returns:
            str: The subdirectory to output JSON files to.
        """
        return self._subdir

    @property
    def full_data(self) -> bool:
        """Return whether to include full data in the JSON output.

        Returns:
            bool: Whether to include full data in the JSON output.
        """
        return self._full_data


class JSONReporter(Reporter):
    """Class for outputting benchmark results to JSON files.

    It supports reporting statistics for various sections,
    either separately or together, to the filesystem, via a callback function,
    or to the console in JSON format.

    The JSON files are tagged with metadata comments including the case title,
    description, and units for clarity.

    Defined command-line flags:
        --json: {filesystem, console, callback} (default=filesystem) Outputs statistical results to JSON.
        --json-data: {filesystem, console, callback} (default=filesystem) Outputs results to JSON with full data.

    Example usage:
        program.py --json               # Outputs results to JSON files in the filesystem (default).
        program.py --json filesystem    # Outputs results to JSON files in the filesystem.
        program.py --json console       # Outputs results to the console in JSON format.
        program.py --json callback      # Outputs results via a callback function in JSON format.
        program.py --json filesystem console  # Outputs results to both JSON files and the console.

    Attributes:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Choices): A collection of Choices instances defining
            the reporter instance, CLI flags, Choice name, supported Result Sections,
            supported output Targets, and supported output Formats for the reporter.
        targets (set[Target]): The supported output targets for the reporter.
        formats (set[Format]): The supported output formats for the reporter.
        choices (Choices): The supported Choices for the reporter.
    """
    def __init__(self) -> None:
        """Initialize the JSONReporter with its name, description, choices, targets, and formats."""
        super().__init__(
            name='json',
            description='Outputs benchmark results to JSON files.',
            sections={Section.NULL},
            targets={Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE},
            formats={Format.JSON},
            choices=Choices([
                Choice(
                    reporter=self,
                    flags=['--json'],
                    flag_type=FlagType.TARGET_LIST,
                    name='json',
                    description='statistical results to JSON (filesystem, console, callback, default=filesystem)',
                    sections=[Section.NULL],  # All sections are always included
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    formats=[Format.JSON],
                    options=JSONChoiceOptions(
                        default_targets=[Target.FILESYSTEM],
                        subdir='json',
                        full_data=False)),
                Choice(
                    reporter=self,
                    flags=['--json-data'],
                    flag_type=FlagType.TARGET_LIST,
                    name='json-data',
                    description=('statistical results + full data to JSON '
                                 '(filesystem, console, callback, default=filesystem)'),
                    sections=[Section.NULL],  # All sections are always included
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    formats=[Format.JSON],
                    options=JSONChoiceOptions(
                        default_targets=[Target.FILESYSTEM],
                        subdir='json_data',
                        full_data=True)),
            ])
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None
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
            path (Path | None): The path to the directory where the JSON file(s) will be saved.
            session (Session | None): The Session instance containing benchmark results.
            callback (ReporterCallback | None):
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
        default_targets: frozenset[Target] = frozenset()
        subdir: str = 'json'
        if isinstance(choice.options, JSONChoiceOptions):
            default_targets = choice.options.default_targets
            subdir = choice.options.subdir

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=default_targets)
        json_output = self._to_json(case=case, choice=choice)

        for output_target in targets:
            match output_target:
                case Target.FILESYSTEM:
                    filename: str = sanitize_filename(case.title) + '.json'
                    self.target_filesystem(
                        path=path, subdir=subdir, filename=filename, output=json_output, unique=True)

                case Target.CALLBACK:
                    self.target_callback(
                        callback=callback,
                        case=case,
                        section=Section.NULL,
                        output_format=Format.JSON,
                        output=json_output)

                case Target.CONSOLE:
                    self.target_console(session=session, output=json_output)

                case _:
                    raise SimpleBenchValueError(
                        f'Unsupported target for JSONReporter: {output_target}',
                        tag=ErrorTag.REPORTER_RUN_REPORT_UNSUPPORTED_TARGET)

    def _to_json(self, *, case: Case, choice: Choice) -> str:
        """Convert the Case data for a given section to a JSON string.
        Machine info is included in the JSON output under the 'metadata' key.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.

        Returns:
            str: The JSON string representation of the Case data.
        """
        full_data: bool = choice.options.full_data if isinstance(choice.options, JSONChoiceOptions) else False
        with StringIO() as jsonfile:
            case_dict = case.as_dict(full_data=full_data)
            try:
                case_dict['metadata'] = get_machine_info()
                json.dump(case_dict, jsonfile, indent=4)
                jsonfile.seek(0)
            except Exception as exc:
                raise SimpleBenchTypeError(
                    f'Error generating JSON output for case {case.title}: {exc}',
                    tag=ErrorTag.REPORTER_JSON_OUTPUT_ERROR) from exc
            return jsonfile.read()

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
