"""Protocols for thawable objects."""
# ruff: noqa: E501

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from simplebench.simplebench_types import CoreDataMapping, CoreDataTypes


class Thawable(Protocol):

    def thaw(self) -> 'dict[str, CoreDataTypes] | CoreDataMapping | list[CoreDataTypes] | tuple[CoreDataTypes, ...] | set[str | int | float | bool | frozenset | tuple | None | CoreDataMapping]':
        """Get the thawed (mutable) dictionary representation of this object.

        This returns a dictionary representation of this object that is mutable
        to the maximum extent possible. The returned dictionary is a deep copy
        of the internal data of this object, so modifying the returned dictionary
        will not affect the original object.

        This can be an expensive operation for large objects, so it should be used with care.

        :return: The thawed (mutable) dictionary representation.
        :rtype: dict[str, CoreDataTypes] | CoreDataMapping
        """
        ...
