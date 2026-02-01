"""Controlling benchmark execution example."""
import simplebench


@simplebench.benchmark(
    min_time=1.0,  # 1 second minimum wallclock time
    max_time=2.0,  # 2 seconds maximum wallclock time,
    iterations=1000,  # target a minimum of 1000 iterations
    rounds=1000,  # 1000 rounds per iteration
    warmup_iterations=100,  # 100 warmup iterations
    timeout=3.0,  # 3 seconds total wallclock timebefore timeout
)
def addition_benchmark() -> int:
    """A simple addition benchmark of Python's built-in sum function."""
    return sum(range(100))


if __name__ == "__main__":
    simplebench.main()
