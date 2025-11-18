"""Tests for argparse mixins in reporters."""
from argparse import ArgumentParser

import pytest

from simplebench.enums import FlagType, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.exceptions import ReporterErrorTag

from ....factories import (
    FactoryReporter,
    choice_conf_kwargs_factory,
    choice_factory,
    flag_name_factory,
    reporter_factory,
    reporter_kwargs_factory,
    reporter_namespace_factory,
)
from ....testspec import Assert, TestAction, TestSpec, idspec


@pytest.mark.parametrize('testspec', [
    idspec('SELECT_TARGETS_FROM_ARGS_001', TestAction(
        name="select_targets_from_args() with args specifying console target returns console target",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory(), Target.CONSOLE.value]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        assertion=Assert.EQUAL,
        expected={Target.CONSOLE})),
    idspec('SELECT_TARGETS_FROM_ARGS_002', TestAction(
        name="select_targets_from_args() with no specified target returns default targets",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        assertion=Assert.EQUAL,
        expected={Target.FILESYSTEM})),
    idspec('SELECT_TARGETS_FROM_ARGS_004', TestAction(
        name="select_targets_from_args() with args specifying multiple targets returns all specified targets",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory(
                            [flag_name_factory(), Target.CONSOLE.value, Target.FILESYSTEM.value]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        assertion=Assert.EQUAL,
        expected={Target.CONSOLE, Target.FILESYSTEM})),
    idspec('SELECT_TARGETS_FROM_ARGS_005', TestAction(
        name=("select_targets_from_args() incorrect args type raises SimpleBenchTypeError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': "not_a_namespace", 'choice': choice_factory(), 'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_ARGS_ARG)),
    idspec('SELECT_TARGETS_FROM_ARGS_006', TestAction(
        name=("select_targets_from_args() incorrect choice type raises SimpleBenchTypeError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': "not_a_choice_instance",
                'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_CHOICE_ARG)),
    idspec('SELECT_TARGETS_FROM_ARGS_007', TestAction(
        name=("select_targets_from_args() incorrect default_targets type raises SimpleBenchTypeError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': choice_factory(),
                'default_targets': "not_a_set_of_targets"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_DEFAULT_TARGETS_ARG)),
    idspec('SELECT_TARGETS_FROM_ARGS_008', TestAction(
        name="select_targets_from_args() with args including unsupported target raises SimpleBenchValueError",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory(
                            args=[flag_name_factory(), Target.CUSTOM.value],
                            choices=[Target.CUSTOM.value, Target.FILESYSTEM.value]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_UNSUPPORTED_TARGET)),
    idspec('SELECT_TARGETS_FROM_ARGS_009', TestAction(
        name=("select_targets_from_args() with an arg that does not match any "
              "Target enums raises SimpleBenchValueError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory(
                            args=[flag_name_factory(), "non_existent_target"],
                            choices=["non_existent_target"]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_UNKNOWN_TARGET_IN_ARGS)),
    idspec('SELECT_TARGETS_FROM_ARGS_010', TestAction(
        name="select_targets_from_args() with default target not supported by choice raises SimpleBenchValueError",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': choice_factory(),
                'default_targets': {Target.CUSTOM}},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_DEFAULT_TARGET_UNSUPPORTED)),
])
def test_select_targets_from_args(testspec: TestSpec) -> None:
    """Test Reporter.select_targets_from_args() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def add_flags_to_argparse_testspecs() -> list[TestSpec]:
    """Generate TestSpecs for testing add_flags_to_argparse method.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def add_a_boolean_flag() -> ArgumentParser:
        """Create an ArgumentParser with a boolean flag added by the reporter.

        :return: An argument parser.
        :rtype: ArgumentParser
        """
        choice_conf_kwargs = choice_conf_kwargs_factory().replace(
            flag_type=FlagType.BOOLEAN, flags=['--boolean-flag'])
        choices_conf = ChoicesConf(choices=[ChoiceConf(**choice_conf_kwargs)])
        reporter_kwargs = reporter_kwargs_factory().replace(choices=choices_conf)
        reporter = FactoryReporter(**reporter_kwargs)
        arg_parser = ArgumentParser(prog='test_reporter')
        reporter.add_flags_to_argparse(arg_parser)
        return arg_parser
    testspecs.extend([
        idspec('ADD_FLAGS_TO_ARGPARSE_001', TestAction(
            name="add_flags_to_argparse() adds parseable boolean flag to an ArgumentParser (present flag)",
            action=add_a_boolean_flag().parse_args,
            kwargs={
                'args': ['--boolean-flag']
            },
            validate_result=lambda result: result.boolean_flag is True)),
        idspec('ADD_FLAGS_TO_ARGPARSE_002', TestAction(
            name="add_flags_to_argparse() adds parseable boolean flag to an ArgumentParser (absent flag)",
            action=add_a_boolean_flag().parse_args,
            kwargs={
                'args': []
            },
            validate_result=lambda result: result.boolean_flag is False)),
    ])

    def add_a_target_list_flag() -> ArgumentParser:
        """Create an ArgumentParser with a target list flag added by the reporter.

        :return: An argument parser.
        :rtype: ArgumentParser
        """
        choice_conf_kwargs = choice_conf_kwargs_factory().replace(
            flag_type=FlagType.TARGET_LIST,
            flags=['--targets-list-flag'],
            targets={Target.CONSOLE, Target.FILESYSTEM},
            default_targets={Target.CONSOLE})
        choices_conf = ChoicesConf(choices=[ChoiceConf(**choice_conf_kwargs)])
        reporter_kwargs = reporter_kwargs_factory().replace(
            targets={Target.CONSOLE, Target.FILESYSTEM},
            choices=choices_conf)
        reporter = FactoryReporter(**reporter_kwargs)
        arg_parser = ArgumentParser(prog='test_reporter')
        reporter.add_flags_to_argparse(arg_parser)
        return arg_parser
    testspecs.extend([
        idspec('ADD_FLAGS_TO_ARGPARSE_003', TestAction(
            name="add_flags_to_argparse() adds parseable target list flag to an ArgumentParser (multiple targets)",
            action=add_a_target_list_flag().parse_args,
            kwargs={
                'args': ['--targets-list-flag', Target.CONSOLE.value, Target.FILESYSTEM.value]
            },
            validate_result=lambda result: len(result.targets_list_flag) == 1 and (
                set(result.targets_list_flag[0]) == {Target.CONSOLE.value, Target.FILESYSTEM.value}
            )
        )),
        idspec('ADD_FLAGS_TO_ARGPARSE_004', TestAction(
            name="add_flags_to_argparse() adds parseable target list flag to an ArgumentParser (no targets listed)",
            action=add_a_target_list_flag().parse_args,
            kwargs={
                'args': ['--targets-list-flag']
            },
            validate_result=lambda result: (
                len(result.targets_list_flag) == 1 and len(result.targets_list_flag[0]) == 0))),
        idspec('ADD_FLAGS_TO_ARGPARSE_005', TestAction(
            name="add_flags_to_argparse() adds parseable target list flag to an ArgumentParser (bad target listed)",
            action=add_a_target_list_flag().parse_args,
            kwargs={
                'args': ['--targets-list-flag', 'invalid_target']
            },
            exception=SystemExit,  # argparse raises SystemExit on parse errors
            )),
    ])

    def add_unsupported_flag_type_to_argparse() -> ArgumentParser:
        """Create an ArgumentParser with an unsupported flag type added by the reporter.

        :return: An argument parser.
        :rtype: ArgumentParser
        """
        choice_conf_kwargs = choice_conf_kwargs_factory().replace(
            flag_type=FlagType.INVALID, flags=['--invalid-flag'])
        choices_conf = ChoicesConf(choices=[ChoiceConf(**choice_conf_kwargs)])
        reporter_kwargs = reporter_kwargs_factory().replace(choices=choices_conf)
        reporter = FactoryReporter(**reporter_kwargs)
        arg_parser = ArgumentParser(prog='test_reporter')
        reporter.add_flags_to_argparse(arg_parser)
        return arg_parser  # pragma: no cover   # should raise before this point
    testspecs.append(idspec('ADD_FLAGS_TO_ARGPARSE_006', TestAction(
        name="add_flags_to_argparse() with unsupported flag type raises SimpleBenchValueError",
        action=add_unsupported_flag_type_to_argparse,
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.ADD_FLAGS_UNSUPPORTED_FLAG_TYPE,
    )))

    testspecs.append(idspec('ADD_FLAGS_TO_ARGPARSE_007', TestAction(
        name="add_flags_to_argparse() with invalid parser arg type raises SimpleBenchTypeError",
        action=reporter_factory().add_flags_to_argparse,
        kwargs={'parser': "not_an_argument_parser"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE,
    )))

    return testspecs


@pytest.mark.parametrize('testspec', add_flags_to_argparse_testspecs())
def test_add_flags_to_argparse(testspec: TestSpec) -> None:
    """Test Reporter.add_flags_to_argparse() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def add_target_list_flags_to_argparse_testspecs() -> list[TestSpec]:
    """Generate TestSpecs for testing add_list_of_targets_flags_to_argparse method.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def add_target_list_flag() -> ArgumentParser:
        """Create an ArgumentParser with a target list flag added by the reporter.

        :return: An argument parser.
        :rtype: ArgumentParser
        """
        choice_name: str = 'targets-list-choice'
        choice_conf_kwargs = choice_conf_kwargs_factory().replace(
            name=choice_name,
            flag_type=FlagType.TARGET_LIST,
            flags=['--targets-list-flag'],
            targets={Target.CONSOLE, Target.FILESYSTEM},
            default_targets={Target.CONSOLE})
        choices_conf = ChoicesConf(choices=[ChoiceConf(**choice_conf_kwargs)])
        reporter_kwargs = reporter_kwargs_factory().replace(
            targets={Target.CONSOLE, Target.FILESYSTEM},
            choices=choices_conf)
        reporter = FactoryReporter(**reporter_kwargs)
        choice = reporter.choices[choice_name]
        arg_parser = ArgumentParser(prog='test_reporter')
        reporter.add_list_of_targets_flags_to_argparse(parser=arg_parser, choice=choice)
        return arg_parser
    testspecs.extend([
        idspec('ADD_LIST_OF_TARGETS_FLAGS_TO_ARGPARSE_001', TestAction(
            name="add_list_of_targets_flags_to_argparse() adds parseable target list flag to an ArgumentParser",
            action=add_target_list_flag().parse_args,
            kwargs={
                'args': ['--targets-list-flag', Target.CONSOLE.value, Target.FILESYSTEM.value]
            },
            validate_result=lambda result: len(result.targets_list_flag) == 1 and (
                set(result.targets_list_flag[0]) == {Target.CONSOLE.value, Target.FILESYSTEM.value}
            )
        )),
        idspec('ADD_LIST_OF_TARGETS_FLAGS_TO_ARGPARSE_002', TestAction(
            name="add_list_of_targets_flags_to_argparse() with invalid parser arg type raises SimpleBenchTypeError",
            action=reporter_factory().add_list_of_targets_flags_to_argparse,
            kwargs={
                'parser': "not_an_argument_parser",
                'choice': choice_factory(),
            },
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE,
        )),
        idspec('ADD_LIST_OF_TARGETS_FLAGS_TO_ARGPARSE_003', TestAction(
            name="add_list_of_targets_flags_to_argparse() with invalid choice arg type raises SimpleBenchTypeError",
            action=reporter_factory().add_list_of_targets_flags_to_argparse,
            kwargs={
                'parser': ArgumentParser(prog='test_reporter'),
                'choice': "not_a_choice_instance",
            },
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.ADD_LIST_OF_TARGETS_FLAGS_INVALID_CHOICE_ARG_TYPE,
        )),
        idspec('ADD_LIST_OF_TARGETS_FLAGS_TO_ARGPARSE_004', TestAction(
            name=("add_list_of_targets_flags_to_argparse() adds parseable "
                  "target list flag to an ArgumentParser (no targets listed)"),
            action=add_target_list_flag().parse_args,
            kwargs={
                'args': ['--targets-list-flag']
            },
            validate_result=lambda result: (
                len(result.targets_list_flag) == 1 and len(result.targets_list_flag[0]) == 0))),
        idspec('ADD_LIST_OF_TARGETS_FLAGS_TO_ARGPARSE_005', TestAction(
            name=("add_list_of_targets_flags_to_argparse() adds parseable "
                  "target list flag to an ArgumentParser (bad target listed)"),
            action=add_target_list_flag().parse_args,
            kwargs={
                'args': ['--targets-list-flag', 'invalid_target']
            },
            exception=SystemExit,  # argparse raises SystemExit on parse errors
        )),
        idspec('ADD_LIST_OF_TARGETS_FLAGS_TO_ARGPARSE_006', TestAction(
            name=("add_list_of_targets_flags_to_argparse() adds parseable "
                  "target list flag to an ArgumentParser (multiple occurrences)"),
            action=add_target_list_flag().parse_args,
            kwargs={
                'args': ['--targets-list-flag', Target.CONSOLE.value, Target.FILESYSTEM.value]
            },
            validate_result=lambda result: (
                len(result.targets_list_flag) == 1 and
                set(result.targets_list_flag[0]) == {Target.CONSOLE.value, Target.FILESYSTEM.value}))),
    ])

    return testspecs


@pytest.mark.parametrize('testspec', add_target_list_flags_to_argparse_testspecs())
def test_add_list_of_targets_flags_to_argparse(testspec: TestSpec) -> None:
    """Test Reporter.add_list_of_targets_flags_to_argparse() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def add_boolean_flags_to_argparse_testspecs() -> list[TestSpec]:
    """Generate TestSpecs for testing add_boolean_flags_to_argparse method.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def add_boolean_flag() -> ArgumentParser:
        """Create an ArgumentParser with a boolean flag added by the reporter.

        :return: An argument parser.
        :rtype: ArgumentParser
        """
        choice_name: str = 'boolean-flag-choice'
        choice_conf_kwargs = choice_conf_kwargs_factory().replace(
            name=choice_name,
            flag_type=FlagType.BOOLEAN,
            flags=['--boolean-flag'])
        choices_conf = ChoicesConf(choices=[ChoiceConf(**choice_conf_kwargs)])
        reporter_kwargs = reporter_kwargs_factory().replace(choices=choices_conf)
        reporter = FactoryReporter(**reporter_kwargs)
        choice = reporter.choices[choice_name]
        arg_parser = ArgumentParser(prog='test_reporter')
        reporter.add_boolean_flags_to_argparse(parser=arg_parser, choice=choice)
        return arg_parser
    testspecs.extend([
        idspec('ADD_BOOLEAN_FLAGS_TO_ARGPARSE_001', TestAction(
            name="add_boolean_flags_to_argparse() adds parseable boolean flag to an ArgumentParser (present flag)",
            action=add_boolean_flag().parse_args,
            kwargs={
                'args': ['--boolean-flag']
            },
            validate_result=lambda result: result.boolean_flag is True)),
        idspec('ADD_BOOLEAN_FLAGS_TO_ARGPARSE_002', TestAction(
            name="add_boolean_flags_to_argparse() adds parseable boolean flag to an ArgumentParser (absent flag)",
            action=add_boolean_flag().parse_args,
            kwargs={
                'args': []
            },
            validate_result=lambda result: result.boolean_flag is False)),
        idspec('ADD_BOOLEAN_FLAGS_TO_ARGPARSE_003', TestAction(
            name="add_boolean_flags_to_argparse() with invalid parser arg type raises SimpleBenchTypeError",
            action=reporter_factory().add_boolean_flags_to_argparse,
            kwargs={
                'parser': "not_an_argument_parser",
                'choice': choice_factory(),
            },
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE,
        )),
        idspec('ADD_BOOLEAN_FLAGS_TO_ARGPARSE_004', TestAction(
            name="add_boolean_flags_to_argparse() with invalid choice arg type raises SimpleBenchTypeError",
            action=reporter_factory().add_boolean_flags_to_argparse,
            kwargs={
                'parser': ArgumentParser(prog='test_reporter'),
                'choice': "not_a_choice_instance",
            },
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.ADD_BOOLEAN_FLAGS_INVALID_CHOICE_ARG_TYPE,
        )),
    ])

    return testspecs


@pytest.mark.parametrize('testspec', add_boolean_flags_to_argparse_testspecs())
def test_add_boolean_flags_to_argparse(testspec: TestSpec) -> None:
    """Test Reporter.add_boolean_flags_to_argparse() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
