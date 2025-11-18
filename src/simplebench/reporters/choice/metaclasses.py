"""Metaclasses for :mod:`simplebench.reporters.choice`"""
from abc import ABCMeta


class IChoice(metaclass=ABCMeta):
    """Interface for :class:`~.Choice` classes.

    This metaclass is used to identify :class:`~.Choice` subclasses for type checking
    without creating circular import dependencies.

    Because :class:`~.Choice` inherits from this metaclass, any subclass of
    :class:`~.Choice` will also inherit from this metaclass.
    """
