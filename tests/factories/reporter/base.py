"""Factories for creating Reporter, Choice, and Choices test objects."""
# pylint: disable=unused-argument
from argparse import Namespace
from pathlib import Path
from typing import Any, ClassVar, Iterable, TypeAlias, overload

from simplebench.case import Case
from simplebench.enums import Format, Section, Target
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices, ChoicesConf
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.session import Session

from ...cache_factory import CACHE_DEFAULT, CacheId, cached_factory, uncached_factory
from ...kwargs import ChoiceConfKWArgs, ChoicesConfKWArgs, ReporterKWArgs
from .._primitives import (
    default_choice_flags,
    default_choice_name,
    default_default_targets,
    default_description,
    default_file_append,
    default_file_suffix,
    default_file_unique,
    default_flag_type,
    default_formats,
    default_output_format,
    default_report_output,
    default_reporter_name,
    default_sections,
    default_subdir,
    default_targets,
)
from .._utils import default_extra
from ..argparse import namespace_factory
from ..case import case_factory
from ..path import path_factory
from ..reporter_callback import default_reporter_callback
from ..reporter_options import FactoryReporterOptions, default_reporter_options
from ..session import session_factory


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


Options: TypeAlias = FactoryReporterOptions


class FactoryReporter(Reporter):
    """A dummy reporter subclass for testing purposes.

    No parameters are preset for this reporter and no defaults are provided.

    Provides a shim implementation of run_report() and render() methods to allow
    instantiation and testing of the Reporter base class functionality with
    both good and bad parameters.

    """
    _OPTIONS_TYPE: ClassVar[type[FactoryReporterOptions]] = FactoryReporterOptions  # pylint: disable=line-too-long  # type: ignore[reportIncompatibleVariableOveride]  # noqa: E501
    """The specific ReporterOptions subclass associated with this reporter."""
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}

    def __init__(  # pylint: disable=redefined-outer-name
                self,
                *,
                name: str,
                description: str,
                sections: Iterable[Section],
                targets: Iterable[Target],
                default_targets: Iterable[Target] | None = None,
                subdir: str = '',
                file_suffix: str,
                file_unique: bool,
                file_append: bool,
                formats: Iterable[Format],
                choices: ChoicesConf) -> None:
        """Initialize Reporter with provided kwargs.

        Args:
            name (str | None): Name of the reporter.
            description (str | None): Description of the reporter.
            sections (Iterable[Section] | None): Supported sections for the reporter.
            targets (Iterable[Target] | None): Supported targets for the reporter.
            default_targets (Iterable[Target] | None): Default targets for the reporter.
            formats (Iterable[Format] | None): Supported formats for the reporter.
            choices (ChoicesConf | None): ChoicesConf for the reporter.
            subdir (str | None): Subdirectory for the reporter.
            file_suffix (str | None): File suffix for the reporter.
            file_unique (str | None): File unique flag for the reporter.
            file_append (str | None): File append flag for the reporter.
        """
        kwargs: dict[str, Any] = {}
        if name is not None:
            kwargs['name'] = name
        if description is not None:
            kwargs['description'] = description
        if sections is not None:
            kwargs['sections'] = sections
        if targets is not None:
            kwargs['targets'] = targets
        if default_targets is not None:
            kwargs['default_targets'] = default_targets
        if formats is not None:
            kwargs['formats'] = formats
        if choices is not None:
            kwargs['choices'] = choices
        if subdir is not None:
            kwargs['subdir'] = subdir
        if file_suffix is not None:
            kwargs['file_suffix'] = file_suffix
        if file_unique is not None:
            kwargs['file_unique'] = file_unique
        if file_append is not None:
            kwargs['file_append'] = file_append

        super().__init__(**kwargs)  # pylint: disable=missing-kwoa  # type: ignore[misc]

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
        self.render_by_case(renderer=self.render,  # type: ignore[misc]
                            args=args,
                            case=case,
                            choice=choice,
                            path=path,
                            session=session,
                            callback=callback)

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:
        """Render the report for the given case, section, and options."""
        return default_report_output()


def default_options_type() -> type[Options]:
    """Return a default ReporterOptions type for testing purposes.

    Returns:
        type[FactoryReporterOptions]: A FactoryReporterOptions type.
    """
    return Options


# overloads provide tooltips and docstrings for the cache_factory decorated function
@overload
def reporter_kwargs_factory() -> ReporterKWArgs:
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
        options_type=default_options_type(),
        sections=default_sections(),
        targets=default_targets(),
        default_targets=default_default_targets(),
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


@overload
def reporter_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ReporterKWArgs:
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
        options_type=default_options_type(),
        sections=default_sections(),
        targets=default_targets(),
        default_targets=default_default_targets(),
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


@cached_factory
def reporter_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ReporterKWArgs:
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
        options_type=default_options_type(),
        sections=default_sections(),
        targets=default_targets(),
        default_targets=default_default_targets(),
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
        sections=default_sections(),
        targets=default_targets(),
        default_targets=default_default_targets(),
        formats=default_formats(),
        choices=default_choices_conf(),
        subdir="",
        file_suffix=default_file_suffix(),
        file_unique=default_file_unique(),
        file_append=default_file_append(),
    )


