"""Factories for creating Case, Session, and Runner test objects."""
# pylint: disable=unused-argument
from __future__ import annotations

from simplebench.case import Case
from simplebench.results import Results
from simplebench.runners import SimpleRunner
from simplebench.session import Session
from simplebench.enums import Verbosity

from ..kwargs import CaseKWArgs
from ..cache_factory import cached_factory, uncached_factory, CacheId, CACHE_DEFAULT
from ._primitives import (
    default_case_group, default_title, default_description, default_iterations, default_warmup_iterations,
    default_rounds, default_min_time, default_max_time, variation_cols_factory, kwargs_variations_factory
)
from .reporter_options import default_reporter_options_tuple
from .reporter_callback import default_reporter_callback


def default_benchcase(bench: SimpleRunner, **kwargs) -> Results:
    """A simple benchmark case function.

    ```python
    def default_benchcase(bench: SimpleRunner, **kwargs) -> Results:

        def action() -> None:
            '''A simple benchmark case function.'''
            sum(range(10))  # Example operation to benchmark
        return bench.run(n=10, action=action, **kwargs)
    ```
    """

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(10))  # Example operation to benchmark

    return bench.run(n=10, action=action, **kwargs)


@cached_factory
def minimal_case_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:
    """Return a minimally configured CaseKWArgs for testing purposes.

    Only the required attribute `action` is set to an explicit value.
    All other attributes will take their default values.

    ```python
       CaseKWArgs(action=default_benchcase)
    ```

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        CaseKWArgs: A minimally configured CaseKWArgs instance.
    """
    return CaseKWArgs(action=default_benchcase)


def default_minimal_case_kwargs() -> CaseKWArgs:
    """Return a default minimally configured CaseKWArgs for testing purposes.

    It always returns the same CaseKWArgs instance created by minimal_case_kwargs_factory().

    Returns:
        CaseKWArgs: A minimally configured CaseKWArgs instance.
    """
    return minimal_case_kwargs_factory(cache_id=f'{__name__}.default_minimal_case_kwargs:singleton')


@cached_factory
def runner_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> type[SimpleRunner]:
    """Return a SimpleRunner type for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        type[SimpleRunner]: `SimpleRunner`
    """
    return SimpleRunner


def default_runner() -> type[SimpleRunner]:
    """Return a default SimpleRunner type for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        type[SimpleRunner]: `SimpleRunner`
    """
    return runner_factory(cache_id=f'{__name__}.default_runner:singleton')


@cached_factory
def case_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:
    """Return a default configured CaseKWArgs for testing purposes.

    The following parameters are all set to explicit values for testing purposes:

    Attributes:
        group = `default_case_group()`
        title = `default_title()`
        description = `default_description()`
        action = `default_benchcase`
        iterations = `default_iterations()`
        warmup_iterations = `default_warmup_iterations()`
        rounds = `default_rounds()`
        min_time = `default_min_time()`
        max_time = `default_max_time()`
        variation_cols = `default_variation_cols()`
        kwargs_variations = `default_kwargs_variations()`
        runner = `default_runner()`
        callback = `default_reporter_allback`
        options = `default_reporter_options()`

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        CaseKWArgs: A fully configured CaseKWArgs instance.
    """
    # pylint: disable=import-outside-toplevel
    return CaseKWArgs(group=default_case_group(),
                      title=default_title(),
                      description=default_description(),
                      action=default_benchcase,
                      iterations=default_iterations(),
                      warmup_iterations=default_warmup_iterations(),
                      rounds=default_rounds(),
                      min_time=default_min_time(),
                      max_time=default_max_time(),
                      variation_cols=variation_cols_factory(cache_id=cache_id),
                      kwargs_variations=kwargs_variations_factory(cache_id=cache_id),
                      runner=default_runner(),
                      callback=default_reporter_callback,
                      options=default_reporter_options_tuple())


@uncached_factory
def case_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Case:
    """Return a default Case instance for testing purposes.

    This is a 'pre-benchmarking' Case with default attributes set but no results.

    The Case is initialized using case_kwargs_factory() and contains no Results.

    It is uncached by default to ensure that each call returns a fresh Case instance.

    This can be overriden by providing a non-None cache_id if needed.

    Because a Case can be mutated after creation (e.g., by running benchmarks),
    it is important to use cache_id appropriately to avoid unintended side effects
    from shared instances in tests.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    """
    return Case(**case_kwargs_factory())


@cached_factory
def session_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Session:
    """Return a default Session instance for testing purposes.

    The Session is initialized with default attributes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    """
    return Session(cases=[case_factory(cache_id=cache_id)], verbosity=Verbosity.QUIET)


@cached_factory
def post_run_case_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Case:
    """Return a default Case instance representing a post-benchmarking run state for testing purposes.

    The Case is initialized with default attributes and includes benchmark results
    based on the `default_benchcase` function.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    """
    case = Case(**case_kwargs_factory())
    case.run()
    return case
