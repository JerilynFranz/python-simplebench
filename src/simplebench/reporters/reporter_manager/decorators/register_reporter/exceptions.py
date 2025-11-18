"""ErrorTags for :func:`~.register_reporter` decorator"""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class RegisterReporterErrorTag(ErrorTag):
    """Error tags for :func:`~.register_reporter` decorator."""
    # @register_reporter decorator errors
    NOT_REPORTER = "NOT_REPORTER"
    """The class decorated with ``@register_reporter`` is not a subclass of
    :class:`~simplebench.reporters.reporter.Reporter`"""

    # add() function errors
    INVALID_REPORTER_TYPE_ARG = "INVALID_REPORTER_TYPE_ARG"
    """Something other than a :class:`~simplebench.reporters.reporter.Reporter` subclass was passed to
    the :func:`~.register_reporter` decorator"""
    BASE_REPORTER_TYPE_ARG = "BASE_REPORTER_TYPE_ARG"
    """The base :class:`~simplebench.reporters.reporter.Reporter` class was passed to the
    :func:`~.register_reporter` decorator"""
