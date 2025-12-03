"""Configuration for a PytestReporter."""
from __future__ import annotations

from typing import Any

from simplebench.enums import FlagType, Format, Section, Target
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.config import ReporterConfig


class PytestConfig(ReporterConfig):
    """Configuration for a PytestReporter.

    This class inherits from :class:`~.ReporterConfig` and provides a
    type-safe, discoverable interface for overriding the default settings
    of a :class:`~.PytestReporter`.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        sections: set[Section] | None = None,
        targets: set[Target] | None = None,
        default_targets: set[Target] | None = None,
        formats: set[Format] | None = None,
        choices: ChoicesConf | None = None,
        file_suffix: str | None = None,
        file_unique: bool | None = None,
        file_append: bool | None = None,
        subdir: str | None = None
    ) -> None:
        """Initialize the PytestReporter configuration.

        Accepts keyword arguments to override any of the default configurations.
        All arguments are optional. If not provided, the default value for
        PytestReporter will be used.

        .. note::

            The parameters of this constructor correspond directly to the
            parameters of the base :class:`~.ReporterConfig` class. This design
            allows users to easily discover and override any configuration option
            available for the PytestReporter while maintaining type safety
            and discoverability through IDEs and documentation tools.

            To prevent future breakage, avoid using the 'rc_', or 'rich_table_' prefixes
            for any new parameters in subclasses as these are reserved for use by SimpleBench.

        **Default Values**:

        *   **name**: ``'pytest'``
        *   **description**: ``'Displays benchmark results as a rich text table on the console.'``
        *   **sections**: ``{Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY}``
        *   **targets**: ``{Target.CUSTOM}``
        *   **default_targets**: ``{Target.CUSTOM}``
        *   **formats**: ``{Format.RICH_TEXT}``
        *   **choices**: A ``ChoicesConf`` with predefined ``ChoiceConf`` objects for rich table reporting.
        *   **file_suffix**: ``'txt'``
        *   **file_unique**: ``False``
        *   **file_append**: ``True``
        *   **subdir**: ``'rich'``

        :param name: The name of the reporter.
        :param description: A brief description of the reporter.
        :param sections: The sections to include in the report.
        :param targets: The output targets for the report.
        :param default_targets: The default output targets if none are specified.
        :param formats: The output formats for the report.
        :param choices: The choice configurations for the reporter.
        :param file_suffix: The file suffix to use for filesystem outputs.
        :param file_unique: Whether to use unique filenames for outputs.
        :param file_append: Whether to append to existing files.
        :param subdir: The subdirectory to use for filesystem outputs.
        :raises SimpleBenchTypeError: If any provided argument has an invalid type.
        :raises SimpleBenchValueError: If any provided argument has an invalid value or combination of values.
        """
        init_sections = {Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY}
        init_targets = {Target.CUSTOM}

        defaults: dict[str, Any] = {
            'name': 'pytest',
            'description': 'Displays benchmark results as a rich text table on the console.',
            'sections': init_sections,
            'targets': init_targets,
            'default_targets': {Target.CUSTOM},
            'formats': {Format.RICH_TEXT},
            'file_suffix': 'txt',
            'file_unique': False,
            'file_append': True,
            'subdir': 'rich',
            'choices': ChoicesConf([
                ChoiceConf(
                    flags=['--pytest'], flag_type=FlagType.TARGET_LIST, name='pytest',
                    description='All results as rich text tables',
                    sections=init_sections,
                    targets=init_targets,
                    output_format=Format.RICH_TEXT),
                ChoiceConf(
                    flags=['--pytest.ops'], flag_type=FlagType.TARGET_LIST, name='pytest-ops',
                    description=(
                        'Ops/second results as rich text tables'),
                    sections={Section.OPS},
                    targets=init_targets,
                    output_format=Format.RICH_TEXT),
                ChoiceConf(
                    flags=['--pytest.timing'], flag_type=FlagType.TARGET_LIST, name='pytest-timing',
                    description='Timing results as rich text tables',
                    sections={Section.TIMING},
                    targets=init_targets,
                    output_format=Format.RICH_TEXT),
                ChoiceConf(
                    flags=['--pytest.memory'], flag_type=FlagType.TARGET_LIST, name='pytest-memory',
                    description='Memory results as rich text tables',
                    sections={Section.MEMORY, Section.PEAK_MEMORY},
                    targets=init_targets,
                    output_format=Format.RICH_TEXT),
            ])
        }
        # Collect all provided overrides from the method signature, filtering out `None`s.
        overrides = {k: v for k, v in locals().items() if k in defaults and v is not None}

        final_config = defaults | overrides
        super().__init__(**final_config)
