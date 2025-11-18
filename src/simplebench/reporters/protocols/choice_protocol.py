"""Protocols for Choice-like objects."""
# pylint: disable=unnecessary-ellipsis

from typing import Iterable, Protocol, runtime_checkable


@runtime_checkable
class ChoiceProtocol(Protocol):
    """A protocol defining the essential attributes for a Choice-like object.

    This ensures that any object used within a generic
    :class:`~simplebench.reporters.choices.Choices` collection has the necessary ``name``
    and ``flags`` attributes for indexing and management.
    """

    @property
    def name(self) -> str:  # type: ignore[reportReturnType]
        """The unique name of the choice, used as a key.

        :return: The name of the choice.
        :rtype: str
        """
    ...

    @property
    def flags(self) -> Iterable[str]:  # type: ignore[reportReturnType]
        """An iterable of unique string flags (e.g., ``--my-flag``) for the choice.

        :return: An iterable of flags.
        :rtype: ~typing.Iterable[str]
        """
    ...
