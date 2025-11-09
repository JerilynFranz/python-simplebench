"""Factories for creating test instances of reporters and related classes.

It is divided into factory functions that create and return specific test instances
of various classes used in the simplebench framework and default functions that
return singleton default instances for use in tests.

The difference between factory functions and default functions is that
factory functions create and return new instances (possibly cached) of the
requested type each time they are called (unless caching is disabled or
a specific cache_id is provided), while default functions always return
the same singleton instance created by the corresponding factory function.

So while path_factory() will return a new Path instance each time it is called,
default_path() function will always return the same Path instance.

Default functions are useful for tests that need a single reference
instance to compare against expected values without needing to create
new instances each time or manage caching behavior. They are only defined
for classes that are immutable or can be safely shared across tests without
risk of unintended side effects from mutations. This means that default
functions are not provided for classes like `Case` that can be mutated
after creation.

It also means that 'is' comparisons can be used in tests to verify that
the same default instance is being used consistently.

By placing these factory functions in a separate module, we keep from
repeatly defining them in multiple test modules. This also allows
centralized updates to the factory functions as needed.

Each factory function is designed to create and return a specific
test instance with default parameters suitable for testing.

They also provide standard references for checking expected values in many tests
without needing 'magic numbers' or hardcoded values in the tests themselves.

Because these complex instances may have interdependencies, the factory functions
are designed to call each other as needed to build up the required instances in
a consistent manner with a minimal likelihood of errors or obfuscating boilerplate
in the tests themselves.

For example, the `choice_factory()` factory function builds a `Choice` instance
by calling the `reporter_factory()` factory function with a configured `ChoicesConf`
from the `default_choices_conf()` factory function and extracting the `Choice` from the
`Reporter.choices` attribute since there is no direct way to create a properly configured
`Choice` instance without going through a `Reporter`.

This modular approach keeps the test code clean and focused on the specific instances being tested
instead of the boilerplate needed to create those instances.

Each factory function includes a docstring that describes the purpose of the function
and the default values it provides for testing. This documentation helps clarify
the intent and usage of each factory function and the significance of the default values chosen.

These docstrings should automatically appear in IDE tooltips and documentation generators,
making it easier for developers to understand the purpose and usage of each factory function
in context without needing to refer back to this module directly.

Most factory functions also accept an optional `cache_id` parameter that allows
distinguishing between different cached instances of the same type.
This is useful when multiple variations of a test instance are needed
within the same test suite. The `cache_id` parameter is passed to the
`cache_factory` decorator to manage caching behavior

The default value for `cache_id` is `CACHE_DEFAULT`, which indicates that
the default cached instance should be used. If `cache_id` is set to `None`,
caching is disabled for that call, and a new instance is created each time.

The cache can be cleared calling the `clear_cache()` function if needed to
reset the cached instances.
"""
from __future__ import annotations
from argparse import ArgumentParser, Namespace
import re
from pathlib import Path
from typing import Any, Iterable, TypeVar, Sequence


from tests.kwargs import ReporterKWArgs, ChoiceConfKWArgs, CaseKWArgs, ChoicesConfKWArgs
from tests.cache_factory import cached_factory, uncached_factory, CacheId, CACHE_DEFAULT
from tests.cache_factory import clear_cache as _clear_cache

from simplebench.case import Case
from simplebench.enums import Section, Target, Format, FlagType, Verbosity
from simplebench.iteration import Iteration
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices, ChoicesConf
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.results import Results
from simplebench.runners import SimpleRunner
from simplebench.session import Session
from simplebench.stats import OperationsPerInterval, MemoryUsage, OperationTimings, PeakMemoryUsage


T = TypeVar('T')


# wrapper to expose clear_cache function from cache_factory module
def clear_cache() -> None:
    """Clear the internal cache of cached factory instances.

    This forces subsequent calls to cached factory functions
    to create new instances instead of returning previously cached ones.
    """
    _clear_cache()


class DefaultExtra:
    """An immutable ReporterExtra subclass for testing ChoiceConf initialization."""
    def __init__(self, full_data: bool = False) -> None:
        """Constructs a DefaultExtra instance.

        Args:
            full_data (bool, default=False):
                Indicates whether the extra data is full or minimal.

        Raises:
            TypeError: If full_data is not a bool.
        """
        if not isinstance(full_data, bool):
            raise TypeError(f'full_data must be a bool, got {full_data!r}')
        self._full_data = full_data

    @property
    def full_data(self) -> bool:
        """Indicates whether the extra data is full or minimal."""
        return self._full_data


@cached_factory
def extra_factory(*, full_data: bool = True) -> DefaultExtra:
    """Return a default DefaultExtra instance for testing purposes.

    Args:
        full_data (bool, default=True):
            Indicates whether the extra data is full or minimal.
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        DefaultExtra: `DefaultExtra(full_data=True)`
    """
    return DefaultExtra(full_data=full_data)


