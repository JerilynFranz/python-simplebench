"""Metaclasses for reporters."""
from abc import ABCMeta


class IReporter(metaclass=ABCMeta):
    """Interface for Reporter derived classes.

    It is primarily used to identify Reporter subclasses for type checking
    without creating circular import dependencies on Reporter itself and
    has no declared methods or properties of its own.

    Because Reporter inherits from this metaclass, any subclass of Reporter
    will also be considered a subclass of IReporter.
    """
