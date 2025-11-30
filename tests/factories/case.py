"""Factories for creating Case, Session, and Runner test objects."""
# pylint: disable=unused-argument
from __future__ import annotations

from typing import overload

from simplebench.case import Case
from simplebench.results import Results
from simplebench.runners import SimpleRunner

from ..cache_factory import CACHE_DEFAULT, CacheId, cached_factory, uncached_factory
from ..kwargs import CaseKWArgs
from ._primitives import (
    default_case_group,
    default_description,
    default_iterations,
    default_max_time,
    default_min_time,
    default_rounds,
    default_title,
    default_warmup_iterations,
    kwargs_variations_factory,
    variation_cols_factory,
)
from .reporter_callback import default_reporter_callback
from .reporter_options import default_reporter_options_tuple


def default_benchcase(_bench: SimpleRunner, **kwargs) -> Results:
    """A simple benchmark case function.

    .. code-block:: python

        def default_benchcase(bench: SimpleRunner, **kwargs) -> Results:

            def action() -> None:
                '''A simple benchmark case function.'''
                sum(range(10))  # Example operation to benchmark
            return bench.run(n=10, action=action, **kwargs)
    """

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(10))  # Example operation to benchmark

    return _bench.run(n=10, action=action, **kwargs)


@cached_factory
def minimal_case_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:
    """Return a minimally configured CaseKWArgs for testing purposes.

    Only the required attribute `action` is set to an explicit value.
    All other attributes will take their default values.

    .. code-block:: python

       CaseKWArgs(action=default_benchcase)

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A minimally configured CaseKWArgs instance.
    :rtype: CaseKWArgs
    """
    return CaseKWArgs(action=default_benchcase)


def default_minimal_case_kwargs() -> CaseKWArgs:
    """Return a default minimally configured CaseKWArgs for testing purposes.

    It always returns the same CaseKWArgs instance created by minimal_case_kwargs_factory().

    :return: A minimally configured CaseKWArgs instance.
    :rtype: CaseKWArgs
    """
    return minimal_case_kwargs_factory(cache_id=f'{__name__}.default_minimal_case_kwargs:singleton')


@cached_factory
def runner_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> type[SimpleRunner]:
    """Return a SimpleRunner type for testing purposes.

    This is for use in configuring benchmark cases in tests.

    :return: `SimpleRunner`
    :rtype: type[SimpleRunner]
    """
    return SimpleRunner


def default_runner() -> type[SimpleRunner]:
    """Return a default SimpleRunner type for testing purposes.

    This is for use in configuring benchmark cases in tests.

    :return: `SimpleRunner`
    :rtype: type[SimpleRunner]
    """
    return runner_factory(cache_id=f'{__name__}.default_runner:singleton')


# provide overloads for better tooltips and docstrings
@overload
def case_kwargs_factory() -> CaseKWArgs:
    """Return a default configured CaseKWArgs for testing purposes.

    The CaseKWArgs instance is fully populated and cached by default for efficiency.

    The following parameters are all set to explicit values for testing purposes:

    :ivar group: `default_case_group()`
    :ivar title: `default_title()`
    :ivar description: `default_description()`
    :ivar action: `default_benchcase`
    :ivar iterations: `default_iterations()`
    :ivar warmup_iterations: `default_warmup_iterations()`
    :ivar rounds: `default_rounds()`
    :ivar min_time: `default_min_time()`
    :ivar max_time: `default_max_time()`
    :ivar variation_cols: `default_variation_cols()`
    :ivar kwargs_variations: `default_kwargs_variations()`
    :ivar runner: `default_runner()`
    :ivar callback: `default_reporter_callback`
    :ivar options: `default_reporter_options()`

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A fully configured CaseKWArgs instance.
    :rtype: CaseKWArgs
    """


