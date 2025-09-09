#!/usr/bin/env python3
"""A simple benchmark case function."""
from __future__ import annotations
from argparse import Namespace
from pathlib import Path

from simplebench.case import Case
from simplebench.runners import SimpleRunner
from simplebench.session import Session, Verbosity


def benchcase_one(benchmark: SimpleRunner) -> None:
    """A simple benchmark case function."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(100))  # Example operation to benchmark
    return benchmark.run(n=100, action=action)


def benchmark_cases_list_factory() -> list[Case]:
    """Factory function to create a list of benchmark cases."""
    return [
        Case(group='example',
             title='benchcase_one',
             action=benchcase_one,
             description='A simple benchmark case function.',
             variation_cols={},
             kwargs_variations={}),
        Case(group='example2',
             title='benchcase_two',
             action=benchcase_one,
             description='A simple benchmark case function (fake second).',
             variation_cols={},
             kwargs_variations={}),
    ]


if __name__ == '__main__':
    args = Namespace(
        rich_table_console=True,
        csv_file=True,
        graph_scatter_file=True,
    )
    session = Session(args=args,
                      cases=benchmark_cases_list_factory(),
                      verbosity=Verbosity.DEBUG,
                      output_path=Path('.benchmark_reports'))
    session.run()
    session.report()

    print("Benchmarking complete.")
