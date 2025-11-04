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
"""
from argparse import ArgumentParser, Namespace
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional, Sequence, Iterable


from tests.kwargs import ReporterKWArgs, ChoiceConfKWArgs, CaseKWArgs

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


class DefaultExtras:
    """A mock ReporterExtras subclass for testing Choice initialization."""
    def __init__(self, full_data: bool = False) -> None:
        self.full_data = full_data


def default_path() -> Path:
    """Return a default Path instance for testing purposes.

    Returns:
        Path: `Path('/tmp/mock_report.txt')`
    """
    return Path('/tmp/mock_report.txt')  # pragma: no cover (path not actually used)


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


def default_group() -> str:
    """Return a default group string for testing purposes.

    Returns:
        str: `"default_group"`

    """
    return "default_group"


def default_title() -> str:
    """Return a default title string for testing purposes.

    Returns:
        str: `"Default Title"`
    """
    return "Default Title"


def default_reporter_callback(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: Any) -> None:
    """A default ReporterCallback conformant callback function for testing purposes.

    ```python

    def default_reporter_callback(
            *, case: Case, section: Section, output_format: Format, output: Any) -> None:
        return None
    ```
    """
    return None  # pragma: no cover


def default_sections() -> list[Section]:
    """Return a default list of Sections for testing purposes.

    Returns:
        list[Section]: `[Section.OPS]`

    """
    return [Section.OPS]


def default_targets() -> list[Target]:
    """Return a default list of Targets for testing purposes.

    Returns:
        list[Target]: `[Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM]`
    """
    return [Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM]


def default_default_targets() -> list[Target]:
    """Return a default list for default_targets for testing purposes."

    Returns:
        list[Target]: `[Target.CONSOLE]`
    """
    return [Target.CONSOLE]


def default_formats_list() -> list[Format]:
    """Return a default list of Formats for testing purposes.

    Returns:
        list[Format]: `[Format.RICH_TEXT]`
    """
    return [Format.RICH_TEXT]


def default_output_format() -> Format:
    """Return a default Format for testing purposes.

    Returns:
        Format: `Format.RICH_TEXT`
    """
    return Format.RICH_TEXT


def default_description() -> str:
    """Return a default description string for testing purposes.

    Returns:
        str: `"A default description for testing."`
    """
    return "A default description for testing."


def default_name() -> str:
    """Return a default name string for testing purposes.

    Returns:
        str: `"default_name"`
    """
    return "default_name"


def default_flags() -> tuple[str, ...]:
    """Return a default tuple of flags for testing purposes.

    Returns:
        (tuple[str, ...]): `tuple(['--default-flag'])`
    """
    return tuple(['--default-flag'])


def default_flag_type() -> FlagType:
    """Return a default FlagType for testing purposes.

    Returns:
        FlagType: `FlagType.TARGET_LIST`
    """
    return FlagType.TARGET_LIST


def default_file_suffix() -> str:
    """Return a default file suffix string for testing purposes.

    Returns:
        str: `"default_suffix"`
    """
    return "default_suffix"


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


def default_choice_conf_instance() -> ChoiceConf:
    """Return a default Choice conf instance for testing purposes.

    It is created by calling `choice_conf_instance()` with default parameters.
    """
    return choice_conf_instance()


def default_choice_confs() -> tuple[ChoiceConf, ...]:
    """Return a default tuple of ChoiceConf instances for testing purposes.

    It contains a single ChoiceConf instance created by default_choice_conf_instance().
    """
    return tuple([default_choice_conf_instance()])


def default_report_output() -> str:
    """Return a default report output string for testing purposes.

    Returns:
        str: `"Rendered Report"`
    """
    return "Rendered Report"


def default_report_parameters() -> dict[str, Any]:
    """Return default report parameters for testing purposes."""
    return {
        'args': default_namespace(),
        'case': default_case_instance(),
        'choice': choice_instance(),
        'path': default_path(),
        'session': default_session_instance(),
        'callback': default_reporter_callback
    }


def minimal_case_kwargs() -> CaseKWArgs:
    """Return a minimally configured CaseKWArgs for testing purposes.

    Only the required attribute `action`is set to an explict value.
    All other attributes will take their default values.

    Attributes:
            action = `default_benchcase`


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


def default_variation_cols() -> dict[str, str]:
    """Return a default dictionary of variation columns for testing purposes.

    This is for use in configuring benchmark cases in tests.

    This is a minimal case without any variation columns.

    Returns:
        (dict[str, str]): `{}`
    """
    return {}


