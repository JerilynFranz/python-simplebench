"""Metaclasses for simplebench."""
from abc import ABCMeta


class ICase(metaclass=ABCMeta):
    """Interface for Case classes."""


class ISession(metaclass=ABCMeta):
    """Interface for Session classes."""


class ISimpleRunner(metaclass=ABCMeta):
    """Interface for SimpleRunner classes."""
