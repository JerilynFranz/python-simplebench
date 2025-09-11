# -*- coding: utf-8 -*-
"""Decorators for benchmark cases."""
from __future__ import annotations
from typing import Any, Callable


from .session import Session


_benchsession: Session = Session()
"""Global Session instance for storing benchmark cases."""


def benchmark(func: Callable[..., Any],
              n: int = 1,
              repeat: int = 100,
              warmup: int = 10,
              *args: Any, **kwargs: Any) -> Any:
    """Decorator to mark a function as a benchmark case.

    This decorator can be used to wrap a function that performs benchmarking.
    The decorated function should accept a `SimpleRunner` instance as its first argument,
    which can be used to run the benchmark.

    Example:
        @benchmark(n=100, repeat=10)
        def my_benchmark():
            sum(range(1000))

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """
    ...
