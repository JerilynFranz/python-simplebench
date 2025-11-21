#!python3
"""Example Scatterplot Benchmark Script"""
import simplebench


@simplebench.benchmark(
    kwargs_variations={'size': [1, 10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]},
    variation_cols={'size': 'Size'},
    use_field_for_n='size')
def addition_benchmark(**kwargs):
    """A simple benchmark that sums a range of numbers."""
    sum(range(kwargs['size']))


if __name__ == "__main__":
    simplebench.main()