def results_kwargs_factory() -> Results:
    """Returns a configured ResultsKWArgs instance for testing purposes.

    It creates a Results instance with default test parameters by calling
    the various factory functions for each parameter.

    Attributes:

        group = `case_group_factory()`
        title = `title_factory()`
        description = `description_factory()`
        n = `n_factory()`
        rounds = `rounds_factory()`
        total_elapsed = `total_elapsed_factory()`
        iterations = `iterations_sequence_factory()`
        variation_cols = `variation_cols_factory()`
        variation_marks = `variation_marks_factory()`
        interval_unit = `interval_unit_factory()`
        interval_scale = `interval_scale_factory()`
        ops_per_interval_unit = `ops_per_interval_unit_factory()`
        ops_per_interval_scale = `ops_per_interval_scale_factory()`
        memory_unit = `memory_unit_factory()`
        memory_scale = `memory_scale_factory()`
        ops_per_second = `ops_per_second_factory()`
        per_round_timings = `per_round_timings_factory()`
        memory = `memory_factory()`
        peak_memory = `peak_memory_factory()`
        extra_info = `results_extra_info_factory()`

    Returns:
        Results: A Results instance with default test parameters.
    """
    return Results(
        group=case_group_factory(),
        title=title_factory(),
        description=description_factory(),
        n=n_factory(),
        rounds=rounds_factory(),
        total_elapsed=total_elapsed_factory(),
        iterations=iterations_sequence_factory(),
        variation_cols=variation_cols_factory(),
        variation_marks=variation_marks_factory(),
        interval_unit=interval_unit_factory(),
        interval_scale=interval_scale_factory(),
        ops_per_interval_unit=ops_per_interval_unit_factory(),
        ops_per_interval_scale=ops_per_interval_scale_factory(),
        memory_unit=memory_unit_factory(),
        memory_scale=memory_scale_factory(),
        ops_per_second=ops_per_interval_factory(),
        per_round_timings=per_round_timings_factory(),
        memory=memory_factory(),
        peak_memory=peak_memory_factory(),
        extra_info=results_extra_info_factory()
    )


def ops_per_interval_factory() -> OperationsPerInterval:
    """Return a default ops per second value for testing purposes.

    Returns:
        OperationsPerInterval: Container for ops per interval data.
    """
    return OperationsPerInterval(
        iterations=[
           Iteration(
                n=n_factory(),
                elapsed=total_elapsed_factory(),
                scale=ops_per_interval_scale_factory(),
                unit=ops_per_interval_unit_factory(),
                memory=2000,
                peak_memory=3000)
        ],
        unit=ops_per_interval_unit_factory(),
        scale=ops_per_interval_scale_factory(),
        data=[100, 110, 90, 105, 95]
    )


def memory_unit_factory() -> str:
    """Return a default memory unit for testing purposes.

    Returns:
        str: `"bytes"`
    """
    return "bytes"


def memory_scale_factory() -> float:
    """Return a default memory scale for testing purposes.

    Returns:
        float: `1.0`
    """
    return 1.0


def ops_per_interval_unit_factory() -> str:
    """Return a default ops per interval unit for testing purposes.

    Returns:
        str: `Ops/s`
    """
    return 'Ops/s'


def ops_per_interval_scale_factory() -> float:
    """Return a default ops per interval scale for testing purposes.

    Returns:
        float: `1.0`
    """
    return 1.0


def interval_unit_factory() -> str:
    """Return a default interval unit for testing purposes.

    Returns:
        str: `"s"`
    """
    return "s"


def interval_scale_factory() -> float:
    """Return a default interval scale for testing purposes.

    Returns:
        float: `1.0`
    """
    return 1.0


def variation_marks_factory() -> dict[str, str]:
    """Return a default dictionary of variation marks for testing purposes.

    Returns:
        dict[str, str]: `{}`
    """
    return {}


def total_elapsed_factory() -> float:
    """Return a default total elapsed time for testing purposes.

    Returns:
        float: `6.0`
    """
    return 6.0


def n_factory() -> int:
    """Return a default number of iterations or rounds for testing purposes.

    Returns:
        int: `1`
    """
    return 1


def default_extra() -> DefaultExtra:
    """Return a default ReporterExtras instance for testing purposes.

    It always returns the same DefaultExtra instance created by extra_factory().

    Returns:
        DefaultExtra: `DefaultExtra(full_data=False)`
    """
    return extra_factory(full_data=False, cache_id=f'{__name__}.default_extra:singleton')


@cached_factory
def path_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Path:  # pylint: disable=unused-argument
    """Return a default Path instance for testing purposes.

    Args:
        cache_id (CacheId, default=CacheDefault):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        Path: `Path('/tmp/mock_report.txt')`
    """
    return Path('/tmp/mock_report.txt')


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
def case_group_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a default group string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"default_case_group"`

    """
    return "default_case_group"


def default_case_group() -> str:
    """Return a default group string for testing purposes.

    It always returns the same group string created by case_group_factory().

    Returns:
        str: `"default_case_group"`
    """
    return case_group_factory(cache_id=f'{__name__}.default_case_group:singleton')


@cached_factory
def title_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a title string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"Default Title"`
    """
    return "Default Title"


def default_title() -> str:
    """Return a default title string for testing purposes.

    It always returns the same title string created by title_factory().

    Returns:
        str: `"Default Title"`
    """
    return title_factory(cache_id=f'{__name__}.default_title:singleton')


def default_reporter_callback(
        *, case: Case, section: Section, output_format: Format, output: Any) -> None:  # pylint: disable=unused-argument
    """A default ReporterCallback conformant callback function for testing purposes.

    ```python

    def default_reporter_callback(
            *, case: Case, section: Section, output_format: Format, output: Any) -> None:
        return None
    ```
    """
    return None  # pragma: no cover


@cached_factory
def reporter_options_type_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> type[ReporterOptions]:   # pylint: disable=unused-argument
    """Return a default ReporterOptions type for testing purposes.

    Returns:
        type[ReporterOptions]: `ReporterOptions`
    """
    return ReporterOptions


def default_reporter_options_type() -> type[ReporterOptions]:
    """Return a default ReporterOptions type for testing purposes.

    It always returns the same ReporterOptions type returned by reporter_options_type_factory().

    Returns:
        type[ReporterOptions]: `ReporterOptions`
    """
    return reporter_options_type_factory(cache_id=f'{__name__}.default_reporter_options_type:singleton')


@cached_factory
def subdir_factory(*,
                   cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a default subdir string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"asubdir"`
    """
    return "asubdir"


def default_subdir() -> str:
    """Return a default subdir string for testing purposes.

    It always returns the same subdir string created by subdir_factory().

    Returns:
        str: `"asubdir"`
    """
    return subdir_factory(cache_id=f'{__name__}.default_subdir:singleton')