@overload
def case_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:
    """Return a default configured CaseKWArgs for testing purposes.

    The CaseKWArgs instance is fully populated and cached by default for efficiency.

    The following parameters are all set to explicit values for testing purposes:

    :ivar group: `default_case_group()`
    :ivar title: `default_title()`
    :ivar description: `default_description()`
    :ivar action: `default_benchcase`
    :ivar iterations: `default_iterations()`
    :ivar warmup_iterations: `default_warmup_iterations()`
    :ivar rounds: `default_rounds()`
    :ivar min_time: `default_min_time()`
    :ivar max_time: `default_max_time()`
    :ivar variation_cols: `default_variation_cols()`
    :ivar kwargs_variations: `default_kwargs_variations()`
    :ivar runner: `default_runner()`
    :ivar callback: `default_reporter_callback`
    :ivar options: `default_reporter_options()`

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A fully configured CaseKWArgs instance.
    :rtype: CaseKWArgs
    """


@cached_factory
def case_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:
    """Return a default configured CaseKWArgs for testing purposes.

    The CaseKWArgs instance is fully populated and cached by default for efficiency.

    The following parameters are all set to explicit values for testing purposes:

    :ivar group: `default_case_group()`
    :ivar title: `default_title()`
    :ivar description: `default_description()`
    :ivar action: `default_benchcase`
    :ivar iterations: `default_iterations()`
    :ivar warmup_iterations: `default_warmup_iterations()`
    :ivar rounds: `default_rounds()`
    :ivar min_time: `default_min_time()`
    :ivar max_time: `default_max_time()`
    :ivar variation_cols: `default_variation_cols()`
    :ivar kwargs_variations: `default_kwargs_variations()`
    :ivar runner: `default_runner()`
    :ivar callback: `default_reporter_callback`
    :ivar options: `default_reporter_options()`

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A fully configured CaseKWArgs instance.
    :rtype: CaseKWArgs
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


# provide overloads for better tooltips and docstrings
@overload
def case_factory() -> Case:
    """Return a default Case instance for testing purposes.

    It is uncached by default to ensure that each call returns a fresh Case instance.

    This is a 'pre-benchmarking' Case with default attributes set but no results.

    The Case is initialized using case_kwargs_factory() and contains no Results.

    It is uncached by default to ensure that each call returns a fresh Case instance.

    This can be overriden by providing a non-None cache_id if needed.

    Because a Case can be mutated after creation (e.g., by running benchmarks),
    it is important to use cache_id appropriately to avoid unintended side effects
    from shared instances in tests.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    """


@overload
def case_factory(*, cache_id: CacheId = None) -> Case:
    """Return a default Case instance for testing purposes.

    It is uncached by default to ensure that each call returns a fresh Case instance.

    This is a 'pre-benchmarking' Case with default attributes set but no results.

    The Case is initialized using case_kwargs_factory() and contains no Results.

    It is uncached by default to ensure that each call returns a fresh Case instance.

    This can be overriden by providing a non-None cache_id if needed.

    Because a Case can be mutated after creation (e.g., by running benchmarks),
    it is important to use cache_id appropriately to avoid unintended side effects
    from shared instances in tests.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    """


@uncached_factory
def case_factory(*, cache_id: CacheId = None) -> Case:
    """Return a default Case instance for testing purposes.

    It is uncached by default to ensure that each call returns a fresh Case instance.

    This is a 'pre-benchmarking' Case with default attributes set but no results.

    The Case is initialized using case_kwargs_factory() and contains no Results.

    It is uncached by default to ensure that each call returns a fresh Case instance.

    This can be overriden by providing a non-None cache_id if needed.

    Because a Case can be mutated after creation (e.g., by running benchmarks),
    it is important to use cache_id appropriately to avoid unintended side effects
    from shared instances in tests.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    """
    return Case(**case_kwargs_factory())


@cached_factory
def post_run_case_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Case:
    """Return a default Case instance representing a post-benchmarking run state for testing purposes.

    The Case is initialized with default attributes and includes benchmark results
    based on the `default_benchcase` function.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    """
    case = Case(**case_kwargs_factory())
    case.run()
    return case
