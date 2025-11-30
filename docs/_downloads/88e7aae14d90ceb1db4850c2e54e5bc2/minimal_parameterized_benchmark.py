"""A basic benchmark."""
import simplebench


@simplebench.benchmark(kwargs_variations={'size': [1, 5, 10, 50, 100, 500, 1000]},
                       variation_cols={'size': 'Input Size'},
                       use_field_for_n='size')
def addition_benchmark(**kwargs):
    """A simple addition benchmark of Python's built-in sum function."""
    sum(range(kwargs['size']))


if __name__ == "__main__":
    simplebench.main()
