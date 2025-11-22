"""Factories for creating primitive test values (strings, numbers, enums).

These factories produce the basic building blocks used by more complex object
factories in other modules.
"""
# pylint: disable=unused-argument
from __future__ import annotations

from pathlib import Path
from typing import TypeAlias, overload

from rich.table import Table
from rich.text import Text

from simplebench.enums import FlagType, Format, Section, Target

from ..cache_factory import CACHE_DEFAULT, CacheId, cached_factory
from .path import path_factory

Output: TypeAlias = str | bytes | Text | Table


def default_output_str() -> str:
    """Return default output for testing purposes.

    :return: "Default Output"
    :rtype: str
    """
    return "Default Output"


def default_output() -> Output:
    """Return default output for testing purposes.

    :return: Text("Default Output")
    :rtype: Output
    """
    return Text("Default Output")


def default_format() -> Format:
    """Return a default Format for testing purposes.

    :return: Format.RICH_TEXT
    :rtype: Format
    """
    return Format.RICH_TEXT


def default_format_plain() -> Format:
    """Return a default Format.PLAIN_TEXT for testing purposes.

    :return: Format.PLAIN_TEXT
    :rtype: Format
    """
    return Format.PLAIN_TEXT


def default_section() -> Section:
    """Return a single default Section for testing purposes.

    :return: Section.OPS
    :rtype: Section
    """
    return Section.OPS


def default_filename_base() -> str:
    """Return a default filename base string for testing purposes.

    It has to be a valid filename stem (alphanumeric, no spaces, not empty or blank).

    :return: "ReportName"
    :rtype: str
    """
    return "ReportName"


# overloads provide a tooltip assist for the decorated function and IDE tooltips
# that is needed because the cache_factory decorators create a function
# with a confusing tooltip (inherently).
@overload
def output_path_factory() -> Path:
    """Return a default output Path instance for testing purposes.

    This path points to a directory inside the system's temporary directory.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Path object pointing to a directory in the temporary directory.
    :rtype: Path
    """


@overload
def output_path_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Path:
    """Return a default output Path instance for testing purposes.

    This path points to a directory inside the system's temporary directory.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Path object pointing to a directory in the temporary directory.
    :rtype: Path
    """


@cached_factory
def output_path_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Path:
    """Return a default output Path instance for testing purposes.

    This path points to a directory inside the system's temporary directory.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Path object pointing to a file in the temporary directory.
    :rtype: Path
    """
    return path_factory(cache_id=cache_id)


@cached_factory
def n_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> int:
    """Return a default number of iterations or rounds for testing purposes.

    :return: `1`
    :rtype: int
    """
    return 1


@cached_factory
def case_group_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default group string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"default_case_group"`
    :rtype: str
    """
    return "default_case_group"


def default_case_group() -> str:
    """Return a default group string for testing purposes.

    It always returns the same group string created by case_group_factory().

    :return: `"default_case_group"`
    :rtype: str
    """
    return case_group_factory(cache_id=f'{__name__}.default_case_group:singleton')


@cached_factory
def title_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a title string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"Default Title"`
    :rtype: str
    """
    return "Default Title"


def default_title() -> str:
    """Return a default title string for testing purposes.

    It always returns the same title string created by title_factory().

    :return: `"Default Title"`
    :rtype: str
    """
    return title_factory(cache_id=f'{__name__}.default_title:singleton')


@cached_factory
def subdir_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default subdir string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"asubdir"`
    :rtype: str
    """
    return "asubdir"


def default_subdir() -> str:
    """Return a default subdir string for testing purposes.

    It always returns the same subdir string created by subdir_factory().

    :return: `"asubdir"`
    :rtype: str
    """
    return subdir_factory(cache_id=f'{__name__}.default_subdir:singleton')


@cached_factory
def sections_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Section, ...]:
    """Return a default tuple of Sections for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `(Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)`
    :rtype: tuple[Section]
    """
    return (Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)


def default_sections() -> tuple[Section, ...]:
    """Return a default tuple of Sections for testing purposes.

    It always returns the same tuple instance of Sections created by sections_factory().

    :return: `(Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)`
    :rtype: tuple[Section]
    """
    return sections_factory(cache_id=f'{__name__}.default_sections:singleton')


@cached_factory
def targets_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Target, ...]:
    """Return a default tuple of Targets for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `(Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)`
    :rtype: tuple[Target]
    """
    return (Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)


def default_targets() -> tuple[Target, ...]:
    """Return a default tuple of Targets for testing purposes.

    It always returns the same tuple instance of Targets created by targets_factory().

    :return: `(Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)`
    :rtype: tuple[Target]
    """
    return targets_factory(cache_id=f'{__name__}.default_targets:singleton')


@cached_factory
def default_targets_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Target]:
    """Return a default tuple for default_targets for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `(Target.CONSOLE,)`
    :rtype: tuple[Target]
    """
    return (Target.CONSOLE, )


