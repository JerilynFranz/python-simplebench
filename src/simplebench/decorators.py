# -*- coding: utf-8 -*-
"""Decorators for simplifying benchmark case creation."""
from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING

from .case import Case
from .runners import SimpleRunner

if TYPE_CHECKING:
    from .reporters.reporter_option import ReporterOption

# A global registry to hold benchmark cases created by the decorator.
_DECORATOR_CASES: list[Case] = []
"""List to store benchmark cases registered via the @benchmark decorator."""


def benchmark(
    *,
    group: str,
    title: str | None = None,
    description: str | None = None,
    n: int | None = None,
    variation_cols: dict[str, str] | None = None,
    kwargs_variations: dict[str, list[Any]] | None = None,
    options: list[ReporterOption] | None = None
) -> Callable[[Callable[[], None]], Callable[[], None]]:
    """
    A decorator to register a function as a benchmark case.

    This simplifies creating a `Case` by wrapping the decorated function.
    The decorated function should contain the code to be benchmarked.

    Args:
        group: The group name for the benchmark case.
        title: The title of the benchmark case. Defaults to the function name.
        description: A description for the case. Defaults to the function's docstring.
        n: The number of rounds to run inside the benchmark timing loop.
        variation_cols: See `Case.variation_cols`.
        kwargs_variations: See `Case.kwargs_variations`.
        options: See `Case.options`.

    Returns:
        A decorator that registers the function and returns it unmodified.
    """
    def decorator(func: Callable[[], None]) -> Callable[[], None]:
        """The actual decorator that wraps the user's function."""

        def case_action_wrapper(runner: SimpleRunner, **kwargs: Any) -> None:
            """
            This wrapper becomes the `action` for the `Case`.
            It calls the user's decorated function inside `runner.run()`.
            """
            # The user's function is passed as the action to run.
            # `n` is passed if provided to the decorator.
            run_kwargs: dict[str, Any] = {'action': func}
            if n is not None:
                run_kwargs['n'] = n

            # kwargs from kwargs_variations are passed through
            run_kwargs.update(kwargs)

            return runner.run(**run_kwargs)

        # Create the Case instance, using sensible defaults from the function.
        case = Case(
            group=group,
            title=title or func.__name__,
            action=case_action_wrapper,
            description=description or func.__doc__ or '(no description)',
            variation_cols=variation_cols or {},
            kwargs_variations=kwargs_variations or {},
            options=options or [],
            _decoration=True
        )

        # Add the created case to the global registry.
        _DECORATOR_CASES.append(case)

        # Return the original function so it remains callable.
        return func

    return decorator


def get_registered_cases() -> list[Case]:
    """
    Retrieve all benchmark cases registered via the `@benchmark` decorator.

    Returns:
        A list of `Case` objects.
    """
    return _DECORATOR_CASES
