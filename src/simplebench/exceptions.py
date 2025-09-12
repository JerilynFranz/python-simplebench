# -*- coding: utf-8 -*-
"""Custom exceptions for the simplebench package."""
from enum import Enum
import argparse


class ErrorTag(str, Enum):
    """Tags for error path identification for tests for the simplebench packages.

    ErrorTags' are used to identify specific error conditions in the simplebench package.
    Tests use these tags to assert specific error condition paths.
    """

    # Case() tags
    CASE_INVALID_ITERATIONS = "CASE_INVALID_ITERATIONS"
    """Invalid iterations argument passed to the Case() constructor"""
    CASE_INVALID_MIN_TIME = "CASE_INVALID_MIN_TIME"
    """Invalid min_time argument passed to the Case() constructor"""
    CASE_INVALID_MAX_TIME = "CASE_INVALID_MAX_TIME"
    """Invalid max_time argument passed to the Case() constructor"""
    CASE_INVALID_TIME_RANGE = "CASE_INVALID_TIME_RANGE"
    """max_time must be greater than or equal to min_time in the Case() constructor"""
    CASE_INVALID_WARMUP_ROUNDS = "CASE_INVALID_WARMUP_ROUNDS"
    """Invalid warmup_rounds argument passed to the Case() constructor"""
    CASE_INVALID_ROUNDS = "CASE_INVALID_ROUNDS"
    """Invalid rounds argument passed to the Case() constructor"""
    CASE_INVALID_NAME = "CASE_INVALID_NAME"
    """Something other than a non-empty string was passed to the Case() constructor as the name arg"""
    CASE_INVALID_DESCRIPTION = "CASE_INVALID_DESCRIPTION"
    """Something other than a string was passed to the Case() constructor as the description arg"""
    CASE_INVALID_RUNNER_NOT_CALLABLE_OR_NONE = "CASE_INVALID_RUNNER_NOT_CALLABLE_OR_NONE"
    """Something other than a callable (function or method) was passed to the Case() constructor as the runner arg"""
    CASE_INVALID_ACTION_NOT_CALLABLE = "CASE_INVALID_ACTION_NOT_CALLABLE"
    """Something other than a callable (function or method) was passed to the Case() constructor as the action arg"""
    CASE_INVALID_SETUP = "CASE_INVALID_SETUP"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the setup arg"""
    CASE_INVALID_TEARDOWN = "CASE_INVALID_TEARDOWN"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the teardown arg"""
    CASE_INVALID_VARIATION_COLS_NOT_DICT = "CASE_INVALID_VARIATION_COLS_NOT_DICT"
    """Something other than a dictionary was passed to the Case() constructor as the variation_cols arg"""
    CASE_INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS = "CASE_INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS"
    """Something other than string keys and string or number values were found in the dictionary passed to
    the Case() constructor as the variation_cols arg"""
    CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT = "CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT"
    """Something other than a dictionary was passed to the Case() constructor as the kwargs_variations arg"""
    CASE_INVALID_GRAPH_ASPECT_RATIO = "CASE_INVALID_GRAPH_ASPECT_RATIO"
    """Something other than a positive number was passed to the Case() constructor as the graph_aspect_ratio arg"""
    CASE_INVALID_GRAPH_Y_STARTS_AT_ZERO = "CASE_INVALID_GRAPH_Y_STARTS_AT_ZERO"
    """Something other than a bool was passed to the Case() constructor as the graph_y_starts_at_zero arg"""
    CASE_INVALID_GRAPH_STYLE = "CASE_INVALID_GRAPH_STYLE"
    """Something other than 'default' or 'dark_background' was passed to the Case() constructor as the
    graph_style arg"""
    CASE_INVALID_GRAPH_X_LABELS_ROTATION = "CASE_INVALID_GRAPH_X_LABELS_ROTATION"
    """Something other than a number was passed to the Case() constructor as the graph_x_labels_rotation arg"""
    CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE = "CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the callback arg"""
    CASE_SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT = "CASE_SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT"
    """Something other than a Section instance was passed to the Case() constructor as the section arg"""
    CASE_SECTION_MEAN_INVALID_SECTION_ARGUMENT = "CASE_SECTION_MEAN_INVALID_SECTION_ARGUMENT"
    """Something other than Section.OPS or Section.TIMING was passed to the Case.section_mean() method"""

    # Results() tags
    RESULTS_RESULTS_SECTION_INVALID_SECTION_TYPE_ARGUMENT = "RESULTS_RESULT_SECTION_INVALID_SECTION_TYPE_ARGUMENT"
    """Something other than a Section instance was passed to the Results.result_section() method"""
    RESULTS_RESULTS_SECTION_UNSUPPORTED_SECTION_ARGUMENT = "RESULTS_RESULT_SECTION_UNSUPPORTED_SECTION_ARGUMENT"
    """Something other than Section.OPS or Section.TIMING was passed to the Results.result_section() method"""

    # Session() tags
    SESSION_INIT_INVALID_CASES_SEQUENCE_ARG = "SESSION_INIT_INVALID_CASES_SEQUENCE_ARG"
    """Something other than a Sequence of Case instances was passed to the Session() constructor"""
    SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE = "SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE"
    """Something other than a Case instance was found in the Sequence passed to the Session() constructor"""
    SESSION_INIT_INVALID_VERBOSITY_ARG = "SESSION_INIT_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the Session() constructor"""
    SESSION_INIT_INVALID_OUTPUT_PATH_ARG = "SESSION_INIT_INVALID_OUTPUT_PATH_ARG"
    """Something other than a Path instance was passed to the Session() constructor as the path arg"""
    SESSION_PROPERTY_INVALID_CASES_ARG = "SESSION_PROPERTY_INVALID_CASES_ARG"
    """Something other than a Sequence of Case instances was passed to the cases property"""
    SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE = "SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE"
    """Something other than a Case instance was found in the Sequence passed to the cases property"""
    SESSION_PROPERTY_INVALID_VERBOSITY_ARG = "SESSION_PROPERTY_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the verbosity property"""
    SESSION_PROPERTY_INVALID_CASE_ARG = "SESSION_PROPERTY_INVALID_CASE_ARG"
    """Something other than a Case instance was found in the Sequence passed to the cases property"""
    SESSION_PROPERTY_INVALID_PROGRESS_ARG = "SESSION_PROPERTY_INVALID_PROGRESS_ARG"
    """Something other than a bool was passed to the progress property"""
    SESSION_PROPERTY_INVALID_OUTPUT_PATH_ARG = "SESSION_PROPERTY_INVALID_OUTPUT_PATH_ARG"
    """Something other than a Path instance was passed to the output_path property"""
    SESSION_RUN_NO_CASES_TO_RUN = "SESSION_RUN_NO_CASES_TO_RUN"
    """No benchmark cases were found to run"""
    SESSION_REPORT_INVALID_CHOICE_RETRIEVED = "SESSION_REPORT_INVALID_CHOICE_RETRIEVED"
    """Something other than a Choice instance was retrieved from the report"""
    SESSION_REPORT_OUTPUT_PATH_NOT_SET = "SESSION_REPORT_OUTPUT_PATH_NOT_SET"
    """The output path must be set to generate reports"""
    SESSION_PARSE_ARGS_INVALID_ARGSPARSER_ARG = "SESSION_PARSE_ARGS_INVALID_ARGSPARSER_ARG"
    """Something other than an ArgumentParser instance was passed to the Session.parse_args() method"""
    SESSION_INIT_INVALID_ARGSPARSER_ARG = "SESSION_INIT_INVALID_ARGSPARSER_ARG"
    """Something other than an ArgumentParser instance was passed to the Session() constructor"""
    SESSION_PROPERTY_INVALID_ARGS_ARG = "SESSION_PROPERTY_INVALID_ARGS_ARG"
    """Something other than a Namespace instance was found in the args property"""

    # Reporters() tags
    REPORTERS_REGISTER_INVALID_REPORTER_ARG = "REPORTERS_REGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the Reporters.register() method"""
    REPORTERS_REGISTER_DUPLICATE_NAME = "REPORTERS_REGISTER_DUPLICATE_NAME"
    """A Reporter with the same name already exists in the Reporters instance"""
    REPORTERS_UNREGISTER_UNKNOWN_NAME = "REPORTERS_UNREGISTER_UNKNOWN_NAME"
    """No Reporter with the given name is registered in the Reporters instance"""
    REPORTERS_UNREGISTER_INVALID_NAME_ARG = "REPORTERS_UNREGISTER_INVALID_NAME_ARG"
    """Something other than a string was passed to the Reporters.unregister() method"""

    # RichTableReporter() tags
    RICH_TABLE_REPORTER_INIT_INVALID_CASE_ARG = "RICH_TABLE_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the RichTableReporter() constructor"""
    RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG = "RICH_TABLE_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the RichTableReporter() constructor"""
    RICH_TABLE_REPORTER_REPORT_INVALID_CASE_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_SESSION_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_CHOICE_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_SECTION = "RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the RichTableReporter.report() method in the Choice.sections"""
    RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_TARGET = "RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the RichTableReporter.report() method in the Choice.targets"""
    RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_FORMAT = "RICH_TABLE_REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the RichTableReporter.report() method in the Choice.formats"""
    RICH_TABLE_REPORTER_REPORT_MISSING_PATH_ARG = "RICH_TABLE_REPORTER_REPORT_MISSING_PATH_ARG"
    """The required 'path' argument was not passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_PATH_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the RichTableReporter.report() method"""
    RICH_TABLE_REPORTER_REPORT_INVALID_CALLBACK_ARG = "RICH_TABLE_REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the RichTableReporter.report() method as the callback argument"""

    # CSVReporter() tags
    CSV_REPORTER_INIT_INVALID_CASE_ARG = "CSV_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter() constructor"""
    CSV_REPORTER_INIT_INVALID_SESSION_ARG = "CSV_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the CSVReporter() constructor"""
    CSV_REPORTER_RUN_REPORT_INVALID_CASE_ARG = "CSV_REPORTER_RUN_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter.run_report() method"""
    CSV_REPORTER_RUN_REPORT_INVALID_SESSION_ARG = "CSV_REPORTER_RUN_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the CSVReporter.run_report() method"""
    CSV_REPORTER_RUN_REPORT_INVALID_CHOICE_ARG = "CSV_REPORTER_RUN_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the CSVReporter.run_report() method"""
    CSV_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION = "CSV_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the CSVReporter.run_report() method in the choice.sections"""
    CSV_REPORTER_TO_CSV_INVALID_CASE_ARG = "CSV_REPORTER_TO_CSV_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter.to_csv() method"""
    CSV_REPORTER_TO_CSV_INVALID_CSVFILE_ARG = "CSV_REPORTER_TO_CSV_INVALID_CSVFILE_ARG"
    """Something other than a file-like object was passed to the CSVReporter.to_csv() method"""
    CSV_REPORTER_TO_CSV_INVALID_BASE_UNIT_ARG = "CSV_REPORTER_TO_CSV_INVALID_BASE_UNIT_ARG"
    """Something other than a non-empty string was passed to the CSVReporter.to_csv() method"""
    CSV_REPORTER_TO_CSV_INVALID_TARGET_ARG = "CSV_REPORTER_TO_CSV_INVALID_TARGET_ARG"
    """Something other than a valid target string was passed to the CSVReporter.to_csv() method"""

    # GraphReporter() tags
    GRAPH_REPORTER_INIT_INVALID_CASE_ARG = "GRAPH_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the GraphReporter() constructor"""
    GRAPH_REPORTER_INIT_INVALID_SESSION_ARG = "GRAPH_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the GraphReporter() constructor"""
    GRAPH_REPORTER_REPORT_INVALID_CASE_ARG = "GRAPH_REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_SESSION_ARG = "GRAPH_REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_CHOICE_ARG = "GRAPH_REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION = "GRAPH_REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the GraphReporter.report() method in the Choice.sections"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_TARGET = "GRAPH_REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the GraphReporter.report() method in the Choice.targets"""
    GRAPH_REPORTER_REPORT_UNSUPPORTED_FORMAT = "GRAPH_REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the GraphReporter.report() method in the Choice.formats"""
    GRAPH_REPORTER_REPORT_MISSING_PATH_ARG = "GRAPH_REPORTER_REPORT_MISSING_PATH_ARG"
    """The required 'path' argument was not passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_PATH_ARG = "GRAPH_REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the GraphReporter.report() method"""
    GRAPH_REPORTER_REPORT_INVALID_CALLBACK_ARG = "GRAPH_REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the GraphReporter.report() method as the callback argument"""
    GRAPH_REPORTER_RUN_REPORT_INVALID_PATH_ARG = "GRAPH_REPORTER_RUN_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the GraphReporter.run_report() method as the path arg"""
    GRAPH_REPORTER_PLOT_INVALID_CASE_ARG = "GRAPH_REPORTER_PLOT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the GraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG = "GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG"
    """Something other than a Path instance was passed to the GraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_SECTION_ARG = "GRAPH_REPORTER_PLOT_INVALID_SECTION_ARG"
    """Something other than a valid Section was passed to the GraphReporter.plot() method"""

    # JSONReporter() tags
    JSON_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION = "JSON_REPORTER_RUN_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the JSONReporter.run_report() method in the choice.sections"""

    # RichTask() tags
    RICH_TASK_INIT_INVALID_NAME_ARG = "RICH_TASK_INIT_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichTask() constructor"""
    RICH_TASK_INIT_INVALID_DESCRIPTION_ARG = "RICH_TASK_INIT_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the RichTask() constructor"""
    RICH_TASK_INIT_INVALID_PROGRESS_ARG = "RICH_TASK_INIT_INVALID_PROGRESS_ARG"
    """Something other than a Progress instance was passed to the RichTask() constructor"""
    RICH_TASK_INIT_EMPTY_STRING_NAME = "RICH_TASK_INIT_EMPTY_STRING_NAME"
    """The name arg cannot be an empty string"""
    RICH_TASK_INIT_EMPTY_STRING_DESCRIPTION = "RICH_TASK_INIT_EMPTY_STRING_DESCRIPTION"
    """The description arg cannot be an empty string"""
    RICH_TASK_UPDATE_INVALID_COMPLETED_ARG = "RICH_TASK_UPDATE_INVALID_COMPLETED_ARG"
    """Something other than an int was passed to the RichTask() update method"""
    RICH_TASK_UPDATE_INVALID_DESCRIPTION_ARG = "RICH_TASK_UPDATE_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the RichTask() update method"""
    RICH_TASK_UPDATE_INVALID_REFRESH_ARG = "RICH_TASK_UPDATE_INVALID_REFRESH_ARG"
    """Something other than a bool was passed to the RichTask() update method"""
    RICH_TASK_UPDATE_ALREADY_TERMINATED_TASK = "RICH_TASK_UPDATE_ALREADY_TERMINATED_TASK"
    """The task has already been terminated"""
    RICH_TASK_TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK = "RICH_TASK_TERMINATE_AND_REMOVE_ALREADY_TERMINATED_TASK"
    """The task has already been terminated"""

    # Rich ProgressTask() tags
    RICH_PROGRESS_TASK_DELITEM_INVALID_NAME_ARG = "RICH_PROGRESS_TASK_DELITEM_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() __delitem__ method"""
    RICH_PROGRESS_TASK_DELITEM_NOT_FOUND = "RICH_PROGRESS_TASK_DELITEM_NOT_FOUND"
    """The requested task was not found"""
    RICH_PROGRESS_TASK_GETITEM_INVALID_NAME_ARG = "RICH_PROGRESS_TASK_GETITEM_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() __getitem__ method"""
    RICH_PROGRESS_TASK_GETITEM_NOT_FOUND = "RICH_PROGRESS_TASK_GETITEM_NOT_FOUND"
    """The requested task was not found"""
    RICH_PROGRESS_TASK_NEW_TASK_INVALID_NAME_ARG = "RICH_PROGRESS_TASK_NEW_TASK_INVALID_NAME_ARG"
    """Something other than a string was passed to the RichProgressTask() new_task method"""
    RICH_PROGRESS_TASK_NEW_TASK_INVALID_DESCRIPTION_ARG = "RICH_PROGRESS_TASK_NEW_TASK_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the RichProgressTask() new_task method"""
    RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_NAME = "RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_NAME"
    """The name arg cannot be an empty string"""
    RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_DESCRIPTION = "RICH_PROGRESS_TASK_NEW_TASK_EMPTY_STRING_DESCRIPTION"
    """The description arg cannot be an empty string"""
    RICH_PROGRESS_TASKS_INIT_INVALID_VERBOSITY_ARG = "RICH_PROGRESS_TASKS_INIT_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the RichProgressTasks()
    constructor as the verbosity arg"""
    RICH_PROGRESS_TASKS_INIT_INVALID_PROGRESS_ARG = "RICH_PROGRESS_TASKS_INIT_INVALID_PROGRESS_ARG"
    """Something other than a Progress instance was passed to the RichProgressTasks() constructor as the progress arg"""

    # reporters.Choice() tags
    CHOICE_INIT_INVALID_REPORTER_ARG = "CHOICE_INIT_INVALID_REPORTER_ARG"
    """Something other than a ReporterProtocol instance was passed to the Choice() constructor"""
    CHOICE_INIT_INVALID_RUNNER_ARG = "CHOICE_INIT_INVALID_RUNNER_ARG"
    """Something other than a callable (function or method) was passed to the Choice() constructor"""
    CHOICE_INIT_INVALID_NAME_ARG = "CHOICE_INIT_INVALID_NAME_ARG"
    """Something other than a string was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_STRING_NAME = "CHOICE_INIT_EMPTY_STRING_NAME"
    """The name arg cannot be an empty string"""
    CHOICE_INIT_INVALID_DESCRIPTION_ARG = "CHOICE_INIT_INVALID_DESCRIPTION_ARG"
    """Something other than a string was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_STRING_DESCRIPTION = "CHOICE_INIT_EMPTY_STRING_DESCRIPTION"
    """The description arg cannot be an empty string"""
    CHOICE_INIT_INVALID_SECTIONS_ARG = "CHOICE_INIT_INVALID_SECTIONS_ARG"
    """Something other than a set of Section enums was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_SECTIONS = "CHOICE_INIT_EMPTY_SECTIONS"
    """The sections arg cannot be an empty set"""
    CHOICE_INIT_INVALID_TARGETS_ARG = "CHOICE_INIT_INVALID_TARGETS_ARG"
    """Something other than a set of Target enums was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_TARGETS = "CHOICE_INIT_EMPTY_TARGETS"
    """The targets arg cannot be an empty set"""
    CHOICE_INIT_INVALID_FORMATS_ARG = "CHOICE_INIT_INVALID_FORMATS_ARG"
    """Something other than a set of Format enums was passed to the Choice() constructor"""
    CHOICE_INIT_EMPTY_FORMATS = "CHOICE_INIT_EMPTY_FORMATS"
    """The formats arg cannot be an empty set"""

    # reporters.Choices() tags
    CHOICES_ADD_INVALID_CHOICE_ARG = "CHOICES_ADD_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the Choices.add() method"""
    CHOICES_ADD_DUPLICATE_CHOICE_NAME = "CHOICES_ADD_DUPLICATE_CHOICE_NAME"
    """A Choice with the same name already exists in the Choices instance"""
    CHOICES_ADD_DUPLICATE_CLI_ARG = "CHOICES_ADD_DUPLICATE_CLI_ARG"
    """A Choice with the same CLI argument already exists in the Choices instance"""
    CHOICES_EXTEND_INVALID_CHOICES_ARG = "CHOICES_EXTEND_INVALID_CHOICES_ARG"
    """Something other than a Choices instance was passed to the Choices.extend() method"""
    CHOICES_EXTEND_INVALID_CHOICES_CONTENT = "CHOICES_EXTEND_INVALID_CHOICES_CONTENT"
    """Something other than a Choice instance was found in the Choices instance passed to the Choices.extend() method"""
    CHOICES_EXTEND_DUPLICATE_CHOICE_NAME = "CHOICES_EXTEND_DUPLICATE_CHOICE_NAME"
    """A Choice with the same name already exists in the Choices instance"""
    CHOICES_EXTEND_DUPLICATE_CLI_ARG = "CHOICES_EXTEND_DUPLICATE_CLI_ARG"
    """A Choice with the same CLI argument already exists in the Choices instance"""
    CHOICES_CHOICE_FOR_FLAG_INVALID_ARG = "CHOICES_CHOICE_FOR_FLAG_INVALID_ARG"
    """Something other than a string was passed to the Choices.choice_for_flag() method"""
    CHOICES_GET_CHOICE_BY_CLI_TAG_INVALID_ARG = "CHOICES_GET_CHOICE_BY_CLI_TAG_INVALID_ARG"
    """Something other than a string was passed to the Choices.get_choice_by_cli_tag() method"""
    CHOICES_ALL_CHOICE_FLAGS_INVALID_RETURN = "CHOICES_ALL_CHOICE_FLAGS_INVALID_RETURN"
    """Something other than a set of strings was returned from the Choices.all_choice_flags() method"""
    CHOICES_REMOVE_UNKNOWN_CHOICE_NAME = "CHOICES_REMOVE_UNKNOWN_CHOICE_NAME"
    """No Choice with the given name exists in the Choices instance"""

    # Reporter() tags
    REPORTER_INIT_NOT_IMPLEMENTED = "REPORTER_INIT_NOT_IMPLEMENTED"
    """The Reporter base class cannot be instantiated directly"""
    REPORTER_CHOICES_NOT_IMPLEMENTED = "REPORTER_CHOICES_NOT_IMPLEMENTED"
    """The Reporter.choices property must be implemented in subclasses"""
    REPORTER_NAME_NOT_IMPLEMENTED = "REPORTER_NAME_NOT_IMPLEMENTED"
    """The Reporter.name property must be implemented in subclasses"""
    REPORTER_DESCRIPTION_NOT_IMPLEMENTED = "REPORTER_DESCRIPTION_NOT_IMPLEMENTED"
    """The Reporter.description property must be implemented in subclasses"""
    REPORTER_REPORT_NOT_IMPLEMENTED = "REPORTER_REPORT_NOT_IMPLEMENTED"
    """The Reporter.report() method must be implemented in subclasses"""
    REPORTER_ADD_FLAGS_NOT_IMPLEMENTED = "REPORTER_ADD_FLAGS_NOT_IMPLEMENTED"
    """The Reporter.add_flags_to_argparse() method must be implemented in subclasses"""
    REPORTER_SUPPORTED_FORMATS_NOT_IMPLEMENTED = "REPORTER_SUPPORTED_FORMATS_NOT_IMPLEMENTED"
    """The Reporter.supported_formats property must be implemented in subclasses"""
    REPORTER_SUPPORTED_SECTIONS_NOT_IMPLEMENTED = "REPORTER_SUPPORTED_SECTIONS_NOT_IMPLEMENTED"
    """The Reporter.supported_sections property must be implemented in subclasses"""
    REPORTER_SUPPORTED_TARGETS_NOT_IMPLEMENTED = "REPORTER_SUPPORTED_TARGETS_NOT_IMPLEMENTED"
    """The Reporter.supported_targets property must be implemented in subclasses"""
    REPORTER_REPORT_INVALID_CASE_ARG = "REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_CHOICE_ARG = "REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_SESSION_ARG = "REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_PATH_ARG = "REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the Reporter.report() method"""
    REPORTER_REPORT_INVALID_CALLBACK_ARG = "REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the Reporter.report() method as the callback argument"""
    REPORTER_REPORT_UNSUPPORTED_SECTION = "REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the Reporter.report() method in the Choice.sections"""
    REPORTER_REPORT_UNSUPPORTED_TARGET = "REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the Reporter.report() method in the Choice.targets"""
    REPORTER_REPORT_UNSUPPORTED_FORMAT = "REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the Reporter.report() method in the Choice.formats"""

    # reporters.ReporterManager() tags
    REPORTER_MANAGER_REGISTER_INVALID_REPORTER_ARG = "REPORTER_MANAGER_REGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the ReporterManager.register() method"""
    REPORTER_MANAGER_REGISTER_INVALID_CHOICES_RETURNED = "REPORTER_MANAGER_REGISTER_INVALID_CHOICES_RETURNED"
    """Something other than a Choices instance was returned from the reporter.choices property"""
    REPORTER_MANAGER_REGISTER_INVALID_CHOICES_CONTENT = "REPORTER_MANAGER_REGISTER_INVALID_CHOICES_CONTENT"
    """Something other than a Choice instance was found in the Choices instance returned
    from the reporter.choices property"""
    REPORTER_MANAGER_REGISTER_DUPLICATE_NAME = "REPORTER_MANAGER_REGISTER_DUPLICATE_NAME"
    """A Reporter with the same name already exists in the ReporterManager instance"""
    REPORTER_MANAGER_REGISTER_DUPLICATE_CLI_ARG = "REPORTER_MANAGER_REGISTER_DUPLICATE_CLI_ARG"
    """A Reporter with the same CLI argument already exists in the ReporterManager instance"""
    REPORTER_MANAGER_UNREGISTER_INVALID_REPORTER_ARG = "REPORTER_MANAGER_UNREGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the ReporterManager.unregister() method"""
    REPORTER_MANAGER_UNREGISTER_UNKNOWN_NAME = "REPORTER_MANAGER_UNREGISTER_UNKNOWN_NAME"
    """No Reporter with the given name is registered in the ReporterManager instance"""
    REPORTER_MANAGER_ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG = (
        "REPORTER_MANAGER_ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG"
    )
    """Something other than an ArgumentParser instance was passed to the
    ReporterManager.add_reporters_to_argparse() method"""
    REPORTER_MANAGER_ARGUMENT_ERROR_ADDING_FLAGS = "REPORTER_MANAGER_ARGUMENT_ERROR_ADDING_FLAGS"
    """An ArgumentError was raised when adding reporter flags to the ArgumentParser instance"""


