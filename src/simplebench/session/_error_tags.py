"""ErrorTags for the session module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings

from ..exceptions.error_tag import ErrorTag


@enum_docstrings
class _SessionErrorTag(ErrorTag):
    """ErrorTags for the session module."""

    PROPERTY_INVALID_CALIBRATE_ARG = auto()
    """Something other than a Calibrate instance or None was assigned to the calibrate property"""
    PROPERTY_INVALID_TIMER_ARG = auto()
    """Something other than a callable was assigned to the timer property"""
    PROPERTY_INVALID_TIMER_RETURN_TYPE = auto()
    """The callable assigned to the timer property did not return an int"""
    INVALID_CASES_SEQUENCE_ARG = auto()
    """Something other than a Sequence of Case instances was passed to the Session() constructor"""
    INIT_INVALID_CASE_ARG_IN_SEQUENCE = auto()
    """Something other than a Case instance was found in the Sequence passed to the Session() constructor"""
    INIT_INVALID_VERBOSITY_ARG = auto()
    """Something other than a Verbosity instance was passed to the Session() constructor"""
    INIT_INVALID_OUTPUT_PATH_ARG = auto()
    """Something other than a Path instance was passed to the Session() constructor as the path arg"""
    PROPERTY_INVALID_CASES_ARG = auto()
    """Something other than a Sequence of Case instances was passed to the cases property"""
    PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE = auto()
    """Something other than a Case instance was found in the Sequence passed to the cases property"""
    PROPERTY_INVALID_VERBOSITY_ARG = auto()
    """Something other than a Verbosity instance was passed to the verbosity property"""
    PROPERTY_INVALID_CASE_ARG = auto()
    """Something other than a Case instance was found in the Sequence passed to the cases property"""
    PROPERTY_INVALID_PROGRESS_ARG = auto()
    """Something other than a bool was passed to the progress property"""
    PROPERTY_INVALID_OUTPUT_PATH_ARG = auto()
    """Something other than a Path instance was passed to the output_path property"""
    RUN_NO_CASES_TO_RUN = auto()
    """No benchmark cases were found to run"""
    REPORT_INVALID_CHOICE_RETRIEVED = auto()
    """Something other than a Choice instance was retrieved from the report"""
    REPORT_OUTPUT_PATH_NOT_SET = auto()
    """The output path must be set to generate reports"""
    PARSE_ARGS_INVALID_ARGSPARSER_ARG = auto()
    """Something other than an ArgumentParser instance was passed to the Session.parse_args() method"""
    PROPERTY_INVALID_ARGSPARSER_ARG = auto()
    """Something other than an ArgumentParser instance was assigned to the args_parser property"""
    PROPERTY_INVALID_ARGS_ARG = auto()
    """Something other than a Namespace instance was found in the args property"""
    PROPERTY_INVALID_DEFAULT_RUNNER_ARG = auto()
    """Something other than a subclass of SimpleRunner or None was assigned to the default_runner property"""
    PROPERTY_INVALID_CONSOLE_ARG = auto()
    """Something other than a Console instance was assigned to the console property"""
    PARSE_ARGS_INVALID_ARGS_TYPE = auto()
    """Something other than a list of strings was passed to the Session.parse_args() method as the args argument"""
    PARSE_ARGS_INVALID_ARGS_ITEM_TYPE = auto()
    """Something other than a string was found in the list passed to the Session.parse_args()
    method as the args argument"""
    ARGUMENT_ERROR_ADDING_FLAGS = auto()
    """An error occurred while adding flags to the ArgumentParser instance"""
