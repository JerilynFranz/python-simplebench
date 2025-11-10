"""Choices for reporters."""
# pylint: disable=useless-parent-delegation
from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

from simplebench.exceptions import SimpleBenchTypeError

from simplebench.reporters.choices.exceptions import ChoicesErrorTag
from simplebench.reporters.choices._base import _BaseChoices

_CHOICE_IMPORTED: bool = False
"""Indicates whether `Choice` has been imported yet."""


def deferred_choice_import() -> None:
    """Deferred import of Choice to avoid circular imports during initialization."""
    global Choice, _CHOICE_IMPORTED  # pylint: disable=global-statement
    if _CHOICE_IMPORTED:
        return
    from simplebench.reporters.choice.choice import Choice  # pylint: disable=import-outside-toplevel
    _CHOICE_IMPORTED = True


if TYPE_CHECKING:
    from simplebench.reporters.choice.choice import Choice


class Choices(_BaseChoices['Choice', ChoicesErrorTag]):
    """A dictionary-like container for Choice instances.

    This class enforces that only `Choice` instances can be added to it,
    and provides methods to manage and retrieve those instances.

    It is designed to be used in the context of reporters that require
    a collection of `Choice` instances.
    """
    def __init__(self, choices: Iterable[Choice] | Choices | None = None) -> None:
        """Construct a Choices container.

        Args:
            choices (Iterable[Choice] | Choices | None, default=None):
                An Iterable of Choice instances or another Choices instance to
                initialize the container with.

                If None, an empty container is created.
        """
        deferred_choice_import()
        super().__init__(item_type=Choice,
                         error_tag_enum=ChoicesErrorTag,
                         choices=choices)

    def add(self, choice: Choice) -> None:
        """Add a Choice instance to the container.

        The choice name attribute is used as the key in the container and
        is required to be unique withing the container.

        Args:
            choice (Choice):
                The Choice instance to add.

        Raises:
            SimpleBenchTypeError: If the argument is not a Choice instance.
            SimpleBenchValueError: If a Choice with the same name already exists in the container.
        """
        super().add(choice)

    def all_choice_args(self) -> set[str]:
        """Return a set of all Namespace arg names from all Choice instances in the container.

        Returns:
            set[str]:
                A set of all Namespace arg names from all Choice instances.
        """
        return set(self._args_index.keys())

    def all_choice_flags(self) -> set[str]:
        """Return a set of all CLI flags from all Choice instances in the container.

        Returns:
            set[str]:
                A set of all CLI flags from all Choice instances.
        """
        return set(self._flags_index.keys())

    def get_choice_for_arg(self, arg: str) -> Choice | None:
        """Return the Choice instance associated with the given Namespace arg name.

        Args:
            arg (str):
                The Namespace arg name to look up.

        Returns:
            Choice | None: The Choice instance associated with the arg,
                or None if no such Choice exists.

        Raises:
            SimpleBenchTypeError: If the arg is not a string.
        """
        if not isinstance(arg, str):
            raise SimpleBenchTypeError(
                "arg must be a string",
                tag=ChoicesErrorTag.GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE)
        return self._args_index.get(arg, None)

    def extend(  # type: ignore[reportIncompatibleMethodOverride, override]
            self, choices: Iterable[Choice] | Choices) -> None:
        """Add Choice instances to the container. It does so by adding each Choice in the
        provided iterable of Choice or by adding the Choice instances from the provided Choices instance.

        Args:
            choices (Iterable[Choice] | Choices): An iterable of Choice instances or an instance of Choices.

        Raises:
            SimpleBenchTypeError: If the choices argument is not an Iterable of Choice instances or a Choices instance.
            SimpleBenchValueError: If any Choice in the iterable has a duplicate name that already exists in
                the container.
        """
        super().extend(choices)

    def remove(self, name: str) -> None:
        """Remove a Choice instance from the container by its name.

        Args:
            name (str): The name of the Choice instance to remove.

        Raises:
            SimpleBenchKeyError: If no Choice under the given name exists in the container.
        """
        super().remove(name)

    # custom __delitem__ method to maintain indexes
    def __delitem__(self, key: str) -> None:
        """Remove a Choice instance from the container by its name.

        Args:
            name (str): The name of the Choice instance to remove.

        Raises:
            SimpleBenchKeyError: If no Choice under the given name exists in the container.
        """
        super().__delitem__(key)

    # custom __setitem__ method to make Choices into a type restricted dict
    # We override __setitem__ to enforce that only Choice instances
    # can be added to the container, and to maintain internal indexes.
    def __setitem__(self, key: str, value: Choice) -> None:
        """Set a value in the Choices container.

        This restricts setting values to only Choice instances with string keys
        and raises an error otherwise. It also prevents duplicate Choice names.

        It also restricts the key to match the Choice.name attribute and updates
        the internal indexes accordingly.

          Example:
            choices = Choices()
            choice = Choice(...)
            choices[choice.name] = choice

        Args:
            key (str):
                The key under which to store the Choice instance.
            value (Choice):
                The Choice instance to add.

        Raises:
            SimpleBenchTypeError: If the key is not a string or the value is not a Choice instance.
            SimpleBenchValueError: If a Choice with the same name already exists
                in the container; if the key does not match the Choice.name attribute;
                or if a Choice with the same flag already exists in the container.
        """
        super().__setitem__(key, value)
