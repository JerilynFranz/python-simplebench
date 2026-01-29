"""FunctionRunner protocol for SimpleBench."""

from typing import Protocol, runtime_checkable

from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.case.results import Results
from simplebench.simplebench_types import VariationMarks


@runtime_checkable
class FunctionRunner(Protocol):
    """A protocol for benchmark action functions used by Case.

    The function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter.
    The 'bench' parameter is a subclass of BenchmarkRunner, and '**kwargs' allows for additional
    keyword arguments to be passed to the function being benchmarked.

    Example action function signature:

    .. code-block:: python

        def my_action(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
            # Benchmark logic here
            def some_function_to_benchmark():
                pass

            return bench.run(action=some_function_to_benchmark, variation_marks=variation_marks)
    """

    def __call__(self, _bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
        """Run the benchmark action.

        :param _bench: The BenchmarkRunner instance.
        :param variation_marks: Variation marks for the action.
        :return: The results of the benchmark action.
        """
        ...
