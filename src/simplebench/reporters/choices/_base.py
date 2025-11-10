"""Choices for reporters."""
from __future__ import annotations

from collections import UserDict
from collections.abc import Hashable
from typing import Generic, Iterable, Type, TypeVar

from simplebench.exceptions import (ErrorTag, SimpleBenchKeyError,
                                    SimpleBenchTypeError,
                                    SimpleBenchValueError)
from simplebench.reporters.protocols import ChoiceProtocol
from simplebench.validators import validate_iterable_of_type

T_Item = TypeVar('T_Item', bound=ChoiceProtocol)  # pylint: disable=invalid-name
T_Error = TypeVar('T_Error', bound=ErrorTag)  # pylint: disable=invalid-name


class _BaseChoices(Hashable, UserDict[str, T_Item], Generic[T_Item, T_Error]):
    """A generic dictionary-like container for Choice-like instances.

    This class enforces that only Choice-like instances can be added to it,
    and provides methods to manage and retrieve those instances.

    It is designed to be used in the context of reporters that require
    a collection of Choice-like instances.
    """
    def __init__(
        self,
        item_type: Type[T_Item],
        error_tag_enum: Type[T_Error],
        choices: Iterable[T_Item] | _BaseChoices[T_Item, T_Error] | None = None,
    ) -> None:
        """Construct generic Choices/ChoicesConf container.

        Args:
            item_type (Type[T_Item]):
                The expected type of items in the container (e.g., Choice or ChoiceConf
                or other ChoiceProtocol conforming subclass type).
            error_tag_enum (Type[T_Error]):
                The enum class containing error tags for this container.
            choices (Iterable[T_Item] | _BaseChoices[T_Item, T_Error] | None, default=None):
                An Iterable of ChoiceProtocol conforming instances or another _BaseChoices
                subclass instance to initialize the container with.

                If None, an empty container is created.
        """
        self._item_type = item_type
        self._error_tags = error_tag_enum
        self._args_index: dict[str, T_Item] = {}
        self._flags_index: dict[str, T_Item] = {}
        super().__init__()

        choices = [] if choices is None else choices

        if isinstance(choices, _BaseChoices):
            self.extend(choices)
            return

        # 4. Use the generic types in the implementation
        choices_list: list[T_Item] = validate_iterable_of_type(
            choices, self._item_type, "choices",
            self._error_tags.CHOICES_INVALID_ARG_TYPE,  # type: ignore[attributeAccessIssue, attr-defined]
            self._error_tags.CHOICES_INVALID_ITEM_VALUE,  # type: ignore[attributeAccessIssue, attr-defined]
            allow_empty=True, exact_type=True)

        if choices_list:
            self.extend(choices_list)

    def add(self, choice: T_Item) -> None:
        """Add a instance to the container.

        The choice name attribute is used as the key in the container and
        is required to be unique within the container.

        Args:
            choice (T_Item):
                The instance to add.

        Raises:
            SimpleBenchTypeError: If the argument is not an instance of the expected item type.
            SimpleBenchValueError: If a ChoiceConf with the same name already exists in the container.
        """
        if not isinstance(choice, self._item_type):
            raise SimpleBenchTypeError(
                f"Only {self._item_type.__name__} instances can be added: ",
                tag=self._error_tags.ADD_CHOICE_INVALID_ARG_TYPE)  # type: ignore[attributeAccessIssue, attr-defined]
        self[choice.name] = choice

    def extend(self, choices: Iterable[T_Item] | _BaseChoices[T_Item, T_Error]) -> None:
        """Add instances to the container. It does so by adding each instance in the
        provided iterable of T_Item instances or by adding the instances from the
        provided _BaseChoices subclass instance.

        Args:
            choices (Iterable[T_Item] | _BaseChoices[T_Item, T_Error]):
                An iterable of instances or an instance of a Choices-like container.
        Raises:
            SimpleBenchTypeError: If the choices argument is not an Iterable of ChoiceConf instances
                or a ChoicesConf instance.
            SimpleBenchValueError: If any ChoiceConf in the iterable has a duplicate name that already exists in
                the container.
        """
        if isinstance(choices, _BaseChoices):
            for choice in choices.values():
                self.add(choice)
        else:
            choices_list = validate_iterable_of_type(
                choices, self._item_type, "choices",
                self._error_tags.EXTEND_CHOICES_INVALID_ARG_TYPE,  # type: ignore[attributeAccessIssue, attr-defined]
                self._error_tags.EXTEND_CHOICES_INVALID_ITEM_VALUE,  # type: ignore[attributeAccessIssue, attr-defined]
                allow_empty=True)
            for choice in choices_list:
                self.add(choice)

    def remove(self, name: str) -> None:
        """Remove an item instance from the container by its name.

        Args:
            name (str):
                The name of the ChoiceConf instance to remove.
        Raises:
            SimpleBenchKeyError: If no ChoiceConf under the given name exists in the container.
        """
        del self[name]

    # custom __delitem__ method to maintain indexes
    def __delitem__(self, key: str) -> None:
        """Remove an instance from the container by its name.

        Args:
            name (str): The name of the instance to remove.

        Raises:
            SimpleBenchKeyError: If no instance under the given name exists in the container.
        """
        if key not in self.data:
            raise SimpleBenchKeyError(
                f"No {self._item_type.__name__} key with the name '{key}' exists",
                tag=self._error_tags.DELITEM_UNKNOWN_CHOICE_NAME)  # type: ignore[attributeAccessIssue, attr-defined]
        choice = self[key]
        for arg in choice.flags:
            if arg in self._flags_index:
                del self._flags_index[arg]
            arg_key = arg.replace('--', '', 1).replace('-', '_')
            if arg_key in self._args_index:
                del self._args_index[arg_key]
        super().__delitem__(key)

    # custom __setitem__ method to make ChoicesConf into a type restricted dict
    # We override __setitem__ to enforce that only ChoiceConf instances
    # can be added to the container, and to maintain internal indexes.
    def __setitem__(self, key: str, value: T_Item) -> None:
        """Set a value in the container.

        This restricts setting values to only instances with string keys
        and raises an error otherwise. It also prevents duplicate names.

        It also restricts the key to match the `name` attribute and updates
        the internal indexes accordingly.

          Example:
            choices = MyChoicesContainer()
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
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                "Choice key must be a string",
                tag=self._error_tags.SETITEM_INVALID_KEY_TYPE)  # type: ignore[attributeAccessIssue, attr-defined]
        if not isinstance(value, self._item_type):
            raise SimpleBenchTypeError(
                f"Only {self._item_type.__name__} instances can be added",
                tag=self._error_tags.SETITEM_INVALID_VALUE_TYPE)  # type: ignore[attributeAccessIssue, attr-defined]
        if key != value.name:
            raise SimpleBenchValueError(
                "key must match the item's .name attribute",
                tag=self._error_tags.SETITEM_KEY_NAME_MISMATCH)  # type: ignore[attributeAccessIssue, attr-defined]
        if key in self.data:
            raise SimpleBenchValueError(
                f"An item with the name '{value.name}' already exists",
                tag=self._error_tags.SETITEM_DUPLICATE_CHOICE_NAME)  # type: ignore[attributeAccessIssue, attr-defined]

        self._args_index.update({flag.replace('--', '', 1).replace('-', '_'): value for flag in value.flags})
        for flag in value.flags:
            if flag in self._flags_index:
                raise SimpleBenchValueError(
                    f"An item with the flag '{flag}' already exists",
                    tag=self._error_tags.SETITEM_DUPLICATE_CHOICE_FLAG)  # type: ignore[attributeAccessIssue, attr-defined]  # noqa: E501
            self._flags_index[flag] = value
        super().__setitem__(key, value)

    def __hash__(self) -> int:
        """Compute a hash value for the Choices container based on its id.

        This makes Choices instances hashable and usable in sets or as dictionary keys
        or by lru_cache.

        However, since the container is mutable, the hash value is based on its id
        and no two instances will have the same hash value.

        Returns:
            int: The computed hash value.
        """
        return id(self)

    def __eq__(self, other: object) -> bool:
        """Check equality between two Choices containers.

        This check is based on identity; two containers are considered equal
        if they are the same instance. Effectively this means that no two distinct
        instances will be considered equal, even if they contain the same items.

        Args:
            other (object): The other Choices container to compare against.

        Returns:
            bool: True if the containers are equal, False otherwise.
        """
        return id(self) == id(other)
