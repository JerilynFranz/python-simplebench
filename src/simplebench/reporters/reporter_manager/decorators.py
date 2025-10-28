"""Decorators for reporters."""
from __future__ import annotations
from typing import TypeVar

from ...exceptions import SimpleBenchTypeError
from ..exceptions.decorators import DecoratorsErrorTag
from ..reporter import Reporter
# from . import ReporterManager

# TODO: Implement automatic registration of reporters using this decorator

T = TypeVar('T', bound=Reporter)


def register_reporter(cls: type[T]) -> type[T]:
    """Class decorator to register a Reporter subclass.

    This decorator can be applied to any subclass of Reporter to
    register it with the system.
    """
    if not issubclass(cls, Reporter):
        raise SimpleBenchTypeError(
            "register_reporter can only be applied to Reporter subclasses.",
            tag=DecoratorsErrorTag.REGISTER_REPORTER_INVALID_CLASS)

    return cls
