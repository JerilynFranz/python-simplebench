#!/usr/bin/env python3
"""A simple benchmark case function."""
from __future__ import annotations
from typing import Any

from simplebench import Case, main
from simplebench.decorators import benchmark
from simplebench.reporters.graph import GraphOptions
from simplebench.results import Results
from simplebench.runners import SimpleRunner


def benchcase_one(bench: SimpleRunner, **kwargs: Any) -> Results:
    """A simple benchmark case function."""
    def action() -> None:
        """A simple benchmark case function."""
        sum(range(100000))  # Example operation to benchmark
    return bench.run(n=100000, action=action, **kwargs)


def benchcase_four(bench: SimpleRunner, **kwargs: Any) -> Results:
    """A simple benchmark case function."""
    def action(size: int) -> int:
        """A simple benchmark case function."""
        return sum(range(size))  # Example operation to benchmark
    return bench.run(n=kwargs['size'], action=action, **kwargs)


@benchmark(
    group='example3',
    title='sum_numbers',
    description='A benchmark case function that sums numbers up to n.',
    min_time=10.0,
    max_time=20.0,
    iterations=200,
    use_field_for_n='size',
    variation_cols={'size': 'Size of range'},
    kwargs_variations={'size': [10, 100, 1000, 10000, 100000]})
def sum_numbers(size: int) -> int:
    """A simple benchmark case function that sums numbers up to n."""
    return sum(range(size))  # Example operation to benchmark


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
        Case(group='example4',
             title='benchcase_four',
             action=benchcase_four,
             description='A simple benchmark case function with size variation.',
             variation_cols={'size': 'Size of the range to sum'},
             kwargs_variations={'size': [10, 100, 1000, 10000, 100000]}),
    ]


if __name__ == '__main__':
    cases = benchmark_cases_list_factory()
    main(cases)