def default_default_targets() -> tuple[Target]:
    """Return a default tuple for default_targets for testing purposes.

    :return: `(Target.CONSOLE,)`
    :rtype: tuple[Target]
    """
    return default_targets_factory(cache_id=f'{__name__}.default_default_targets:singleton')


@cached_factory
def formats_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[Format]:
    """Return a default tuple of Formats for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `(Format.RICH_TEXT,)`
    :rtype: tuple[Format]
    """
    return (Format.RICH_TEXT, )


def default_formats() -> tuple[Format]:
    """Return a default tuple of Formats for testing purposes.

    It always returns the same tuple instance of Formats created by formats_factory().

    :return: `(Format.RICH_TEXT,)`
    :rtype: tuple[Format]
    """
    return formats_factory(cache_id=f'{__name__}.default_formats:singleton')


@cached_factory
def output_format_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Format:
    """Return a default Format for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `Format.RICH_TEXT`
    :rtype: Format
    """
    return Format.RICH_TEXT


def default_output_format() -> Format:
    """Return a default Format for testing purposes.

    It always returns the same Format instance created by output_format_factory().

    :return: `Format.RICH_TEXT`
    :rtype: Format
    """
    return output_format_factory(cache_id=f'{__name__}.default_output_format:singleton')


@cached_factory
def description_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a description string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"A description for testing."`
    :rtype: str
    """
    return "A description for testing."


def default_description() -> str:
    """Return a default description string for testing purposes.

    It always returns the same description string created by description_factory().

    :return: `"A description for testing."`
    :rtype: str
    """
    return description_factory(cache_id=f'{__name__}.default_description:singleton')


@cached_factory
def reporter_name_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default reporter name string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"default_reporter_name"`
    :rtype: str
    """
    return "default_reporter_name"


def default_reporter_name() -> str:
    """Return a default reporter name string for testing purposes.

    It always returns the same reporter name string created by reporter_name_factory().

    :return: `"default_reporter_name"`
    :rtype: str
    """
    return reporter_name_factory(cache_id=f'{__name__}.default_reporter_name:singleton')


@cached_factory
def choice_name_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a choice name string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"choice_name"`
    :rtype: str
    """
    return "choice_name"


def flag_name_factory() -> str:
    """Return a default flag name string for testing purposes.

    It always returns the same flag name string.

    :return: `"--default-flag"`
    :rtype: str
    """
    return '--default-flag'


def default_choice_name() -> str:
    """Return a default choice name string for testing purposes.

    It always returns the same choice name string created by choice_name_factory().

    :return: `"choice_name"`
    :rtype: str
    """
    return choice_name_factory(cache_id=f'{__name__}.default_choice_name:singleton')


@cached_factory
def choice_flags_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[str, ...]:
    """Return a tuple of flags for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `tuple(['--default-flag'])`
    :rtype: tuple[str, ...]
    """
    return tuple([flag_name_factory()])


def default_choice_flags() -> tuple[str, ...]:
    """Return a default tuple of choice flags for testing purposes.

    It always returns the same tuple of flags created by choice_flags_factory().

    :return: `tuple(['--default-flag'])`
    :rtype: tuple[str, ...]
    """
    return choice_flags_factory(cache_id=f'{__name__}.default_choice_flags:singleton')


@cached_factory
def flag_type_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> FlagType:
    """Return a FlagType for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `FlagType.TARGET_LIST`
    :rtype: FlagType
    """
    return FlagType.TARGET_LIST


def default_flag_type() -> FlagType:
    """Return a default FlagType for testing purposes.

    It always returns the same FlagType created by flag_type_factory().

    :return: `FlagType.TARGET_LIST`
    :rtype: FlagType
    """
    return flag_type_factory(cache_id=f'{__name__}.default_flag_type:singleton')


