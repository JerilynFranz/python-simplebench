"""Typed dictionaries for the V1 MemoryInfo data structure.

This module defines two distinct dictionary types for handling SwapMemery data,
both modeled on the JSON schema for version 1 MemoryInfo in
version 1: :class:`~simplebench.report.versions.v1.MemoryInfoSchema`.

- :class:`SwapMemoryObjectDict`: A mutable typed dictionary for general use.
- :class:`ImmutableSwapMemoryObjectDict`: An immutable typed dictionary variant.
  This type is marked to be treated as immutable by the
  :func:`typechecked.is_immutable` function and recognized as
  a subclass of :class:`~typechecked.Immutable`. by :func:`issubclass` checks.

    These types ensure proper validation and serialization of MemoryInfo data
"""
from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

__all__ = [
    'SwapMemoryObjectDict',
    'ImmutableSwapMemoryObjectDict',
]


class _RequiredSwapMemoryObject(ReportElementTypedDict, total=True):
    """Required fields for V1 SwapMemory data used as INPUT.

    :param Required[int] total: Total swap memory in bytes.
    :param Required[int] used: Used swap memory in bytes.
    """
    total: Required[int]
    used: Required[int]
    free: Required[int]
    percent: Required[float]
    swap_in: Required[int]
    swap_out: Required[int]


class SwapMemoryObjectDict(_RequiredSwapMemoryObject, total=True):
    """Typed dictionary for V1 SwapMemory data used as INPUT or OUTPUT.

    All fields are required (`total=True`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.
    :param Required[int] total: Total swap memory in bytes.
    :param Required[int] used: Used swap memory in bytes.
    :param Required[int] free: Free swap memory in bytes.
    :param Required[float] percent: Percentage of swap memory used.
    :param Required[int] swap_in: Swap memory sent to disk in bytes.
    :param Required[int] swap_out: Swap memory received from disk in bytes.
    """


class ImmutableSwapMemoryObjectDict(_RequiredSwapMemoryObject, total=False):
    """Typed dictionary for V1 SwapMemory data used as INPUT or OUTPUT (Immutable).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`typechecked.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~typechecked.Immutable`.

    Because it inherits from `SwapMemoryData`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[int] total: Total swap memory in bytes.
    :param Required[int] used: Used swap memory in bytes.
    :param Required[int] free: Free swap memory in bytes.
    :param Required[float] percent: Percentage of swap memory used.
    :param Required[int] swap_in: Swap memory sent to disk in bytes.
    :param Required[int] swap_out: Swap memory received from disk in bytes.
    """
    __immutable__: NotRequired[Never]
