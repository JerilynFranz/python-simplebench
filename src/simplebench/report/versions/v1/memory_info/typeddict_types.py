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

from .swap_memory import ImmutableSwapMemoryObjectDict, SwapMemoryObjectDict
from .virtual_memory import ImmutableVirtualMemoryObjectDict, VirtualMemoryObjectDict

__all__ = []


class _RequiredMemoryInfo(ReportElementTypedDict, total=True):
    """Base required fields for V1 MemoryInfo TypedDict data.

    :param Required[SwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[VirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    """

    swap_memory: Required[SwapMemoryObjectDict]
    virtual_memory: Required[VirtualMemoryObjectDict]


class MemoryInfoData(_RequiredMemoryInfo, total=False):
    """Typed dictionary for V1 MemoryInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).

    The optional fields allow for more lenient input validation when constructing
    a MemoryInfo from external data sources since these fields can be
    programmatically inferred or assigned later.

    :param Required[SwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[VirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the memory information.
    """

    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]


class _RequiredImmutableMemoryInfo(ReportElementTypedDict, total=True):
    """Base required fields for V1 MemoryInfo TypedDict for immutable data.

    :param Required[ImmutableSwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[ImmutableVirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    """

    swap_memory: Required[ImmutableSwapMemoryObjectDict]
    virtual_memory: Required[ImmutableVirtualMemoryObjectDict]


class ImmutableMemoryInfoData(_RequiredImmutableMemoryInfo, total=False):
    """Typed dictionary for V1 MemoryInfo data used as INPUT (Immutable).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`typechecked.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~typechecked.Immutable`.

    Because it inherits from `MemoryInfoData`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[ImmutableSwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[ImmutableVirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the memory information.
    """

    __immutable__: NotRequired[Never]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class MemoryInfoDict(_RequiredMemoryInfo, total=True):
    """Typed dictionary for the JSON representation of a V1 MemoryInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, `node`, and `hash_id` to be
    present. It is used for output serialization and so strictly defines the expected
    structure of the MemoryInfo data.

    All fields are required (`total=True`), and their types are immutable.

    The type asserts to type checkers that all required fields are present and
    that all fields are of the correct immutable types, but cannot enforce
    immutability of the instance itself (Python limitation).

    :param Required[SwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[VirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the memory information.
    """

    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableMemoryInfoDict(MemoryInfoDict, total=False):
    """Typed dictionary for the JSON representation of a V1 MemoryInfo (OUTPUT, Immutable).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    Because it inherits from :class:`MemoryInfoDict`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[ImmutableSwapMemoryObjectDict] swap_memory: Swap memory object.
    :param Required[ImmutableVirtualMemoryObjectDict] virtual_memory: Virtual memory object.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the memory information.
    """

    __immutable__: NotRequired[Never]
