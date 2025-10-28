"""Choices for reporters."""
from __future__ import annotations
from collections import UserDict
from typing import Sequence

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchKeyError
from simplebench.validators import validate_sequence_of_type

# simplebench.reporters imports
from ..choice import Choice


# simplebench.reporters.choices imports
from .exceptions import ChoicesErrorTag
from .metaclasses import IChoices


class Choices(UserDict[str, Choice], IChoices):
    """A dictionary-like container for Choice instances."""
    def __init__(self, choices: Sequence[Choice] | Choices | None = None) -> None:
        """Construct a Choices container.

        Args:
            choices (Sequence[Choice] | Choices): An optional sequence of Choice instances
                or another Choices instance to initialize the container with.
                If not provided, the container will be initialized empty."""
        self._args_index: dict[str, Choice] = {}
        self._flags_index: dict[str, Choice] = {}
        super().__init__()
        choices_list: list[Choice] = []
        if isinstance(choices, Sequence) and not isinstance(choices, str):
            for choice in choices:
                if not isinstance(choice, Choice):
                    raise SimpleBenchTypeError(
                        f"Expected a Sequence of Choice instances but got an item of type {type(choice)}",
                        tag=ChoicesErrorTag.INVALID_CHOICES_ITEM_VALUE)
            choices_list = list(choices)
        elif choices is not None:
            if isinstance(choices, Choices):
                choices_list = list(choices.values())
            else:
                raise SimpleBenchTypeError(
                    f"Expected a Sequence of Choice instances or a Choices instance but got {type(choices)}",
                    tag=ChoicesErrorTag.INVALID_CHOICES_ARG_TYPE)

        if choices_list:
            self.extend(choices_list)

    def add(self, choice: Choice) -> None:
        """Add a Choice instance to the container.

        The choice name attribute is used as the key in the container.

        Args:
            choice (Choice): The Choice instance to add.

        Raises:
            SimpleBenchTypeError: If the argument is not a Choice instance.
            SimpleBenchValueError: If a Choice with the same name already exists in the container.
        """
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ChoicesErrorTag.ADD_INVALID_CHOICE_ARG_TYPE)
        self[choice.name] = choice

    def all_choice_args(self) -> set[str]:
        """Return a set of all Namespace arg names from all Choice instances in the container.

        Returns:
            set[str]: A set of all Namespace arg names from all Choice instances.
        """
        return set(self._args_index.keys())

    def all_choice_flags(self) -> set[str]:
        """Return a set of all CLI flags from all Choice instances in the container.

        Returns:
            set[str]: A set of all CLI flags from all Choice instances.
        """
        return set(self._flags_index.keys())

    def get_choice_for_arg(self, arg: str) -> Choice | None:
        """Return the Choice instance associated with the given Namespace arg name.

        Args:
            arg (str): The Namespace arg name to look up.

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

    def extend(self, choices: Sequence[Choice] | Choices) -> None:
        """Add Choice instances to the container.

        Args:
            choices (Sequence[Choice] | Choices): A sequence of Choice instances or an instance of Choices.

        Raises:
            SimpleBenchTypeError: If the choices argument is not a Sequence of Choice instances or a Choices instance.
            SimpleBenchValueError: If any Choice in the sequence has a duplicate name that already exists in
                the container.
        """
        if isinstance(choices, Choices):
            for choice in choices.values():
                self.add(choice)
        else:
            choices_list = validate_sequence_of_type(
                choices, Choice, "choices",
                ChoicesErrorTag.EXTEND_INVALID_CHOICES_ARG_SEQUENCE_TYPE,
                ChoicesErrorTag.EXTEND_INVALID_CHOICES_ITEM_VALUE,
                allow_empty=True)
            for choice in choices_list:
                self.add(choice)

    def remove(self, name: str) -> None:
        """Remove a Choice instance from the container by its name.

        Args:
            name (str): The name of the Choice instance to remove.
        Raises:
            SimpleBenchKeyError: If no Choice under the given name exists in the container.
        """
        del self[name]

    # custom __delitem__ method to maintain indexes
    def __delitem__(self, key: str) -> None:
        """Remove a Choice instance from the container by its name.

        Args:
            name (str): The name of the Choice instance to remove.

        Raises:
            SimpleBenchKeyError: If no Choice under the given name exists in the container.
        """
        if key not in self.data:
            raise SimpleBenchKeyError(
                f"No Choice key with the name '{key}' exists",
                tag=ChoicesErrorTag.DELITEM_UNKNOWN_CHOICE_NAME)
        choice = self[key]
        for arg in choice.flags:
            if arg in self._flags_index:
                del self._flags_index[arg]
            arg_key = arg.replace('--', '', 1).replace('-', '_')
            if arg_key in self._args_index:
                del self._args_index[arg_key]
        super().__delitem__(key)

    # custom __setitem__ method to make Choices into a type restricted dict
    def __setitem__(self, key: str, value: Choice) -> None:
        """Set a value in the Choices container.

        This restricts setting values to only Choice instances with string keys
        and raises an error otherwise. It also prevents duplicate Choice names.

        It also restricts the key to match the Choice.name attribute and updates
        the internal indexes accordingly.

          Example:
            choices = Choices()
            choice = Choice(...)
            choices['my_choice'] = choice

        Args:
            key (str): The key under which to store the Choice instance.
            value (Choice): The Choice instance to store.

        Raises:
            SimpleBenchTypeError: If the key is not a string or the value is not a Choice instance.
            SimpleBenchValueError: If a Choice with the same name already exists
                in the container; if the key does not match the Choice.name attribute;
                or if a Choice with the same flag already exists in the container.
        """
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                "Choice key must be a string",
                tag=ChoicesErrorTag.SETITEM_INVALID_KEY_TYPE)
        if not isinstance(value, Choice):
            raise SimpleBenchTypeError(
                "Only Choice instances can be added to Choices",
                tag=ChoicesErrorTag.SETITEM_INVALID_VALUE_TYPE)
        if key != value.name:
            raise SimpleBenchValueError(
                "Choice key must match the Choice.name attribute",
                tag=ChoicesErrorTag.SETITEM_KEY_NAME_MISMATCH)
        if value.name in self.data:
            raise SimpleBenchValueError(
                f"A Choice with the name '{value.name}' already exists",
                tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME)

        self._args_index.update({flag.replace('--', '', 1).replace('-', '_'): value for flag in value.flags})
        for flag in value.flags:
            if flag in self._flags_index:
                raise SimpleBenchValueError(
                    f"A Choice with the flag '{flag}' already exists",
                    tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_FLAG)
            self._flags_index[flag] = value
        super().__setitem__(key, value)
