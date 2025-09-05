# -*- coding: utf-8 -*-
"""Reporter for benchmark results using rich tables in the console."""
from __future__ import annotations
from typing import Literal

from rich.table import Table

from ..constants import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE
from ..exceptions import SimpleBenchTypeError, ErrorTag
from ..session import Session
from ..case import Case
from ..results import Results
from ..utils import sigfigs, si_scale_for_smallest
from .choices import Choice, Choices, Section, Format, Target
from .interfaces import Reporter


class RichTableReporter(Reporter):
    """Reporter for displaying benchmark results as a rich table on the console
    """
    def __init__(self, session: Session, case: Case) -> None:
        if not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "Expected a Session instance",
                ErrorTag.RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG)
        self._session: Session = session

        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.RICH_TABLE_REPORTER_INIT_INVALID_CASE_ARG)
        self._case: Case = case
        self._choices: Choices = Choices()
        self._choices.add(
            Choice(
                reporter=self,
                runner=self.ops_results_as_rich_table,
                flags=['--rich-table-ops'],
                name='rich-table-ops',
                description='Display operations per second results as a rich text table on the console',
                sections=[Section.OPS],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT]))
        self._choices.add(
            Choice(
                reporter=self,
                runner=self.timing_results_as_rich_table,
                flags=['--rich-table-timings'],
                name='rich-table-timings',
                description='Display timing results as a rich text table on the console',
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
        raise NotImplementedError

    @property
    def description(self) -> str:
        """Return a brief description of the reporter."""
        raise NotImplementedError

    def results_as_rich_table(self,
                              base_unit: str,
                              target: Literal['ops_per_second', 'per_round_timings']) -> None:
        """Prints the benchmark results in a rich table format if available.
        """
        case: Case = self._case
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
        self._session.console.print(table)

    def ops_results_as_rich_table(self) -> None:
        """Prints the Operations Per Second benchmark results in a rich table format if available.
        """
        return self.results_as_rich_table(base_unit=BASE_OPS_PER_INTERVAL_UNIT, target='ops_per_second')

    def timing_results_as_rich_table(self) -> None:
        """Prints the Timing benchmark results in a rich table format if available.
        """
        return self.results_as_rich_table(base_unit=BASE_INTERVAL_UNIT, target='per_round_timings')