def default_reporter_kwargs() -> ReporterKWArgs:
    """A preconfigured ReporterKWArgs instance for testing purposes.

    It always returns the same ReporterKWArgs instance created by reporter_kwargs_factory().

    ReporterKWArgs(
        name=default_name(),
        description=default_description(),
        options_type=default_options_type(),
        sections=default_sections(),
        targets=default_targets(),
        default_targets=default_default_targets(),
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


@overload
def choice_conf_kwargs_factory() -> ChoiceConfKWArgs:
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


# Overloads provide IDE tooltips and docstrings for the cache_factory decorated function.
# They are not strictly necessary for functionality, but improve developer experience.
@overload
def choice_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoiceConfKWArgs:
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
            extra=default_extra(),
        )
    ```

    Args:
        cache_id (CacheId, optional, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        ChoiceConfKWArgs: A default ChoiceConfKWArgs instance.
    """


@cached_factory
def choice_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoiceConfKWArgs:
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
            extra=default_extra(),
        )
    ```

    Args:
        cache_id (CacheId, optional, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

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
        extra=default_extra(),
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


@overload
def choices_conf_kwargs_factory() -> ChoicesConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It contains a single ChoiceConf created by default_choice_conf_kwargs().

    Returns:
        ChoicesConfKWArgs: A default ChoicesConfKWArgs instance.
    """


# overloads provide IDE tooltips and docstrings for the cache_factory decorated function.
# They are not strictly necessary for functionality, but improve developer experience.
@overload
def choices_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It contains a single ChoiceConf created by default_choice_conf_kwargs().

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        ChoicesConfKWArgs: A default ChoicesConfKWArgs instance.
    """


@cached_factory
def choices_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConfKWArgs:
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
def choice_conf_factory(*,
                        cache_id: CacheId = CACHE_DEFAULT,
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
        extra=default_extra(),
    )


def default_choice_conf() -> ChoiceConf:
    """Return a default ChoiceConf instance for testing purposes.

    It is created by calling ChoiceConf with default_choice_conf_kwargs().

    It always returns the same instance for consistency in tests. Because
    ChoiceConf instances are immutable after creation, this is safe.

    Returns:
        ChoiceConf: A default ChoiceConf instance.
    """
    return choice_conf_factory(cache_id=f'{__name__}.default_choice_conf:singleton')


@overload
def choice_factory() -> Choice:
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
    Returns:
        Choice: A Choice instance.
    """


@overload
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

    The choice instance has the following parameters:

    ```python
         Choice(
                reporter=FactoryReporter(),
                flags=default_choice_flags(),
                flag_type=default_flag_type(),
                name=default_choice_name(),
                description=default_description(),
                sections=default_sections(),
                targets=default_targets(),
                output_format=default_output_format(),
                file_suffix=default_file_suffix(),
                file_unique=default_file_unique(),
                file_append=default_file_append(),
                options=default_reporter_options(),
                extra=default_extra()
         )
     ```
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
    is_default: bool = name is None and flags is None
    if name is None:
        name = default_choice_name()
    if flags is None:
        flags = default_choice_flags()
    if not isinstance(name, str):
        raise TypeError(f"Invalid type for name argument: {name!r}")
    if not isinstance(flags, tuple) or not all(isinstance(f, str) for f in flags):
        raise TypeError(f"Invalid type for flags argument: {flags!r}")
    if not is_default:
        choices_conf = choices_conf_factory(cache_id=cache_id,
                                            choices=(choice_conf_factory(cache_id=cache_id, name=name, flags=flags), ))
    else:
        choices_conf = choices_conf_factory(cache_id=cache_id)
    kwargs = default_reporter_kwargs().replace(choices=choices_conf)
    reporter = reporter_factory(cache_id=cache_id, reporter_kwargs=kwargs)
    return reporter.choices[name]


# overloads provide IDE tooltips and docstrings for the cache_factory decorated function.
# They are not strictly necessary for functionality, but improve developer experience.
@overload
def choices_conf_factory(choices: tuple[ChoiceConf, ...]) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    Args:
        choices (tuple[ChoiceConf, ...] | None, default=None):
            A tuple of ChoiceConf instances to initialize the ChoicesConf with.

            If None, a default ChoicesConf instance with a single ChoiceConf
            instance created by default_choice_conf() is returned.

            Tuple is used to ensure hashability for caching.

        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different ChoicesConf instances if needed.
            If None, caching is disabled for this call.
    Returns:
        ChoicesConf: A ChoicesConf instance.
    """


@overload
def choices_conf_factory(*,
                         choices: tuple[ChoiceConf, ...] | None = None,
                         cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    Args:
        choices (tuple[ChoiceConf, ...] | None, default=None):
            A tuple of ChoiceConf instances to initialize the ChoicesConf with.

            If None, a default ChoicesConf instance with a single ChoiceConf
            instance created by default_choice_conf() is returned.

            Tuple is used to ensure hashability for caching.
        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different ChoicesConf instances if needed.
            If None, caching is disabled for this call.

    Returns:
        ChoicesConf: A ChoicesConf instance.
    """


@cached_factory
def choices_conf_factory(*, choices: tuple[ChoiceConf, ...] | None = None) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    Args:
        choices (tuple[ChoiceConf, ...] | None, default=None):
            A tuple of ChoiceConf instances to initialize the ChoicesConf with.

            If None, a default ChoicesConf instance with a single ChoiceConf
            instance created by default_choice_conf() is returned.

            Tuple is used to ensure hashability for caching.
        cache_id (CacheId, default=CACHE_DEFAULT):
            An identifier to cache different ChoicesConf instances if needed.
            If None, caching is disabled for this call.

    Returns:
        ChoicesConf: A ChoicesConf instance.
    """
    if choices is None:
        choices = (default_choice_conf(), )

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
def reporter_factory(*,
                     cache_id: CacheId = CACHE_DEFAULT,
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
