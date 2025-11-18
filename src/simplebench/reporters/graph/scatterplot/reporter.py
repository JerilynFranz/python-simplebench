# -*- coding: utf-8 -*-
"""Reporter for benchmark results using graphs."""
from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from simplebench.enums import FlagType, Format, Section, Target
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter import ReporterOptions
from simplebench.results import Results
from simplebench.si_units import si_scale_for_smallest
from simplebench.type_proxies import is_case
from simplebench.validators import validate_type

from ..matplotlib import MatPlotLibReporter
from .exceptions import ScatterPlotReporterErrorTag
from .options import ScatterPlotOptions

Options: TypeAlias = ScatterPlotOptions

if TYPE_CHECKING:
    from simplebench.case import Case


class ScatterPlotReporter(MatPlotLibReporter):
    """Class for outputting benchmark results as scatter plot graphs.

    This reporter generates scatter plot visualizations for various result sections,
    saving them to the filesystem or passing them to a callback function. It provides
    a visual way to compare the performance of different benchmark variations.

    **Defined command-line flags:**

    * ``--scatter-plot: {filesystem, callback}`` (default=filesystem)
    * ``--scatter-plot.ops: ...``
    * ``--scatter-plot.timings: ...``
    * ``--scatter-plot.memory: ...``

    **Example usage:**

    .. code-block:: none

        program.py --scatter-plot               # Outputs graphs to the filesystem.
        program.py --scatter-plot.ops filesystem  # Outputs only ops graphs to the filesystem.

    """

    _OPTIONS_TYPE: ClassVar[type[ScatterPlotOptions]] = ScatterPlotOptions  # pylint: disable=line-too-long  # type: ignore[reportIncompatibleVariableOveride]  # noqa: E501
    """:ivar: The specific :class:`~.ReporterOptions` subclass associated with this reporter.
    :vartype: ~typing.ClassVar[type[~.ScatterPlotOptions]]
    """
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = ScatterPlotOptions.DEFAULT_KWARGS
    """:ivar: The default keyword arguments for the :class:`~.ScatterPlotOptions` subclass.
    :vartype: ~typing.ClassVar[dict[str, ~typing.Any]]
    """

    def __init__(self) -> None:
        """Initialize the ScatterPlotReporter.

        .. note::

            The exception documentation below refers to validation of subclass configuration
            class variables ``_OPTIONS_TYPE`` and ``_OPTIONS_KWARGS``. These must be correctly
            defined in any subclass of :class:`ScatterPlotReporter` to ensure proper
            functionality.

            In simple use, these exceptions should never be raised, as
            :class:`ScatterPlotReporter` provides valid implementations. They are documented
            here for completeness.

        :raises ~simplebench.exceptions.SimpleBenchTypeError: If the subclass configuration
            types are invalid.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If the subclass configuration
            values are invalid.
        """
        super().__init__(
            name='scatter-plot',
            description='Outputs benchmark results as scatter plot graphs.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.FILESYSTEM, Target.CALLBACK},
            formats={Format.GRAPH},
            file_suffix='svg',
            file_unique=True,
            file_append=False,
            choices=ChoicesConf([
                ChoiceConf(
                    flags=['--scatter-plot'],
                    flag_type=FlagType.TARGET_LIST,
                    name='scatter-plot',
                    description='Output scatter plot graphs of benchmark results',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    default_targets=[Target.FILESYSTEM],
                    output_format=Format.GRAPH),
                ChoiceConf(
                    flags=['--scatter-plot.ops'],
                    flag_type=FlagType.TARGET_LIST,
                    name='scatter-plot-ops',
                    description='Create scatter plots of operations per second results.',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.GRAPH),
                ChoiceConf(
                    flags=['--scatter-plot.timings'],
                    flag_type=FlagType.TARGET_LIST,
                    name='scatter-plot-timings',
                    description='Create scatter plots of timing results.',
                    sections=[Section.TIMING],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.GRAPH),
                ChoiceConf(
                    flags=['--scatter-plot.memory'],
                    flag_type=FlagType.TARGET_LIST,
                    name='scatter-plot-memory',
                    description='Create scatter plots of memory usage results.',
                    sections=[Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK],
                    output_format=Format.GRAPH),
            ])
        )

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> bytes:
        """Render the scatter plot graph and return it as bytes.

        :param case: The :class:`~simplebench.case.Case` instance representing the
            benchmarked code.
        :param section: The section of the results to plot.
        :param options: The options for rendering the scatter plot.
        :return: The rendered graph as bytes. The format is determined by the options.
            The defaults are defined in :class:`~.ScatterPlotOptions`.
        :raises ~simplebench.exceptions.SimpleBenchTypeError: If the provided arguments are not
            of the expected types or values.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If the provided values are not
            valid.
        """
        # is_* checks provide deferred import validation to avoid circular imports
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"'case' argument must be a Case instance, got {type(case)}",
                tag=ScatterPlotReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                ScatterPlotReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(
                options, Options, 'options',
                ScatterPlotReporterErrorTag.RENDER_INVALID_OPTIONS)

        base_unit = self.get_base_unit_for_section(section=section)
        results: list[Results] = case.results

        all_numbers = self.get_all_stats_values(results=results, section=section)
        common_unit, common_scale = si_scale_for_smallest(numbers=all_numbers, base_unit=base_unit)
        target_name = f'{section.value} ({base_unit})'

        with BytesIO() as graphfile:
            with mpl.rc_context():
                plot_data = []
                x_axis_legend = '\n'.join([
                    f"{case.variation_cols.get(k, k)}" for k in case.variation_cols.keys()])
                for result in results:
                    target_stats = result.results_section(section)
                    variation_label = '\n'.join([f"{v}" for v in result.variation_marks.values()])
                    plot_data.append({
                        x_axis_legend: variation_label,
                        target_name: target_stats.mean * common_scale,
                    })

                # See https://matplotlib.org/stable/users/explain/customizing.html#the-matplotlibrc-file
                benchmarking_theme = options.theme
                mpl.rcParams.update(benchmarking_theme)
                df = pd.DataFrame(plot_data)

                # Create the plot
                with plt.style.context(options.style):
                    g = sns.relplot(data=df, y=target_name, x=x_axis_legend)
                    g.figure.suptitle(case.title, fontsize='large', weight='bold')
                    g.figure.subplots_adjust(top=.9)
                    g.figure.set_dpi(options.dpi)  # dots per inch
                    g.figure.set_figheight(options.height / options.dpi)  # inches
                    g.figure.set_figwidth(options.width / options.dpi)  # inches
                    g.tick_params("x", rotation=options.x_labels_rotation)
                    # format the labels with f-strings
                    for ax in g.axes.flat:
                        ax.yaxis.set_major_formatter('{x}' + f' {common_unit}')
                    if options.y_starts_at_zero:
                        _, top = plt.ylim()
                        plt.ylim(bottom=0, top=top * 1.10)  # Add 10% headroom
                    plt.savefig(graphfile, format=options.image_type)
                    plt.close()  # Close the figure to free memory
                    graphfile.flush()
            return graphfile.getvalue()
