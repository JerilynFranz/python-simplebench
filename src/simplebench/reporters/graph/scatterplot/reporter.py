# -*- coding: utf-8 -*-
"""Reporter for benchmark results using graphs."""
from __future__ import annotations
from argparse import Namespace
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from simplebench.enums import Section, Target, Format, FlagType

from simplebench.results import Results
from simplebench.si_units import si_scale_for_smallest
from simplebench.validators import validate_type

from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import ReporterOptions

from ..matplotlib import MatPlotLibReporter
from .exceptions import ScatterPlotReporterErrorTag
from .options import ScatterPlotOptions

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.session import Session

Options = ScatterPlotOptions


class ScatterPlotReporter(MatPlotLibReporter):
    """Class for outputting benchmark results as scatter plot graphs."""

    _HARDCODED_DEFAULT_OPTIONS = ScatterPlotOptions()
    """Built-in default ReporterOptions subclass instance for the reporter used if
    none is specified in a passed `Case`, `Choice`, or by `_DEFAULT_OPTIONS`. It
    forms the basis for the dynamic default options functionality provided by the
    `set_default_options()` and `get_default_options()` methods."""

    def __init__(self) -> None:
        super().__init__(
            name='graph',
            description='Outputs benchmark results as graphs.',
            options_type=Options,
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            targets={Target.FILESYSTEM, Target.CALLBACK},
            formats={Format.GRAPH},
            file_suffix='svg',
            file_unique=True,
            file_append=False,
            choices=[
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
            ]
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None) -> None:
        """Output the benchmark results as individual graphs for each case and section."""
        self.render_by_section(
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> bytes:
        """Render the scatter plot graph and return it as bytes.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            section (Section): The section of the results to plot. Must be Section.OPS or Section.TIMING.
            options (ReporterOptions): The options for rendering the scatter plot.

        Returns:
            bytes: The rendered graph as bytes.

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or values.
            SimpleBenchValueError: If the provided values are not valid.
        """
        case = validate_type(case, Case, 'case',
                             ScatterPlotReporterErrorTag.RENDER_INVALID_CASE)
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
