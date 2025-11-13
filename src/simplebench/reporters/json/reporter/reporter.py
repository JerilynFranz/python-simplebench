"""Reporter for benchmark results using JSON files."""
from __future__ import annotations

import json
from argparse import Namespace
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

from simplebench.enums import FlagType, Format, Section, Target
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.protocols.reporter_callback import ReporterCallback
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.type_proxies import is_case
from simplebench.utils import get_machine_info, sigfigs
from simplebench.validators import validate_type

from .exceptions import JSONReporterErrorTag
from .options import JSONOptions

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.session import Session


Options = JSONOptions


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
    _HARDCODED_DEFAULT_OPTIONS = JSONOptions(full_data=False)
    """Built-in default JSONOptions instance for the reporter used if none is specified
    in a passed `Case`, `Choice`, or by `_DEFAULT_OPTIONS`. It forms the basis for the
    dynamic default options functionality provided by the `set_default_options()` and
    `get_default_options()` methods."""

    def __init__(self) -> None:
        """Initialize the JSONReporter with its name, description, choices, targets, and formats."""
        super().__init__(
            name='json',
            description='Outputs benchmark results to JSON files.',
            options_type=Options,
            sections={Section.NULL},
            targets={Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE},
            formats={Format.JSON},
            file_suffix='json',
            file_unique=True,
            file_append=False,
            choices=ChoicesConf([
                ChoiceConf(
                    flags=['--json'],
                    flag_type=FlagType.TARGET_LIST,
                    name='json',
                    description='statistical results to JSON (filesystem, console, callback, default=filesystem)',
                    sections=[Section.NULL],  # All sections are always included
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    output_format=Format.JSON,
                    options=Options(full_data=False)),
                ChoiceConf(
                    flags=['--json-data'],
                    flag_type=FlagType.TARGET_LIST,
                    name='json-data',
                    description=('statistical results + full data to JSON '
                                 '(filesystem, console, callback, default=filesystem)'),
                    sections=[Section.NULL],  # All sections are always included
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    output_format=Format.JSON,
                    options=Options(full_data=True)),
            ]),
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

        This method is called by the base class's `report()` method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid without a large amount of boilerplate code. The base class also handles lazy
        loading of the reporter classes, so subclasses can assume any required imports are available

        The run_report() method's main responsibilities are to select the appropriate output method
        (`render_by_case()` in this case) based on the provided arguments and to pass the
        actual rendering method to be used (the render() method in this case). The rendering method
        must conform with the `ReportRenderer` protocol.

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
        """
        self.render_by_case(
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
        """Convert the Case data for all sections to a JSON string.
        Machine info is included in the JSON output under the 'metadata' key.

        Args:
            case (Case): The Case instance holding the benchmarked code statistics.
            section (Section): The Section to render (ignored, all sections are included).
            options (JSONOptions): The JSONOptions instance specifying rendering options
                or None if not provided. (JSONOptions is a subclass of ReporterOptions.)

        Returns:
            str: The JSON string representation of the Case data.
        """
        # is_* checks provide deferred import validation to avoid circular imports
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"'case' argument must be a Case instance, got {type(case)}",
                tag=JSONReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                JSONReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(options, Options, 'options',
                                JSONReporterErrorTag.RENDER_INVALID_OPTIONS)

        full_data: bool = options.full_data if isinstance(options, Options) else False
        with StringIO() as jsonfile:
            case_dict = case.as_dict(full_data=full_data)
            try:
                case_dict['metadata'] = get_machine_info()
                json.dump(case_dict, jsonfile, indent=4)
                jsonfile.seek(0)
            except Exception as exc:
                raise SimpleBenchTypeError(
                    f'Error generating JSON output for case {case.title}: {exc}',
                    tag=JSONReporterErrorTag.JSON_OUTPUT_ERROR) from exc
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