def default_kwargs_variations() -> dict[str, list[Any]]:
    """Return a default set of kwargs variations for testing purposes.

    This is for use in configuring benchmark cases in tests.

    This is a minimal case without any kwargs variations.

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


def default_reporter_options() -> list[ReporterOptions]:
    """Return a list of default ReporterOptions instances for testing purposes.

    Returns:
        list[ReporterOptions]: `[ReporterOptions]`
    """
    return [ReporterOptions()]


def default_case_kwargs() -> CaseKWArgs:
    """Return a default configured CaseKWargs for testing purposes.

    The following attributes are all set to explicit values for testing purposes:

    Attributes:
            group = `default_group()`
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
    """
    return CaseKWArgs(
        group=default_group(),
        title=default_title(),
        description=default_description(),
        action=default_benchcase,
        iterations=default_iterations(),
        warmup_iterations=default_warmup_iterations(),
        rounds=default_rounds(),
        min_time=default_min_time(),
        max_time=default_max_time(),
        variation_cols=default_variation_cols(),
        kwargs_variations=default_kwargs_variations(),
        runner=default_runner(),
        callback=default_reporter_callback,
        options=default_reporter_options()
    )


def default_case_instance() -> Case:
    """Return a default Case instance for testing purposes.

    This is a 'pre-benchmarking' Case with default attributes set.
    """
    return Case(
        group=default_group(),
        title=default_title(),
        description=default_description(),
        action=default_benchcase)


def default_session_instance() -> Session:
    """Return a default Session instance for testing purposes.

    The Session is initialized with default attributes.
    """
    return Session(
        cases=[default_case_instance()],
        verbosity=Verbosity.QUIET,

    )


def default_namespace() -> Namespace:
    """Return a default ArgumentParser instance for testing purposes.

    It is minimally configured with the program name 'simplebench'.
    """
    arg_parser = ArgumentParser(prog='simplebench')
    args = arg_parser.parse_args([])
    return args


@lru_cache(typed=True)
def choice_conf_instance(cache_id: str = 'default',  # pylint: disable=unused-argument
                         name: str = 'mock', flags: tuple[str, ...] = ('--mock',)) -> ChoiceConf:
    """Factory function to return the same mock ChoiceConf instance for testing.

    It caches the instance based on the cache_id so that multiple calls with the same
    cache_id return the same instance.

    Args:
        cache_id (str, default='default'):
            An identifier to cache different ChoiceConf instances if needed.
        name (str, default='mock'):
            The name of the ChoiceConf instance.
        flags (tuple[str, ...], default=('--mock',)):
            The flags associated with the ChoiceConf instance.
    """
    return ChoiceConf(
        flags=default_flags(),
        flag_type=default_flag_type(),
        name=default_name(),
        description=default_description(),
        sections=default_sections(),
        targets=default_targets(),
        output_format=default_output_format(),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append(),
        options=None,
        extra='mock_extra')


@lru_cache(typed=True)
def choice_instance(cache_id: str = 'default',
                    name: str | None = None,
                    flags: tuple[str, ...] | None = None) -> Choice:
    """Factory function to return a single cached Choice instance for testing.

    The choice instance is created using MockReporter() and is
    extracted from the MockReporter.choices attribute.

    It is cached based on the cache_id so that multiple calls with the same
    cache_id, name, and flags return the same instance.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Choice instances if needed.
        name (str | None, default=None):
            The name of the Choice instance.

            If None, the default name from default_name() is used.

        flags (tuple[str, ...] | None, default=None):
            The flags associated with the Choice instance.

            If None, the default flags from default_flags() are used.

            Tuple is used to ensure hashability for caching.
    """
    if name is None:
        name = default_name()
    if flags is None:
        flags = default_flags()
    if not isinstance(name, str):
        raise TypeError(f"Invalid type for name argument: {name!r}")
    if not isinstance(flags, tuple) or not all(isinstance(f, str) for f in flags):
        raise TypeError(f"Invalid type for flags argument: {flags!r}")
    choice_conf = choice_conf_instance(cache_id, name=name, flags=flags)
    reporter = reporter_instance(cache_id, choices_conf=(choice_conf,))
    return reporter.choices[name]


@lru_cache(typed=True)
def choices_conf_instance(cache_id: str = "default",
                          choices: tuple[ChoiceConf, ...] | None = None) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different ChoicesConf instances if needed.
        choices (tuple[ChoiceConf, ...] | None, default=None):
            A tuple of ChoiceConf instances to initialize the ChoicesConf with.

            If None, a default ChoicesConf instance with a single ChoiceConf
            instance created by default_choice_conf() is returned.

            Tuple is used to ensure hashability for caching.
    """
    if not isinstance(cache_id, str):
        raise TypeError(f"Invalid type for cache_id argument (should be str): {cache_id!r}")
    if choices is None:
        choices = (default_choice_conf(),)

    if not isinstance(choices, tuple) or not all(isinstance(c, ChoiceConf) for c in choices):
        raise TypeError(f"Invalid type for choices argument (should be tuple[ChoiceConf, ...]): {choices!r}")

    return ChoicesConf(choices)


@lru_cache(typed=True)
def reporter_instance(cache_id: str = "default",  # pylint: disable=unused-argument
                      choices_conf: ChoicesConf | None = None) -> Reporter:
    """Factory function to return a cached Reporter instance for testing.

    The instance is a MockReporter. It is cached based on the cache_id.
    This makes it possible to have multiple cached instances and for
    each to retain its own state if needed.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Reporter instances if needed.
        choices_conf (ChoicesConf | None, default=None):
            A ChoicesConf instance to initialize the Reporter with.
    """
    return MockReporter(choices_conf=choices_conf)


