"""Choices for reporters."""
# pylint: disable=useless-parent-delegation
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.choices._base import _BaseChoices
from simplebench.reporters.choices.exceptions import _ChoicesErrorTag

_CHOICE_IMPORTED: bool = False
"""Indicates whether :class:`~simplebench.reporters.choice.Choice` has been imported yet."""


def deferred_choice_import() -> None:
    """Deferred import of :class:`~simplebench.reporters.choice.Choice`
    to avoid circular imports during initialization."""
    global Choice, _CHOICE_IMPORTED  # pylint: disable=global-statement
    if _CHOICE_IMPORTED:
        return
    from simplebench.reporters.choice.choice import Choice  # pylint: disable=import-outside-toplevel
    _CHOICE_IMPORTED = True


if TYPE_CHECKING:
    from simplebench.reporters.choice.choice import Choice


class Choices(_BaseChoices['Choice', _ChoicesErrorTag]):
    """A dictionary-like container for :class:`~simplebench.reporters.choice.Choice` instances.

    This class enforces that only :class:`~simplebench.reporters.choice.Choice` instances
    can be added to it, and provides methods to manage and retrieve those instances.

    It is designed to be used in the context of reporters that require
    a collection of :class:`~simplebench.reporters.choice.Choice` instances.
    """
    def __init__(self, choices: Iterable[Choice] | Choices | None = None) -> None:
        """Construct a :class:`~.Choices` container.

        :param choices: An ``Iterable`` of :class:`~simplebench.reporters.choice.Choice`
                        instances or another :class:`~.Choices` instance to
                        initialize the container with. If ``None``, an empty container
                        is created.
        :type choices: Iterable[:class:`~simplebench.reporters.choice.Choice`] | \
            :class:`~.Choices` | None
        """
        deferred_choice_import()
        super().__init__(item_type=Choice,
                         error_tag_enum=_ChoicesErrorTag,
                         choices=choices)

    def add(self, choice: Choice) -> None:
        """Add a :class:`~simplebench.reporters.choice.Choice` instance to the container.

        The ``choice.name`` attribute is used as the key in the container and
        is required to be unique withing the container.

        :param choice: The :class:`~simplebench.reporters.choice.Choice` instance to add.
        :type choice: :class:`~simplebench.reporters.choice.Choice`
        :raises SimpleBenchTypeError: If the argument is not a
                                     :class:`~simplebench.reporters.choice.Choice` instance.
        :raises SimpleBenchValueError: If a :class:`~simplebench.reporters.choice.Choice`
                                       with the same name already exists in the container.
        """
        super().add(choice)

    def all_choice_args(self) -> set[str]:
        """Return a set of all ``Namespace`` arg names from all
        :class:`~simplebench.reporters.choice.Choice` instances in the container.

        :return: A set of all ``Namespace`` arg names from all
                 :class:`~simplebench.reporters.choice.Choice` instances.
        :rtype: set[str]
        """
        return set(self._args_index.keys())

    def all_choice_flags(self) -> set[str]:
        """Return a set of all CLI flags from all
        :class:`~simplebench.reporters.choice.Choice` instances in the container.

        :return: A set of all CLI flags from all
                 :class:`~simplebench.reporters.choice.Choice` instances.
        :rtype: set[str]
        """
        return set(self._flags_index.keys())

    def get_choice_for_arg(self, arg: str) -> Choice | None:
        """Return the :class:`~simplebench.reporters.choice.Choice` instance associated with
        the given ``Namespace`` arg name.

        :param arg: The ``Namespace`` arg name to look up.
        :type arg: str
        :return: The :class:`~simplebench.reporters.choice.Choice` instance associated with
                 the arg, or ``None`` if no such
                 :class:`~simplebench.reporters.choice.Choice` exists.
        :rtype: :class:`~simplebench.reporters.choice.Choice` | None
        :raises SimpleBenchTypeError: If the arg is not a string.
        """
        if not isinstance(arg, str):
            raise SimpleBenchTypeError(
                "arg must be a string",
                tag=_ChoicesErrorTag.GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE)
        return self._args_index.get(arg, None)

    def extend(  # type: ignore[reportIncompatibleMethodOverride, override]
            self, choices: Iterable[Choice] | Choices) -> None:
        """Add :class:`~simplebench.reporters.choice.Choice` instances to the container.
        It does so by adding each :class:`~simplebench.reporters.choice.Choice` in the
        provided ``Iterable`` of :class:`~simplebench.reporters.choice.Choice` or by adding
        the :class:`~simplebench.reporters.choice.Choice` instances from the provided
        :class:`~.Choices` instance.

        :param choices: An ``Iterable`` of :class:`~simplebench.reporters.choice.Choice`
                        instances or an instance of :class:`~.Choices`.
        :type choices: Iterable[:class:`~simplebench.reporters.choice.Choice`] | \
            :class:`~.Choices`
        :raises SimpleBenchTypeError: If the ``choices`` argument is not an ``Iterable`` of
                                     :class:`~simplebench.reporters.choice.Choice` instances
                                     or a :class:`~.Choices` instance.
        :raises SimpleBenchValueError: If any :class:`~simplebench.reporters.choice.Choice`
                                       in the ``Iterable`` has a duplicate name that already
                                       exists in the container.
        """
        super().extend(choices)

    def remove(self, name: str) -> None:
        """Remove a :class:`~simplebench.reporters.choice.Choice` instance from the container
        by its name.

        :param name: The name of the :class:`~simplebench.reporters.choice.Choice` instance
                     to remove.
        :type name: str
        :raises SimpleBenchKeyError: If no :class:`~simplebench.reporters.choice.Choice`
                                     under the given name exists in the container.
        """
        super().remove(name)

    # custom __delitem__ method to maintain indexes
    def __delitem__(self, key: str) -> None:
        """Remove a :class:`~simplebench.reporters.choice.Choice` instance from the container
        by its name.

        :param name: The name of the :class:`~simplebench.reporters.choice.Choice` instance
                     to remove.
        :type name: str
        :raises SimpleBenchKeyError: If no :class:`~simplebench.reporters.choice.Choice`
                                     under the given name exists in the container.
        """
        super().__delitem__(key)

    # custom __setitem__ method to make Choices into a type restricted dict
    # We override __setitem__ to enforce that only Choice instances
    # can be added to the container, and to maintain internal indexes.
    def __setitem__(self, key: str, value: Choice) -> None:
        """Set a value in the :class:`~.Choices` container.

        This restricts setting values to only :class:`~simplebench.reporters.choice.Choice`
        instances with string keys and raises an error otherwise. It also prevents duplicate
        :class:`~simplebench.reporters.choice.Choice` names.

        It also restricts the key to match the ``Choice.name`` attribute and updates
        the internal indexes accordingly.

        .. code-block:: python

            choices = Choices()
            choice = Choice(...)
            choices[choice.name] = choice

        :param key: The key under which to store the
                    :class:`~simplebench.reporters.choice.Choice` instance.
        :type key: str
        :param value: The :class:`~simplebench.reporters.choice.Choice` instance to add.
        :type value: :class:`~simplebench.reporters.choice.Choice`
        :raises SimpleBenchTypeError: If the key is not a string or the value is not a
                                     :class:`~simplebench.reporters.choice.Choice` instance.
        :raises SimpleBenchValueError: If a :class:`~simplebench.reporters.choice.Choice`
                                       with the same name already exists
                                       in the container; if the key does not match the
                                       ``Choice.name`` attribute;
                                       or if a :class:`~simplebench.reporters.choice.Choice`
                                       with the same flag already exists in the container.
        """
        super().__setitem__(key, value)