@cached_factory
def file_suffix_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default file suffix string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"suffix"`
    :rtype: str
    """
    return "suffix"


def default_file_suffix() -> str:
    """Return a default file suffix string for testing purposes.

    It always returns the same file suffix string created by file_suffix_factory().

    :return: `"suffix"`
    :rtype: str
    """
    return file_suffix_factory(cache_id=f'{__name__}.default_file_suffix:singleton')


@cached_factory
def file_unique_factory() -> bool:
    """Return a default file unique boolean for testing purposes.

    It always returns `True`.

    This is coordinated with `default_file_append()` to ensure that
    file_unique is `True` and file_append is `False`, which are compatible settings.

    :return: `True`
    :rtype: bool
    """
    return True


def default_file_unique() -> bool:
    """Return a default file unique boolean for testing purposes.

    It always returns the same boolean created by file_unique_factory().

    :return: `True`
    :rtype: bool
    """
    return file_unique_factory(cache_id=f'{__name__}.default_file_unique:singleton')


@cached_factory
def file_append_factory() -> bool:
    """Return a default file append boolean for testing purposes.

    It always returns `False`.

    This is coordinated with `default_file_unique()` to ensure that
    file_unique is `True` and file_append is `False`, which are compatible settings.

    :return: `False`
    :rtype: bool
    """
    return False


def default_file_append() -> bool:
    """Return a default file append boolean for testing purposes.

    It always returns the same boolean created by file_append_factory().

    :return: `False`
    :rtype: bool
    """
    return file_append_factory(cache_id=f'{__name__}.default_file_append:singleton')


@cached_factory
def report_output_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a report output string for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `"Rendered Report"`
    :rtype: str
    """
    return "Rendered Report"


def default_report_output() -> str:
    """Return a default report output string for testing purposes.

    It always returns the same report output string created by report_output_factory().

    :return: `"Rendered Report"`
    :rtype: str
    """
    return report_output_factory(cache_id=f'{__name__}.default_report_output:singleton')


@cached_factory
def iterations_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> int:
    """Return a default number of iterations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    :return: `100`
    :rtype: int
    """
    return 100


def default_iterations() -> int:
    """Return a default number of iterations for testing purposes.

    It always returns the same number instance created by iterations_factory().

    :return: `100`
    :rtype: int
    """
    return iterations_factory(cache_id=f'{__name__}.default_iterations:singleton')


@cached_factory
def warmup_iterations_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> int:
    """Return a default number of warmup iterations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    :return: `100`
    :rtype: int
    """
    return 100


def default_warmup_iterations() -> int:
    """Return a default number of warmup iterations for testing purposes.

    It always returns the same number instance created by warmup_iterations_factory().

    :return: `100`
    :rtype: int
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

    :return: `1500`
    :rtype: int
    """
    return 1500


def default_rounds() -> int:
    """Return a default number of rounds for testing purposes.

    It always returns the same number instance created by rounds_factory().

    :return: `1500`
    :rtype: int
    """
    return rounds_factory(cache_id=f'{__name__}.default_rounds:singleton')


@cached_factory
def min_time_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default minimum time for testing purposes.

    This is for use in configuring benchmark cases in tests.

    :return: `0.1`
    :rtype: float
    """
    return 0.1


def default_min_time() -> float:
    """Return a default minimum time for testing purposes.

    It always returns the same number instance created by min_time_factory().

    :return: `0.1`
    :rtype: float
    """
    return min_time_factory(cache_id=f'{__name__}.default_min_time:singleton')


@cached_factory
def max_time_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default maximum time for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    This is for use in configuring benchmark cases in tests.

    :return: `0.2`
    :rtype: float
    """
    return 0.2


def default_max_time() -> float:
    """Return a default maximum time for testing purposes.

    It always returns the same number instance created by max_time_factory().

    :return: `0.2`
    :rtype: float
    """
    return max_time_factory(cache_id=f'{__name__}.default_max_time:singleton')


@cached_factory
def variation_cols_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, str]:
    """Return a dictionary of variation columns for testing purposes.

    This is for use in configuring benchmark cases in tests.

    This is a minimal case without any variation columns.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `{}`
    :rtype: dict[str, str]
    """
    return {}


@cached_factory
def kwargs_variations_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, list]:
    """Return a set of kwargs variations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    This is a minimal case without any kwargs variations.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `{}`
    :rtype: dict[str, list[Any]]
    """
    return {}


@cached_factory
def total_elapsed_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default total elapsed time for testing purposes.

    :return: `6.0`
    :rtype: float
    """
    return 6.0


@cached_factory
def interval_unit_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default interval unit for testing purposes.

    :return: `"s"`
    :rtype: str
    """
    return "s"


@cached_factory
def interval_scale_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default interval scale for testing purposes.

    :return: `1.0`
    :rtype: float
    """
    return 1.0


@cached_factory
def ops_per_interval_unit_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default ops per interval unit for testing purposes.

    :return: `Ops/s`
    :rtype: str
    """
    return 'Ops/s'


@cached_factory
def ops_per_interval_scale_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default ops per interval scale for testing purposes.

    :return: `1.0`
    :rtype: float
    """
    return 1.0


@cached_factory
def memory_unit_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> str:
    """Return a default memory unit for testing purposes.

    :return: `"bytes"`
    :rtype: str
    """
    return "bytes"


@cached_factory
def memory_scale_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default memory scale for testing purposes.

    :return: `1.0`
    :rtype: float
    """
    return 1.0


@cached_factory
def variation_marks_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, str]:
    """Return a default dictionary of variation marks for testing purposes.

    :return: `{}`
    :rtype: dict[str, str]
    """
    return {}


@cached_factory
def timestamp_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> float:
    """Return a default timestamp for testing purposes.

    :return: `1700000000.0`
    :rtype: float
    """
    return 1700000000.0


def default_timestamp() -> float:
    """Return a default timestamp for testing purposes.

    It always returns the same timestamp created by timestamp_factory().

    :return: `1700000000.0`
    :rtype: float
    """
    return timestamp_factory(cache_id=f'{__name__}.default_timestamp:singleton')
