#!/usr/bin/env python3
"""A simple benchmark case function."""
from __future__ import annotations
from typing import Any

from simplebench import main, benchmark, Case, SimpleRunner
from simplebench.reporters.graph import GraphOptions
from simplebench.results import Results


@benchmark(
    group='example',
    title='benchcase one',
    description='A simple benchmark case function via decorators.',
    n=100,
    warmup_iterations=10,
    options=[GraphOptions(output_format='png')]
)
def benchcase_one():
    """A simple benchmark case function via decorators."""
    sum(range(100))  # Example operation to benchmark


def benchcase_two(bench: SimpleRunner, **kwargs: Any) -> Results:
    """A simple benchmark case function."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(100))  # Example operation to benchmark
    return bench.run(n=100, action=action, **kwargs)


def benchmark_cases_list_factory() -> list[Case]:
    """Factory function to create a list of benchmark cases."""
    return [
        Case(group='example_without_decorator',
             title='benchcase two',
             action=benchcase_two,
             description='A simple benchmark case function without decorators.',
             variation_cols={},
             kwargs_variations={},
             options=[GraphOptions(output_format='png')]),
    ]


if __name__ == '__main__':
    main(benchmark_cases_list_factory())
