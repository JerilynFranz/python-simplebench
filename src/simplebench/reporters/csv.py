# -*- coding: utf-8 -*-
"""Reporter for benchmark results using CSV files."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Literal

from ..constants import (BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT,
                         DEFAULT_INTERVAL_SCALE)
from ..exceptions import SimpleBenchTypeError, ErrorTag
from ..session import Session
from ..case import Case
from ..utils import sigfigs, si_scale_for_smallest
from .choices import Choice, Choices, Section, Format, Target
from .interfaces import Reporter


class CSVReporter(Reporter):
    """Class for outputting benchmark results to CSV files."""

    def __init__(self, session: Session, case: Case) -> None:
        if not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "Expected a Session instance",
                ErrorTag.CSV_REPORTER_INIT_INVALID_SESSION_ARG)
        self._session: Session = session

        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.CSV_REPORTER_INIT_INVALID_CASE_ARG)
        self._case: Case = case

        self._choices: Choices = Choices()
        self._choices.add(
            Choice(
                reporter=self,
                runner=self.output_ops_results_to_csv,
                flags=['--csv-ops'],
                name='csv-ops',
                description='Save operations per second results to a CSV file',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM],
                formats=[Format.CSV]))
        self._choices.add(
            Choice(
                reporter=self,
                runner=self.output_timing_results_to_csv,
                flags=['--csv-timings'],
                name='csv-timings',
                description='Save per round timing results to a CSV file',
                sections=[Section.TIMING],
                targets=[Target.FILESYSTEM],
                formats=[Format.CSV]))

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
        case = self._case
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

    def output_ops_results_to_csv(self, path: Path) -> None:
        """Output the benchmark results to a file as tagged CSV if available.
        """
        return self.output_results_to_csv(filepath=path.joinpath('csv', 'ops_per_second.csv'),
                                          base_unit=BASE_OPS_PER_INTERVAL_UNIT,
                                          target='ops_per_second')

    def output_timing_results_to_csv(self, path: Path) -> None:
        """Outputs the timing benchmark results to file as tagged CSV.
        """
        return self.output_results_to_csv(filepath=path.joinpath('csv', 'per_round_timings.csv'),
                                          base_unit=BASE_INTERVAL_UNIT,
                                          target='per_round_timings')
