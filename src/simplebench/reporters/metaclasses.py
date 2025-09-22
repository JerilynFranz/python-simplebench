"""Metaclasses for reporters."""
from abc import ABCMeta


class IReporter(metaclass=ABCMeta):
    """Interface for Reporter derived classes."""


class IChoice(metaclass=ABCMeta):
    """Interface for Choice classes."""


class IChoices(metaclass=ABCMeta):
    """Interface for Choices classes."""
