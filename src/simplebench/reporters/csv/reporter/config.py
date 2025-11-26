"""Configuration for a CSVReporter."""
from __future__ import annotations

from typing import Any, Iterable

from simplebench.enums import FlagType, Format, Section, Target
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.config import ReporterConfig


class CSVConfig(ReporterConfig):
    """Configuration for a :class:`~.CSVReporter`.

    This class inherits from :class:`~.ReporterConfig` and provides a
    type-safe, discoverable interface for overriding the default settings
    of a :class:`~.CSVReporter`.

    By default, the CSVReporter is configured to output benchmark results
    to CSV files in the filesystem, with options to also output to console
    and via callback. The default sections included are OPS, TIMING, MEMORY,
    and PEAK_MEMORY.

    Attributes
    ----------
    :ivar name: The name of the reporter. Default is 'csv'.
    :ivar description: A brief description of the reporter. Default is
        'Outputs benchmark results to CSV files.'.
    :ivar sections: The sections to include in the report. Default includes
        OPS, TIMING, MEMORY, and PEAK_MEMORY.
    :ivar targets: The output targets for the report. Default includes
        FILESYSTEM, CONSOLE, and CALLBACK.
    :ivar default_targets: The default output target if none is specified. Default is FILESYSTEM.
    :ivar formats: The output formats supported by the reporter. Default is CSV.
    :ivar file_suffix: The file suffix to use for output files. Default is 'csv'.
    :ivar file_unique: Whether to generate unique filenames for each report. Default is True.
    :ivar file_append: Whether to append to existing files. Default is False.
    :ivar subdir: The subdirectory to place output files in. Default is '' (current directory).
    :ivar choices: The choice configurations available for this reporter. Default includes
        several pre-defined choices for different sections of the report.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        sections: Iterable[Section] | None = None,
        targets: Iterable[Target] | None = None,
        default_targets: Iterable[Target] | None = None,
        formats: Iterable[Format] | None = None,
        choices: ChoicesConf | None = None,
        file_suffix: str | None = None,
        file_unique: bool | None = None,
        file_append: bool | None = None,
        subdir: str | None = None
    ) -> None:
        """Initialize the CSVReporter configuration.

        Accepts keyword arguments to override any of the default configurations.
        All arguments are optional. If not provided, the default value for
        CSVReporter will be used.
        """
        defaults: dict[str, Any] = {
            'name': 'csv',
            'description': 'Outputs benchmark results to CSV files.',
            'sections': {Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            'targets': {Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE},
            'default_targets': {Target.FILESYSTEM},
            'formats': {Format.CSV},
            'file_suffix': 'csv',
            'file_unique': True,
            'file_append': False,
            'subdir': '',
            'choices': ChoicesConf([
                ChoiceConf(
                    flags=['--csv'], flag_type=FlagType.TARGET_LIST, name='csv',
                    description='Output all results to CSV (filesystem, console, callback, default=filesystem)',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV),
                ChoiceConf(
                    flags=['--csv.ops'], flag_type=FlagType.TARGET_LIST, name='csv-ops',
                    description='Output ops/second results to CSV (filesystem, console, callback, default=filesystem)',
                    sections=[Section.OPS],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV),
                ChoiceConf(
                    flags=['--csv.timing'], flag_type=FlagType.TARGET_LIST, name='csv-timing',
                    description='Output timing results to CSV (filesystem, console, callback, default=filesystem)',
                    sections=[Section.TIMING],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV),
                ChoiceConf(
                    flags=['--csv.memory'], flag_type=FlagType.TARGET_LIST, name='csv-memory',
                    description='Output memory results to CSV (filesystem, console, callback, default=filesystem)',
                    sections=[Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CONSOLE, Target.CALLBACK],
                    output_format=Format.CSV),
            ])
        }
        # Collect all provided overrides from the method signature, filtering out `None`s.
        overrides = {k: v for k, v in locals().items() if k in defaults and v is not None}

        final_config = defaults | overrides
        super().__init__(**final_config)