@cached_factory
def sections_factory(*,
                     cache_id: CacheId = CACHE_DEFAULT) -> tuple[Section, ...]:  # pylint: disable=unused-argument
    """Return a default tuple of Sections for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Section]: `(Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)`

    """
    return (Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)


def default_sections() -> tuple[Section, ...]:
    """Return a default tuple of Sections for testing purposes.

    It always returns the same tuple instance of Sections created by sections_factory().

    Returns:
        tuple[Section]: `(Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)`
    """
    return sections_factory(cache_id=f'{__name__}.default_sections:singleton')


@cached_factory
def targets_factory(*,
                    cache_id: CacheId = CACHE_DEFAULT) -> tuple[Target, ...]:  # pylint: disable=unused-argument
    """Return a default tuple of Targets for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Target]: `(Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)`
    """
    return (Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)


def default_targets() -> tuple[Target, ...]:
    """Return a default tuple of Targets for testing purposes.

    It always returns the same tuple instance of Targets created by targets_factory().

    Returns:
        tuple[Target]: `(Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)`
    """
    return targets_factory(cache_id=f'{__name__}.default_targets:singleton')


@cached_factory
def default_targets_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> tuple[Target]:  # pylint: disable=unused-argument
    """Return a default tuple for default_targets for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Target]: `(Target.CONSOLE,)`
    """
    return (Target.CONSOLE,)


def default_default_targets() -> tuple[Target]:
    """Return a default tuple for default_targets for testing purposes.

    Returns:
        tuple[Target]: `(Target.CONSOLE,)`
    """
    return default_targets_factory(cache_id=f'{__name__}.default_default_targets:singleton')


@cached_factory
def formats_factory(*,
                    cache_id: CacheId = CACHE_DEFAULT) -> tuple[Format]:  # pylint: disable=unused-argument
    """Return a default tuple of Formats for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Format]: `(Format.RICH_TEXT,)`
    """
    return (Format.RICH_TEXT,)


def default_formats() -> tuple[Format]:
    """Return a default tuple of Formats for testing purposes.
    It always returns the same tuple instance of Formats created by formats_factory().
    Returns:
        tuple[Format]: `(Format.RICH_TEXT,)`
    """
    return formats_factory(cache_id=f'{__name__}.default_formats:singleton')


@cached_factory
def output_format_factory(*,
                          cache_id: CacheId = CACHE_DEFAULT) -> Format:  # pylint: disable=unused-argument
    """Return a default Format for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        Format: `Format.RICH_TEXT`
    """
    return Format.RICH_TEXT


def default_output_format() -> Format:
    """Return a default Format for testing purposes.

    It always returns the same Format instance created by output_format_factory().

    Returns:
        Format: `Format.RICH_TEXT`
    """
    return output_format_factory(cache_id=f'{__name__}.default_output_format:singleton')


