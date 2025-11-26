"""Configuration for a ScatterPlotReporter."""
from __future__ import annotations

from typing import Any, Iterable

from simplebench.enums import FlagType, Format, Section, Target
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.config import ReporterConfig


class ScatterPlotConfig(ReporterConfig):
    """Configuration for a ScatterPlotReporter.

    This class inherits from :class:`~.ReporterConfig` and provides a
    type-safe, discoverable interface for overriding the default settings
    of a :class:`~.ScatterPlotReporter`.
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
        """Initialize the ScatterPlotReporter configuration.

        Accepts keyword arguments to override any of the default configurations.
        All arguments are optional. If not provided, the default value for
        ScatterPlotReporter will be used.
        """
        defaults: dict[str, Any] = {
            'name': 'scatter-plot',
            'description': 'Outputs benchmark results as scatter plot graphs.',
            'sections': {Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            'targets': {Target.FILESYSTEM, Target.CALLBACK},
            'default_targets': {Target.FILESYSTEM},
            'formats': {Format.GRAPH},
            'file_suffix': 'svg',
            'file_unique': True,
            'file_append': False,
            'subdir': 'graphs',
            'choices': ChoicesConf([
                ChoiceConf(
                    flags=['--scatter-plot'], flag_type=FlagType.TARGET_LIST, name='scatter-plot',
                    description='Output scatter plot graphs of benchmark results',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.GRAPH),
                ChoiceConf(
                    flags=['--scatter-plot.ops'], flag_type=FlagType.TARGET_LIST, name='scatter-plot-ops',
                    description='Create scatter plots of operations per second results.',
                    sections=[Section.OPS],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.GRAPH),
                ChoiceConf(
                    flags=['--scatter-plot.timings'], flag_type=FlagType.TARGET_LIST, name='scatter-plot-timings',
                    description='Create scatter plots of timing results.',
                    sections=[Section.TIMING],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.GRAPH),
                ChoiceConf(
                    flags=['--scatter-plot.memory'], flag_type=FlagType.TARGET_LIST, name='scatter-plot-memory',
                    description='Create scatter plots of memory usage results.',
                    sections=[Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.GRAPH),
            ])
        }
        # Collect all provided overrides from the method signature, filtering out `None`s.
        overrides = {k: v for k, v in locals().items() if k in defaults and v is not None}

        final_config = defaults | overrides
        super().__init__(**final_config)
