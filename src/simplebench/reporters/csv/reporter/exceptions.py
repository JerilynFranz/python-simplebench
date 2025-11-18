"""ErrorTags for :class:`~.CSVReporter` exceptions."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class CSVReporterErrorTag(ErrorTag):
    """Error tags for :class:`~.CSVReporter` class related exceptions."""
    SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_TYPE = "SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_TYPE"
    """Invalid targets argument type:
    - must be of type `frozenset[Target]` or `None.`"""
    SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_VALUE = "SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_VALUE"
    """Invalid targets argument value:
    - must be a `frozenset` of `Target` enum members."""
    SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_TYPE = "SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_TYPE"
    """Invalid subdir argument type:
    - must be of type `str` or `None.`"""
    SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_VALUE = "SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_VALUE"
    """Invalid subdir argument value:
    - must be a `str` of only alphanumeric characters (A-Z, a-z, 0-9) or `None`."""
    GET_OPTIONS_INVALID_OPTIONS_ARG_TYPE = "GET_OPTIONS_INVALID_OPTIONS_ARG_TYPE"
    """Invalid options argument type:
    - must be of type `Iterable[ReporterOptions]` or `None`."""
    GET_OPTIONS_INVALID_OPTIONS_ARG_VALUE = "GET_OPTIONS_INVALID_OPTIONS_ARG_VALUE"
    """Invalid options argument value:
    - options argument iterable contains something other than `ReporterOptions` instances."""
    RUN_REPORT_UNSUPPORTED_TARGET = "RUN_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the CSVReporter.run_report() method in the choice.targets"""
    RUN_REPORT_UNSUPPORTED_DEFAULT_TARGETS = "RUN_REPORT_UNSUPPORTED_DEFAULT_TARGETS"
    """The default_targets attribute for a Choice contains unsupported Target values."""
    RENDER_INVALID_CASE = "RENDER_INVALID_CASE"
    """Something other than a valid Case instance was passed to the CSVReporter.render() method."""
    RENDER_INVALID_SECTION = "RENDER_INVALID_SECTION"
    """Something other than a valid Section enum member was passed to the CSVReporter.render() method."""
    RENDER_INVALID_OPTIONS = "RENDER_INVALID_OPTIONS"
