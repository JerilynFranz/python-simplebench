"""ChoicesConf class for reporters.

This module defines the ChoicesConf class, which is a container for managing
ChoiceConf instances used in reporter configurations.

It ensures type safety by enforcing that only ChoiceConf instances can be added
to the container, and provides methods for adding, retrieving, and managing
these instances.

It is designed to be used in the context of reporters that require
a collection of ChoiceConf instances.

It has no methods of its own; all functionality is inherited from _BaseChoices.
"""
# pylint: disable=useless-parent-delegation
from __future__ import annotations
from typing import Iterable

from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.exceptions import ChoicesErrorTag

from simplebench.reporters.choices._base import _BaseChoices


class ChoicesConf(_BaseChoices[ChoiceConf, ChoicesErrorTag]):
    """A dictionary-like container for ChoiceConf instances.

    This class enforces that only `ChoiceConf` instances can be added to it,
    and provides methods to manage and retrieve those instances.

    It is designed to be used in the context of reporters that require
    a collection of `ChoiceConf` instances.
    """
    def __init__(self, choices: Iterable[ChoiceConf] | ChoicesConf | None = None) -> None:
        """Construct a Choices container.

        Args:
            choices (Iterable[ChoiceConf] | ChoicesConf | None, default=None):
                An Iterable of ChoiceConf instances or another ChoicesConf instance to
                initialize the container with.

                If None, an empty container is created.
        """
        super().__init__(item_type=ChoiceConf,
                         error_tag_enum=ChoicesErrorTag,
                         choices=choices)

    def add(self, choice: ChoiceConf) -> None:
        """Add a ChoiceConf instance to the container.

        The choice name attribute is used as the key in the container and
        is required to be unique withing the container.

        Args:
            choice (ChoiceConf):
                The ChoiceConf instance to add.

        Raises:
            SimpleBenchTypeError: If the argument is not a ChoiceConf instance.
            SimpleBenchValueError: If a ChoiceConf with the same name already exists in the container.
        """
        super().add(choice)

    def extend(  # type: ignore[reportIncompatibleMethodOverride, override]
            self, choices: Iterable[ChoiceConf] | ChoicesConf) -> None:
        """Add ChoiceConf instances to the container.

        It does so by adding each ChoiceConf in the provided iterable of ChoiceConf or
        by adding the ChoiceConf instances from the provided ChoicesConf instance.

        Args:
            choices (Iterable[ChoiceConf] | ChoicesConf):
                An iterable of ChoiceConf instances or an instance of ChoicesConf.

        Raises:
            SimpleBenchTypeError: If the choices argument is not an Iterable of ChoiceConf instances
                or a ChoicesConf instance.
            SimpleBenchValueError: If any ChoiceConf in the iterable has a duplicate name that already
                exists in the container.
        """
        super().extend(choices)

    def remove(self, name: str) -> None:
        """Remove a ChoiceConf instance from the container by its name.

        Args:
            name (str):
            The name of the ChoiceConf instance to remove.

        Raises:
            SimpleBenchKeyError: If no ChoiceConf under the given name exists in the container.
        """
        super().remove(name)

    # custom __delitem__ method to maintain indexes
    def __delitem__(self, key: str) -> None:
        """Remove a ChoiceConf instance from the container by its name.

        Args:
            name (str): The name of the ChoiceConf instance to remove.

        Raises:
            SimpleBenchKeyError: If no ChoiceConf under the given name exists in the container.
        """
        super().__delitem__(key)

    def __setitem__(self, key: str, value: ChoiceConf) -> None:
        """Set a value in the ChoicesConf container.

        This restricts setting values to only ChoiceConf instances with string keys
        and raises an error otherwise. It also prevents duplicate ChoiceConf names.

        It also restricts the key to match the ChoiceConf.name attribute and updates
        the internal indexes accordingly.

          Example:
            choices = ChoicesConf()
            choice = ChoiceConf(...)
            choices[choice.name] = choice

        Args:
            key (str):
                The key under which to store the ChoiceConf instance.
            value (ChoiceConf):
                The ChoiceConf instance to add.

        Raises:
            SimpleBenchTypeError: If the key is not a string or the value is not a ChoiceConf instance.
            SimpleBenchValueError: If a ChoiceConf with the same name already exists
                in the container; if the key does not match the ChoiceConf.name attribute;
                or if a ChoiceConf with the same flag already exists in the container.
        """
        super().__setitem__(key, value)
