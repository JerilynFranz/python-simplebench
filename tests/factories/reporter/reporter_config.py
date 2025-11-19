"""Factories for ReporterConfig instances for use in tests."""
# pylint: disable=import-outside-toplevel
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from simplebench.enums import Format, Section, Target
from simplebench.reporters.choices.choices_conf import ChoicesConf

from ...factories import (
    default_default_targets,
    default_description,
    default_file_append,
    default_file_suffix,
    default_file_unique,
    default_formats,
    default_reporter_name,
    default_sections,
    default_subdir,
    targets_factory,
)
from ...kwargs import NoDefaultValue, ReporterConfigKWArgs

# Modules to defer import to avoid circular imports
_DEFERRED_MODULES_IMPORTED = False
if TYPE_CHECKING:
    from simplebench.reporters.reporter.config import ReporterConfig

    from ...factories import default_choices_conf
    _DEFERRED_MODULES_IMPORTED = True
else:
    default_choices_conf = None  # pylint: disable=invalid-name
    ReporterConfig = None  # pylint: disable=invalid-name


def deferred_modules_import() -> None:
    """Defer the import of some modules to avoid circular imports."""
    global _DEFERRED_MODULES_IMPORTED, ReporterConfig, default_choices_conf  # pylint: disable=global-statement
    if not _DEFERRED_MODULES_IMPORTED:
        from simplebench.reporters.reporter.config import ReporterConfig

        from ...factories import default_choices_conf
        _DEFERRED_MODULES_IMPORTED = True


def reporter_config_kwargs_factory(  # pylint: disable=unused-argument
        *,
        name: str | NoDefaultValue = NoDefaultValue(),
        description: str | NoDefaultValue = NoDefaultValue(),
        sections: Iterable[Section] | NoDefaultValue = NoDefaultValue(),
        targets: Iterable[Target] | NoDefaultValue = NoDefaultValue(),
        default_targets: Iterable[Target] | NoDefaultValue = NoDefaultValue(),
        subdir: str | NoDefaultValue = NoDefaultValue(),
        file_suffix: str | NoDefaultValue = NoDefaultValue(),
        file_unique: bool | NoDefaultValue = NoDefaultValue(),
        file_append: bool | NoDefaultValue = NoDefaultValue(),
        formats: Iterable[Format] | NoDefaultValue = NoDefaultValue(),
        choices: ChoicesConf | NoDefaultValue = NoDefaultValue()) -> ReporterConfigKWArgs:
    """Constructs a ReporterConfigKWArgs instance for use in tests.
    :param name: The unique identifying name of the reporter. Must be a non-empty string.
    :type name: str
    :param description: A brief description of the reporter. Must be a non-empty string.
    :type description: str
    :param sections: The set of all Sections supported by the reporter.
    :type sections: Iterable[Section]
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
    deferred_modules_import()

    defaults = {
        'name': default_reporter_name(),
        'description': default_description(),
        'sections': default_sections(),
        'targets': targets_factory(),
        'default_targets': default_default_targets(),
        'subdir': default_subdir(),
        'file_suffix': default_file_suffix(),
        'file_unique': default_file_unique(),
        'file_append': default_file_append(),
        'formats': default_formats(),
        'choices': default_choices_conf(),
    }
    overrides = {k: v for k, v in locals().items() if k in defaults and not isinstance(v, NoDefaultValue)}
    kwargs = defaults | overrides
    return ReporterConfigKWArgs(**kwargs)  # type: ignore[arg-type]


def reporter_config_factory(
        *,
        name: str | NoDefaultValue = NoDefaultValue(),
        description: str | NoDefaultValue = NoDefaultValue(),
        sections: Iterable[Section] | NoDefaultValue = NoDefaultValue(),
        targets: Iterable[Target] | NoDefaultValue = NoDefaultValue(),
        default_targets: Iterable[Target] | NoDefaultValue = NoDefaultValue(),
        subdir: str | NoDefaultValue = NoDefaultValue(),
        file_suffix: str | NoDefaultValue = NoDefaultValue(),
        file_unique: bool | NoDefaultValue = NoDefaultValue(),
        file_append: bool | NoDefaultValue = NoDefaultValue(),
        formats: Iterable[Format] | NoDefaultValue = NoDefaultValue(),
        choices: ChoicesConf | NoDefaultValue = NoDefaultValue()) -> ReporterConfig:
    """Constructs a preconfigured ReporterConfig instance for use in tests.

    :param name: The unique identifying name of the reporter. Must be a non-empty string.
    :type name: str
    :param description: A brief description of the reporter. Must be a non-empty string.
    :type description: str
    :param sections: The set of all Sections supported by the reporter.
    :type sections: Iterable[Section]
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
    deferred_modules_import()

    # Directly use the kwargs factory to get the final set of arguments
    kwargs = reporter_config_kwargs_factory(
        name=name,
        description=description,
        sections=sections,
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
