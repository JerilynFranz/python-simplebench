"""Exception ErrorTags for the rich_table reporter."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions.error_tag import ErrorTag


@enum_docstrings
class _RichTableReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the rich_table reporter."""

    RENDER_METRIC_NONE = auto()
    """The ``metric`` argument passed to :meth:`~.RichTableReporter.render` is None,
    but a specific metric is required to render the report.
    """
    RENDER_INVALID_CASE = auto()
    """The ``case`` argument passed to :meth:`~.RichTableReporter.render` is not a
    :class:`~simplebench.case.Case` instance.
    """
    RENDER_INVALID_OPTIONS = auto()
    """The ``options`` argument passed to :meth:`~.RichTableReporter.render` is not a
    :class:`~.RichTableOptions` instance.
    """
    RENDER_INVALID_SECTION = auto()
    """The ``metric`` argument passed to :meth:`~.RichTableReporter.render` is not a
    :class:`~simplebench.metric.Metric` enum member.
    """
    CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE = auto()
    """The default targets specified in the :class:`~.RichTableOptions` are not valid
    :class:`~simplebench.enums.Target` enum members.
    """
    CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE = auto()
    """The default targets specified in the :class:`~.RichTableOptions` cannot be empty."""
    CHOICE_OPTIONS_INVALID_SUBDIR_TYPE = auto()
    """The ``subdir`` specified in the :class:`~.RichTableOptions` must be a string."""
    CHOICE_OPTIONS_INVALID_SUBDIR_VALUE = auto()
    """The ``subdir`` specified in the :class:`~.RichTableOptions` cannot be an empty
    string.
    """
    CHOICE_OPTIONS_INVALID_WIDTH_TYPE = auto()
    """The ``width`` specified in the :class:`~.RichTableOptions` must be an integer."""
    CHOICE_OPTIONS_INVALID_WIDTH_VALUE = auto()
    """The ``width`` specified in the :class:`~.RichTableOptions` must be greater than
    zero.
    """
    CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE = auto()
    """The default targets specified in the :class:`~.RichTableOptions` must be an
    iterable of :class:`~simplebench.enums.Target` enum members.
    """
    RUN_REPORT_UNSUPPORTED_TARGET = auto()
    """The rich table reporter does not support a target included in the targets."""
    RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE = auto()
    """The ``choice_options`` argument passed to :meth:`~.RichTableReporter.report` is not a
    :class:`~.RichTableOptions` instance.
    """
