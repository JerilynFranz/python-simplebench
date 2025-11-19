"""Configuration for a JSONReporter."""
from __future__ import annotations

from typing import Any, Iterable

from simplebench.enums import FlagType, Format, Section, Target
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.json.reporter.options import JSONOptions
from simplebench.reporters.reporter.config import ReporterConfig


class JSONConfig(ReporterConfig):
    """Configuration for a JSONReporter.

    This class inherits from :class:`~.ReporterConfig` and provides a
    type-safe, discoverable interface for overriding the default settings
    of a :class:`~.JSONReporter`.
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
        """Initialize the JSONReporter configuration.

        Accepts keyword arguments to override any of the default configurations.
        All arguments are optional. If not provided, the default value for
        JSONReporter will be used.
        """
        init_sections = {Section.NULL}  # JSON reporter only supports NULL section
        init_targets = {Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE}
        defaults: dict[str, Any] = {
            'name': 'json',
            'description': 'Outputs benchmark results to JSON files.',
            'sections': init_sections,
            'targets': init_targets,
            'default_targets': {Target.FILESYSTEM},
            'formats': {Format.JSON},
            'file_suffix': 'json',
            'file_unique': True,
            'file_append': False,
            'subdir': '',
            'choices': ChoicesConf([
                ChoiceConf(
                    flags=['--json'], flag_type=FlagType.TARGET_LIST, name='json',
                    description='statistical results to JSON (filesystem, console, callback, default=filesystem)',
                    sections=init_sections,
                    targets=init_targets,
                    output_format=Format.JSON,
                    options=JSONOptions(full_data=False)),
                ChoiceConf(
                    flags=['--json-data'], flag_type=FlagType.TARGET_LIST, name='json-data',
                    description=(
                        'statistical results + full data to JSON (filesystem, console, callback, default=filesystem)'),
                    sections=init_sections,
                    targets=init_targets,
                    output_format=Format.JSON,
                    options=JSONOptions(full_data=True)),
            ])
        }
        # Collect all provided overrides from the method signature, filtering out `None`s.
        overrides = {k: v for k, v in locals().items() if k in defaults and v is not None}

        final_config = defaults | overrides
        super().__init__(**final_config)
