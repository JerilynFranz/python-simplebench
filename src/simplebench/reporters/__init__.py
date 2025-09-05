# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from collections import UserDict

from .choices import Choices
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
            ValueError: If a Reporter with the same name is already registered.
        """
        if not isinstance(reporter, Reporter):
            raise TypeError("reporter must be an instance of Reporter")
        name = reporter.name
        if name in self._reporters:
            raise ValueError(f"A reporter with the name '{name}' is already registered.")
        self._reporters[name] = reporter

    def unregister(self, name: str) -> None:
        """Unregister a Reporter by its unique name.

        Args:
            name (str): The unique name of the reporter to unregister.

        Raises:
            KeyError: If no reporter with the given name is registered.
        """
        if name not in self._reporters:
            raise KeyError(f"No reporter with the name '{name}' is registered.")
        del self._reporters[name]


__all__ = [
    'Choices',
    'CSVReporter',
    'GraphReporter',
    'Reporter',
    'RichTableReporter',
]
