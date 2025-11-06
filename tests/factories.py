"""Factories for creating test instances of reporters and related classes.

By placing these factory functions in a separate module, we keep from
repeatly defining them in multiple test modules. This also allows
centralized updates to the factory functions as needed.

Each factory function is designed to create and return a specific
test instance with default parameters suitable for testing.

They also provide standard references for checking expected values in many tests
without needing 'magic numbers' or hardcoded values in the tests themselves.

Most of the default values are simple literals or basic types, but
some factory functions create more complex instances like `Case`, `Session`,
`Choice`, and `Reporter`.

Because these complex instances may have interdependencies, the factory functions
are designed to call each other as needed to build up the required instances in
a consistent manner with a minimal likelihood of errors or obfuscating boilerplate
in the tests themselves.

For example, the `default_choice_instance()` factory function builds a `Choice` instance
by calling the `reporter_instance()` factory function with a configured `ChoicesConf`
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
from pathlib import Path
from typing import Any, Optional, Sequence, Iterable, TypeVar


from tests.kwargs import ReporterKWArgs, ChoiceConfKWArgs, CaseKWArgs, ChoicesConfKWArgs
from tests.cache_factory import cache_factory, CacheId, CACHE_DEFAULT
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


@cache_factory
def extra_instance(full_data: bool = True) -> DefaultExtra:
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


def default_extra() -> DefaultExtra:
    """Return a default ReporterExtras instance for testing purposes.

    It always returns the same DefaultExtra instance created by extra_instance().

    Returns:
        DefaultExtra: `DefaultExtra(full_data=False)`
    """
    return extra_instance(full_data=False, cache_id=f'{__name__}.default_extra:singleton')


@cache_factory
def default_path() -> Path:
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


@cache_factory
def default_case_group() -> str:
    """Return a default group string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"default_case_group"`

    """
    return "default_case_group"


@cache_factory
def default_title() -> str:
    """Return a default title string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"Default Title"`
    """
    return "Default Title"


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


def default_reporter_options_type() -> type[ReporterOptions]:
    """Return a default ReporterOptions type for testing purposes.

    Returns:
        type[ReporterOptions]: `ReporterOptions`
    """
    return ReporterOptions


@cache_factory
def default_subdir() -> str:
    """Return a default subdir string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"asubdir"`
    """
    return "asubdir"


@cache_factory
def default_sections() -> tuple[Section, ...]:
    """Return a default tuple of Sections for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Section]: `(Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)`

    """
    return (Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY)


@cache_factory
def default_targets() -> tuple[Target, ...]:
    """Return a default tuple of Targets for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Target]: `(Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)`
    """
    return (Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM)


@cache_factory
def default_default_targets() -> tuple[Target]:
    """Return a default tuple for default_targets for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[Target]: `(Target.CONSOLE,)`
    """
    return (Target.CONSOLE,)


@cache_factory
def default_formats() -> tuple[Format]:
    """Return a default tuple of Formats for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        tuple[Format]: `(Format.RICH_TEXT,)`
    """
    return (Format.RICH_TEXT,)


@cache_factory
def default_output_format() -> Format:
    """Return a default Format for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        Format: `Format.RICH_TEXT`
    """
    return Format.RICH_TEXT


@cache_factory
def default_description() -> str:
    """Return a default description string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"A default description for testing."`
    """
    return "A default description for testing."


@cache_factory
def default_reporter_name() -> str:
    """Return a default reporter name string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"default_reporter_name"`
    """
    return "default_reporter_name"


@cache_factory
def default_choice_name() -> str:
    """Return a default choice name string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"default_choice_name"`
    """
    return "default_choice_name"


@cache_factory
def default_choice_flags() -> tuple[str, ...]:
    """Return a default tuple of flags for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        (tuple[str, ...]): `tuple(['--default-flag'])`
    """
    return tuple(['--default-flag'])


@cache_factory
def default_flag_type() -> FlagType:
    """Return a default FlagType for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        FlagType: `FlagType.TARGET_LIST`
    """
    return FlagType.TARGET_LIST


@cache_factory
def default_file_suffix() -> str:
    """Return a default file suffix string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"suffix"`
    """
    return "suffix"


def default_file_unique() -> bool:
    """Return a default file unique boolean for testing purposes.

    It always returns `True`.

    This is coordinated with `default_file_append()` to ensure that
    file_unique is `True` and file_append is `False`, which are compatible settings.

    Returns:
        bool: `True`
    """
    return True


def default_file_append() -> bool:
    """Return a default file append boolean for testing purposes.

    It always returns `False`.

    This is coordinated with `default_file_unique()` to ensure that
    file_unique is `True` and file_append is `False`, which are compatible settings.

    Returns:
        bool: `False`
    """
    return False


@cache_factory
def default_choice_conf_instance() -> ChoiceConf:
    """Return a default Choice conf instance for testing purposes.

    It is created by calling `choice_conf_instance()` with default parameters.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        ChoiceConf: A default ChoiceConf instance.
    """
    return choice_conf_instance()


@cache_factory
def default_choice_confs(*, cache_id: CacheId = CACHE_DEFAULT) -> tuple[ChoiceConf, ...]:
    """Return a default tuple of ChoiceConf instances for testing purposes.

    It contains a single ChoiceConf instance created by default_choice_conf_instance().

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[ChoiceConf, ...]: A tuple containing default ChoiceConf instances.
    """
    return tuple([default_choice_conf_instance(cache_id=cache_id)])


@cache_factory
def default_report_output() -> str:
    """Return a default report output string for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        str: `"Rendered Report"`
    """
    return "Rendered Report"


@cache_factory
def default_report_parameters(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, Any]:
    """Return default report parameters for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        dict[str, Any]: A dictionary of default report parameters.
    """
    return {
        'args': default_namespace(cache_id=cache_id),
        'case': default_case_instance(cache_id=cache_id),
        'choice': choice_instance(cache_id=cache_id),
        'path': default_path(cache_id=cache_id),
        'session': default_session_instance(cache_id=cache_id),
        'callback': default_reporter_callback
    }


@cache_factory
def minimal_case_kwargs() -> CaseKWArgs:
    """Return a minimally configured CaseKWArgs for testing purposes.

    Only the required attribute `action`is set to an explict value.
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
    return CaseKWArgs(
        action=default_benchcase,
    )


def default_iterations() -> int:
    """Return a default number of iterations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        int: `100`
    """
    return 100


def default_warmup_iterations() -> int:
    """Return a default number of warmup iterations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        int: `100`
    """
    return 100


def default_rounds() -> int:
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


def default_min_time() -> float:
    """Return a default minimum time for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        float: `0.1`
    """
    return 0.1


def default_max_time() -> float:
    """Return a default maximum time for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        float: `10.0`
    """
    return 10.0


@cache_factory
def default_variation_cols() -> dict[str, str]:
    """Return a default dictionary of variation columns for testing purposes.

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


@cache_factory
def default_kwargs_variations() -> dict[str, list[Any]]:
    """Return a default set of kwargs variations for testing purposes.

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


def default_runner() -> type[SimpleRunner]:
    """Return a default SimpleRunner type for testing purposes.

    This is for use in configuring benchmark cases in tests.

    Returns:
        type[SimpleRunner]: `SimpleRunner`
    """
    return SimpleRunner


@cache_factory
def default_reporter_options() -> ReporterOptions:
    """Return a default ReporterOptions instance for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        ReporterOptions: `ReporterOptions`
    """
    return ReporterOptions()


@cache_factory
def default_case_kwargs(*, cache_id: CacheId = CACHE_DEFAULT) -> CaseKWArgs:
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
        group=default_case_group(cache_id=cache_id),
        title=default_title(cache_id=cache_id),
        description=default_description(cache_id=cache_id),
        action=default_benchcase,
        iterations=default_iterations(),
        warmup_iterations=default_warmup_iterations(),
        rounds=default_rounds(),
        min_time=default_min_time(),
        max_time=default_max_time(),
        variation_cols=default_variation_cols(cache_id=cache_id),
        kwargs_variations=default_kwargs_variations(cache_id=cache_id),
        runner=default_runner(),
        callback=default_reporter_callback,
        options=[default_reporter_options(cache_id=cache_id)]
    )


@cache_factory
def default_case_instance(*, cache_id: CacheId = CACHE_DEFAULT) -> Case:
    """Return a default Case instance for testing purposes.

    This is a 'pre-benchmarking' Case with default attributes set.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    """
    return Case(
        group=default_case_group(cache_id=cache_id),
        title=default_title(cache_id=cache_id),
        description=default_description(cache_id=cache_id),
        action=default_benchcase)


@cache_factory
def default_session_instance(*, cache_id: CacheId = CACHE_DEFAULT) -> Session:
    """Return a default Session instance for testing purposes.

    The Session is initialized with default attributes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    """
    return Session(
        cases=[default_case_instance(cache_id=cache_id)],
        verbosity=Verbosity.QUIET)


@cache_factory
def default_namespace() -> Namespace:
    """Return a default ArgumentParser instance for testing purposes.

    It is minimally configured with the program name 'simplebench'.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    """
    arg_parser = ArgumentParser(prog='simplebench')
    args = arg_parser.parse_args([])
    return args


class MockReporterExtras:
    """A mock ReporterExtras subclass for testing Choice initialization."""
    def __init__(self, full_data: bool = False) -> None:
        self.full_data = full_data


class MockReporter(Reporter):
    """A mock Reporter subclass for testing Choice initialization.

    It provides a minimal implementation of the abstract methods required by the Reporter base class.

    It initializes with a single ChoiceConf instance for testing purposes by default.
    This can be overridden by providing a different list of ChoiceConf instances.

    The default ChoiceConf instance is created using the choice_conf_instance factory function and
    has the name 'mock' and flag '--mock'.

    Args
    """
    def __init__(
            self, choices_conf: ChoicesConf | None = None) -> None:
        """Constructs a MockReporter instance for testing.

        Args:
            choices_conf (ChoicesConf | None, default=None):
               A `ChoicesConf` instance to initialize the `Reporter` with.
               If None, a default instance will be used.
        """
        if not isinstance(choices_conf, ChoicesConf) and choices_conf is not None:
            raise TypeError(f'choices_conf must be a ChoicesConf instance or None, got {choices_conf!r}')
        choices_conf = default_choices_conf() if choices_conf is None else choices_conf
        super().__init__(
            name=default_reporter_name(),
            description=default_description(),
            sections=default_sections(),
            default_targets=default_default_targets(),
            targets=default_targets(),
            subdir=default_subdir(),
            options_type=default_reporter_options_type(),
            file_suffix=default_file_suffix(),
            file_unique=default_file_unique(),
            file_append=default_file_append(),
            formats=default_formats(),
            choices=choices_conf
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Mock implementation of run_report."""

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """Mock implementation of render method."""
        return "mocked_rendered_output"


class UnconfiguredReporterOptions(ReporterOptions):
    """A dummy ReporterOptions subclass for testing purposes.

    The UnconfiguredReporter is preconfigured with no options so all
    parameters are must be provided at runtime (unless defaults are set elsewhere).
    """


USE_SELF_FOR_REPORTER = object()
"""Sentinel value to indicate that the reporter parameter should be set to self.

This is used to avoid circular references when initializing UnconfiguredReporter
while still allowing the testing of reporter parameter handling of the Reporter base class.
"""


class UnconfiguredReporter(Reporter):
    """A dummy reporter subclass for testing purposes.

    No parameters are preset for this reporter.

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
            choices: Choices | None = None,
            file_suffix: str | None = None,
            file_unique: str | None = None,
            file_append: str | None = None) -> None:
        """Initialize UnconfiguredReporter with provided kwargs.

        Args:
            name (str | None): Name of the reporter.
            description (str | None): Description of the reporter.
            options_type (ReporterOptions | None): Options type for the reporter.
            sections (Iterable[Section] | None): Supported sections for the reporter.
            targets (Iterable[Target] | None): Supported targets for the reporter.
            formats (Iterable[Format] | None): Supported formats for the reporter.
            choices (Choices | None): Choices for the reporter.
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


class ConfiguredReporter(Reporter):
    """A mock reporter subclass with default options already set for testing purposes.

    Creates a Reporter with default parameters for testing that can be overridden as needed.

        - name=default_name(),
        - description=default_description(),
        - options_type=ConfiguredReporterOptions,
        - sections=default_sections(),
        - targets=default_targets(),
        - formats=default_formats(),
        - choices=default_choice_confs(),
        - file_suffix=default_file_suffix(),
        - file_unique=default_file_unique(),
        - file_append=default_file_append()

    """
    def __init__(self) -> None:
        """Preconfigured Reporter for testing purposes.
            - name=default_name(),
            - description=default_description(),
            - options_type=ConfiguredReporterOptions,
            - sections=default_sections(),
            - targets=default_targets(),
            - formats=default_formats(),
            - choices=default_choice_confs(),
            - file_suffix=default_file_suffix(),
            - file_unique=default_file_unique(),
            - file_append=default_file_append()
        """

        super().__init__(
            name=default_reporter_name(),
            description=default_description(),
            options_type=default_options_type(),
            sections=default_sections(),
            targets=default_targets(),
            formats=default_formats(),
            choices=default_choices_conf(),
            file_suffix=default_file_suffix(),
            file_unique=default_file_unique(),
            file_append=default_file_append())

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Run the report with the given arguments, case, and choice."""
        self.render_by_case(
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """Render the report for the given case, section, and options."""
        return default_report_output()


@cache_factory
def default_reporter_kwargs(*, cache_id: CacheId = CACHE_DEFAULT) -> ReporterKWArgs:
    """A preconfigured ReporterKWArgs instance for testing purposes.

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

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        ReporterKWArgs: A preconfigured instance with default values for testing.
    """
    return ReporterKWArgs(
        name=default_reporter_name(cache_id=cache_id),
        description=default_description(cache_id=cache_id),
        options_type=default_options_type(),
        sections=default_sections(cache_id=cache_id),
        targets=default_targets(cache_id=cache_id),
        formats=default_formats(cache_id=cache_id),
        choices=default_choices_conf(cache_id=cache_id),
        file_suffix=default_file_suffix(cache_id=cache_id),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )


class ConfiguredChoiceConf(ChoiceConf):
    """A dummy Choice subclass for testing purposes.

    Creates a Choice with default parameters for testing that can be overridden as needed.

    """
    def __init__(
            self,
            *,
            flags: list[str] | None = None,
            name: str | None = None,
            description: str | None = None,
            flag_type: FlagType | None = None,
            sections: Sequence[Section] | None = None,
            targets: Sequence[Target] | None = None,
            output_format: Format | None = None,
            ) -> None:
        super().__init__(
            flags=flags if flags is not None else default_choice_flags(),
            flag_type=flag_type if flag_type is not None else default_flag_type(),
            name=name if name is not None else default_choice_name(),
            description=description if description is not None else default_description(),
            sections=sections if sections is not None else default_sections(),
            targets=targets if targets is not None else default_targets(),
            output_format=output_format if output_format is not None else default_output_format()
        )


@cache_factory
def choice_conf_kwargs_instance() -> ChoiceConfKWArgs:
    """Return default ChoiceConfKWArgs for testing purposes.

    It contains all parameters set to explicit default values for testing purposes.
    Because ChoiceConfKWArgs has many parameters, they are listed here for clarity:

    ```python
       ChoiceConfKWArgs(
        flags=default_choice_flags(cache_id=None),
        flag_type=default_flag_type(cache_id=None),
        name=default_choice_name(cache_id=None),
        description=default_description(cache_id=None),
        subdir=default_subdir(cache_id=None),
        sections=default_sections(cache_id=None),
        targets=default_targets(cache_id=None),
        default_targets=default_default_targets(cache_id=None),
        output_format=default_output_format(cache_id=None),
        file_suffix=default_file_suffix(cache_id=None),
        file_unique=default_file_unique(),
        file_append=default_file_append(),
        options=default_reporter_options(cache_id=None),
        extra=default_extra(cache_id=None)
       )
    ```
    Returns:
        ChoiceConfKWArgs: A default ChoiceConfKWArgs instance.
    """
    return ChoiceConfKWArgs(
        flags=default_choice_flags(cache_id=None),
        flag_type=default_flag_type(cache_id=None),
        name=default_choice_name(cache_id=None),
        description=default_description(cache_id=None),
        subdir=default_subdir(cache_id=None),
        sections=default_sections(cache_id=None),
        targets=default_targets(cache_id=None),
        default_targets=default_default_targets(cache_id=None),
        output_format=default_output_format(cache_id=None),
        file_suffix=default_file_suffix(cache_id=None),
        file_unique=default_file_unique(),
        file_append=default_file_append(),
        options=default_reporter_options(cache_id=None),
        extra=default_extra()
    )


def default_choice_conf_kwargs() -> ChoiceConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It always returns the same ChoiceConf instance created by choice_conf_kwargs_instance().
    It is safe to cache this instance because ChoiceConfKWArgs is immutable. It will always
    return the same values for the same attributes and behaves consistently across tests.

    Returns:
        ChoicesConfKWArgs: A default ChoicesConfKWArgs instance.
    """
    return choice_conf_kwargs_instance(cache_id=f'{__name__}.default_choice_conf_kwargs:singleton')


@cache_factory
def default_choices_conf_kwargs() -> ChoicesConfKWArgs:
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


@cache_factory
def default_choices_conf(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConf:
    """Return a default ChoicesConf instance for testing purposes.

    It contains a single ChoiceConf created using default_choice_conf_kwargs().

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        ChoicesConf: A default ChoicesConf instance.
    """
    return ChoicesConf([ChoiceConf(**default_choices_conf_kwargs(cache_id=cache_id))])


class ConfiguredCase(Case):
    """A dummy Case subclass for testing purposes.

    This Case is preconfigured with default parameters and made-up results
    to facilitate testing of reporter functionality without needing to
    run actual benchmarks each time.
    """
    def __init__(self) -> None:
        super().__init__(
            group='test_case',
            title='Test Case',
            description='A test case for testing.',
            action=default_benchcase)
        self._results.append(Results(  # made-up results for testing purposes
            group='test_case', title='Test Case', description='A test case for testing.',
            n=10, total_elapsed=6.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0), Iteration(elapsed=3.0)]))


configured_case_instance = ConfiguredCase()

"""A preconfigured ConfiguredCase instance for testing purposes.

Used to avoid re-instantiating multiple times in tests that
need multiple access to the same Case instance.
"""


class ConfiguredSession(Session):
    """A dummy Session subclass for testing purposes."""
    def __init__(self) -> None:

        super().__init__(cases=[ConfiguredCase()], verbosity=Verbosity.QUIET)


configured_session_instance = ConfiguredSession()
"""A preconfigured ConfiguredSession instance for testing purposes.

Used to avoid re-instantiating multiple times in tests
that need multiple access to the same Session instance.
"""


@cache_factory
def choice_conf_instance(*,
                         cache_id: CacheId = CACHE_DEFAULT,
                         name: str | None = None, flags: tuple[str, ...] | None = None) -> ChoiceConf:
    """Factory function to return the same mock ChoiceConf instance for testing.

    It caches the instance based on the cache_id so that multiple calls with the same
    cache_id return the same instance.

    If name is None, the default name from default_choice_name() is used.
    If flags is None, the default flags from default_choice_flags() are used.

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
        flags=default_choice_flags(cache_id=cache_id) if flags is None else flags,
        flag_type=default_flag_type(),
        name=default_choice_name(cache_id=cache_id) if name is None else name,
        description=default_description(cache_id=cache_id),
        sections=default_sections(cache_id=cache_id),
        targets=default_targets(cache_id=cache_id),
        output_format=default_output_format(cache_id=cache_id),
        file_suffix=default_file_suffix(cache_id=cache_id),
        file_unique=default_file_unique(),
        file_append=default_file_append(),
        options=default_reporter_options(cache_id=cache_id),
        extra=default_extra())


@cache_factory
def choice_instance(*,
                    cache_id: CacheId = CACHE_DEFAULT,
                    name: str | None = None,
                    flags: tuple[str, ...] | None = None) -> Choice:
    """Factory function to return a single cached Choice instance for testing.

    The choice instance is created using MockReporter() and is
    extracted from the MockReporter.choices attribute.

    It is cached based on the cache_id so that multiple calls with the same
    cache_id, name, and flags return the same instance.

    Because choice instances are immutable after creation, this caching
    is safe and helps ensure consistency across tests that need the same
    choice instance.

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
        name = default_choice_name(cache_id=cache_id)
    if flags is None:
        flags = default_choice_flags(cache_id=cache_id)
    if not isinstance(name, str):
        raise TypeError(f"Invalid type for name argument: {name!r}")
    if not isinstance(flags, tuple) or not all(isinstance(f, str) for f in flags):
        raise TypeError(f"Invalid type for flags argument: {flags!r}")
    if flags is not None or name is not None:
        choices_conf = choices_conf_instance(
            cache_id=cache_id,
            choices=(choice_conf_instance(cache_id=cache_id, name=name, flags=flags),))
    else:
        choices_conf = default_choices_conf(cache_id=cache_id)
    kwargs = default_reporter_kwargs().replace(choices=choices_conf)
    reporter = reporter_instance(cache_id=cache_id, reporter_kwargs=kwargs)
    return reporter.choices[name]


def default_choice_conf() -> ChoiceConf:
    """Return a default ChoiceConf instance for testing purposes.

    It is created by calling ChoiceConf with default_choice_conf_kwargs().

    It always returns the same instance for consistency in tests. Because
    ChoiceConf instances are immutable after creation, this is safe.

    Returns:
        ChoiceConf: A default ChoiceConf instance.
    """
    return choice_conf_instance(cache_id=f'{__name__}.default_choice_conf:singleton')


@cache_factory
def choices_conf_instance(*, choices: tuple[ChoiceConf, ...] | None = None) -> ChoicesConf:
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


@cache_factory
def reporter_instance(
        *,
        cache_id: CacheId = CACHE_DEFAULT,
        reporter_kwargs: ReporterKWArgs | None = None) -> UnconfiguredReporter:
    """Factory function to return a cached UnconfiguredReporter instance for testing.

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
    kwargs = default_reporter_kwargs(cache_id=cache_id) if reporter_kwargs is None else reporter_kwargs
    return UnconfiguredReporter(**kwargs)


@cache_factory
def choices_instance(*,
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
    reporter = reporter_instance(cache_id=cache_id, reporter_kwargs=kwargs)
    return reporter.choices
