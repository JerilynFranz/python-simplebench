#!/usr/bin/env python3
"""A simple benchmark case function."""
from __future__ import annotations

from simplebench import main, benchmark
from simplebench.reporters.graph.scatter import ScatterGraphOptions
from simplebench.reporters.graph.enums import ImageType


@benchmark(
    'example',
    n=100,
    options=[ScatterGraphOptions(output_format=ImageType.PNG)]
)
def benchcase_one():
    """A simple benchmark case function via decorators."""
    sum(range(100))  # Example operation to benchmark


@benchmark(
    'example2',
    title='benchcase_two',
    description='A simple benchmark case function (fake second) via decorators.',
    n=100,
    options=[ScatterGraphOptions(style='default', output_format=ImageType.SVG)]
)
def benchcase_two_action():
    """This just re-uses the same operation for demonstration."""
    sum(range(100))


if __name__ == '__main__':
    # The main function can now automatically collect cases from the decorator's registry.
    main()
