#!/usr/bin/env python3
"""A simple benchmark case function."""
from typing import Any

import simplebench
from simplebench import Case
from simplebench.reporters.graph import ImageType
from simplebench.reporters.graph.matplotlib import Style
from simplebench.reporters.graph.scatterplot import ScatterPlotOptions
from simplebench.results import Results
from simplebench.runners import SimpleRunner


def benchcase_one(bench: SimpleRunner, **kwargs: Any) -> Results:
    """A simple benchmark case function."""
    def action() -> None:
        """A simple benchmark case function."""
        sum(range(100000))  # Example operation to benchmark
    return bench.run(n=100000, action=action, kwargs=kwargs)


def benchcase_four(bench: SimpleRunner, **kwargs: Any) -> Results:
    """A simple benchmark case function."""
    def action(size: int) -> int:
        """A simple benchmark case function."""
        return sum(range(size))  # Example operation to benchmark
    return bench.run(n=kwargs['size'], action=action, kwargs=kwargs)


@simplebench.benchmark(
    'example3',
    title='sum_numbers',
    description='A benchmark case function that sums numbers up to n.',
    min_time=1.0,
    max_time=5.0,
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
             options=[ScatterPlotOptions(image_type=ImageType.PNG)]),
        Case(group='example2',
             title='benchcase_two',
             action=benchcase_one,
             description='A simple benchmark case function (fake second).',
             variation_cols={},
             kwargs_variations={},
             options=[ScatterPlotOptions(style=Style.SEABORN_V0_8, image_type=ImageType.SVG)]),
        Case(group='example4',
             title='benchcase_four',
             action=benchcase_four,
             description='A simple benchmark case function with size variation.',
             variation_cols={'size': 'Size of the range to sum'},
             kwargs_variations={'size': [10, 100, 1000, 10000, 100000]}),
    ]


if __name__ == '__main__':
    cases = benchmark_cases_list_factory()
    simplebench.main(cases)
