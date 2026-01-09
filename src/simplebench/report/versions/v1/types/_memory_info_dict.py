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
from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

__all__ = [
    'SwapMemoryObjectDict',
    'ImmutableSwapMemoryObjectDict',
    'VirtualMemoryObjectDict',
    'ImmutableVirtualMemoryObjectDict',
    'MemoryInfoData',
    'ImmutableMemoryInfoData',
    'MemoryInfoDict',
    'ImmutableMemoryInfoDict',
]

# --- For data used as INPUT (e.g., to `from_dict`) ---

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


class _RequiredVirtualMemoryObject(ReportElementTypedDict, total=True):
    """Typed dictionary for V1 VirtualMemory data used as INPUT.

    All fields are required (`total=True`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.
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
    """Typed dictionary for V1 VirtualMemory data used as INPUT or OUTPUT.

    All fields are required (`total=True`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.
    :param Required[int] total: Total virtual memory in bytes.
    :param Required[int] available: Available virtual memory in bytes.
    :param Required[float] percent: Percentage of virtual memory used.
    :param Required[int] used: Used virtual memory in bytes.
    :param Required[int] free: Free virtual memory in bytes.
    """


class ImmutableVirtualMemoryObjectDict(_RequiredVirtualMemoryObject, total=False):
    """Typed dictionary for V1 VirtualMemory data used as INPUT or OUTPUT (Immutable).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`typechecked.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~typechecked.Immutable`.

    Because it inherits from `VirtualMemoryData`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[int] total: Total virtual memory in bytes.
    :param Required[int] available: Available virtual memory in bytes.
    :param Required[float] percent: Percentage of virtual memory used.
    :param Required[int] used: Used virtual memory in bytes.
    :param Required[int] free: Free virtual memory in bytes.
    """
    __immutable__: NotRequired[Never]


class _RequiredMemoryInfo(ReportElementTypedDict, total=True):
    """Required fields for V1 MemoryInfo data used as INPUT.

    :param Required[int] total_available: Total physical memory in bytes.
    :param Required[int] total_swap: Total configured swap memory in bytes.
    """
    swap_memory: Required[SwapMemoryObjectDict]
    virtual_memory: Required[VirtualMemoryObjectDict]

class MemoryInfoData(_RequiredMemoryInfo, total=False):
    """Typed dictionary for V1 MemoryInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.

    :param Required[SwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[VirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the memory information.
        """
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]

class ImmutableMemoryInfoData(_RequiredMemoryInfo, total=False):
    """Typed dictionary for V1 MemoryInfo data used as INPUT (Immutable).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`typechecked.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~typechecked.Immutable`.

    Because it inherits from `MemoryInfoData`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[SwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[VirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the memory information.
    """
    __immutable__: NotRequired[Never]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredMemoryInfoDict(ReportElementTypedDict, total=True):
    """Required fields for V1 MemoryInfo data used as OUTPUT.

    All fields are required (`total=True`), and their values are immutable types.
    
    :param Required[int] total_available: Total available physical memory in bytes.
    :param Required[int] total_swap: Total configured swap memory in bytes.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the memory information.
    """
    total_available: Required[int]
    total_swap: Required[int]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]

class MemoryInfoDict(_RequiredMemoryInfoDict, total=True):
    """Typed dictionary for the JSON representation of a V1 MemoryInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, `node`, and `hash_id` to be
    present

    All fields are required (`total=True`), and their types are immutable.

    The type asserts to type checkers that all required fields are present and
    that all fields are of the correct immutable types, but cannot enforce
    immutability of the instance itself (Python limitation).

    :param Required[int] total_available: Total physical memory in bytes.
    :param Required[int] total_swap: Total configured swap memory in bytes.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the memory information.
    """

class ImmutableMemoryInfoDict(_RequiredMemoryInfoDict, total=False):
    """Typed dictionary for the JSON representation of a V1 MemoryInfo (OUTPUT, Immutable).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`typechecked.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~typechecked.Immutable`.

    Because it inherits from `MemoryInfoDict`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[int] total_available: Total physical memory in bytes.
    :param Required[int] total_swap: Total configured swap memory in bytes.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the memory information.
    """
    __immutable__: NotRequired[Never]
