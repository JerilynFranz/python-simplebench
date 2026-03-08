"""ErrorTags for :func:`~.register_reporter` decorator"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _RegisterReporterErrorTag(ErrorTag):
    """Error tags for :func:`~.register_reporter` decorator."""

    # @register_reporter decorator errors
    NOT_REPORTER = auto()
    """The class decorated with ``@register_reporter`` is not a subclass of
    :class:`~simplebench.reporters.reporter.Reporter`"""

    # add() function errors
    INVALID_REPORTER_TYPE_ARG = auto()
    """Something other than a :class:`~simplebench.reporters.reporter.Reporter` subclass was passed to
    the :func:`~.register_reporter` decorator"""
    BASE_REPORTER_TYPE_ARG = auto()
    """The base :class:`~simplebench.reporters.reporter.Reporter` class was passed to the
    :func:`~.register_reporter` decorator"""
