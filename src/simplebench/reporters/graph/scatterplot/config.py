"""Configuration for a ScatterPlotReporter."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from simplebench.enums import FlagType, Format, Target
from simplebench.metrics import (
    MetricCategory,
    Metrics,
    MetricsCollection,
    MetricsSelection,
    filtered_metrics,
    metrics_registry,
)
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter._config import ReporterConfig


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
        metrics: MetricsSelection | None = None,
        targets: Iterable[Target] | None = None,
        default_targets: Iterable[Target] | None = None,
        formats: Iterable[Format] | None = None,
        choices: ChoicesConf | None = None,
        file_suffix: str | None = None,
        file_unique: bool | None = None,
        file_append: bool | None = None,
        subdir: str | None = None,
    ) -> None:
        """Initialize the ScatterPlotReporter configuration.

        Accepts keyword arguments to override any of the default configurations.
        All arguments are optional. If not provided, the default value for
        ScatterPlotReporter will be used.
        """
        all_processable_metrics: Metrics = filtered_metrics(metric_categories=MetricCategory.STATISTICAL)
        all_processable_metrics += metrics_registry['STD_TOTAL_ELAPSED_TIME']
        allowed_targets = {Target.FILESYSTEM, Target.CALLBACK}
        defaults: dict[str, Any] = {
            'name': 'scatter-plot',
            'description': 'Outputs benchmark results as scatter plot graphs.',
            'metrics': MetricsCollection(all_processable_metrics),
            'targets': allowed_targets,
            'default_targets': {Target.FILESYSTEM},
            'formats': {Format.GRAPH},
            'file_suffix': 'svg',
            'file_unique': True,
            'file_append': False,
            'subdir': 'graphs',
            'choices': ChoicesConf(
                [
                    ChoiceConf(
                        flags=['--scatter-plot'],
                        flag_type=FlagType.TARGET_LIST,
                        name='scatter-plot',
                        description='Output scatter plot graphs of all available benchmark results',
                        metrics=MetricsCollection(all_processable_metrics),
                        targets=allowed_targets,
                        output_format=Format.GRAPH,
                    ),
                    ChoiceConf(
                        flags=['--scatter-plot.ops'],
                        flag_type=FlagType.TARGET_LIST,
                        name='scatter-plot-ops',
                        description='Create scatter plots of operations per second results.',
                        metrics=MetricsCollection(
                            [metrics_registry['STD_OPS_STATS'], metrics_registry['STD_TOTAL_ELAPSED_TIME']]
                        ),
                        targets=allowed_targets,
                        output_format=Format.GRAPH,
                    ),
                    ChoiceConf(
                        flags=['--scatter-plot.timings'],
                        flag_type=FlagType.TARGET_LIST,
                        name='scatter-plot-timings',
                        description='Create scatter plots of timing results.',
                        metrics=MetricsCollection(
                            [metrics_registry['STD_TIMING_STATS'], metrics_registry['STD_TOTAL_ELAPSED_TIME']]
                        ),
                        targets=allowed_targets,
                        output_format=Format.GRAPH,
                    ),
                    ChoiceConf(
                        flags=['--scatter-plot.memory'],
                        flag_type=FlagType.TARGET_LIST,
                        name='scatter-plot-memory',
                        description='Create scatter plots of memory usage results.',
                        metrics=MetricsCollection([
                                metrics_registry['STD_MEMORY_STATS'],
                                metrics_registry['STD_PEAK_MEMORY_STATS'],
                                metrics_registry['STD_TOTAL_ELAPSED_TIME'],
                            ]
                        ),
                        targets=allowed_targets,
                        output_format=Format.GRAPH,
                    ),
                ]
            ),
        }
        # Collect all provided overrides from the method signature, filtering out `None`s.
        overrides = {k: v for k, v in locals().items() if k in defaults and v is not None}

        final_config = defaults | overrides
        super().__init__(**final_config)