@lru_cache(typed=True)
def choices_instance(cache_id: str = "default", *,  # pylint: disable=unused-argument
                     choices: tuple[Choice, ...] | Choices | None = None) -> Choices:
    """Factory function to return a cached Choices instance for testing.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Choices instances if needed.
        choices (tuple[Choice, ...] | Choices | None, default=None):
            A sequence of Choice instances or a Choices instance to initialize the Choices instance.
    """
    if choices is None:
        result = Choices()
        if not isinstance(result, Choices):
            raise TypeError(f"{cache_id}: Invalid type for choices instance: {result!r}")
        return result
    if isinstance(choices, Choices):
        result = Choices(choices)
        if not isinstance(result, Choices):
            raise TypeError(f"{cache_id}: Invalid type for choices instance: {result!r}")
        return result
    if isinstance(choices, tuple) and all(isinstance(c, Choice) for c in choices):
        result = Choices(choices=choices)
        if not isinstance(result, Choices):
            raise TypeError(f"{cache_id}: Invalid type for choices instance: {result!r}")
        return result
    raise TypeError(f"Invalid type for choices argument: {choices!r}")


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
        choices_conf =  choices_conf_instance() if choices_conf is None else choices_conf
        super().__init__(
            name=default_name(),
            description=default_description(),
            sections=default_sections(),
            default_targets=default_default_targets(),
            targets=default_targets(),
            subdir='mockreports',
            options_type=ReporterOptions,
            file_suffix='mock',
            file_unique=True,
            file_append=False,
            formats={Format.JSON},
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
    """Return a default ReporterOptions instance for testing purposes."""
    return ConfiguredReporterOptions


class ConfiguredReporter(Reporter):
    """A mock reporter subclass with default options already set for testing purposes.

    Creates a Reporter with default parameters for testing that can be overridden as needed.

        - name=default_name(),
        - description=default_description(),
        - options_type=ConfiguredReporterOptions,
        - sections=default_sections(),
        - targets=default_targets(),
        - formats=default_formats_list(),
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
            - formats=default_formats_list(),
            - choices=default_choice_confs(),
            - file_suffix=default_file_suffix(),
            - file_unique=default_file_unique(),
            - file_append=default_file_append()
        """

        super().__init__(
            name=default_name(),
            description=default_description(),
            options_type=default_options_type(),
            sections=default_sections(),
            targets=default_targets(),
            formats=default_formats_list(),
            choices=default_choice_confs(),
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


def reporter_kwargs() -> ReporterKWArgs:
    """A preconfigured ReporterKWArgs instance for testing purposes.

    ReporterKWArgs(
        name=default_name(),
        description=default_description(),
        sections=default_sections(),
        targets=default_targets(),
        formats=default_formats_list(),
        choices=default_choices_instance(reporter=ConfiguredReporter()),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )

    Returns:
        ReporterKWArgs: A preconfigured instance with default values for testing.
    """
    return ReporterKWArgs(
        name=default_name(),
        description=default_description(),
        options_type=default_options_type(),
        sections=default_sections(),
        targets=default_targets(),
        formats=default_formats_list(),
        choices=default_choice_confs(),
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append()
    )


reporter_kwargs_instance = reporter_kwargs()


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
            flags=flags if flags is not None else default_flags(),
            flag_type=flag_type if flag_type is not None else default_flag_type(),
            name=name if name is not None else default_name(),
            description=description if description is not None else default_description(),
            sections=sections if sections is not None else default_sections(),
            targets=targets if targets is not None else default_targets(),
            output_format=output_format if output_format is not None else default_output_format()
        )


def default_choice_conf_kwargs() -> ChoiceConfKWArgs:
    """Return default ChoiceConKWArgs for testing purposes."""
    return ChoiceConfKWArgs(
        flags=default_flags(),
        flag_type=default_flag_type(),
        name=default_name(),
        description=default_description(),
        sections=default_sections(),
        targets=default_targets(),
        output_format=default_output_format()
    )


default_choice_conf_kwargs_instance = default_choice_conf_kwargs()


class ConfiguredCase(Case):
    """A dummy Case subclass for testing purposes."""
    def __init__(self) -> None:
        super().__init__(
            group='test_case',
            title='Test Case',
            description='A test case for testing.',
            action=default_benchcase())
        self._results.append(Results(  # made-up results for testing purposes
            group='test_case', title='Test Case', description='A test case for testing.',
            n=10, total_elapsed=6.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0), Iteration(elapsed=3.0)]))


case_instance = ConfiguredCase()
"""A preconfigured ConfiguredCase instance for testing purposes.

Used to avoid re-instantiating multiple times in tests that
need multiple access to the same Case instance.
"""


class ConfiguredSession(Session):
    """A dummy Session subclass for testing purposes."""
    def __init__(self) -> None:

        super().__init__(cases=[case_instance])


session_instance = ConfiguredSession()
"""A preconfigured ConfiguredSession instance for testing purposes.

Used to avoid re-instantiating multiple times in tests
that need multiple access to the same Session instance.
"""

