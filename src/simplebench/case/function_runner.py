"""FunctionRunner protocol for SimpleBench."""

from typing import Protocol, runtime_checkable, overload

from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.case.results import Results
from simplebench.simplebench_types import VariationMarks


@runtime_checkable
class FunctionRunner(Protocol):
    """A protocol for benchmark action functions used by Case.

    The function must accept two parameters: a 'bench' parameter and a 'variation_marks' parameter.
    The 'bench' parameter is a subclass of BenchmarkRunner, and 'variation_marks' allows for
    keyword arguments to be passed to the function being benchmarked in the form of VariationMarks.

    Example action function signature:

    .. code-block:: python

        def my_action(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
            # Benchmark logic here
            def some_function_to_benchmark():
                pass

            return bench.run(action=some_function_to_benchmark, variation_marks=variation_marks)
    """

    def __call__(self, bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
        """Run the benchmark action.

        :param bench: The BenchmarkRunner instance.
        :type bench: BenchmarkRunner
        :param variation_marks: Variation marks for the action.
        :type variation_marks: VariationMarks
        :return: The results of the benchmark action.
        """
        ...
