"""Test simplebench/reporters/reporter/reporter.py module"""
from __future__ import annotations

import pytest

from simplebench.enums import Format, Section, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.reporter import ReporterConfig
from simplebench.reporters.reporter.exceptions import ReporterConfigErrorTag
from simplebench.validators.exceptions import _ValidatorsErrorTag

from ...factories import reporter_config_kwargs_factory
from ...testspec import Assert, TestAction, TestSpec, idspec


@pytest.mark.parametrize('testspec', [
    idspec('INIT_008', TestAction(
        name="Init of ReporterConfig with missing name raises TypeError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory() - ['name'],
        exception=TypeError)),
    idspec('INIT_009', TestAction(
        name="Init of ReporterConfig with missing description raises TypeError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory() - ['description'],
        exception=TypeError)),
    idspec('INIT_010', TestAction(
        name="Init of ReporterConfig with missing sections raises TypeError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory() - ['sections'],
        exception=TypeError)),
    idspec('INIT_011', TestAction(
        name=("Init of ReporterConfig with empty targets raises "
              "SimpleBenchValueError/TARGETS_INVALID_ARG_TYPE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(targets=set()),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_TARGETS_VALUE)),
    idspec('INIT_012', TestAction(
        name=("Init of ReporterConfig with empty formats raises "
              "SimpleBenchValueError/SECTIONS_ITEMS_ARG_VALUE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(formats=set()),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_FORMATS_VALUE)),
    idspec('INIT_013', TestAction(
        name="Init of ReporterConfig with missing choices raises TypeError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory() - ['choices'],
        exception=TypeError)),
    idspec('INIT_014', TestAction(
        name=("Init of ReporterConfig with choices not being a ChoicesConf instance raises "
              "SimpleBenchTypeError/INVALID_CHOICES_ARG_TYPE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(
            choices="not_a_choices_instance"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ReporterConfigErrorTag.INVALID_CHOICES_TYPE)),
    idspec('INIT_015', TestAction(
        name=("Init of ReporterConfig with sections containing a non-Section enum raises "
              "SimpleBenchTypeError/SECTION_INVALID_ENTRY_TYPE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(sections={
            Section.OPS, "not_a_section_enum"}),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ReporterConfigErrorTag.INVALID_SECTIONS_TYPE)),
    idspec('INIT_016', TestAction(
        name=("Init of ReporterConfig with targets containing non-Target enum raises "
              "SimpleBenchTypeError/TARGETS_INVALID_ARG_TYPE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(targets={
            Target.CONSOLE, "not_a_target_enum"}),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ReporterConfigErrorTag.INVALID_TARGETS_TYPE)),
    idspec('INIT_017', TestAction(
        name=("Init of ReporterConfig with formats set to a non-Format enum raises "
              "SimpleBenchTypeError/FORMATS_INVALID_ARG_TYPE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(formats={
            Format.JSON, "not_a_format_enum"}),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ReporterConfigErrorTag.INVALID_FORMATS_TYPE)),
    idspec('INIT_018', TestAction(
        name=("Init of ReporterConfig with empty name raises "
              "SimpleBenchValueError/NAME_INVALID_ARG_VALUE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(name=''),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_NAME_VALUE)),
    idspec('INIT_019', TestAction(
        name=("Init of ReporterConfig with blank name raises "
              "SimpleBenchValueError/NAME_INVALID_ARG_VALUE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(name='  '),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_NAME_VALUE)),
    idspec('INIT_020', TestAction(
        name=("Init of ReporterConfig with empty description raises "
              "SimpleBenchValueError/DESCRIPTION_INVALID_ARG_VALUE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(description=''),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_DESCRIPTION_VALUE)),
    idspec('INIT_021', TestAction(
        name=("Init of ReporterConfig with blank description raises "
              "SimpleBenchValueError/DESCRIPTION_INVALID_ARG_VALUE"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(description='   '),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_DESCRIPTION_VALUE)),
    idspec('INIT_024', TestAction(
        name="Init of ReporterConfig with a subdir path element longer than 64 characters raises SimpleBenchValueError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory(subdir='a' * 65),
        exception=SimpleBenchValueError,
        exception_tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_ELEMENT_TOO_LONG)),
    idspec('INIT_025', TestAction(
        name=("Init of ReporterConfig with subdir name containing "
              "non-alphanumeric characters raises SimpleBenchValueError"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(subdir='invalid subdir!'),
        exception=SimpleBenchValueError,
        exception_tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_INVALID_CHARACTERS)),
    idspec('INIT_026', TestAction(
        name="Init of ReporterConfig with file_suffix as non-string raises SimpleBenchTypeError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_suffix=123),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterConfigErrorTag.INVALID_FILE_SUFFIX_TYPE)),
    idspec('INIT_027', TestAction(
        name="Init of ReporterConfig with file_suffix longer than 10 characters raises SimpleBenchValueError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_suffix='a' * 11),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_FILE_SUFFIX_VALUE_TOO_LONG)),
    idspec('INIT_028', TestAction(
        name=("Init of ReporterConfig with file_suffix containing "
              "non-alphanumeric characters raises SimpleBenchValueError"),
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_suffix='invalid!'),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_FILE_SUFFIX_VALUE)),
    idspec('INIT_029', TestAction(
        name="Init of ReporterConfig with file_unique as a non-boolean raises SimpleBenchTypeError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_unique='not_a_bool'),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterConfigErrorTag.INVALID_FILE_UNIQUE_TYPE)),
    idspec('INIT_030', TestAction(
        name="Init of ReporterConfig with file_append as a non-boolean raises SimpleBenchTypeError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_append='not_a_bool'),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterConfigErrorTag.INVALID_FILE_UNIQUE_TYPE)),
    idspec('INIT_031', TestAction(
        name="Init of ReporterConfig with file_unique and file_append both True raises SimpleBenchValueError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_unique=True, file_append=True),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_FILE_APPEND_FILE_UNIQUE_COMBINATION)),
    idspec('INIT_032', TestAction(
        name="Init of ReporterConfig with file_unique and file_append both False raises SimpleBenchValueError",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_unique=False, file_append=False),
        exception=SimpleBenchValueError,
        exception_tag=ReporterConfigErrorTag.INVALID_FILE_APPEND_FILE_UNIQUE_ONE_MUST_BE_TRUE)),
    idspec('INIT_033', TestAction(
        name="Init of ReporterConfig with file_append as True and file_unique as False works",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_append=True, file_unique=False),
        assertion=Assert.ISINSTANCE,
        expected=ReporterConfig)),
    idspec('INIT_034', TestAction(
        name="Init of ReporterConfig with file_unique as False and file_append as True works",
        action=ReporterConfig,
        kwargs=reporter_config_kwargs_factory().replace(file_unique=False, file_append=True),
        assertion=Assert.ISINSTANCE,
        expected=ReporterConfig)),
])
def test_reporter_config_init(testspec: TestSpec) -> None:
    """Test ReporterConfig init parameters.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
