"""Typed dictionaries for the V1 ValueBlock data structure.

This module defines four distinct dictionary types for handling ValueBlock data,
all modeled on the JSON schema for version 1 ValueBlocks in
version 1: :class:`~simplebench.report.versions.v1.ValueBlockSchema`.

    - `ValueBlockData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, accepting `int` or `float` for the `value` field and making `type` and `version` optional.
    - `ImmutableValueBlockData`: An immutable subclass of `ValueBlockData` for
    type-checking purposes.
    - `ValueBlockDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `value` is a `float` and that `type` and `version` are present.
    - `ImmutableValueBlockDict`: An immutable subclass of `ValueBlockDict` for
    type-checking purposes.

    These types ensure proper validation and serialization of ValueBlock data
"""

from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

__all__ = []

# --- For data used as INPUT (e.g., to `from_dict`) ---


class _RequiredValueBlockData(ReportElementTypedDict, total=True):
    """Required fields for V1 ValueBlock data used as INPUT.

    The input type allows `value` to be either `int` or `float`.

    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float | int] value: The numeric value of the block.
    """

    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    value: Required[float | int]


class ValueBlockData(_RequiredValueBlockData, total=False):
    """Typed dictionary for V1 ValueBlock data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `timer` to be
    omitted, and accepting either `int` or `float` for the `value` field.

    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float | int] value: The numeric value of the block.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] cpu_timer: The name of the CPU timer associated with this value.
    """

    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    timer: NotRequired[str]
    cpu_timer: NotRequired[str]


class ImmutableValueBlockData(ValueBlockData, total=False):
    """Immutable typed dictionary for V1 ValueBlock data used as INPUT.

    This type is identical to :class:`ValueBlockData` but is immutable
    (all fields are read-only) for type-checking purposes.
    """

    __immutable__: NotRequired[Never]  # Marker for immutability


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class _RequiredValueBlockDict(ReportElementTypedDict, total=True):
    """Required fields for V1 ValueBlock data used as OUTPUT.

    `value` is guaranteed to be a `float`.

    All fields are required (`total=True`), and their values are immutable.

    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the value block.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float] value: The numeric value of the block (guaranteed to be float).

    """

    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    value: Required[float]  # Guaranteed to be float rather than int | float


class ValueBlockDict(_RequiredValueBlockDict, total=False):
    """Typed dictionary for the JSON representation of a V1 ValueBlock (OUTPUT).

    This type is strict, requiring `type` and`version`` to be present.
    `value` is guaranteed to be a `float`, `timer` is optional.

    All fields are immutable.

    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float] value: The numeric value of the block (guaranteed to be float).
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] cpu_timer: The name of the CPU timer associated with this value.
    """

    timer: NotRequired[str]
    cpu_timer: NotRequired[str]


class ImmutableValueBlockDict(ValueBlockDict, total=False):
    """Immutable version of :class:`ValueBlockDict` (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The ``__immutable__`` field is a class marker to indicate immutability
    for type-checking purposes. It should not be set or used at runtime.

    Because it inherits from `ValueBlockDict`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.
    """

    __immutable__: NotRequired[Never]  # Marker to indicate immutability
