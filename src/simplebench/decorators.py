# -*- coding: utf-8 -*-
"""Decorators for benchmark cases."""
from __future__ import annotations
from typing import Any, Callable, Optional, Sequence


from .case import Case
from .session import Session


_benchsession: Session = Session()
"""Global Session instance for storing benchmark cases."""


def benchmark(func: Callable[..., Any],
              *args: Any, **kwargs: Any) -> Any:
    """Decorator to mark a function as a benchmark case.

    This decorator can be used to wrap a function that performs benchmarking.
    The decorated function should accept a `SimpleRunner` instance as its first argument,
    which can be used to run the benchmark.

    Example:
        @benchmark
        def my_benchmark(benchmark: SimpleRunner):
            def action():
                # Code to benchmark
                pass
            return benchmark.run(n=1000, action=action)

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """
    def case(func, *args, **kwargs) -> None:
        """Decorator to add benchmark cases to a function.

        It takes the same arguments as the Case class and adds the created Case instance
        to the global _benchsession instance.
        """
        _benchsession.add(Case(*args, **kwargs))
        func(*args, **kwargs)

    return action(_benchsession, *args, *kwargs)
