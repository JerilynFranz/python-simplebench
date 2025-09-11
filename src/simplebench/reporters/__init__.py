# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from argparse import ArgumentParser

from ..exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from .choices import Choices, Choice, Section, Target, Format
from .csv import CSVReporter
from .graph import GraphReporter
from .interfaces import Reporter
from .rich_table import RichTableReporter


_PREDEFINED_REPORTERS = [CSVReporter, GraphReporter, RichTableReporter]
"""Container for all predefined Reporter classes."""


class ReporterManager():
    """Manager for all available Reporter classes.

    This class maintains a registry of Reporter instances and their associated
    CLI arguments. It allows for the registration, retrieval, and unregistration of
    Reporters.

    Initially, it registers a set of built-in Reporters: CSVReporter, GraphReporter, and RichTableReporter.

    New Reporters can be added using the `register` method, and existing ones can be
    removed using the `unregister` or `unregister_by_name` methods.

    Reporters are required to have unique names and CLI arguments in their Choices to avoid conflicts
    and the manager will raise exceptions if duplicates are detected during registration.

    Example:
        reporter_manager = ReporterManager()
        my_custom_reporter = CustomReporter()
        reporter_manager.register(my_custom_reporter)
    """
    def __init__(self) -> None:
        self._registered_reporter_choices: Choices = Choices()
        self._registered_reporters: dict[str, Reporter] = {}

        for reporter in _PREDEFINED_REPORTERS:
            self.register(reporter())

    @property
    def choices(self) -> Choices:
        """Return a Choices instance containing all registered reporter choices.

        Returns:
            Choices: A Choices instance with all registered reporter choices.
        """
        return self._registered_reporter_choices

    def choice_for_arg(self, arg: str) -> Choice | None:
        """Return the Choice instance for a given CLI argument.

        Args:
            arg (str): The CLI argument to look up.

        Returns:
            Choice | None: The corresponding Choice instance, or None if not found.
        """
        return self._registered_reporter_choices.get_choice_for_arg(arg)

    def register(self, reporter: Reporter) -> None:
        """Register a new Reporter.

        Args:
            reporter (Reporter): The Reporter to register.

        Raises:
            SimpleBenchValueError: If a Reporter with the same name or CLI argument is already registered.
            SimpleBenchTypeError: If the provided reporter is not an instance of Reporter.
        """
        if not isinstance(reporter, Reporter):
            raise SimpleBenchTypeError(
                "reporter must be an instance of Reporter",
                ErrorTag.REPORTER_MANAGER_REGISTER_INVALID_REPORTER_ARG
            )
        choices: Choices = reporter.choices
        if not isinstance(choices, Choices):
            raise SimpleBenchTypeError(
                "reporter.choices must return a Choices instance",
                ErrorTag.REPORTER_MANAGER_REGISTER_INVALID_CHOICES_RETURNED
            )
        all_choice_flags: set[str] = self._registered_reporter_choices.all_choice_flags()
        for choice in choices.values():
            if not isinstance(choice, Choice):
                print(f'Invalid choice type: {choice} ({type(choice)})')
                raise SimpleBenchTypeError((
                    "reporter.choices must return a Choices instance containing only Choice instances: "
                    f'Found {choices} {type(choice)} from reporter {reporter.name!r}'),
                    ErrorTag.REPORTER_MANAGER_REGISTER_INVALID_CHOICES_CONTENT
                )
            if choice.name in self._registered_reporter_choices:
                raise SimpleBenchValueError(
                    f"A reporter with the name '{choice.name}' is already registered.",
                    ErrorTag.REPORTER_MANAGER_REGISTER_DUPLICATE_NAME
                )
            for flag in choice.flags:
                if flag in all_choice_flags:
                    raise SimpleBenchValueError(
                        f"A reporter with the same CLI argument '{flag}' is already registered.",
                        ErrorTag.REPORTER_MANAGER_REGISTER_DUPLICATE_CLI_ARG
                    )
        self._registered_reporter_choices.extend(choices)
        self._registered_reporters[reporter.name] = reporter

    def all_reporters(self) -> dict[str, Reporter]:
        """Return all available Reporter instances as a dictionary keyed by their names.

        Returns:
            dict[str, Reporter]: A dictionary of all Reporter instances
                with their names as keys.
        """
        return {reporter.name: reporter for reporter in self._registered_reporters.values()}

    def unregister(self, reporter: Reporter) -> None:
        """Unregister a Reporter by an instance exemplar.

        It looks up the reporter by its name and removes it from the registry.

        Example:
            reporter_manager.unregister(MyCustomReporter())

        Args:
            reporter (Reporter): Reporter instance exemplar to unregister.

        Raises:
            SimpleBenchKeyError: If no reporter with the given name is registered.
            SimpleBenchTypeError: If the provided reporter is not an instance of Reporter.
        """
        if not isinstance(reporter, Reporter):
            raise SimpleBenchTypeError(
                "reporter must be an instance of Reporter",
                ErrorTag.REPORTER_MANAGER_UNREGISTER_INVALID_REPORTER_ARG
            )
        if reporter.name not in self._registered_reporters:
            raise SimpleBenchKeyError(
                f"No reporter with the name '{reporter.name}' is registered.",
                ErrorTag.REPORTER_MANAGER_UNREGISTER_UNKNOWN_NAME
            )
        for choice in reporter.choices.values():
            del self._registered_reporter_choices[choice.name]
        del self._registered_reporters[reporter.name]

    def unregister_by_name(self, name: str) -> None:
        """Unregister a Reporter by its name.

        Args:
            name (str): The name of the Reporter to unregister.
        Raises:
            SimpleBenchKeyError: If no reporter with the given name is registered.
        """
        if name not in self._registered_reporters:
            raise SimpleBenchKeyError(
                f"No reporter with the name '{name}' is registered.",
                ErrorTag.REPORTER_MANAGER_UNREGISTER_UNKNOWN_NAME
            )
        self.unregister(self._registered_reporters[name])

    def add_reporters_to_argparse(self, parser) -> None:
        """Add all registered reporter choices to an ArgumentParser.

        This method adds the CLI arguments for all registered reporters
        to the provided ArgumentParser instance.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                f'parser must be an ArgumentParser instance - cannot be a {type(parser)}',
                ErrorTag.REPORTER_MANAGER_ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG
            )
        for reporter in self._registered_reporters.values():
            reporter.add_flags_to_argparse(parser)


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
