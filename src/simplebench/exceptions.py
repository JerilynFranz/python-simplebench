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

    # CSVReporter() tags
    CSV_REPORTER_INIT_INVALID_CASE_ARG = "CSV_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the CSVReporter() constructor"""
    CSV_REPORTER_INIT_INVALID_SESSION_ARG = "CSV_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the CSVReporter() constructor"""

    # GraphReporter() tags
    GRAPH_REPORTER_INIT_INVALID_CASE_ARG = "GRAPH_REPORTER_INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the GraphReporter() constructor"""
    GRAPH_REPORTER_INIT_INVALID_SESSION_ARG = "GRAPH_REPORTER_INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the GraphReporter() constructor"""

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


