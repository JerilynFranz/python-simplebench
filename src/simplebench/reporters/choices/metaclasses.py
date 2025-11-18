"""Metaclasses for :mod:`simplebench.reporters.choices`"""
from abc import ABCMeta


class IChoices(metaclass=ABCMeta):
    """Interface for :class:`~.Choices` classes.

    This metaclass is used to identify :class:`~.Choices` subclasses for type checking
    without creating circular import dependencies.

    Because :class:`~.Choices` inherits from this metaclass, any subclass of
    :class:`~.Choices` will also inherit from this metaclass.
    """
