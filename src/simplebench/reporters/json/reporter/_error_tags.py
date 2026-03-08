"""ErrorTags for the ``simplebench.reporters.json`` module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _JSONReporterErrorTag(ErrorTag):
    """ErrorTags for the :class:`~.JSONReporter` class."""

    RENDER_INVALID_CASE = auto()
    """An invalid :class:`~simplebench.case.Case` instance was passed to the
    :meth:`~.JSONReporter.render` method.
    """
    RENDER_INVALID_SECTION = auto()
    """An invalid :class:`~simplebench.metric.Metric` enum member was passed to the
    :meth:`~.JSONReporter.render` method.
    """
    RENDER_INVALID_OPTIONS = auto()
    """An invalid :class:`~.JSONOptions` instance was passed to the
    :meth:`~.JSONReporter.render` method.
    """
    RUN_REPORT_UNSUPPORTED_TARGET = auto()
    """An unsupported :class:`~simplebench.enums.Target` was passed to the reporter's
    :meth:`~.JSONReporter.run_report` method.
    """
    JSON_OUTPUT_ERROR = auto()
    """An error occurred while serializing the JSON output."""
    RUN_REPORT_INVALID_DEFAULT_TARGETS_TYPE = auto()
    """The ``DEFAULT_TARGETS`` class attribute is not of type
    ``frozenset[Target]``.
    """
    RUN_REPORT_INVALID_DEFAULT_TARGETS_VALUE = auto()
    """The ``DEFAULT_TARGETS`` class attribute contains something other than
    :class:`~simplebench.enums.Target` values.
    """
    RUN_REPORT_INVALID_DEFAULT_SUBDIR_TYPE = auto()
    """The ``DEFAULT_SUBDIR`` class attribute is not of type :class:`str`."""
    RUN_REPORT_INVALID_DEFAULT_SUBDIR_VALUE = auto()
    """The ``DEFAULT_SUBDIR`` class attribute must consist only of alphanumeric characters
    if not empty.
    """
    RENDER_INVALID_CASE_ARG_TYPE = auto()
    """The ``case`` argument passed to the :meth:`~.JSONReporter.render` method was not of
    type :class:`~simplebench.case.Case`.
    """
    RENDER_INVALID_OPTIONS_ARG = auto()
    """The ``options`` argument passed to the :meth:`~.JSONReporter.render` method is not of
    the expected type (:class:`~.JSONOptions` or ``None``).
    """
