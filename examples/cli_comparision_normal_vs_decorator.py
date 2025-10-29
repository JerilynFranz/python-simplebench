#!/usr/bin/env python3
"""A simple benchmark case function."""
from __future__ import annotations
from typing import Any

from simplebench.cli import main
from simplebench.decorators import benchmark
from simplebench.case import Case
from simplebench.runners import SimpleRunner
from simplebench.reporters.graph.scatterplot import ScatterPlotOptions
from simplebench.reporters.graph.enums import ImageType
from simplebench.results import Results


@benchmark(
    'example',
    title='benchcase one',
    description='A simple benchmark case function via decorators.',
    n=100,
    warmup_iterations=10,
    options=[ScatterPlotOptions(image_type=ImageType.PNG)]
)
def benchcase_one():
    """A simple benchmark case function via decorators."""
    sum(range(100))  # Example operation to benchmark


def benchcase_two(bench: SimpleRunner, **kwargs: Any) -> Results:
    """A simple benchmark case function."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(100))  # Example operation to benchmark
    return bench.run(n=100, action=action, kwargs=kwargs)


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
    main(benchmark_cases_list_factory())