@cached_factory
def description_factory(*,
                        cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a description string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"A description for testing."`
    """
    return "A description for testing."


def default_description() -> str:
    """Return a default description string for testing purposes.

    It always returns the same description string created by description_factory().

    Returns:
        str: `"A description for testing."`
    """
    return description_factory(cache_id=f'{__name__}.default_description:singleton')


@cached_factory
def reporter_name_factory(*,
                          cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a default reporter name string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"default_reporter_name"`
    """
    return "default_reporter_name"


def default_reporter_name() -> str:
    """Return a default reporter name string for testing purposes.

    It always returns the same reporter name string created by reporter_name_factory().

    Returns:
        str: `"default_reporter_name"`
    """
    return reporter_name_factory(cache_id=f'{__name__}.default_reporter_name:singleton')


@cached_factory
def choice_name_factory(*,
                        cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a choice name string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"choice_name"`
    """
    return "choice_name"


def flag_name_factory() -> str:
    """Return a default flag name string for testing purposes.

    It always returns the same flag name string.
    Returns:
        str: `"--default-flag"`
    """
    return '--default-flag'


def default_choice_name() -> str:
    """Return a default choice name string for testing purposes.

    It always returns the same choice name string created by choice_name_factory().

    Returns:
        str: `"choice_name"`
    """
    return choice_name_factory(cache_id=f'{__name__}.default_choice_name:singleton')


@cached_factory
def choice_flags_factory(*,
                         cache_id: CacheId = CACHE_DEFAULT) -> tuple[str, ...]:  # pylint: disable=unused-argument
    """Return a tuple of flags for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        (tuple[str, ...]): `tuple(['--default-flag'])`
    """
    return tuple([flag_name_factory()])


def default_choice_flags() -> tuple[str, ...]:
    """Return a default tuple of choice flags for testing purposes.

    It always returns the same tuple of flags created by choice_flags_factory().

    Returns:
        (tuple[str, ...]): `tuple(['--default-flag'])`
    """
    return choice_flags_factory(cache_id=f'{__name__}.default_choice_flags:singleton')


@cached_factory
def flag_type_factory(*,
                      cache_id: CacheId = CACHE_DEFAULT) -> FlagType:  # pylint: disable=unused-argument
    """Return a FlagType for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        FlagType: `FlagType.TARGET_LIST`
    """
    return FlagType.TARGET_LIST


def default_flag_type() -> FlagType:
    """Return a default FlagType for testing purposes.

    It always returns the same FlagType created by flag_type_factory().

    Returns:
        FlagType: `FlagType.TARGET_LIST`
    """
    return flag_type_factory(cache_id=f'{__name__}.default_flag_type:singleton')


@cached_factory
def file_suffix_factory(*,
                        cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a default file suffix string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"suffix"`
    """
    return "suffix"


def default_file_suffix() -> str:
    """Return a default file suffix string for testing purposes.

    It always returns the same file suffix string created by file_suffix_factory().

    Returns:
        str: `"suffix"`
    """
    return file_suffix_factory(cache_id=f'{__name__}.default_file_suffix:singleton')


@cached_factory
def file_unique_factory() -> bool:
    """Return a default file unique boolean for testing purposes.

    It always returns `True`.

    This is coordinated with `default_file_append()` to ensure that
    file_unique is `True` and file_append is `False`, which are compatible settings.

    Returns:
        bool: `True`
    """
    return True


def default_file_unique() -> bool:
    """Return a default file unique boolean for testing purposes.

    It always returns the same boolean created by file_unique_factory().

    Returns:
        bool: `True`
    """
    return file_unique_factory(cache_id=f'{__name__}.default_file_unique:singleton')


@cached_factory
def file_append_factory() -> bool:
    """Return a default file append boolean for testing purposes.

    It always returns `False`.

    This is coordinated with `default_file_unique()` to ensure that
    file_unique is `True` and file_append is `False`, which are compatible settings.

    Returns:
        bool: `False`
    """
    return False


def default_file_append() -> bool:
    """Return a default file append boolean for testing purposes.

    It always returns the same boolean created by file_append_factory().

    Returns:
        bool: `False`
    """
    return file_append_factory(cache_id=f'{__name__}.default_file_append:singleton')


@cached_factory
def report_output_factory(*,
                          cache_id: CacheId = CACHE_DEFAULT) -> str:  # pylint: disable=unused-argument
    """Return a report output string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        str: `"Rendered Report"`
    """
    return "Rendered Report"


def default_report_output() -> str:
    """Return a default report output string for testing purposes.

    It always returns the same report output string created by report_output_factory().

    Returns:
        str: `"Rendered Report"`
    """
    return report_output_factory(cache_id=f'{__name__}.default_report_output:singleton')


@uncached_factory
def report_parameters_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, Any]:
    """Return report parameters for testing purposes.

    It is uncached by default to ensure that each call returns a fresh dictionary.
    This can be overridden by providing a non-None cache_id.

    Because the parameters include mutable instances like Case and Choice,
    it is important to use cache_id appropriately to avoid unintended side effects
    from shared instances in tests.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        dict[str, Any]: A dictionary of default report parameters.
    """
    return {
        'args': namespace_factory(),
        'case': case_factory(cache_id=cache_id),
        'choice': choice_factory(cache_id=cache_id),
        'path': path_factory(cache_id=cache_id),
        'session': session_factory(cache_id=cache_id),
        'callback': default_reporter_callback
    }


@cached_factory
def minimal_case_kwargs_factory(*,
                                cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:  # pylint: disable=unused-argument
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
def iterations_factory(*,
                       cache_id: CacheId = CACHE_DEFAULT) -> int:  # pylint: disable=unused-argument
    """Return a default number of iterations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        int: `100`
    """
    return 100


def default_iterations() -> int:
    """Return a default number of iterations for testing purposes.

    It always returns the same number instance created by iterations_factory().

    Returns:
        int: `100`
    """
    return iterations_factory(cache_id=f'{__name__}.default_iterations:singleton')


@cached_factory
def warmup_iterations_factory(*,
                              cache_id: CacheId = CACHE_DEFAULT) -> int:  # pylint: disable=unused-argument
    """Return a default number of warmup iterations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        int: `100`
    """
    return 100


def default_warmup_iterations() -> int:
    """Return a default number of warmup iterations for testing purposes.

    It always returns the same number instance created by warmup_iterations_factory().

    Returns:
        int: `100`
    """
    return warmup_iterations_factory(cache_id=f'{__name__}.default_warmup_iterations:singleton')


@cached_factory
def rounds_factory(*,
                   cache_id: CacheId = CACHE_DEFAULT) -> int:  # pylint: disable=unused-argument
    """Return a default number of rounds for testing purposes.

    This is for use in configuring benchmark cases in tests.

    The number is set unusually high to facilitate testing of the code
    that handles multiple rounds. A simplerunner should be able to handle
    any positive integer number of rounds but there are internal optimizations
    that may behave differently with higher numbers of rounds.

    Returns:
        int: `1500`
    """
    return 1500


def default_rounds() -> int:
    """Return a default number of rounds for testing purposes.

    It always returns the same number instance created by rounds_factory().

    Returns:
        int: `1500`
    """
    return rounds_factory(cache_id=f'{__name__}.default_rounds:singleton')


@cached_factory
def min_time_factory(*,
                     cache_id: CacheId = CACHE_DEFAULT) -> float:  # pylint: disable=unused-argument
    """Return a default minimum time for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        float: `0.1`
    """
    return 0.1


def default_min_time() -> float:
    """Return a default minimum time for testing purposes.

    It always returns the same number instance created by min_time_factory().

    Returns:
        float: `0.1`
    """
    return min_time_factory(cache_id=f'{__name__}.default_min_time:singleton')


@cached_factory
def max_time_factory(*,
                     cache_id: CacheId = CACHE_DEFAULT) -> float:  # pylint: disable=unused-argument
    """Return a default maximum time for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    This is for use in configuring benchmark cases in tests.

    Returns:
        float: `10.0`
    """
    return 10.0


def default_max_time() -> float:
    """Return a default maximum time for testing purposes.

    It always returns the same number instance created by max_time_factory().

    Returns:
        float: `10.0`
    """
    return max_time_factory(cache_id=f'{__name__}.default_max_time:singleton')


@cached_factory
def variation_cols_factory(*,
                           cache_id: CacheId = CACHE_DEFAULT) -> dict[str, str]:  # pylint: disable=unused-argument
    """Return a dictionary of variation columns for testing purposes.

    This is for use in configuring benchmark cases in tests.

    This is a minimal case without any variation columns.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        (dict[str, str]): `{}`
    """
    return {}


@cached_factory
def kwargs_variations_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> dict[str, list[Any]]:  # pylint: disable=unused-argument
    """Return a set of kwargs variations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    This is a minimal case without any kwargs variations.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        (dict[str, list[Any]]): `{}`
    """
    return {}


@cached_factory
def runner_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> type[SimpleRunner]:  # pylint: disable=unused-argument
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
def reporter_options_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> ReporterOptions:  # pylint: disable=unused-argument
    """Return a ReporterOptions instance for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        ReporterOptions: `ReporterOptions`
    """
    return ReporterOptions()


def default_reporter_options() -> ReporterOptions:
    """Return a default ReporterOptions instance for testing purposes.

    It always returns the same ReporterOptions instance created by reporter_options_factory().

    Returns:
        ReporterOptions: `ReporterOptions`
    """
    return reporter_options_factory(cache_id=f'{__name__}.default_reporter_options:singleton')


@cached_factory
def reporter_options_tuple_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> tuple[ReporterOptions]:  # pylint: disable=unused-argument
    """Return a tuple containing a ReporterOptions instance for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[ReporterOptions]: A tuple containing a ReporterOptions instance.
    """
    return (default_reporter_options(),)


def default_reporter_options_tuple() -> tuple[ReporterOptions]:
    """Return a default tuple containing a ReporterOptions instance for testing purposes.

    It always returns the same tuple created by reporter_options_tuple_factory().

    Returns:
        tuple[ReporterOptions]: A tuple containing a ReporterOptions instance.
    """
    return reporter_options_tuple_factory(cache_id=f'{__name__}.default_reporter_options_tuple:singleton')


@cached_factory
def case_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:
    """Return a default configured CaseKWargs for testing purposes.

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
    return CaseKWArgs(
        group=default_case_group(),
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
        options=default_reporter_options_tuple()
    )


@uncached_factory
def case_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Case:   # pylint: disable=unused-argument
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
    return Session(
        cases=[case_factory(cache_id=cache_id)],
        verbosity=Verbosity.QUIET)


def namespace_factory(*, argparser: ArgumentParser | None = None, args: Sequence[str] | None = None) -> Namespace:
    """Return an ArgumentParser Namespace instance for testing purposes.


    If passed an ArgumentParser instance, it uses that to parse the arguments (if provided).
    Otherwise, it creates a new ArgumentParser instance with a default program name of 'simplebench'.

    It never performs caching of calls.

    Args:
        argparser (ArgumentParser | None, default=None):
            An optional ArgumentParser instance to use for parsing.
        args (Sequence[str] | None, default=None):
            An optional sequence of command-line arguments to parse.

    Returns:
        Namespace: An ArgumentParser Namespace instance.
    """
    if args is None:
        args = []

    if argparser is not None:
        return argparser.parse_args(args=args)
    arg_parser = ArgumentParser(prog='simplebench')
    return arg_parser.parse_args(args=args)


def boolean_flag_factory(flag: str, default: bool = False) -> dict[str, Any]:
    """Returns an argument parser flag configuration for a boolean flag.

    The default value determines whether the flag enables or disables the feature.
    - If default is False, the flag enables the feature when present.
    - If default is True, the flag disables the feature when present.

    Args:
        flag (str):
            The name of the flag (including the leading dashes).
        default (bool, default=False):
            The default value for the flag.

    Returns:
        (dict[str, Any]): A dictionary suitable for unpacking as argparser.add_argument() flag parameters.

    return {
        'flag': flag,
        'action': 'store_true' if not default else 'store_false',
        'default': default,
        'help': f'Enable {flag.lstrip("-")}' if not default else f'Disable {flag.lstrip("-")}'
    }
    """
    if not isinstance(flag, str):
        raise TypeError("'flag' argument must be a string")
    if not flag.startswith('--'):
        raise ValueError("'flag' argument must start with '--'")
    if not re.match(r'^--[A-Za-z0-9\-_.]+$', flag):
        raise ValueError(
            "'flag' argument contains invalid characters for a command-line flag. "
            "It must be prefixed with '--' and only letters, numbers, hyphens, underscores, "
            "and periods are allowed after the prefix.")
    if not isinstance(default, bool):
        raise TypeError("default arg must be a boolean")

    return {
        'name_or_flags': flag,
        'action': 'store_true' if not default else 'store_false',
        'default': default,
        'help': f'Enable {flag.lstrip("-")}' if not default else f'Disable {flag.lstrip("-")}'
    }


def list_of_strings_flag_factory(flag: str,
                                 choices: Iterable[str] | None = None,
                                 description: str = 'Help string') -> dict[str, Any]:
    """Returns an argument parser flag configuration for a list flag

    It is suitable to multiple values being provided by repeating the flag
    on the command line, e.g.:

        `--flag value1 --flag value2 value3`

    It sets the nargs to '*' to allow zero or more values per flag occurrence.

    No caching is performed for this factory function.
    Args:
        flag (str):
            The name of the flag (including the leading dashes).
        choices (Iterable[str] | None, default=None):
            An optional iterable of valid string choices for the flag values.
            If None, no choices are enforced.
        description (str, default='Help string'):
            A help string description for the flag.

    Returns:
        (dict[str, Any]): A dictionary suitable for unpacking as argparser.add_argument() flag parameters.
    """
    if not isinstance(flag, str):
        raise TypeError("'flag' argument must be a string")
    if not flag.startswith('--'):
        raise ValueError("'flag' argument must start with '--'")
    if not re.match(r'^--[A-Za-z0-9\-_.]+$', flag):
        raise ValueError(
            "'flag' argument contains invalid characters for a command-line flag. "
            "It must be prefixed with '--' and only letters, numbers, hyphens, underscores, "
            "and periods are allowed after the prefix.")

    if not (choices is None or isinstance(choices, Iterable)):
        raise TypeError("'choices' argument must be an iterable of strings")
    if choices is not None:
        for choice in choices:
            if not isinstance(choice, str):
                raise TypeError("all items in 'choices' must be strings")

    if not isinstance(description, str):
        raise TypeError("'description' argument must be a string")

    return {
        'name_or_flags': flag,
        'action': 'append',
        'nargs': '*',
        'choices': choices,
        'help': description,
    }


def argument_parser_factory(prog: str = 'simplebench',
                            arguments: Sequence[dict[str, Any]] | None = None) -> ArgumentParser:
    """Return an ArgumentParser instance for testing purposes.

    It creates an ArgumentParser with the specified program name and adds any provided arguments.

    No caching is performed for this factory function.

    Args:
        prog (str, default='simplebench'):
            The program name for the ArgumentParser.
        arguments (Sequence[dict[str, Any]] | None, default=None):
            An optional sequence of argument configurations to add to the parser.
            Each argument configuration should be a dictionary suitable for
            unpacking into the `add_argument()` method of ArgumentParser.
    Returns:
        ArgumentParser: An ArgumentParser instance.
    """
    if not isinstance(prog, str):
        raise TypeError("'prog' argument must be a string")
    if arguments is not None:
        if not isinstance(arguments, Sequence):
            raise TypeError("'arguments' argument must be a sequence of dictionaries")
        for arg in arguments:
            if not isinstance(arg, dict):
                raise TypeError("each item in 'arguments' must be a dictionary")
    if arguments is not None:
        parser = ArgumentParser(prog=prog)
        for arg in arguments:
            name_or_flags = arg.get('name_or_flags')
            if name_or_flags is None:
                raise ValueError("each argument dictionary must contain a 'name_or_flags' key")
            kwargs = {k: v for k, v in arg.items() if k != 'name_or_flags'}
            parser.add_argument(name_or_flags, **kwargs)
        return parser
    return ArgumentParser(prog=prog)


class FactoryReporter(Reporter):
    """A dummy reporter subclass for testing purposes.

    No parameters are preset for this reporter and no defaults are provided.

    Provides a shim implementation of run_report() and render() methods to allow
    instantiation and testing of the Reporter base class functionality with
    both good and bad parameters.

    """
    def __init__(
            self,
            name: str | None = None,
            description: str | None = None,
            options_type: ReporterOptions | None = None,
            sections: Iterable[Section] | None = None,
            targets: Iterable[Target] | None = None,
            formats: Iterable[Format] | None = None,
            choices: ChoicesConf | None = None,
            subdir: str | None = None,
            file_suffix: str | None = None,
            file_unique: str | None = None,
            file_append: str | None = None) -> None:
        """Initialize Reporter with provided kwargs.

        Args:
            name (str | None): Name of the reporter.
            description (str | None): Description of the reporter.
            options_type (ReporterOptions | None): Options type for the reporter.
            sections (Iterable[Section] | None): Supported sections for the reporter.
            targets (Iterable[Target] | None): Supported targets for the reporter.
            formats (Iterable[Format] | None): Supported formats for the reporter.
            choices (ChoicesConf | None): ChoicesConf for the reporter.
            subdir (str | None): Subdirectory for the reporter.
            file_suffix (str | None): File suffix for the reporter.
            file_unique (str | None): File unique flag for the reporter.
            file_append (str | None): File append flag for the reporter.
        """
        # Types don't match because we are TESTING the base class parameter validation code.
        # This is expected and intentional.
        super().__init__(
            name=name,  # type: ignore[arg-type,reportArgumentType]
            description=description,  # type: ignore[arg-type,reportArgumentType]
            options_type=options_type,  # type: ignore[arg-type,reportArgumentType]
            sections=sections,  # type: ignore[arg-type,reportArgumentType]
            targets=targets,  # type: ignore[arg-type,reportArgumentType]
            formats=formats,  # type: ignore[arg-type,reportArgumentType]
            choices=choices,  # type: ignore[arg-type,reportArgumentType]
            subdir=subdir,  # type: ignore[arg-type,reportArgumentType]
            file_suffix=file_suffix,  # type: ignore[arg-type,reportArgumentType]
            file_unique=file_unique,  # type: ignore[arg-type,reportArgumentType]
            file_append=file_append  # type: ignore[arg-type,reportArgumentType]
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None) -> None:
        """Run the report with the given arguments, case, and choice.

        Args:
            args (Namespace):
            Parsed command-line arguments.
            case (Case):
                The benchmark `Case` to report on.
            choice (Choice):
                The `Choice` configuration for the report.
            path (Path | None, default=None):
                Optional file `Path` for the report output.
            session (Session | None, default=None):
                Optional `Session` context for the report.
            callback (ReporterCallback | None, default=None):
                Optional `ReporterCallback` function for the report.

        Return:
            None
        """
        self.render_by_case(
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """Render the report for the given case, section, and options."""
        return default_report_output()


class ConfiguredReporterOptions(ReporterOptions):
    """A mock ReporterOptions subclass for testing purposes."""


def default_options_type() -> type[ConfiguredReporterOptions]:
    """Return a default ReporterOptions type for testing purposes."""
    return ConfiguredReporterOptions


@cached_factory
def reporter_kwargs_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> ReporterKWArgs:  # pylint: disable=unused-argument
    """Return a preconfigured ReporterKWArgs instance for testing purposes.

    The returned ReporterKWArgs instance is preconfigured for testing and is immutable.

    It is cached by default to ensure that repeated calls return the same instance.
    This is safe because ReporterKWArgs is immutable and will always return the same values
    for the same attributes, behaving consistently across tests.

    If there is a need for a fresh instance, provide a unique cache_id or set cache_id to `None`.

    It contains all parameters set to explicit default values for testing purposes:

    ```python

    ReporterKWArgs(
        name=default_name(),
        description=default_description(),
        sections=default_sections(),
        targets=default_targets(),
        formats=default_formats(),
        choices=default_choices_confs(),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )
    ```

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        ReporterKWArgs: A preconfigured instance with default values for testing.
    """
    return ReporterKWArgs(
        name=default_reporter_name(),
        description=default_description(),
        options_type=default_options_type(),
        sections=default_sections(),
        targets=default_targets(),
        formats=default_formats(),
        choices=default_choices_conf(),
        subdir='',
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )


def default_reporter_kwargs() -> ReporterKWArgs:
    """A preconfigured ReporterKWArgs instance for testing purposes.

    It always returns the same ReporterKWArgs instance created by reporter_kwargs_factory().

    ReporterKWArgs(
        name=default_name(),
        description=default_description(),
        sections=default_sections(),
        targets=default_targets(),
        formats=default_formats(),
        choices=default_choices_confs(),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )

    Returns:
        ReporterKWArgs: A preconfigured instance with default values for testing.
    """
    return reporter_kwargs_factory(cache_id=f'{__name__}.default_reporter_kwargs:singleton')


@cached_factory
def choice_conf_kwargs_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> ChoiceConfKWArgs:  # pylint: disable=unused-argument
    """Return a ChoiceConfKWArgs for testing purposes.

    It contains all parameters set to explicit default values for testing purposes.
    Because ChoiceConfKWArgs has many parameters, they are listed here for clarity:

    ```python

       ChoiceConfKWArgs(
            flags=default_choice_flags(),
            flag_type=default_flag_type(),
            name=default_choice_name(),
            description=default_description(),
            subdir=default_subdir(),
            sections=default_sections(),
            targets=default_targets(),
            default_targets=default_default_targets(),
            output_format=default_output_format(),
            file_suffix=default_file_suffix(),
            file_unique=default_file_unique(),
            file_append=default_file_append(),
            options=default_reporter_options(),
            extra=default_extra()
       )
    ```
    Returns:
        ChoiceConfKWArgs: A default ChoiceConfKWArgs instance.
    """
    return ChoiceConfKWArgs(
        flags=default_choice_flags(),
        flag_type=default_flag_type(),
        name=default_choice_name(),
        description=default_description(),
        subdir=default_subdir(),
        sections=default_sections(),
        targets=default_targets(),
        default_targets=default_default_targets(),
        output_format=default_output_format(),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append(),
        options=default_reporter_options(),
        extra=default_extra()
    )


def default_choice_conf_kwargs() -> ChoiceConfKWArgs:
    """Return default `ChoicesConfKWArgs` for testing purposes.

    It always returns the same `ChoiceConf` instance created by `choice_conf_kwargs_factory()`.
    It is safe to cache this instance because `ChoiceConfKWArgs` is immutable. It will always
    return the same values for the same attributes and behaves consistently across tests.

    ```python

       ChoiceConfKWArgs(
            flags=default_choice_flags(),
            flag_type=default_flag_type(),
            name=default_choice_name(),
            description=default_description(),
            subdir=default_subdir(),
            sections=default_sections(),
            targets=default_targets(),
            default_targets=default_default_targets(),
            output_format=default_output_format(),
            file_suffix=default_file_suffix(),
            file_unique=default_file_unique(),
            file_append=default_file_append(),
            options=default_reporter_options(),
            extra=default_extra()
       )
    ```

    Returns:
        ChoicesConfKWArgs: A default ChoicesConfKWArgs instance.
    """
    return choice_conf_kwargs_factory(cache_id=f'{__name__}.default_choice_conf_kwargs:singleton')


@cached_factory
def choices_conf_kwargs_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConfKWArgs:  # pylint: disable=unused-argument
    """Return default ChoicesConfKWArgs for testing purposes.

    It contains a single ChoiceConf created by default_choice_conf_kwargs().

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        ChoicesConfKWArgs: A default ChoicesConfKWArgs instance.
    """
    return ChoicesConfKWArgs()


def default_choices_conf_kwargs() -> ChoicesConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It always returns the same ChoicesConfKWArgs instance created by choices_conf_kwargs_factory().

    Returns:
        ChoicesConfKWArgs: A default ChoicesConfKWArgs instance.
    """
    return choices_conf_kwargs_factory(cache_id=f'{__name__}.default_choices_conf_kwargs:singleton')


@cached_factory
def choice_conf_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT,  # pylint: disable=unused-argument
        name: str | None = None,
        flags: tuple[str, ...] | None = None) -> ChoiceConf:
    """Factory function to return the same mock ChoiceConf instance for testing.

    It caches the instance based on the cache_id, name, and flags so that multiple calls with
    the same combination always return the same instance.

    If name is None, the default name from default_choice_name() is used.
    If flags is None, the default flags from default_choice_flags() are used.

    The caching behavior can be overridden by providing a unique cache_id or setting cache_id to None.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different ChoiceConf instances if needed.
            If None, caching is disabled for this call.
        name (str | None, default=None):
            The name of the ChoiceConf instance.
        flags (tuple[str, ...] | None, default=None):
            The flags associated with the ChoiceConf instance.
    """
    return ChoiceConf(
        flags=default_choice_flags() if flags is None else flags,
        flag_type=default_flag_type(),
        name=default_choice_name() if name is None else name,
        description=default_description(),
        sections=default_sections(),
        targets=default_targets(),
        output_format=default_output_format(),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append(),
        options=default_reporter_options(),
        extra=default_extra())


def default_choice_conf() -> ChoiceConf:
    """Return a default ChoiceConf instance for testing purposes.

    It is created by calling ChoiceConf with default_choice_conf_kwargs().

    It always returns the same instance for consistency in tests. Because
    ChoiceConf instances are immutable after creation, this is safe.

    Returns:
        ChoiceConf: A default ChoiceConf instance.
    """
    return choice_conf_factory(cache_id=f'{__name__}.default_choice_conf:singleton')


@uncached_factory
def choice_factory(*,
                   cache_id: CacheId = CACHE_DEFAULT,
                   name: str | None = None,
                   flags: tuple[str, ...] | None = None) -> Choice:
    """Factory function to return a single cached Choice instance for testing.

    The choice instance is created using MockReporter() and is
    extracted from the MockReporter.choices attribute.

    It is uncached by default to ensure that each call returns a fresh Choice instance.
    This can be overridden by providing a non-None cache_id.

    If cached, multiple calls with the same cache_id, name, and flags
    return the same instance.

    Because choice instances embed state related to the reporter they belong to,
    it is important to use cache_id appropriately to avoid unintended side effects
    from shared instances in tests.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different Choice instances if needed.
            If None, caching is disabled for this call.

        name (str | None, default=None):
            The name of the Choice instance.

            If None, the default name from default_choice_name() is used.

        flags (tuple[str, ...] | None, default=None):
            The flags associated with the Choice instance.

            If None, the default flags from default_choice_flags() are used.

            Tuple is used to ensure hashability for caching.
    """
    if name is None:
        name = default_choice_name()
    if flags is None:
        flags = default_choice_flags()
    if not isinstance(name, str):
        raise TypeError(f"Invalid type for name argument: {name!r}")
    if not isinstance(flags, tuple) or not all(isinstance(f, str) for f in flags):
        raise TypeError(f"Invalid type for flags argument: {flags!r}")
    if flags is not None or name is not None:
        choices_conf = choices_conf_factory(
            cache_id=cache_id,
            choices=(choice_conf_factory(cache_id=cache_id, name=name, flags=flags),))
    else:
        choices_conf = choices_conf_factory(cache_id=cache_id)
    kwargs = default_reporter_kwargs().replace(choices=choices_conf)
    reporter = reporter_factory(cache_id=cache_id, reporter_kwargs=kwargs)
    return reporter.choices[name]


@cached_factory
def choices_conf_factory(*, choices: tuple[ChoiceConf, ...] | None = None) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different ChoicesConf instances if needed.
            If None, caching is disabled for this call.
        choices (tuple[ChoiceConf, ...] | None, default=None):
            A tuple of ChoiceConf instances to initialize the ChoicesConf with.

            If None, a default ChoicesConf instance with a single ChoiceConf
            instance created by default_choice_conf() is returned.

            Tuple is used to ensure hashability for caching.
    """
    if choices is None:
        choices = (default_choice_conf(),)

    if not isinstance(choices, tuple) or not all(isinstance(c, ChoiceConf) for c in choices):
        raise TypeError(f"Invalid type for choices argument (should be tuple[ChoiceConf, ...]): {choices!r}")

    return ChoicesConf(choices)


def default_choices_conf() -> ChoicesConf:
    """Return a default ChoicesConf instance for testing purposes.

    It always returns the same ChoicesConf instance created by choices_conf_factory().

    Returns:
        ChoicesConf: A default ChoicesConf instance.
    """
    return choices_conf_factory(cache_id=f'{__name__}.default_choices_conf:singleton')


@uncached_factory
def reporter_factory(
        *,
        cache_id: CacheId = CACHE_DEFAULT,  # pylint: disable=unused-argument
        reporter_kwargs: ReporterKWArgs | None = None) -> FactoryReporter:
    """Factory function to return an uncached FactortyReporter instance for testing.

    By default, it uses default_reporter_kwargs() to provide a set of parameters
    to initialize the FactoryReporter. However, custom parameters can be provided
    via the reporter_kwargs argument.

    It does not cache the created FactoryReporter instance by default, so each call
    returns a new instance.

    To override this caching behavior, provide a non-None cache_id and it will be cached
    based on that identifier.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different UnconfiguredReporter instances if needed.
            If None, caching is disabled for this call.
        reporter_kwargs (ReporterKWArgs | None, default=None):
            Keyword arguments to initialize the UnconfiguredReporter.

            If none, default_reporter_kwargs() is used to provide a default set of parameters.
    """
    if reporter_kwargs is not None and not isinstance(reporter_kwargs, ReporterKWArgs):
        raise TypeError(f"Invalid type for reporter_kwargs argument: {reporter_kwargs!r}")
    kwargs = default_reporter_kwargs() if reporter_kwargs is None else reporter_kwargs
    return FactoryReporter(**kwargs)


@cached_factory
def choices_factory(*,
                    cache_id: CacheId = CACHE_DEFAULT,
                    choices: tuple[ChoiceConf, ...] | ChoicesConf | None = None) -> Choices:
    """Factory function to return a cached Choices instance for testing.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different Choices instances if needed.
            If None, caching is disabled for this call.
        choices (tuple[ChoiceConf, ...] | ChoicesConf | None, default=None):
            A sequence of ChoiceConf instances or a ChoicesConf instance to initialize the Choices instance.
    """
    if choices is None:
        return Choices()

    if isinstance(choices, tuple) and all(isinstance(c, ChoiceConf) for c in choices):
        choices_conf = ChoicesConf(choices)
    elif isinstance(choices, ChoicesConf):
        choices_conf = choices
    else:
        raise TypeError(f"Invalid type for choices argument: {choices!r}")

    kwargs = default_reporter_kwargs().replace(choices=choices_conf)
    reporter = reporter_factory(cache_id=cache_id, reporter_kwargs=kwargs)
    return reporter.choices


def reporter_namespace_factory(args: list[str],
                               choices: list[str] | None = None) -> Namespace:
    """Create a parsed `argparse.Namespace` for testing.

    It create a default argument parser with a flag named according to
    the `flag_name_factory()` function and with choices corresponding to
    the `Target` enum values. It then parses the provided args list
    and returns the resulting `Namespace`.

    Args:
        args: A list of strings representing command-line arguments to be parsed.
        choices: An optional list of valid choices for the reporter target flag.

                 If `None`, it defaults to
                 `[Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value]`

    """
    if not isinstance(args, list):
        raise TypeError("args must be a list of strings")
    if not all(isinstance(arg, str) for arg in args):
        raise TypeError("all items in args must be strings")
    if choices is None:
        choices = [Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value]
    return argument_parser_factory(
            arguments=[
                list_of_strings_flag_factory(
                    flag=flag_name_factory(),
                    choices=choices,
                    description='Select reporter targets.')]).parse_args(args=args)
