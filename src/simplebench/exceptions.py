# -*- coding: utf-8 -*-
"""Custom exceptions for the simplebench package."""
from enum import Enum


class ErrorTag(str, Enum):
    """Tags for error path identification for tests for the simplebench packages.

    ErrorTags' are used to identify specific error conditions in the simplebench package.
    Tests use these tags to assert specific error condition paths.
    """
    # Session() tags
    SESSION_INIT_INVALID_CASES_SEQUENCE_ARG = "SESSION_INIT_INVALID_CASES_SEQUENCE_ARG"
    """Something other than a Sequence of Case instances was passed to the Session() constructor_"""
    SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE = "SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE"
    """Something other than a Case instance was found in the Sequence passed to the Session() constructor_"""
    SESSION_INIT_INVALID_VERBOSITY_ARG = "SESSION_INIT_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the Session() constructor_"""
    SESSION_PROPERTY_INVALID_CASES_ARG = "SESSION_PROPERTY_INVALID_CASES_ARG"
    """Something other than a Sequence of Case instances was passed to the cases property"""
    SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE = "SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE"
    """Something other than a Case instance was found in the Sequence passed to the cases property"""
    SESSION_PROPERTY_INVALID_VERBOSITY_ARG = "SESSION_PROPERTY_INVALID_VERBOSITY_ARG"
    """Something other than a Verbosity instance was passed to the verbosity property"""

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
    CSV_REPORTER_REPORT_INVALID_CASE_ARG = "CSV_REPORTER_REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter.report() method"""
    CSV_REPORTER_REPORT_INVALID_SESSION_ARG = "CSV_REPORTER_REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the CSVReporter.report() method"""
    CSV_REPORTER_REPORT_INVALID_CHOICE_ARG = "CSV_REPORTER_REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the CSVReporter.report() method"""
    CSV_REPORTER_REPORT_UNSUPPORTED_SECTION = "CSV_REPORTER_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the CSVReporter.report() method in the Choice.sections"""
    CSV_REPORTER_REPORT_UNSUPPORTED_TARGET = "CSV_REPORTER_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the CSVReporter.report() method in the Choice.targets"""
    CSV_REPORTER_REPORT_UNSUPPORTED_FORMAT = "CSV_REPORTER_REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the CSVReporter.report() method in the Choice.formats"""
    CSV_REPORTER_REPORT_MISSING_PATH_ARG = "CSV_REPORTER_REPORT_MISSING_PATH_ARG"
    """The required 'path' argument was not passed to the CSVReporter.report() method"""
    CSV_REPORTER_REPORT_INVALID_PATH_ARG = "CSV_REPORTER_REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the CSVReporter.report() method"""
    CSV_REPORTER_REPORT_INVALID_CALLBACK_ARG = "CSV_REPORTER_REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the CSVReporter.report() method as the callback argument"""

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
    GRAPH_REPORTER_PLOT_INVALID_CASE_ARG = "GRAPH_REPORTER_PLOT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the GraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG = "GRAPH_REPORTER_PLOT_INVALID_GRAPHPATH_ARG"
    """Something other than a Path instance was passed to the GraphReporter.plot() method"""
    GRAPH_REPORTER_PLOT_INVALID_TARGET_ARG = "GRAPH_REPORTER_PLOT_INVALID_TARGET_ARG"
    """Something other than a valid target string was passed to the GraphReporter.plot() method"""

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
