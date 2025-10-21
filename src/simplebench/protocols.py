"""Protocols for SimpleBench."""
from __future__ import annotations
from typing import Protocol

from .runners import SimpleRunner
from .results import Results


class ActionRunner(Protocol):
    """A protocol for benchmark action functions used by Case.

    The action function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter.
    The 'bench' parameter is an instance of SimpleRunner, and '**kwargs' allows for additional
    keyword arguments to be passed to the function being benchmarked.

    Example action function signature:

        def my_action(bench: SimpleRunner, **kwargs) -> Results:
            # Benchmark logic here
            def some_function_to_benchmark():
                pass
            return bench.run(action=some_function_to_benchmark, **kwargs)
    """
    def __call__(self, bench: SimpleRunner, **kwargs) -> Results:  # type: ignore[reportReturnType]
        """Run the benchmark action.

        Args:
            bench: The SimpleRunner instance.
            **kwargs: Additional keyword arguments for the action.

        Returns:
            Results: The results of the benchmark action.
        """
