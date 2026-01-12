"""ActionRunner protocol for SimpleBench."""

from __future__ import annotations

from typing import Protocol

from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.case.results import Results


class FunctionRunner(Protocol):
    """A protocol for benchmark action functions used by Case.

    The function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter.
    The 'bench' parameter is a subclass of BenchmarkRunner, and '**kwargs' allows for additional
    keyword arguments to be passed to the function being benchmarked.

    Example action function signature:

    .. code-block:: python

        def my_action(bench: BenchmarkRunner, **kwargs) -> Results:
            # Benchmark logic here
            def some_function_to_benchmark():
                pass

            return bench.run(action=some_function_to_benchmark, **kwargs)
    """

    def __call__(self, _bench: BenchmarkRunner, **kwargs) -> Results:  # type: ignore[reportReturnType]
        """Run the benchmark action.

        :param _bench: The BenchmarkRunner instance.
        :param kwargs: Additional keyword arguments for the action.
        :return: The results of the benchmark action.
        """
