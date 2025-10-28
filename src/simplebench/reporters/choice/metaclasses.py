"""Metaclasses for simplebench.reporters.choice"""
from abc import ABCMeta


class IChoice(metaclass=ABCMeta):
    """Interface for Choice classes.

    This metaclass is used to identify Choice subclasses for type checking
    without creating circular import dependencies.

    Because Choice inherits from this metaclass, any subclass of
    Choice will also inherit from this metaclass.
    """
