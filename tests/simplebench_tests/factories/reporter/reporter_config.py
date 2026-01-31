"""Factories for ReporterConfig instances for use in tests."""
# pyright: ignore[reportCallIssue]
# ruff: noqa: F821,F401

from collections.abc import Iterable
from typing import TYPE_CHECKING

from simplebench_tests import factories
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, NoDefaultValue, ReporterConfigKWArgs

from simplebench.enums import Format, Target
from simplebench.metrics import Metric, MetricsSelection
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.simplebench_types import ElementCollection

if TYPE_CHECKING:
    from simplebench.reporters.reporter._config import ReporterConfig


def reporter_config_kwargs_factory(  # pylint: disable=unused-argument
        *,
        name: str | NoDefaultValue = NO_DEFAULT_VALUE,
        description: str | NoDefaultValue = NO_DEFAULT_VALUE,
        metrics: MetricsSelection | NoDefaultValue = NO_DEFAULT_VALUE,
        targets: Iterable[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
        default_targets: Iterable[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
        subdir: str | NoDefaultValue = NO_DEFAULT_VALUE,
        file_suffix: str | NoDefaultValue = NO_DEFAULT_VALUE,
        file_unique: bool | NoDefaultValue = NO_DEFAULT_VALUE,
        file_append: bool | NoDefaultValue = NO_DEFAULT_VALUE,
        formats: Iterable[Format] | NoDefaultValue = NO_DEFAULT_VALUE,
        choices: ChoicesConf | NoDefaultValue = NO_DEFAULT_VALUE) -> ReporterConfigKWArgs:
    """Constructs a ReporterConfigKWArgs instance for use in tests.
    :param name: The unique identifying name of the reporter. Must be a non-empty string.
    :type name: str
    :param description: A brief description of the reporter. Must be a non-empty string.
    :type description: str
    :param metrics: The set of all Metrics supported by the reporter.
    :type metrics: Iterable[Metric]
    :param targets: The set of all Targets supported by the reporter.
    :type targets: Iterable[Target]
    :param default_targets: The default set of Targets for the reporter.
    :type default_targets: Iterable[Target]
    :param subdir: The subdirectory where report files will be saved.
    :type subdir: str
    :param file_suffix: An optional file suffix for reporter output files.
                        - May be an empty string ('')
                        - Cannot contain non-alphanumeric characters (characters other than A-Z, a-z, 0-9).
                        - Cannot be longer than 10 characters.
    :type file_suffix: str
    :param file_unique: Whether output files should have unique names.
    :type file_unique: bool
    """

    defaults = {
        'name': factories.default_reporter_name(),
        'description': factories.default_description(),
        'metrics': factories.default_metrics_selection(),
        'targets': factories.targets_factory(),
        'default_targets': factories.default_default_targets(),
        'subdir': factories.default_subdir(),
        'file_suffix': factories.default_file_suffix(),
        'file_unique': factories.default_file_unique(),
        'file_append': factories.default_file_append(),
        'formats': factories.default_formats(),
        'choices': factories.default_choices_conf(),
    }
    overrides = {k: v for k, v in locals().items() if k in defaults and not isinstance(v, NoDefaultValue)}
    kwargs = defaults | overrides
    return ReporterConfigKWArgs(**kwargs)  # type: ignore[arg-type]


def reporter_config_factory(
        *,
        name: str | NoDefaultValue = NO_DEFAULT_VALUE,
        description: str | NoDefaultValue = NO_DEFAULT_VALUE,
        metrics: MetricsSelection | NoDefaultValue = NO_DEFAULT_VALUE,
        targets: Iterable[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
        default_targets: Iterable[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
        subdir: str | NoDefaultValue = NO_DEFAULT_VALUE,
        file_suffix: str | NoDefaultValue = NO_DEFAULT_VALUE,
        file_unique: bool | NoDefaultValue = NO_DEFAULT_VALUE,
        file_append: bool | NoDefaultValue = NO_DEFAULT_VALUE,
        formats: Iterable[Format] | NoDefaultValue = NO_DEFAULT_VALUE,
        choices: ChoicesConf | NoDefaultValue = NO_DEFAULT_VALUE) -> 'ReporterConfig':
    """Constructs a preconfigured ReporterConfig instance for use in tests.

    :param name: The unique identifying name of the reporter. Must be a non-empty string.
    :type name: str
    :param description: A brief description of the reporter. Must be a non-empty string.
    :type description: str
    :param metrics: The set of all Metrics supported by the reporter.
    :type metrics: Iterable[Metric]
    :param targets: The set of all Targets supported by the reporter.
    :type targets: Iterable[Target]
    :param default_targets: The default set of Targets for the reporter.
    :type default_targets: Iterable[Target]
    :param subdir: The subdirectory where report files will be saved.
    :type subdir: str
    :param file_suffix: An optional file suffix for reporter output files.
                        - May be an empty string ('')
                        - Cannot contain non-alphanumeric characters (characters other than A-Z, a-z, 0-9).
                        - Cannot be longer than 10 characters.
    :type file_suffix: str
    :param file_unique: Whether output files should have unique names.
    :type file_unique: bool
    :param file_append: Whether output files should be appended to.
    :type file_append: bool
    :param formats: The set of all Formats supported by the reporter.
    :type formats: Iterable[Format]
    :param choices: The ChoicesConf instance defining choice configurations for the reporter.
    :type choices: ChoicesConf
    :return: A ReporterConfig instance.
    :rtype: ReporterConfig
    """
    from simplebench.reporters.reporter._config import ReporterConfig

    # Directly use the kwargs factory to get the final set of arguments
    kwargs = reporter_config_kwargs_factory(
        name=name,
        description=description,
        metrics=metrics,
        targets=targets,
        default_targets=default_targets,
        subdir=subdir,
        file_suffix=file_suffix,
        file_unique=file_unique,
        file_append=file_append,
        formats=formats,
        choices=choices,
    )
    return ReporterConfig(**kwargs)
