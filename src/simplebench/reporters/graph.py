# -*- coding: utf-8 -*-
"""Reporter for benchmark results using graphs."""
from __future__ import annotations
from pathlib import Path
from typing import Literal

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ..constants import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT
from ..exceptions import SimpleBenchTypeError, ErrorTag
from ..session import Session
from ..case import Case
from ..results import Results
from ..utils import si_scale_for_smallest
from .choices import Choice, Choices, Section, Format, Target
from .interfaces import Reporter


class GraphReporter(Reporter):
    """Class for outputting benchmark results as graphs."""
    def __init__(self) -> None:
        self._choices: Choices = Choices()
        self._choices.add(
            Choice(
                reporter=self,
                runner=self.plot_ops_results,
                flags=['--graph-scatter-ops'],
                name='graph-scatter-ops',
                description='Save a scatter graph of operations per second results to a file',
                sections=[Section.OPS],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                runner=self.plot_timing_results,
                flags=['--graph-scatter-timings'],
                name='graph-scatter-timings',
                description='Save a scatter graph of timing results to a file',
                sections=[Section.TIMING],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT])
        )

    @property
    def choices(self) -> Choices:
        """Return the Choices instance for the reporter, including sections,
        output targets, and formats.
        """
        return self._choices

    @property
    def name(self) -> str:
        """Return the unique identifying name of the reporter."""
        return 'graph'

    @property
    def description(self) -> str:
        """Return a brief description of the reporter."""
        return 'Outputs benchmark results as graphs.'

    def plot_results(self,
                     session: Session,
                     case: Case,
                     filepath: Path,
                     target: Literal['ops_per_second', 'per_round_timings'],
                     base_unit: str = '',
                     target_name: str = ''
                     ) -> None:
        """Generates and saves a bar plot of the ops/sec results.

        Args:
            filepath (Path): The path to the output file.
            target (Literal['ops_per_second', 'per_round_timings']): The target metric to plot.
            base_unit (str): The base unit for the y-axis.
            target_name (str): The name of the target metric.
            scale (float): The scale factor for the y-axis.
        """
        if not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "Expected a Session instance",
                ErrorTag.GRAPH_REPORTER_PLOT_RESULTS_INVALID_SESSION_ARG)

        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.GRAPH_REPORTER_PLOT_RESULTS_INVALID_CASE_ARG)

        if not isinstance(filepath, Path):
            raise SimpleBenchTypeError(
                "Expected a Path instance",
                ErrorTag.GRAPH_REPORTER_PLOT_RESULTS_INVALID_FILEPATH_ARG)

        if not isinstance(target, str) or target not in ['ops_per_second', 'per_round_timings']:
            raise SimpleBenchTypeError(
                "target must be either 'ops_per_second' or 'per_round_timings'",
                ErrorTag.GRAPH_REPORTER_PLOT_RESULTS_INVALID_TARGET_ARG)

        results: list[Results] = case.results
        if not results:
            return

        all_numbers: list[float] = []
        all_numbers.extend([getattr(result, target).mean for result in results])
        common_unit, common_scale = si_scale_for_smallest(numbers=all_numbers, base_unit=base_unit)
        target_name = f'{target_name} ({base_unit})'

        # Prepare data for plotting
        plot_data = []
        x_axis_legend = '\n'.join([f"{case.variation_cols.get(k, k)}"
                                   for k in case.variation_cols.keys()])
        for result in results:
            target_stats = getattr(result, target)
            variation_label = '\n'.join([f"{v}" for v in result.variation_marks.values()])
            plot_data.append({
                x_axis_legend: variation_label,
                target_name: target_stats.mean * common_scale,
            })

        if not plot_data:
            return

        # See https://matplotlib.org/stable/users/explain/customizing.html#the-matplotlibrc-file
        benchmarking_theme = {
            'axes.grid': True,
            'grid.linestyle': '-',
            'grid.color': '#444444',
            'legend.framealpha': 1,
            'legend.shadow': True,
            'legend.fontsize': 14,
            'legend.title_fontsize': 16,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'axes.labelsize': 16,
            'axes.titlesize': 20,
            'figure.dpi': 100}
        mpl.rcParams.update(benchmarking_theme)
        df = pd.DataFrame(plot_data)

        # Create the plot
        plt.style.use(case.graph_style)
        g = sns.relplot(data=df, y=target_name, x=x_axis_legend)
        g.figure.suptitle(case.title, fontsize='large', weight='bold')
        g.figure.subplots_adjust(top=.9)
        g.figure.set_dpi(160)
        g.figure.set_figheight(10)
        g.figure.set_figwidth(10 * case.graph_aspect_ratio)
        g.tick_params("x", rotation=case.graph_x_labels_rotation)
        # format the labels with f-strings
        for ax in g.axes.flat:
            ax.yaxis.set_major_formatter('{x}' + f' {common_unit}')
        if case.graph_y_starts_at_zero:
            _, top = plt.ylim()
            plt.ylim(bottom=0, top=top * 1.10)  # Add 10% headroom
        plt.savefig(filepath)
        plt.close()  # Close the figure to free memory

    def plot_ops_results(self, session: Session, case: Case, path: Path) -> None:
        """Plots the operations per second results graph.

        Args:
            path (Path): The path to the output directory.
        """
        return self.plot_results(
            session=session,
            case=case,
            filepath=path.joinpath('graphs', 'ops_per_second.png'),
            target='ops_per_second',
            base_unit=BASE_OPS_PER_INTERVAL_UNIT,
            target_name='Operations per Second')

    def plot_timing_results(self, session: Session, case: Case, path: Path) -> None:
        """Plots the timing results graph.

        Args:
            filepath (Path): The path to the output directory.
        """
        return self.plot_results(
            session=session,
            case=case,
            filepath=path.joinpath('graphs', 'per_round_timings.png'),
            target='per_round_timings',
            base_unit=BASE_INTERVAL_UNIT,
            target_name='Time Per Round')