class SimpleBenchTypeError(TypeError):
    """Base class for all SimpleBench type errors.

    It differs from a standard TypeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, tag: ErrorTag) -> None:
        """Create a new SimpleBenchTypeError.

        Args:
            msg (str): The error message.
            tag (str): The tag code.
        """
        self.tag_code: ErrorTag = tag
        super().__init__(msg)


class SimpleBenchKeyError(KeyError):
    """Base class for all SimpleBench key errors.

    It differs from a standard KeyError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, tag: ErrorTag) -> None:
        """Create a new SimpleBenchKeyError.

        Args:
            msg (str): The error message.
            tag (str): The tag code.
        """
        self.tag_code: ErrorTag = tag
        super().__init__(msg)


class SimpleBenchValueError(ValueError):
    """Base class for all SimpleBench value errors.

    It differs from a standard ValueError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, tag: ErrorTag) -> None:
        """Create a new SimpleBenchValueError.

        Args:
            msg (str): The error message.
            tag (str): The tag code.
        """
        self.tag_code: ErrorTag = tag
        super().__init__(msg)


class SimpleBenchRuntimeError(RuntimeError):
    """Base class for all SimpleBench runtime errors.

    It differs from a standard RuntimeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, tag: ErrorTag) -> None:
        """Create a new SimpleBenchRuntimeError.

        Args:
            msg (str): The error message.
            tag (str): The tag code.
        """
        self.tag_code: ErrorTag = tag
        super().__init__(msg)


