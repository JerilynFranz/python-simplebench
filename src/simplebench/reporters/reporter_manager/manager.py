"""ReporterManager for benchmark results.

This module contains the :class:`~.ReporterManager` class, which manages the registration,
retrieval, and unregistration of :class:`~simplebench.reporters.reporter.Reporter`
classes and instances.

This registry is global. When a :class:`~simplebench.reporters.reporter.Reporter` is registered,
it is added to the global registry, and when it is unregistered, it is removed from the
global registry.
"""
from __future__ import annotations

import importlib
from argparse import ArgumentParser

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.choice import Choice
from simplebench.reporters.choices import Choices
from simplebench.reporters.reporter import Reporter

from .decorators.register_reporter import get_registered_reporters
from .exceptions import _ReporterManagerErrorTag

_PREDEFINED_REPORTERS: list[tuple[str, str]] = [
    ("simplebench.reporters.csv", "CSVReporter"),
    ("simplebench.reporters.graph.scatterplot", "ScatterPlotReporter"),
    ("simplebench.reporters.rich_table", "RichTableReporter"),
    ("simplebench.reporters.json", "JSONReporter"),
]
"""Container for all predefined Reporter classes.

These reporters are registered by default in the ReporterManager.
- :class:`~simplebench.reporters.csv.reporter.CSVReporter`
- :class:`~simplebench.reporters.graph.scatterplot.reporter.ScatterPlotReporter`
- :class:`~simplebench.reporters.rich_table.reporter.RichTableReporter`
- :class:`~simplebench.reporters.json.reporter.JSONReporter`
"""


