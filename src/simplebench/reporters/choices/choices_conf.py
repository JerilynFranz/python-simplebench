"""ChoicesConf class for reporters.

This module defines the :class:`~.ChoicesConf` class, which is a container for managing
:class:`~simplebench.reporters.choice.ChoiceConf` instances used in reporter configurations.

It ensures type safety by enforcing that only
:class:`~simplebench.reporters.choice.ChoiceConf` instances can be added
to the container, and provides methods for adding, retrieving, and managing
these instances.

It is designed to be used in the context of reporters that require
a collection of :class:`~simplebench.reporters.choice.ChoiceConf` instances.

It has no methods of its own; all functionality is inherited from
:class:`~simplebench.reporters.choices._base._BaseChoices`.
"""
# pylint: disable=useless-parent-delegation
from __future__ import annotations

from typing import Iterable

from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices._base import _BaseChoices
from simplebench.reporters.choices.exceptions import _ChoicesErrorTag


class ChoicesConf(_BaseChoices[ChoiceConf, _ChoicesErrorTag]):
    """A dictionary-like container for
    :class:`~simplebench.reporters.choice.ChoiceConf` instances.

    This class enforces that only :class:`~simplebench.reporters.choice.ChoiceConf`
    instances can be added to it, and provides methods to manage and retrieve those
    instances.

    It is designed to be used in the context of reporters that require
    a collection of :class:`~simplebench.reporters.choice.ChoiceConf` instances.
    """
    def __init__(self, choices: Iterable[ChoiceConf] | ChoicesConf | None = None) -> None:
        """Construct a :class:`~.Choices` container.

        :param choices: An ``Iterable`` of
                        :class:`~simplebench.reporters.choice.ChoiceConf` instances
                        or another :class:`~.ChoicesConf` instance to
                        initialize the container with. If ``None``, an empty container
                        is created.
        :type choices: Iterable[:class:`~simplebench.reporters.choice.ChoiceConf`] | \
            :class:`~.ChoicesConf` | None
        """
        super().__init__(item_type=ChoiceConf,
                         error_tag_enum=_ChoicesErrorTag,
                         choices=choices)

    def add(self, choice: ChoiceConf) -> None:
        """Add a :class:`~simplebench.reporters.choice.ChoiceConf` instance to the container.

        The ``choice.name`` attribute is used as the key in the container and
        is required to be unique withing the container.

        :param choice: The :class:`~simplebench.reporters.choice.ChoiceConf` instance to add.
        :type choice: :class:`~simplebench.reporters.choice.ChoiceConf`
        :raises SimpleBenchTypeError: If the argument is not a
                                     :class:`~simplebench.reporters.choice.ChoiceConf`
                                     instance.
        :raises SimpleBenchValueError: If a
                                       :class:`~simplebench.reporters.choice.ChoiceConf`
                                       with the same name already exists in the container.
        """
        super().add(choice)

    def extend(  # type: ignore[reportIncompatibleMethodOverride, override]
            self, choices: Iterable[ChoiceConf] | ChoicesConf) -> None:
        """Add :class:`~simplebench.reporters.choice.ChoiceConf` instances to the container.

        It does so by adding each :class:`~simplebench.reporters.choice.ChoiceConf` in the
        provided ``Iterable`` of :class:`~simplebench.reporters.choice.ChoiceConf` or
        by adding the :class:`~simplebench.reporters.choice.ChoiceConf` instances from the
        provided :class:`~.ChoicesConf` instance.

        :param choices: An ``Iterable`` of
                        :class:`~simplebench.reporters.choice.ChoiceConf` instances
                        or an instance of :class:`~.ChoicesConf`.
        :type choices: Iterable[:class:`~simplebench.reporters.choice.ChoiceConf`] | \
            :class:`~.ChoicesConf`
        :raises SimpleBenchTypeError: If the ``choices`` argument is not an ``Iterable`` of
                                     :class:`~simplebench.reporters.choice.ChoiceConf`
                                     instances or a :class:`~.ChoicesConf` instance.
        :raises SimpleBenchValueError: If any
                                       :class:`~simplebench.reporters.choice.ChoiceConf`
                                       in the ``Iterable`` has a duplicate name that already
                                       exists in the container.
        """
        super().extend(choices)

    def remove(self, name: str) -> None:
        """Remove a :class:`~simplebench.reporters.choice.ChoiceConf` instance from the
        container by its name.

        :param name: The name of the :class:`~simplebench.reporters.choice.ChoiceConf`
                     instance to remove.
        :type name: str
        :raises SimpleBenchKeyError: If no
                                     :class:`~simplebench.reporters.choice.ChoiceConf`
                                     under the given name exists in the container.
        """
        super().remove(name)

    # custom __delitem__ method to maintain indexes
    def __delitem__(self, key: str) -> None:
        """Remove a :class:`~simplebench.reporters.choice.ChoiceConf` instance from the
        container by its name.

        :param name: The name of the :class:`~simplebench.reporters.choice.ChoiceConf`
                     instance to remove.
        :type name: str
        :raises SimpleBenchKeyError: If no
                                     :class:`~simplebench.reporters.choice.ChoiceConf`
                                     under the given name exists in the container.
        """
        super().__delitem__(key)

    def __setitem__(self, key: str, value: ChoiceConf) -> None:
        """Set a value in the :class:`~.ChoicesConf` container.

        This restricts setting values to only
        :class:`~simplebench.reporters.choice.ChoiceConf` instances with string keys
        and raises an error otherwise. It also prevents duplicate
        :class:`~simplebench.reporters.choice.ChoiceConf` names.

        It also restricts the key to match the ``ChoiceConf.name`` attribute and updates
        the internal indexes accordingly.

        .. code-block:: python

            choices = ChoicesConf()
            choice = ChoiceConf(...)
            choices[choice.name] = choice

        :param key: The key under which to store the
                    :class:`~simplebench.reporters.choice.ChoiceConf` instance.
        :type key: str
        :param value: The :class:`~simplebench.reporters.choice.ChoiceConf` instance to add.
        :type value: :class:`~simplebench.reporters.choice.ChoiceConf`
        :raises SimpleBenchTypeError: If the key is not a string or the value is not a
                                     :class:`~simplebench.reporters.choice.ChoiceConf`
                                     instance.
        :raises SimpleBenchValueError: If a
                                       :class:`~simplebench.reporters.choice.ChoiceConf`
                                       with the same name already exists
                                       in the container; if the key does not match the
                                       ``ChoiceConf.name`` attribute;
                                       or if a
                                       :class:`~simplebench.reporters.choice.ChoiceConf`
                                       with the same flag already exists in the container.
        """
        super().__setitem__(key, value)
