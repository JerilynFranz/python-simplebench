"""Protocols for SimpleBench."""
from __future__ import annotations

from typing import Protocol

from .results import Results
from .runners import SimpleRunner


class ActionRunner(Protocol):
    """A protocol for benchmark action functions used by Case.

    The action function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter.
    The 'bench' parameter is an instance of SimpleRunner, and '**kwargs' allows for additional
    keyword arguments to be passed to the function being benchmarked.

    Example action function signature:

    .. code-block:: python

        def my_action(bench: SimpleRunner, **kwargs) -> Results:
            # Benchmark logic here
            def some_function_to_benchmark():
                pass
            return bench.run(action=some_function_to_benchmark, **kwargs)
    """
    def __call__(self, _bench: SimpleRunner, **kwargs) -> Results:  # type: ignore[reportReturnType]
        """Run the benchmark action.

        :param _bench: The SimpleRunner instance.
        :param kwargs: Additional keyword arguments for the action.
        :return: The results of the benchmark action.
        """