class ReporterManager():
    """Manager for all available :class:`~simplebench.reporters.reporter.Reporter` classes.

    This class maintains a registry of :class:`~simplebench.reporters.reporter.Reporter`
    instances and their associated CLI arguments. It allows for the registration, retrieval,
    and unregistration of :class:`~simplebench.reporters.reporter.Reporter` instances.

    Initially, it registers a set of built-in :class:`~simplebench.reporters.reporter.Reporter`
    instances: :class:`~simplebench.reporters.csv.reporter.CSVReporter`,
    :class:`~simplebench.reporters.graph.scatterplot.reporter.ScatterPlotReporter`,
    and :class:`~simplebench.reporters.rich_table.reporter.RichTableReporter`.

    New :class:`~simplebench.reporters.reporter.Reporter` instances can be added using the
    :meth:`~.register` method, and existing ones can be removed using the :meth:`~.unregister`
    or :meth:`~.unregister_by_name` methods.

    :class:`~simplebench.reporters.reporter.Reporter` instances are required to have unique
    names and CLI arguments in their :class:`~simplebench.reporters.choices.Choices` to avoid
    conflicts and the manager will raise exceptions if duplicates are detected during registration.

    .. code-block:: python
      :caption: Registering a custom reporter example
      :linenos:

      reporter_manager = ReporterManager()
      my_custom_reporter = CustomReporter()
      reporter_manager.register(my_custom_reporter)

    """

    def __init__(self, load_defaults: bool = True) -> None:
        """Initialize the ReporterManager.

        By default, this loads a set of predefined :class:`~simplebench.reporters.reporter.Reporter`
        instances and then any reporters registered via the :func:`~.register_reporter` decorator.

        If one of the predefined reporters' dependencies are not installed, that reporter
        will be skipped and not registered.

        If desired, this can be skipped by setting ``load_defaults`` to ``False``. In
        which case, the manager starts with an empty registry and
        :class:`~simplebench.reporters.reporter.Reporter` instances can be added via the
        :meth:`~.register` method.


        :param load_defaults: Whether to load the predefined reporters. Defaults to ``True``.
        :type load_defaults: bool
        """
        self._registered_reporter_choices: Choices = Choices()
        self._registered_reporters: dict[str, Reporter] = {}

        if not load_defaults:
            return
        for module_name, class_name in _PREDEFINED_REPORTERS:
            try:
                module = importlib.import_module(module_name)
                reporter_class = getattr(module, class_name)
                self.register(reporter_class())
            except ImportError:
                # This allows for optional dependencies. If a reporter's dependencies
                # are not installed, it will not be available and we can just
                # skip it.
                pass
        for registered_reporter in get_registered_reporters():
            self.register(registered_reporter)

    @property
    def choices(self) -> Choices:
        """Return a :class:`~simplebench.reporters.choices.Choices` instance containing all
        registered reporter choices.

        :return: A :class:`~simplebench.reporters.choices.Choices` instance with all
                 registered reporter choices.
        :rtype: :class:`~simplebench.reporters.choices.Choices`
        """
        return self._registered_reporter_choices

    def choice_for_arg(self, arg: str) -> Choice | None:
        """Return the :class:`~simplebench.reporters.choice.Choice` instance for a given CLI argument.

        :param arg: The CLI argument to look up.
        :type arg: str
        :return: The corresponding :class:`~simplebench.reporters.choice.Choice` instance,
                 or ``None`` if not found.
        :rtype: :class:`~simplebench.reporters.choice.Choice` | None
        """
        return self._registered_reporter_choices.get_choice_for_arg(arg)

    def register(self, reporter: Reporter) -> None:
        """Register a new :class:`~simplebench.reporters.reporter.Reporter`.

        This method adds a new :class:`~simplebench.reporters.reporter.Reporter` to the registry.
        Unlike the predefined reporters and the :func:`~.register_reporter` decorator which both
        register by class, this method requires an instance of the
        :class:`~simplebench.reporters.reporter.Reporter`.

        This allows for more flexibility, such as registering
        :class:`~simplebench.reporters.reporter.Reporter` instances with custom
        initialization parameters.

        :param reporter: The :class:`~simplebench.reporters.reporter.Reporter` to register.
        :type reporter: :class:`~simplebench.reporters.reporter.Reporter`
        :raises SimpleBenchValueError: If a :class:`~simplebench.reporters.reporter.Reporter`
                                      with the same name or CLI argument is already registered.
        :raises SimpleBenchTypeError: If the provided reporter is not an instance of
                                     :class:`~simplebench.reporters.reporter.Reporter`.
        """
        if type(reporter) is Reporter:  # pylint: disable=unidiomatic-typecheck
            raise SimpleBenchValueError(
                "Cannot register the base Reporter class itself, please register a subclass instead.",
                tag=_ReporterManagerErrorTag.CANNOT_REGISTER_BASE_CLASS
            )
        if not isinstance(reporter, Reporter):
            raise SimpleBenchTypeError(
                "reporter must be an instance of Reporter",
                tag=_ReporterManagerErrorTag.REGISTER_INVALID_REPORTER_ARG
            )
        choices: Choices = reporter.choices
        if not isinstance(choices, Choices):
            raise SimpleBenchTypeError(
                "reporter.choices must return a Choices instance",
                tag=_ReporterManagerErrorTag.REGISTER_INVALID_CHOICES_RETURNED
            )
        all_choice_flags: set[str] = self._registered_reporter_choices.all_choice_flags()
        for choice in choices.values():
            if not isinstance(choice, Choice):
                print(f'Invalid choice type: {choice} ({type(choice)})')
                raise SimpleBenchTypeError((
                    "reporter.choices must return a Choices instance containing only Choice instances: "
                    f'Found {choices} {type(choice)} from reporter {reporter.name!r}'),
                    tag=_ReporterManagerErrorTag.REGISTER_INVALID_CHOICES_CONTENT
                )
            if choice.name in self._registered_reporter_choices:
                raise SimpleBenchValueError(
                    f"A reporter with the name '{choice.name}' is already registered.",
                    tag=_ReporterManagerErrorTag.REGISTER_DUPLICATE_NAME
                )
            for flag in choice.flags:
                if flag in all_choice_flags:
                    raise SimpleBenchValueError(
                        f"A reporter with the same CLI argument '{flag}' is already registered.",
                        tag=_ReporterManagerErrorTag.REGISTER_DUPLICATE_CLI_ARG
                    )
        self._registered_reporter_choices.extend(choices)
        self._registered_reporters[reporter.name] = reporter

    def all_reporters(self) -> dict[str, Reporter]:
        """Return all available :class:`~simplebench.reporters.reporter.Reporter` instances
        as a dictionary keyed by their names.

        :return: A dictionary of all :class:`~simplebench.reporters.reporter.Reporter`
                 instances with their names as keys.
        :rtype: dict[str, :class:`~simplebench.reporters.reporter.Reporter`]
        """
        return {reporter.name: reporter for reporter in self._registered_reporters.values()}

    def unregister(self, reporter: Reporter) -> None:
        """Unregister a :class:`~simplebench.reporters.reporter.Reporter` by an instance exemplar.

        It looks up the reporter by its name and removes it from the registry.

        .. code-block:: python

            reporter_manager.unregister(MyCustomReporter())

        :param reporter: :class:`~simplebench.reporters.reporter.Reporter` instance exemplar
                         to unregister.
        :type reporter: :class:`~simplebench.reporters.reporter.Reporter`
        :raises SimpleBenchKeyError: If no reporter with the given name is registered.
        :raises SimpleBenchTypeError: If the provided reporter is not an instance of
                                     :class:`~simplebench.reporters.reporter.Reporter`.
        """
        if not isinstance(reporter, Reporter):
            raise SimpleBenchTypeError(
                "reporter must be an instance of Reporter",
                tag=_ReporterManagerErrorTag.UNREGISTER_INVALID_REPORTER_ARG
            )
        if reporter.name not in self._registered_reporters:
            raise SimpleBenchKeyError(
                f"No reporter with the name '{reporter.name}' is registered.",
                tag=_ReporterManagerErrorTag.UNREGISTER_UNKNOWN_NAME
            )
        for choice in reporter.choices.values():
            del self._registered_reporter_choices[choice.name]
        del self._registered_reporters[reporter.name]

    def unregister_by_name(self, name: str) -> None:
        """Unregister a :class:`~simplebench.reporters.reporter.Reporter` by its name.

        :param name: The name of the :class:`~simplebench.reporters.reporter.Reporter`
                     to unregister.
        :type name: str
        :raises SimpleBenchKeyError: If no reporter with the given name is registered.
        """
        if name not in self._registered_reporters:
            raise SimpleBenchKeyError(
                f"No reporter with the name '{name}' is registered.",
                tag=_ReporterManagerErrorTag.UNREGISTER_UNKNOWN_NAME
            )
        self.unregister(self._registered_reporters[name])

    def unregister_all(self) -> None:
        """Unregister all :class:`~simplebench.reporters.reporter.Reporter` instances.

        This clears the entire registry of :class:`~simplebench.reporters.reporter.Reporter`
        instances.
        """
        self._registered_reporter_choices.clear()
        self._registered_reporters.clear()

    def add_reporters_to_argparse(self, parser: ArgumentParser) -> None:
        """Add all registered reporter choices to an :class:`~argparse.ArgumentParser`.

        This method adds the CLI arguments for all registered reporters
        to the provided :class:`~argparse.ArgumentParser` instance using the
        :meth:`~simplebench.reporters.reporter.Reporter.add_flags_to_argparse` method
        of each :class:`~simplebench.reporters.reporter.Reporter`.

        :param parser: The :class:`~argparse.ArgumentParser` to add the flags to.
        :type parser: :class:`~argparse.ArgumentParser`
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                f'parser must be an ArgumentParser instance - cannot be a {type(parser)}',
                tag=_ReporterManagerErrorTag.ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG
            )
        # Add flags for each registered reporter
        # The reporter is responsible for adding its own flags, so we just call its method
        # here. This allows each reporter to define its own flags and behavior.
        # We assume that the reporter's add_flags_to_argparse method is implemented correctly
        # and will handle any errors internally.
        for reporter in self._registered_reporters.values():
            reporter.add_flags_to_argparse(parser=parser)
