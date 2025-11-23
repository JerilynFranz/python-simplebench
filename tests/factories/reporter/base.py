"""Factories for creating Reporter, Choice, and Choices test objects."""
# pylint: disable=unused-argument
from typing import Any, ClassVar, TypeAlias, overload

from rich.table import Table
from rich.text import Text

from simplebench.case import Case
from simplebench.enums import Section
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices, ChoicesConf
from simplebench.reporters.reporter import Reporter, ReporterConfig, ReporterOptions

from ...cache_factory import CACHE_DEFAULT, CacheId, cached_factory, uncached_factory
from ...kwargs import ChoiceConfKWArgs, ChoicesConfKWArgs
from .._primitives import (
    default_choice_flags,
    default_choice_name,
    default_default_targets,
    default_description,
    default_file_append,
    default_file_suffix,
    default_file_unique,
    default_flag_type,
    default_output_format,
    default_report_output,
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
from .report_log_metadata import report_log_metadata_factory
from .reporter_config import reporter_config_factory, reporter_config_kwargs_factory


@uncached_factory
def report_parameters_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> dict[str, Any]:
    """Return report parameters for testing purposes.

    It is uncached by default to ensure that each call returns a fresh dictionary.
    This can be overridden by providing a non-None cache_id.

    Because the parameters include mutable instances like Case and Choice,
    it is important to use cache_id appropriately to avoid unintended side effects
    from shared instances in tests.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A dictionary of default report parameters.
    :rtype: dict[str, Any]
    """
    return {
        'args': namespace_factory(),
        'log_metadata': report_log_metadata_factory(),
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
                reporter_config: ReporterConfig) -> None:
        """Initialize Reporter with provided kwargs.

        :param reporter_config: The ReporterConfig instance to use for this reporter.
        :type reporter_config: ReporterConfig
        """
        config = reporter_config_factory() if reporter_config is None else reporter_config
        super().__init__(config)

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str | bytes | Text | Table:
        """Render the report for the given case, section, and options.

        :param case: The case to render.
        :type case: Case
        :param section: The section to render.
        :type section: Section
        :param options: The options for rendering.
        :type options: ReporterOptions
        :return: The rendered report.
        :rtype: str | bytes | Text | Table
        """
        return default_report_output()


def default_options_type() -> type[Options]:
    """Return a default ReporterOptions type for testing purposes.

    :return: A FactoryReporterOptions type.
    :rtype: type[FactoryReporterOptions]
    """
    return Options


@overload
def choice_conf_kwargs_factory() -> ChoiceConfKWArgs:
    """Return a ChoiceConfKWArgs for testing purposes.

    It contains all parameters set to explicit default values for testing purposes.
    Because ChoiceConfKWArgs has many parameters, they are listed here for clarity:

    .. code-block:: python

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
    :return: A default ChoiceConfKWArgs instance.
    :rtype: ChoiceConfKWArgs
    """


# Overloads provide IDE tooltips and docstrings for the cache_factory decorated function.
# They are not strictly necessary for functionality, but improve developer experience.
@overload
def choice_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoiceConfKWArgs:
    """Return a ChoiceConfKWArgs for testing purposes.

    It contains all parameters set to explicit default values for testing purposes.
    Because ChoiceConfKWArgs has many parameters, they are listed here for clarity:

    .. code-block:: python

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

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A default ChoiceConfKWArgs instance.
    :rtype: ChoiceConfKWArgs
    """


@cached_factory
def choice_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoiceConfKWArgs:
    """Return a ChoiceConfKWArgs for testing purposes.

    It contains all parameters set to explicit default values for testing purposes.
    Because ChoiceConfKWArgs has many parameters, they are listed here for clarity:

    .. code-block:: python

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

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A default ChoiceConfKWArgs instance.
    :rtype: ChoiceConfKWArgs
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

    .. code-block:: python

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

    :return: A default ChoicesConfKWArgs instance.
    :rtype: ChoicesConfKWArgs
    """
    return choice_conf_kwargs_factory(cache_id=f'{__name__}.default_choice_conf_kwargs:singleton')


@overload
def choices_conf_kwargs_factory() -> ChoicesConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It contains a single ChoiceConf created by default_choice_conf_kwargs().

    :return: A default ChoicesConfKWArgs instance.
    :rtype: ChoicesConfKWArgs
    """


# overloads provide IDE tooltips and docstrings for the cache_factory decorated function.
# They are not strictly necessary for functionality, but improve developer experience.
@overload
def choices_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It contains a single ChoiceConf created by default_choice_conf_kwargs().

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A default ChoicesConfKWArgs instance.
    :rtype: ChoicesConfKWArgs
    """


@cached_factory
def choices_conf_kwargs_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It contains a single ChoiceConf created by default_choice_conf_kwargs().

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A default ChoicesConfKWArgs instance.
    :rtype: ChoicesConfKWArgs
    """
    return ChoicesConfKWArgs()


def default_choices_conf_kwargs() -> ChoicesConfKWArgs:
    """Return default ChoicesConfKWArgs for testing purposes.

    It always returns the same ChoicesConfKWArgs instance created by choices_conf_kwargs_factory().

    :return: A default ChoicesConfKWArgs instance.
    :rtype: ChoicesConfKWArgs
    """
    return choices_conf_kwargs_factory(cache_id=f'{__name__}.default_choices_conf_kwargs:singleton')


@overload
def choice_conf_factory() -> ChoiceConf:
    """Factory to create ChoiceConf with default values.

    This factory constructs a ChoiceConf instance populated with
    default values for testing the ChoiceConf class.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        - renderer (ReportRenderer): RenderRecorder()
        - args (Namespace): namespace_factory(cache_id=cache_id),
        - case (Case): case_factory(cache_id=cache_id).
        - choice (Choice): choice_factory(cache_id=cache_id).
        - path (Path): path_factory(cache_id=cache_id).
        - session (Session): session_factory(cache_id=cache_id).
        - callback (ReporterCallback): CallbackRecorder()

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A ChoiceConf instance.
    :rtype: ChoiceConf
    """


@overload
def choice_conf_factory(*,
                        cache_id: CacheId = CACHE_DEFAULT,
                        name: str | None = None,
                        flags: tuple[str, ...] | None = None) -> ChoiceConf:
    """Factory to create ChoiceConf with default values.

    This factory constructs a ChoiceConf instance populated with
    default values for testing the ChoiceConf class.
    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        - renderer (ReportRenderer): RenderRecorder()
        - args (Namespace): namespace_factory(cache_id=cache_id),
        - case (Case): case_factory(cache_id=cache_id).
        - choice (Choice): choice_factory(cache_id=cache_id).
        - path (Path): path_factory(cache_id=cache_id).
        - session (Session): session_factory(cache_id=cache_id).
        - callback (ReporterCallback): CallbackRecorder()

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param name: The name of the ChoiceConf instance.
    :type name: str | None
    :param flags: The flags associated with the ChoiceConf instance.
    :type flags: tuple[str, ...] | None
    :return: A ChoiceConf instance.
    :rtype: ChoiceConf
    """


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

    :param cache_id: An identifier to cache different ChoiceConf instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param name: The name of the ChoiceConf instance.
    :type name: str | None
    :param flags: The flags associated with the ChoiceConf instance.
    :type flags: tuple[str, ...] | None
    :return: A ChoiceConf instance.
    :rtype: ChoiceConf
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

    :return: A default ChoiceConf instance.
    :rtype: ChoiceConf
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

    :param cache_id: An identifier to cache different Choice instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Choice instance.
    :rtype: Choice
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

    .. code-block:: python

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

    :param cache_id: An identifier to cache different Choice instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param name: The name of the Choice instance.
                 If None, the default name from default_choice_name() is used.
    :type name: str | None
    :param flags: The flags associated with the Choice instance.
                  If None, the default flags from default_choice_flags() are used.
                  Tuple is used to ensure hashability for caching.
    :type flags: tuple[str, ...] | None
    :return: A Choice instance.
    :rtype: Choice
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

    :param cache_id: An identifier to cache different Choice instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param name: The name of the Choice instance.
                 If None, the default name from default_choice_name() is used.
    :type name: str | None
    :param flags: The flags associated with the Choice instance.
                  If None, the default flags from default_choice_flags() are used.
                  Tuple is used to ensure hashability for caching.
    :type flags: tuple[str, ...] | None
    :return: A Choice instance.
    :rtype: Choice
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
                                            choices=(choice_conf_factory(cache_id=cache_id,
                                                                         name=name,
                                                                         flags=flags), ))
    else:
        choices_conf = choices_conf_factory(cache_id=cache_id)
    kwargs = reporter_config_kwargs_factory().replace(choices=choices_conf)
    config = ReporterConfig(**kwargs)
    reporter = reporter_factory(cache_id=cache_id, reporter_config=config)
    return reporter.choices[name]


# overloads provide IDE tooltips and docstrings for the cache_factory decorated function.
# They are not strictly necessary for functionality, but improve developer experience.
@overload
def choices_conf_factory(choices: tuple[ChoiceConf, ...]) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    :param choices: A tuple of ChoiceConf instances to initialize the ChoicesConf with.
                    If None, a default ChoicesConf instance with a single ChoiceConf
                    instance created by default_choice_conf() is returned.
                    Tuple is used to ensure hashability for caching.
    :type choices: tuple[ChoiceConf, ...] | None
    :param cache_id: An identifier to cache different ChoicesConf instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A ChoicesConf instance.
    :rtype: ChoicesConf
    """


@overload
def choices_conf_factory(*,
                         choices: tuple[ChoiceConf, ...] | None = None,
                         cache_id: CacheId = CACHE_DEFAULT) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    :param choices: A tuple of ChoiceConf instances to initialize the ChoicesConf with.
                    If None, a default ChoicesConf instance with a single ChoiceConf
                    instance created by default_choice_conf() is returned.
                    Tuple is used to ensure hashability for caching.
    :type choices: tuple[ChoiceConf, ...] | None
    :param cache_id: An identifier to cache different ChoicesConf instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A ChoicesConf instance.
    :rtype: ChoicesConf
    """


@cached_factory
def choices_conf_factory(*, choices: tuple[ChoiceConf, ...] | None = None) -> ChoicesConf:
    """Factory function to return a cached ChoicesConf instance for testing.

    :param choices: A tuple of ChoiceConf instances to initialize the ChoicesConf with.
                    If None, a default ChoicesConf instance with a single ChoiceConf
                    instance created by default_choice_conf() is returned.
                    Tuple is used to ensure hashability for caching.
    :type choices: tuple[ChoiceConf, ...] | None
    :param cache_id: An identifier to cache different ChoicesConf instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A ChoicesConf instance.
    :rtype: ChoicesConf
    """
    if choices is None:
        choices = (default_choice_conf(), )

    if not isinstance(choices, tuple) or not all(isinstance(c, ChoiceConf) for c in choices):
        raise TypeError(f"Invalid type for choices argument (should be tuple[ChoiceConf, ...]): {choices!r}")

    return ChoicesConf(choices)


def default_choices_conf() -> ChoicesConf:
    """Return a default ChoicesConf instance for testing purposes.

    It always returns the same ChoicesConf instance created by choices_conf_factory().

    :return: A default ChoicesConf instance.
    :rtype: ChoicesConf
    """
    return choices_conf_factory(cache_id=f'{__name__}.default_choices_conf:singleton')


@overload
def reporter_factory() -> FactoryReporter:
    """Factory function to return an uncached FactortyReporter instance for testing.

    By default, it uses default_reporter_kwargs() to provide a set of parameters
    to initialize the FactoryReporter. However, custom parameters can be provided
    via the reporter_kwargs argument.

    It does not cache the created FactoryReporter instance by default, so each call
    returns a new instance.

    To override this caching behavior, provide a non-None cache_id and it will be cached
    based on that identifier.

    :param cache_id: An identifier to cache different UnconfiguredReporter instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param reporter_kwargs: Keyword arguments to initialize the UnconfiguredReporter.
                            If none, default_reporter_kwargs() is used to provide a default set of parameters.
    :type reporter_kwargs: ReporterKWArgs | None
    :return: A FactoryReporter instance.
    :rtype: FactoryReporter
    """


@overload
def reporter_factory(*,
                     cache_id: CacheId = CACHE_DEFAULT,
                     reporter_config: ReporterConfig | None = None) -> FactoryReporter:
    """Factory function to return an uncached FactortyReporter instance for testing.

    By default, it uses default_reporter_kwargs() to provide a set of parameters
    to initialize the FactoryReporter. However, custom parameters can be provided
    via the reporter_kwargs argument.
    It does not cache the created FactoryReporter instance by default, so each call
    returns a new instance.
    To override this caching behavior, provide a non-None cache_id and it will be cached
    based on that identifier.

    :param cache_id: An identifier to cache different UnconfiguredReporter instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param reporter_config: ReporterConfig to initialize the UnconfiguredReporter.
                            If none, default_reporter_config() is used to provide a default config.
    :type reporter_config: ReporterConfig | None
    :return: A FactoryReporter instance.
    :rtype: FactoryReporter
    """


@uncached_factory
def reporter_factory(*,
                     cache_id: CacheId = CACHE_DEFAULT,
                     reporter_config: ReporterConfig | None = None) -> FactoryReporter:
    """Factory function to return an uncached FactortyReporter instance for testing.

    By default, it uses default_reporter_kwargs() to provide a set of parameters
    to initialize the FactoryReporter. However, custom parameters can be provided
    via the reporter_kwargs argument.

    It does not cache the created FactoryReporter instance by default, so each call
    returns a new instance.

    To override this caching behavior, provide a non-None cache_id and it will be cached
    based on that identifier.

    :param cache_id: An identifier to cache different UnconfiguredReporter instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param reporter_config: ReporterConfig to initialize the UnconfiguredReporter.
                            If none, default_reporter_config_kwargs() is used to provide a default set of parameters.
    :type reporter_config: ReporterConfig | None
    :return: A FactoryReporter instance.
    :rtype: FactoryReporter
    """
    if reporter_config is not None and not isinstance(reporter_config, ReporterConfig):
        raise TypeError(f"Invalid type for reporter_config argument: {reporter_config!r}")
    config = reporter_config_factory() if reporter_config is None else reporter_config
    return FactoryReporter(reporter_config=config)


@cached_factory
def choices_factory(*,
                    cache_id: CacheId = CACHE_DEFAULT,
                    choices: tuple[ChoiceConf, ...] | ChoicesConf | None = None) -> Choices:
    """Factory function to return a cached Choices instance for testing.

    :param cache_id: An identifier to cache different Choices instances if needed.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :param choices: A sequence of ChoiceConf instances or a ChoicesConf instance to initialize the Choices instance.
    :type choices: tuple[ChoiceConf, ...] | ChoicesConf | None
    :return: A Choices instance.
    :rtype: Choices
    """
    if choices is None:
        return Choices()

    if isinstance(choices, tuple) and all(isinstance(c, ChoiceConf) for c in choices):
        choices_conf = ChoicesConf(choices)
    elif isinstance(choices, ChoicesConf):
        choices_conf = choices
    else:
        raise TypeError(f"Invalid type for choices argument: {choices!r}")

    kwargs = reporter_config_kwargs_factory().replace(choices=choices_conf)
    config = ReporterConfig(**kwargs)
    reporter = reporter_factory(cache_id=cache_id, reporter_config=config)
    return reporter.choices
