"""Factories for creating primitive test values (strings, numbers, enums).

These factories produce the basic building blocks used by more complex object
factories in other modules.
"""
# pylint: disable=unused-argument
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TypeAlias, overload

from rich.table import Table
from rich.text import Text

from simplebench.enums import FlagType, Format, Section, Target

from ..cache_factory import CACHE_DEFAULT, CacheId, cached_factory

Output: TypeAlias = str | bytes | Text | Table


def default_output_text() -> str:
    """Return default output for testing purposes.

    Returns:
        str: "Default Output"
    """
    return "Default Output"


def default_output() -> Output:
    """Return default output for testing purposes.

    Returns:
        Output: Text("Default Output")
    """
    return Text("Default Output")


def default_section() -> Section:
    """Return a single default Section for testing purposes.

    Returns:
        Section: Section.OPS
    """
    return Section.OPS


def default_filename_base() -> str:
    """Return a default filename base string for testing purposes.

    Returns:
        str: "A Report Name"
    """
    return "A Report Name"


# overloads provide a tooltip assist for the decorated function and IDE tooltips
# that is needed because the cache_factory decorators create a function
# with a confusing tooltip (inherently).
@overload
def output_path_factory() -> Path:
    """Return a default output Path instance for testing purposes.

    This path points to a directory inside the system's temporary directory.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        Path: A Path object pointing to a directory in the temporary directory.
    """


@overload
def output_path_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Path:
    """Return a default output Path instance for testing purposes.

    This path points to a directory inside the system's temporary directory.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        Path: A Path object pointing to a directory in the temporary directory.
    """


@cached_factory
def output_path_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Path:
    """Return a default output Path instance for testing purposes.

    This path points to a directory inside the system's temporary directory.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        Path: A Path object pointing to a file in the temporary directory.
    """
    # Use tempfile.gettempdir() to get a cross-platform temporary directory
    # e.g., '/tmp' on Linux, 'C:\Users\...\AppData\Local\Temp' on Windows
    return Path(tempfile.gettempdir())


@cached_factory
def n_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> int:
    """Return a default number of iterations or rounds for testing purposes.

    Returns:
        int: `1`
    """
    return 1


@cached_factory
def case_group_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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
def title_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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


@cached_factory
def subdir_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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
def sections_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Section, ...]:
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
def targets_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Target, ...]:
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
def default_targets_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Target]:
    """Return a default tuple for default_targets for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Target]: `(Target.CONSOLE,)`
    """
    return (Target.CONSOLE, )


def default_default_targets() -> tuple[Target]:
    """Return a default tuple for default_targets for testing purposes.

    Returns:
        tuple[Target]: `(Target.CONSOLE,)`
    """
    return default_targets_factory(cache_id=f'{__name__}.default_default_targets:singleton')


@cached_factory
def formats_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Format]:
    """Return a default tuple of Formats for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Format]: `(Format.RICH_TEXT,)`
    """
    return (Format.RICH_TEXT, )


def default_formats() -> tuple[Format]:
    """Return a default tuple of Formats for testing purposes.
    It always returns the same tuple instance of Formats created by formats_factory().
    Returns:
        tuple[Format]: `(Format.RICH_TEXT,)`
    """
    return formats_factory(cache_id=f'{__name__}.default_formats:singleton')


@cached_factory
def output_format_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Format:
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
def description_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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
def reporter_name_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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
def choice_name_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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
def choice_flags_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[str, ...]:
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
def flag_type_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> FlagType:
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
def file_suffix_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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
def report_output_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
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


@cached_factory
def iterations_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> int:
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
def warmup_iterations_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> int:
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
def rounds_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> int:
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
def min_time_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
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
def max_time_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default maximum time for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    This is for use in configuring benchmark cases in tests.

    Returns:
        float: `0.2`
    """
    return 0.2


def default_max_time() -> float:
    """Return a default maximum time for testing purposes.

    It always returns the same number instance created by max_time_factory().

    Returns:
        float: `0.2`
    """
    return max_time_factory(cache_id=f'{__name__}.default_max_time:singleton')


@cached_factory
def variation_cols_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, str]:
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
def kwargs_variations_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, list]:
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
def total_elapsed_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default total elapsed time for testing purposes.

    Returns:
        float: `6.0`
    """
    return 6.0


@cached_factory
def interval_unit_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default interval unit for testing purposes.

    Returns:
        str: `"s"`
    """
    return "s"


@cached_factory
def interval_scale_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default interval scale for testing purposes.

    Returns:
        float: `1.0`
    """
    return 1.0


@cached_factory
def ops_per_interval_unit_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default ops per interval unit for testing purposes.

    Returns:
        str: `Ops/s`
    """
    return 'Ops/s'


@cached_factory
def ops_per_interval_scale_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default ops per interval scale for testing purposes.

    Returns:
        float: `1.0`
    """
    return 1.0


@cached_factory
def memory_unit_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default memory unit for testing purposes.

    Returns:
        str: `"bytes"`
    """
    return "bytes"


@cached_factory
def memory_scale_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default memory scale for testing purposes.

    Returns:
        float: `1.0`
    """
    return 1.0


@cached_factory
def variation_marks_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, str]:
    """Return a default dictionary of variation marks for testing purposes.

    Returns:
        dict[str, str]: `{}`
    """
    return {}
