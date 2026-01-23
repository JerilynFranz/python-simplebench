"""Typed dictionaries for the V1 MemoryInfo data structure.

This module defines three distinct dictionary types for handling MemoryInfo data,
all modeled on the JSON schema for version 1 MemoryInfo in
version 1: :class:`~simplebench.report.versions.v1.MemoryInfoSchema`.

    - `MemoryInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `MemoryInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
    - `ImmutableMemoryInfoDict`: An immutable subclass of `MemoryInfoDict` for
    type-checking purposes.

    These types ensure proper validation and serialization of MemoryInfo data
"""

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

__all__ = []


class _RequiredVirtualMemoryObject(ReportElementTypedDict, total=True):
    """Base typed dictionary for V1 VirtualMemory data.

    All fields are required.

    :param Required[int] total: Total virtual memory in bytes.
    :param Required[int] available: Available virtual memory in bytes.
    :param Required[float] percent: Percentage of virtual memory used.
    :param Required[int] used: Used virtual memory in bytes.
    :param Required[int] free: Free virtual memory in bytes.
    """

    total: Required[int]
    available: Required[int]
    percent: Required[float]
    used: Required[int]
    free: Required[int]


class VirtualMemoryObjectDict(_RequiredVirtualMemoryObject, total=True):
    """Typed dictionary for V1 VirtualMemory data used as either INPUT or OUTPUT.

    Because it is a sub-object of :class:`~simplebench.report.versions.v1.MemoryInfo`,
    all fields are required and it does not have 'type', 'version', or 'hash_id' fields.

    :param Required[int] total: Total virtual memory in bytes.
    :param Required[int] available: Available virtual memory in bytes.
    :param Required[float] percent: Percentage of virtual memory used.
    :param Required[int] used: Used virtual memory in bytes.
    :param Required[int] free: Free virtual memory in bytes.
    """


class ImmutableVirtualMemoryObjectDict(_RequiredVirtualMemoryObject, total=False):
    """Typed dictionary for V1 VirtualMemory data used as INPUT or OUTPUT (Immutable).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability
    (e.g., using :class:`types.MappingProxyType` and casting to
    :class:`ImmutableVirtualMemoryObjectDict`).

    Because it directly inherits from :class:`VirtualMemoryObjectDict`, all fields are
    the same and it can be used interchangeably where immutability is not a concern.

    A TypedDict is marked as immutable in SimpleBench for type-checking purposes by defining
    an `__immutable__` attribute with a type of `NotRequired[Never]`.

    :param Required[int] total: Total virtual memory in bytes.
    :param Required[int] available: Available virtual memory in bytes.
    :param Required[float] percent: Percentage of virtual memory used.
    :param Required[int] used: Used virtual memory in bytes.
    :param Required[int] free: Free virtual memory in bytes.
    """

    __immutable__: NotRequired[Never]
