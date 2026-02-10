"""Typed dictionaries for the V1 CPUInfo data structure.

This module defines four distinct dictionary types for handling CPUInfo data,
both modeled on the JSON schema for version 1 CPUInfo in
version 1: :class:`~simplebench.report.versions.v1.CPUInfoSchema`.

- `CPUInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
lenient, making `type`, `version`, and `hash_id` optional.
- `ImmutableCPUInfoData`: An immutable subclass of `CPUInfoData` for
type-checking purposes.
- `CPUInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
- `ImmutableCPUInfoDict`: An immutable subclass of `CPUInfoDict` for
type-checking purposes.

These types ensure proper validation and serialization of CPUInfo data
"""

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.simplebench_types import (
    CoreDataMapping,
    CoreDataMappingType,
    CoreDataTypes,  # noqa: F401  # Load bearing import for type annotations
    Never,
    NotRequired,
    Required,
)

__all__ = ['CPUInfoData', 'CPUInfoDict', 'ImmutableCPUInfoData', 'ImmutableCPUInfoDict']

# --- For data used as INPUT (e.g., to `from_dict`) ---

class CPUInfoData(ReportElementTypedDict):
    """Typed dictionary for V1 CPUInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).

    :param Required[CoreDataMappingType] data: The CPU information data.
    :param NotRequired[str] hash_id: The unique hash identifier for the CPU information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    data: Required[CoreDataMappingType]
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]


class ImmutableCPUInfoData(ReportElementTypedDict):
    """Immutable typed dictionary for V1 CPUInfo data used as INPUT.

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`~simplebench.simplebench_types.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~simplebench.simplebench_types.Immutable`.

    :param Required[CoreDataMapping] data: The CPU information data.
    :param NotRequired[str] hash_id: The unique hash identifier for the CPU information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    data: Required[CoreDataMapping]
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    __immutable__: NotRequired[Never]  # Class marker to indicate immutability

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class CPUInfoDict(ReportElementTypedDict):
    """Typed dictionary for the JSON representation of a V1 CPUInfo (OUTPUT).

    :param Required[CoreDataMappingType] data: The CPU information data.
    :param Required[str] hash_id: The unique hash identifier for the CPU information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """
    data: Required[CoreDataMappingType]
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]


class ImmutableCPUInfoDict(ReportElementTypedDict):
    """Immutable typed dictionary for the JSON representation of a V1 CPUInfo (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    It is a stricter version of `CPUInfoDict` that guarantees the
    presence of `type`, `version`, and `hash_id` and requires
    `data` to be a `CoreDataMapping` (not just a `CoreDataMappingType`).

    The :func:`~simplebench.simplebench_types.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~simplebench.simplebench_types.Immutable`.

    :param Required[CoreDataMapping] data: The CPU information data.
    :param Required[str] hash_id: The unique hash identifier for the CPU information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """
    data: Required[CoreDataMapping]
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability
