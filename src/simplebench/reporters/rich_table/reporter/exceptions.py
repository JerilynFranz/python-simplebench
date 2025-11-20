"""Exception ErrorTags for the rich_table reporter."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions.base import ErrorTag


@enum_docstrings
class _RichTableReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the rich_table reporter."""
    RENDER_INVALID_CASE = "RENDER_INVALID_CASE"
    """The ``case`` argument passed to :meth:`~.RichTableReporter.render` is not a
    :class:`~simplebench.case.Case` instance.
    """
    RENDER_INVALID_OPTIONS = "RENDER_INVALID_OPTIONS"
    """The ``options`` argument passed to :meth:`~.RichTableReporter.render` is not a
    :class:`~.RichTableOptions` instance.
    """
    RENDER_INVALID_SECTION = "RENDER_INVALID_SECTION"
    """The ``section`` argument passed to :meth:`~.RichTableReporter.render` is not a
    :class:`~simplebench.enums.Section` enum member.
    """
    CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE = (
        "CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE")
    """The default targets specified in the :class:`~.RichTableOptions` are not valid
    :class:`~simplebench.enums.Target` enum members.
    """
    CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE = (
        "CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE")
    """The default targets specified in the :class:`~.RichTableOptions` cannot be empty."""
    CHOICE_OPTIONS_INVALID_SUBDIR_TYPE = "CHOICE_OPTIONS_INVALID_SUBDIR_TYPE"
    """The ``subdir`` specified in the :class:`~.RichTableOptions` must be a string."""
    CHOICE_OPTIONS_INVALID_SUBDIR_VALUE = "CHOICE_OPTIONS_INVALID_SUBDIR_VALUE"
    """The ``subdir`` specified in the :class:`~.RichTableOptions` cannot be an empty
    string.
    """
    CHOICE_OPTIONS_INVALID_WIDTH_TYPE = "CHOICE_OPTIONS_INVALID_WIDTH_TYPE"
    """The ``width`` specified in the :class:`~.RichTableOptions` must be an integer."""
    CHOICE_OPTIONS_INVALID_WIDTH_VALUE = "CHOICE_OPTIONS_INVALID_WIDTH_VALUE"
    """The ``width`` specified in the :class:`~.RichTableOptions` must be greater than
    zero.
    """
    CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE = (
        "CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE")
    """The default targets specified in the :class:`~.RichTableOptions` must be an
    iterable of :class:`~simplebench.enums.Target` enum members.
    """
    RUN_REPORT_UNSUPPORTED_TARGET = "RUN_REPORT_UNSUPPORTED_TARGET"
    """The rich table reporter does not support a target included in the targets."""
    RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE = "RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE"
    """The ``choice_options`` argument passed to :meth:`~.RichTableReporter.report` is not a
    :class:`~.RichTableOptions` instance.
    """
