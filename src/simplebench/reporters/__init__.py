# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from collections import UserDict

from ..exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from .choices import Choices, Choice, Section, Target, Format
from .csv import CSVReporter
from .graph import GraphReporter
from .interfaces import Reporter
from .rich_table import RichTableReporter


class Reporters(UserDict[str, Reporter]):
    """Container for all available Reporter classes."""
    def __init__(self) -> None:
        self._reporters: dict[str, Reporter] = {
            'csv': CSVReporter(),
            'graph': GraphReporter(),
            'rich-table': RichTableReporter(),
        }
        super().__init__(self._reporters)

    def all(self) -> dict[str, Reporter]:
        """Return all available Reporter instances.

        Returns:
            dict[str, Reporter]: A dictionary of all Reporter instances
                with their unique names as keys.
        """
        return self._reporters

    def register(self, reporter: Reporter) -> None:
        """Register a new Reporter.

        Args:
            reporter (Reporter): The Reporter to register.

        Raises:
            SimpleBenchValueError: If a Reporter with the same name is already registered.
            SimpleBenchTypeError: If the provided reporter is not an instance of Reporter.
        """
        if not isinstance(reporter, Reporter):
            raise SimpleBenchTypeError(
                "reporter must be an instance of Reporter",
                ErrorTag.REPORTERS_REGISTER_INVALID_REPORTER_ARG
            )
        name = reporter.name
        if name in self._reporters:
            raise SimpleBenchValueError(
                f"A reporter with the name '{name}' is already registered.",
                ErrorTag.REPORTERS_REGISTER_DUPLICATE_NAME
            )
        self._reporters[name] = reporter

    def unregister(self, name: str) -> None:
        """Unregister a Reporter by its unique name.

        Args:
            name (str): The unique name of the reporter to unregister.

        Raises:
            SimpleBenchKeyError: If no reporter with the given name is registered.
        """
        if not isinstance(name, str):
            raise SimpleBenchTypeError(
                "name must be a string",
                ErrorTag.REPORTERS_UNREGISTER_INVALID_NAME_ARG
            )
        if name not in self._reporters:
            raise SimpleBenchKeyError(
                f"No reporter with the name '{name}' is registered.",
                ErrorTag.REPORTERS_UNREGISTER_UNKNOWN_NAME
            )
        del self._reporters[name]


__all__ = [
    'Choices',
    'Choice',
    'CSVReporter',
    'Format',
    'GraphReporter',
    'Reporter',
    'RichTableReporter',
    'Section',
    'Target',
]
