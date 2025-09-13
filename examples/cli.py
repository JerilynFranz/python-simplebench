#!/usr/bin/env python3
"""A simple benchmark case function."""
from __future__ import annotations

from simplebench import Case, SimpleRunner, main
from simplebench.reporters.graph import GraphOptions


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
             kwargs_variations={},
             options=[GraphOptions(output_format='png')]),
        Case(group='example2',
             title='benchcase_two',
             action=benchcase_one,
             description='A simple benchmark case function (fake second).',
             variation_cols={},
             kwargs_variations={},
             options=[GraphOptions(style='default', output_format='svg')]),
    ]


if __name__ == '__main__':
    cases = benchmark_cases_list_factory()
    main(cases)