class SimpleBenchNotImplementedError(NotImplementedError):
    """Base class for all SimpleBench not implemented errors.

    It differs from a standard NotImplementedError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, tag: ErrorTag) -> None:
        """Create a new SimpleBenchRuntimeError.

        Args:
            msg (str): The error message.
            tag (str): The tag code.
        """
        self.tag_code: ErrorTag = tag
        super().__init__(msg)


class SimpleBenchArgumentError(argparse.ArgumentError):
    """Base class for re-raising all SimpleBench ArgumentError errors.

    It is designed to be used in places where an argparse.ArgumentError
    would be appropriate and for re-raising ArgumentErrors
    caught from argparse operations.

    It differs from a argparse.ArgumentError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support
    and by directly setting the argument_name property to the name of the
    argument that caused the error. This is because the argparse.ArgumentError
    constructor expects an argparse.Action instance as the first argument
    and that is not always available when re-raising the exception.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Args:
        argument_name (str | None): The argument name.
        message (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, argument_name: str | None, message: str, tag: ErrorTag) -> None:
        """Create a new SimpleBenchArgumentError.

        Args:
            argument_name (str | None): The argument name.
            message (str): The error message.
            tag (str): The tag code.
        """
        self.tag_code: ErrorTag = tag
        super().__init__(argument=None, message=message)
        self.argument_name = argument_name
