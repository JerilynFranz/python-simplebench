#!/usr/bin/env python3
"""A simple benchmark case function."""

from simplebench.benchmark_runner import BenchmarkRunner

import simplebench
from simplebench.case import Case, Results
from simplebench.reporters.graph.enums import ImageType
from simplebench.options import ScatterPlotOptions
from simplebench.simplebench_types import VariationMarks


@simplebench.benchmark(
    'example',
    title='benchcase one',
    description='A simple benchmark case function via decorators.',
    n=100,
    warmup_iterations=10,
    options=[ScatterPlotOptions(image_type=ImageType.PNG)]
)


def benchcase_one() -> None:
    """A simple benchmark case function via decorators."""
    sum(range(100))  # Example operation to benchmark


def benchcase_two(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
    """A simple benchmark case function."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(100))  # Example operation to benchmark
    return bench.run(n=100, action=action, variation_marks=variation_marks)


def benchmark_cases_list_factory() -> list[Case]:
    """Factory function to create a list of benchmark cases."""
    return [
        Case(group='example_without_decorator',
             title='benchcase two',
             action=benchcase_two,
             description='A simple benchmark case function without decorators.',
             variation_cols={},
             kwargs_variations={},
             options=[ScatterPlotOptions(image_type=ImageType.PNG)]),
    ]


if __name__ == '__main__':
    simplebench.main(benchmark_cases_list_factory())
