#!/usr/bin/env python3
"""A simple benchmark case function."""
import simplebench
from simplebench import ImageType, Style, options


@simplebench.benchmark(
    'example', n=100,
    options=[options.ScatterPlotOptions(image_type=ImageType.PNG)]
)
def benchcase_one() -> None:
    """A simple benchmark case function via decorators."""
    sum(range(100))  # Example operation to benchmark


@simplebench.benchmark(
    'example2',
    title='benchcase_two',
    description='A simple benchmark case function (fake second) via decorators.',
    n=100,
    options=[options.ScatterPlotOptions(style=Style.CLASSIC, image_type=ImageType.SVG)]
)
def benchcase_two_action() -> None:
    """This just re-uses the same operation for demonstration."""
    sum(range(100))


if __name__ == '__main__':
    # The main function can now automatically collect cases from the decorator's registry.
    simplebench.main()
