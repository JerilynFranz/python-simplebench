"""ErrorTags for the ``simplebench.reporters.json`` module."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _JSONReporterErrorTag(ErrorTag):
    """ErrorTags for the :class:`~.JSONReporter` class."""
    RENDER_INVALID_CASE = "RENDER_INVALID_CASE"
    """An invalid :class:`~simplebench.case.Case` instance was passed to the
    :meth:`~.JSONReporter.render` method.
    """
    RENDER_INVALID_SECTION = "RENDER_INVALID_SECTION"
    """An invalid :class:`~simplebench.enums.Section` enum member was passed to the
    :meth:`~.JSONReporter.render` method.
    """
    RENDER_INVALID_OPTIONS = "RENDER_INVALID_OPTIONS"
    """An invalid :class:`~.JSONOptions` instance was passed to the
    :meth:`~.JSONReporter.render` method.
    """
    RUN_REPORT_UNSUPPORTED_TARGET = "RUN_REPORT_UNSUPPORTED_TARGET"
    """An unsupported :class:`~simplebench.enums.Target` was passed to the reporter's
    :meth:`~.JSONReporter.run_report` method.
    """
    JSON_OUTPUT_ERROR = "JSON_OUTPUT_ERROR"
    """An error occurred while serializing the JSON output."""
    RUN_REPORT_INVALID_DEFAULT_TARGETS_TYPE = "RUN_REPORT_INVALID_DEFAULT_TARGETS_TYPE"
    """The ``DEFAULT_TARGETS`` class attribute is not of type
    ``frozenset[Target]``.
    """
    RUN_REPORT_INVALID_DEFAULT_TARGETS_VALUE = "RUN_REPORT_INVALID_DEFAULT_TARGETS_VALUE"
    """The ``DEFAULT_TARGETS`` class attribute contains something other than
    :class:`~simplebench.enums.Target` values.
    """
    RUN_REPORT_INVALID_DEFAULT_SUBDIR_TYPE = "RUN_REPORT_INVALID_DEFAULT_SUBDIR_TYPE"
    """The ``DEFAULT_SUBDIR`` class attribute is not of type :class:`str`."""
    RUN_REPORT_INVALID_DEFAULT_SUBDIR_VALUE = "RUN_REPORT_INVALID_DEFAULT_SUBDIR_VALUE"
    """The ``DEFAULT_SUBDIR`` class attribute must consist only of alphanumeric characters
    if not empty.
    """
    RENDER_INVALID_CASE_ARG_TYPE = "RENDER_INVALID_CASE_ARG_TYPE"
    """The ``case`` argument passed to the :meth:`~.JSONReporter.render` method was not of
    type :class:`~simplebench.case.Case`.
    """
    RENDER_INVALID_OPTIONS_ARG = "RENDER_INVALID_OPTIONS_ARG"
    """The ``options`` argument passed to the :meth:`~.JSONReporter.render` method is not of
    the expected type (:class:`~.JSONOptions` or ``None``).
    """
