# -*- coding: utf-8 -*-
"""Classes for reporting benchmark results."""
import csv
from enum import Enum
from pathlib import Path
from typing import Literal, Sequence

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from rich.table import Table
import seaborn as sns

from .case import Case
from .constants import (BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE)
from .exceptions import ErrorTag, SimpleBenchTypeError
from .results import Results
from .session import Session
from .utils import si_scale_for_smallest, sigfigs


class Reporters:
    """Container for reporters."""


class RichTableReporter:
    """Reporter for displaying benchmark results as a rich table on the console
    """
    def __init__(self, session: Session, case: Case, sections: Sequence[str]) -> None:
        if not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "Expected a Session instance",
                ErrorTag.RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG)
        self.session: Session = session

        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.RICH_TABLE_REPORTER_INIT_INVALID_CASE_ARG)
        self.case: Case = case

        if not isinstance(sections, Sequence):
            raise SimpleBenchTypeError(
                "Expected a Sequence of Section instances for sections arg",
                ErrorTag.RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG)
        for entry in sections:
            if not isinstance(entry, Sections):
                raise SimpleBenchTypeError(
                    f'Expected section items to be Section instances - cannot be a {type(entry)}',
                    ErrorTag.RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG)

    def run_reports(self) -> None:
        """Run all reports for the case."""
        case: Case = self.case
        if not case.results:
            return
        if self.session.verbosity in (Verbosity.NORMAL, Verbosity.VERBOSE):
            if case.ops_per_second_enabled:
                self.ops_results_as_rich_table()
            if case.timing_enabled:
                self.timing_results_as_rich_table()

    def results_as_rich_table(self,
                              base_unit: str,
                              target: Literal['ops_per_second', 'per_round_timings']) -> None:
        """Prints the benchmark results in a rich table format if available.
        """
        case: Case = self.case
        results: list[Results] = case.results
        mean_unit, mean_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).mean for result in results],
            base_unit=base_unit)
        median_unit, median_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).median for result in results],
            base_unit=base_unit)
        min_unit, min_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).minimum for result in results],
            base_unit=base_unit)
        max_unit, max_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).maximum for result in results],
            base_unit=base_unit)
        p5_unit, p5_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).percentiles[5] for result in results],
            base_unit=base_unit)
        p95_unit, p95_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).percentiles[95] for result in results],
            base_unit=base_unit)
        stddev_unit, stddev_scale = si_scale_for_smallest(
            numbers=[getattr(result, target).standard_deviation for result in results],
            base_unit=base_unit)

        table = Table(title=(case.title + '\n\n' + case.description),
                      show_header=True,
                      title_style='bold green1',
                      header_style='bold magenta')
        table.add_column('N', justify='center')
        table.add_column('Iterations', justify='center')
        table.add_column('Elapsed Seconds', justify='center', max_width=7)
        table.add_column(f'mean {mean_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'median {median_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'min {min_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'max {max_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'5th {p5_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'95th {p95_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'std dev {stddev_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column('rsd%', justify='center', vertical='bottom', overflow='fold')
        for value in case.variation_cols.values():
            table.add_column(value, justify='center', vertical='bottom', overflow='fold')
        for result in results:
            stats_target = getattr(result, target)
            row: list[str] = [
                f'{result.n:>6d}',
                f'{len(result.iterations):>6d}',
                f'{result.total_elapsed * DEFAULT_INTERVAL_SCALE:>4.2f}',
                f'{sigfigs(stats_target.mean * mean_scale):>8.2f}',
                f'{sigfigs(stats_target.median * median_scale):>8.2f}',
                f'{sigfigs(stats_target.minimum * min_scale):>8.2f}',
                f'{sigfigs(stats_target.maximum * max_scale):>8.2f}',
                f'{sigfigs(stats_target.percentiles[5] * p5_scale):>8.2f}',
                f'{sigfigs(stats_target.percentiles[95] * p95_scale):>8.2f}',
                f'{sigfigs(stats_target.standard_deviation * stddev_scale):>8.2f}',
                f'{sigfigs(stats_target.relative_standard_deviation):>5.2f}%'
            ]
            for value in result.variation_marks.values():
                row.append(f'{value!s}')
            table.add_row(*row)
        self.session.console.print(table)

    def ops_results_as_rich_table(self) -> None:
        """Prints the Operations Per Second benchmark results in a rich table format if available.
        """
        return self.results_as_rich_table(
            base_unit=BASE_OPS_PER_INTERVAL_UNIT,
            target='ops_per_second'
        )

    def timing_results_as_rich_table(self) -> None:
        """Prints the Timing benchmark results in a rich table format if available.
        """
        return self.results_as_rich_table(
            base_unit=BASE_INTERVAL_UNIT,
            target='per_round_timings'
        )


class CSVReporter:
    """Class for outputting benchmark results to CSV files."""

    def __init__(self, session: Session, case: Case) -> None:
        if not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "Expected a Session instance",
                ErrorTag.CSV_REPORTER_INIT_INVALID_SESSION_ARG)
        self.session: Session = session

        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.CSV_REPORTER_INIT_INVALID_CASE_ARG)
        self.case: Case = case

    def output_results_to_csv(self,
                              filepath: Path,
                              base_unit: str,
                              target: Literal['ops_per_second', 'per_round_timings']) -> None:
        """Output the benchmark results to a file as tagged CSV if available.

        Args:
            filepath: The path to the CSV file to write.
            results: The benchmark results to write.
            target: The target metric to write (either 'ops_per_second' or 'per_round_timings').
        """
        case = self.case
        results = case.results
        if not results:
            return

        all_numbers: list[float] = []
        all_numbers.extend([getattr(result, target).mean for result in results])
        all_numbers.extend([getattr(result, target).median for result in results])
        all_numbers.extend([getattr(result, target).minimum for result in results])
        all_numbers.extend([getattr(result, target).maximum for result in results])
        all_numbers.extend([getattr(result, target).percentiles[5] for result in results])
        all_numbers.extend([getattr(result, target).percentiles[95] for result in results])
        all_numbers.extend([getattr(result, target).standard_deviation for result in results])
        common_unit, common_scale = si_scale_for_smallest(numbers=all_numbers, base_unit=base_unit)

        with filepath.open(mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f'# {case.title}'])
            writer.writerow([f'# {case.description}'])
            header: list[str] = [
                'N',
                'Iterations',
                'Elapsed Seconds',
                f'mean ({common_unit})',
                f'median ({common_unit})',
                f'min ({common_unit})',
                f'max ({common_unit})',
                f'5th ({common_unit})',
                f'95th ({common_unit})',
                f'std dev ({common_unit})',
                'rsd (%)'
            ]
            for value in case.variation_cols.values():
                header.append(value)
            writer.writerow(header)
            for result in results:
                stats_target = getattr(result, target)
                row: list[str | float | int] = [
                    result.n,
                    len(result.iterations),
                    result.total_elapsed * DEFAULT_INTERVAL_SCALE,
                    sigfigs(stats_target.mean * common_scale),
                    sigfigs(stats_target.median * common_scale),
                    sigfigs(stats_target.minimum * common_scale),
                    sigfigs(stats_target.maximum * common_scale),
                    sigfigs(stats_target.percentiles[5] * common_scale),
                    sigfigs(stats_target.percentiles[95] * common_scale),
                    sigfigs(stats_target.standard_deviation * common_scale),
                    sigfigs(stats_target.relative_standard_deviation)
                ]
                for value in result.variation_marks.values():
                    row.append(value)
                writer.writerow(row)

        return

    def output_ops_results_to_csv(self, filepath: Path) -> None:
        """Output the benchmark results to a file as tagged CSV if available.
        """
        return self.output_results_to_csv(filepath=filepath,
                                          base_unit=BASE_OPS_PER_INTERVAL_UNIT,
                                          target='ops_per_second')

    def output_timing_results_to_csv(self, filepath: Path) -> None:
        """Outputs the timing benchmark results to file as tagged CSV.
        """
        return self.output_results_to_csv(filepath=filepath,
                                          base_unit=BASE_INTERVAL_UNIT,
                                          target='per_round_timings')


class GraphReporter:
    """Class for outputting benchmark results as graphs."""
    def __init__(self, session: Session, case: Case) -> None:
        if not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "Expected a Session instance",
                ErrorTag.GRAPH_REPORTER_INIT_INVALID_SESSION_ARG)
        self.session: Session = session

        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.GRAPH_REPORTER_INIT_INVALID_CASE_ARG)
        self.case: Case = case

    def plot_results(self,
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
        case: Case = self.case
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

    def plot_ops_results(self, filepath: Path) -> None:
        """Plots the operations per second results graph.

        Args:
            filepath (Path): The path to the output file.
        """
        return self.plot_results(filepath=filepath,
                                 target='ops_per_second',
                                 base_unit=BASE_OPS_PER_INTERVAL_UNIT,
                                 target_name='Operations per Second')

    def plot_timing_results(self, filepath: Path) -> None:
        """Plots the timing results graph.

        Args:
            filepath (Path): The path to the output file.
        """
        return self.plot_results(filepath=filepath,
                                 target='per_round_timings',
                                 base_unit=BASE_INTERVAL_UNIT,
                                 target_name='Time Per Round')
