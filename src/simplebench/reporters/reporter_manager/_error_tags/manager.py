"""ErrorTags for :mod:`~simplebench.reporters.reporter_manager` module in simplebench.reporters."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReporterManagerErrorTag(ErrorTag):
    """ErrorTags for the :class:`~simplebench.reporters.reporter_manager.ReporterManager` class."""

    CANNOT_REGISTER_BASE_CLASS = auto()
    """The base :class:`~simplebench.reporters.reporter.Reporter` class cannot be registered
    in the :class:`~simplebench.reporters.reporter_manager.ReporterManager` instance"""
    REGISTER_INVALID_REPORTER_ARG = auto()
    """Something other than a :class:`~simplebench.reporters.reporter.Reporter` instance was
    passed to the
    :meth:`~simplebench.reporters.reporter_manager.ReporterManager.register` method"""
    REGISTER_INVALID_CHOICES_RETURNED = auto()
    """Something other than a :class:`~simplebench.reporters.choices.Choices` instance was
    returned from the ``reporter.choices`` property"""
    REGISTER_INVALID_CHOICES_CONTENT = auto()
    """Something other than a :class:`~simplebench.reporters.choice.Choice` instance was
    found in the :class:`~simplebench.reporters.choices.Choices` instance returned
    from the ``reporter.choices`` property"""
    REGISTER_DUPLICATE_NAME = auto()
    """A :class:`~simplebench.reporters.reporter.Reporter` with the same name already exists
    in the :class:`~simplebench.reporters.reporter_manager.ReporterManager` instance"""
    REGISTER_DUPLICATE_CLI_ARG = auto()
    """A :class:`~simplebench.reporters.reporter.Reporter` with the same CLI argument already
    exists in the :class:`~simplebench.reporters.reporter_manager.ReporterManager` instance"""
    UNREGISTER_INVALID_REPORTER_ARG = auto()
    """Something other than a :class:`~simplebench.reporters.reporter.Reporter` instance was
    passed to the
    :meth:`~simplebench.reporters.reporter_manager.ReporterManager.unregister` method"""
    UNREGISTER_UNKNOWN_NAME = auto()
    """No :class:`~simplebench.reporters.reporter.Reporter` with the given name is registered
    in the :class:`~simplebench.reporters.reporter_manager.ReporterManager` instance"""
    ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG = auto()
    """Something other than an :class:`~argparse.ArgumentParser` instance was passed to the
    :meth:`~simplebench.reporters.reporter_manager.ReporterManager.add_reporters_to_argparse`
    method"""
    ARGUMENT_ERROR_ADDING_FLAGS = auto()
    """An ``ArgumentError`` was raised when adding reporter flags to the
    :class:`~argparse.ArgumentParser` instance"""
