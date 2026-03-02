"""Typed dictionaries for the V1 SystemInfo data structure.

This module defines four distinct dictionary types for handling SystemInfo data,
both modeled on the JSON schema for version 1 SystemInfo in
version 1: :class:`~simplebench.report.versions.v1.SystemInfoSchema`.

    - `SystemInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `ImmutableSystemInfoData`: An immutable variant of `SystemInfoData` for use
    as INPUT. It serves as a marker for type-checking to indicate immutability.
    - `SystemInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
    - `ImmutableSystemInfoDict`: An immutable variant of `SystemInfoDict` for use
    as OUTPUT. It serves as a marker for type-checking to indicate immutability.

    These types ensure proper validation and serialization of SystemInfo data
"""

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

__all__: list[str] = []

# --- For data used as INPUT (e.g., to `from_dict`) ---

class SystemInfoData(ReportElementTypedDict):
    """Typed dictionary for V1 SystemInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the system information.
    """
    system: Required[str]
    system_version: Required[str]
    release: Required[str]
    machine: Required[str]
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]


class ImmutableSystemInfoData(ReportElementTypedDict):
    """Immutable version of :class:`SystemInfoData` (INPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the system information.

    The `__immutable__` attribute serves as a class marker for type-checking
    to indicate that instances of this type should be treated as immutable
    and should never be given an actual value.
    """
    system: Required[str]
    system_version: Required[str]
    release: Required[str]
    machine: Required[str]
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]

    __immutable__: NotRequired[Never]  # Marker to indicate immutability

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class SystemInfoDict(ReportElementTypedDict):
    """Typed dictionary for the JSON representation of a V1 SystemInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, and `hash_id` to be
    present to strictly conform with the JSON schema and for output serialization.

    The type asserts to type checkers that all required fields are present and
    that all fields are of the correct immutable types, but cannot enforce
    immutability of the instance itself (Python limitation).

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the system information.
    """
    system: Required[str]
    system_version: Required[str]
    release: Required[str]
    machine: Required[str]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableSystemInfoDict(ReportElementTypedDict):
    """Immutable typed dictionary for the JSON representation of a V1 SystemInfo (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    Because it inherits from `SystemInfoDict`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the system information.
    """
    system: Required[str]
    system_version: Required[str]
    release: Required[str]
    machine: Required[str]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability
