"""A basic benchmark."""
import simplebench


@simplebench.benchmark
def addition_benchmark():
    """A simple addition benchmark of Python's built-in sum function."""
    sum(range(1000))


if __name__ == "__main__":
    simplebench.main()
