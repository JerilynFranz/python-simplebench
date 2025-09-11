# -*- coding: utf-8 -*-
"""Reporter for benchmark results using graphs."""
from __future__ import annotations
from argparse import ArgumentParser
from io import BytesIO, BufferedWriter
from pathlib import Path
from typing import Optional, Callable, Any, TYPE_CHECKING

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ..case import Case
from ..constants import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT
from ..exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from ..results import Results
from ..utils import sanitize_filename, si_scale_for_smallest
from .choices import Choice, Choices, Section, Format, Target
from .interfaces import Reporter

if TYPE_CHECKING:
    from ..session import Session

_lazy_classes_loaded: bool = False


def _lazy_load_classes() -> None:
    """Lazily load any classes or modules that cannot be loaded during initial setup."""
    global _lazy_classes_loaded  # pylint: disable=global-statement
    global Session  # pylint: disable=global-statement
    if not _lazy_classes_loaded:
        from ..session import Session  # pylint: disable=import-outside-toplevel
        _lazy_classes_loaded = True


class GraphReporter(Reporter):
    """Class for outputting benchmark results as graphs."""
    def __init__(self) -> None:
        self._choices: Choices = Choices()
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--graph-scatter-file'],
                name='graph-scatter-file',
                description='Save a scatter graph of operations per second results to a file',
                sections=[Section.OPS, Section.TIMING],
                targets=[Target.FILESYSTEM],
                formats=[Format.GRAPH]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--graph-scatter-ops-file'],
                name='graph-scatter-ops-file',
                description='Save a scatter graph of operations per second results to a file',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM],
                formats=[Format.GRAPH]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--graph-scatter-timings-file'],
                name='graph-scatter-timings-file',
                description='Save a scatter graph of timing results to a file',
                sections=[Section.TIMING],
                targets=[Target.FILESYSTEM],
                formats=[Format.GRAPH])
        )
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--graph-scatter-callback'],
                name='graph-scatter-callback',
                description='Return scatter graph of operations per second results to a callback function',
                sections=[Section.OPS, Section.TIMING],
                targets=[Target.CALLBACK],
                formats=[Format.GRAPH]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--graph-scatter-ops-callback'],
                name='graph-scatter-ops-callback',
                description='Return scatter graph of operations per second results to a callback function',
                sections=[Section.OPS],
                targets=[Target.CALLBACK],
                formats=[Format.GRAPH]))
        self._choices.add(
            Choice(
                reporter=self,
                flags=['--graph-scatter-timings-callback'],
                name='graph-scatter-timings-callback',
                description='Return scatter graph of timing results to a callback function',
                sections=[Section.TIMING],
                targets=[Target.CALLBACK],
                formats=[Format.GRAPH])
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

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        for choice in self.choices.values():
            for flag in choice.flags:
                parser.add_argument(flag, action='store_true', help=choice.description)

    def report(self,
               case: Case,
               choice: Choice,
               path: Optional[Path] = None,
               session: Optional[Session] = None,
               callback: Optional[Callable[[Case, Section, Format, Any], None]] = None) -> None:
        """Output the benchmark results a graph to a file and/or a callback function.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the graph file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[Callable[[Case, Section, Format, Any], None]]):
                A callback function for additional processing of the report.
                The function should accept four arguments:
                    - the Case instance
                    - the Section being reported
                    - the Format of the report
                    - the graph data as bytes
                Leave as None if no callback is needed.

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types. Also raised if
                required arguments are missing. Also raised if the callback is not callable when
                provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
                target is specified.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        _lazy_load_classes()
        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.GRAPH_REPORTER_REPORT_INVALID_CASE_ARG)
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                ErrorTag.GRAPH_REPORTER_REPORT_INVALID_CHOICE_ARG)
        for section in choice.sections:
            if section not in (Section.OPS, Section.TIMING):
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    ErrorTag.GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in (Target.FILESYSTEM, Target.CALLBACK):
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    ErrorTag.GRAPH_REPORTER_REPORT_UNSUPPORTED_TARGET)
        if Target.CALLBACK in choice.targets:
            if callback is not None and not callable(callback):
                raise SimpleBenchTypeError(
                    "Callback function must be callable if provided",
                    ErrorTag.GRAPH_REPORTER_REPORT_INVALID_CALLBACK_ARG)
        if Target.FILESYSTEM in choice.targets and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "Path must be a pathlib.Path instance when using FILESYSTEM target",
                ErrorTag.GRAPH_REPORTER_REPORT_INVALID_PATH_ARG)
        for output_format in choice.formats:
            if output_format is not Format.GRAPH:
                raise SimpleBenchValueError(
                    f"Unsupported Format in Choice: {output_format}",
                    ErrorTag.GRAPH_REPORTER_REPORT_UNSUPPORTED_FORMAT)
        # if session is not None and not isinstance(session, Session):
        #    raise SimpleBenchTypeError(
        #        "session must be a Session instance if provided",
        #        ErrorTag.GRAPH_REPORTER_REPORT_INVALID_SESSION_ARG)

        # Only proceed if there are results to report
        results = case.results
        if not results:
            return

        for section in choice.sections:
            base_unit: str = ''
            if section is Section.OPS:
                base_unit = BASE_OPS_PER_INTERVAL_UNIT
            elif section is Section.TIMING:
                base_unit = BASE_INTERVAL_UNIT
            else:  # This should never happen due to earlier validation
                raise SimpleBenchValueError(
                    f"Unsupported section: {section} (this should not happen)",
                    ErrorTag.GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION)

            filename: str = sanitize_filename(section.name)
            if Target.FILESYSTEM in choice.targets:
                file = path.joinpath('graph', f'{filename}.svg')  # type: ignore[reportOptionalMemberAccess]
                file.parent.mkdir(parents=True, exist_ok=True)
                with file.open(mode='wb') as graphfile:
                    self.plot(case=case, target=section.value, graphfile=graphfile, base_unit=base_unit)
                    graphfile.close()
            if Target.CALLBACK in choice.targets and case.callback is not None:
                with BytesIO() as graphfile:
                    self.plot(case=case, target=section.value, graphfile=graphfile, base_unit=base_unit)
                    graphfile.seek(0)
                    case.callback(case, section, Format.GRAPH, graphfile.read())
                    graphfile.close()

    def plot(self,
             case: Case,
             target: str,
             graphfile: BytesIO | BufferedWriter,
             base_unit: str = '') -> None:
        """Generates and saves a scatter plot of the ops/sec and/or round timings results.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            graphfile (BytesIO | BufferedWriter): The file-like object to save the graph to.
            target (str): The target metric to plot ('ops_per_second' or 'per_round_timings').
            base_unit (str): The base unit for the y-axis.

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or values.
            SimpleBenchValueError: If the provided values are not valid.

        Returns:
            None
        """
        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.GRAPH_REPORTER_PLOT_INVALID_CASE_ARG)

        if not isinstance(graphfile, (BytesIO, BufferedWriter)):
            raise SimpleBenchTypeError(
                "Expected a BytesIO or BufferedWriter instance",
                ErrorTag.GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG)

        if not isinstance(target, str) or target not in ['ops_per_second', 'per_round_timings']:
            raise SimpleBenchTypeError(
                "target must be either 'ops_per_second' or 'per_round_timings'",
                ErrorTag.GRAPH_REPORTER_PLOT_INVALID_TARGET_ARG)

        results: list[Results] = case.results
        if not results:
            return

        all_numbers: list[float] = []
        all_numbers.extend([getattr(result, target).mean for result in results])
        common_unit, common_scale = si_scale_for_smallest(numbers=all_numbers, base_unit=base_unit)
        target_name = f'{target} ({base_unit})'

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
        plt.savefig(graphfile, format='svg')
        plt.close()  # Close the figure to free memory
        graphfile.flush()
