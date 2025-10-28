"""Metaclasses for simplebench.reporters.choices"""
from abc import ABCMeta


class IChoices(metaclass=ABCMeta):
    """Interface for Choices classes.

    This metaclass is used to identify Choices subclasses for type checking
    without creating circular import dependencies.

    Because Choices inherits from this metaclass, any subclass of
    Choices will also inherit from this metaclass.
    """
