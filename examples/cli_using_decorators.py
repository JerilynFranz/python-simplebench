#!/usr/bin/env python3
"""A simple benchmark case function."""
from __future__ import annotations

from simplebench import main, benchmark
from simplebench.reporters.graph import GraphOptions


@benchmark(
    group='example',
    n=100,
    options=[GraphOptions(output_format='png')]
)
def benchcase_one():
    """A simple benchmark case function via decorators."""
    sum(range(100))  # Example operation to benchmark


@benchmark(
    group='example2',
    title='benchcase_two',
    description='A simple benchmark case function (fake second) via decorators.',
    n=100,
    options=[GraphOptions(style='default', output_format='svg')]
)
def benchcase_two_action():
    """This just re-uses the same operation for demonstration."""
    sum(range(100))


if __name__ == '__main__':
    # The main function can now automatically collect cases from the decorator's registry.
    main()
