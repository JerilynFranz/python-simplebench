"""Typed dictionaries for the V1 ValueBlock data structure.

This module defines four distinct dictionary types for handling ValueBlock data,
all modeled on the JSON schema for version 1 ValueBlocks in
version 1: :class:`~simplebench.report.versions.v1.ValueBlockSchema`.

    - :class:`ValueBlockData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, accepting `int` or `float` for the `value` field and making `hash_id`, `type` and `version` optional.
    - :class:`ImmutableValueBlockData`: An immutable subclass of `ValueBlockData` for
    type-checking purposes.
    - :class:`ValueBlockDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `value` is a `float` and that `hash_id`, `type` and `version` are present.
    - :class:`ImmutableValueBlockDict`: An immutable subclass of `ValueBlockDict` for
    type-checking purposes.

    These types ensure proper validation and serialization of ValueBlock data
"""

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

__all__: list[str] = []

# --- For data used as INPUT (e.g., to `from_dict`) ---

class ValueBlockData(ReportElementTypedDict):
    """Typed dictionary for V1 ValueBlock data used as INPUT.

    This type is lenient, allowing `hash_id`, `type`, `version`, and `timer` to be
    omitted, and accepting either `int` or `float` for the `value` field.

    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float | int] value: The numeric value of the block.
    :param NotRequired[str] hash_id: The unique hash identifier for the value block.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    """
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    value: Required[float | int]  # Allow int or float for input
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    timer: NotRequired[str]


class ImmutableValueBlockData(ReportElementTypedDict):
    """Immutable typed dictionary for V1 ValueBlock data used as INPUT.

    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float | int] value: The numeric value of the block.
    :param NotRequired[str] hash_id: The unique hash identifier for the value block.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    This type is identical to :class:`ValueBlockData` but is immutable
    (all fields are read-only) for type-checking purposes.
    """
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    value: Required[float | int]  # Allow int or float for input
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    timer: NotRequired[str]
    __immutable__: NotRequired[Never]  # Marker for immutability

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class ValueBlockDict(ReportElementTypedDict):
    """Typed dictionary for the JSON representation of a V1 ValueBlock (OUTPUT).

    This type is strict, requiring `hash_id`, `type` and`version` to be present.
    `value` is guaranteed to be a `float`, `timer` is optional.

    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float] value: The numeric value of the block (guaranteed to be float).
    :param Required[str] hash_id: The unique hash identifier for the value block.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    """
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    value: Required[float]  # Guaranteed to be float rather than int | float
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    timer: NotRequired[str]


class ImmutableValueBlockDict(ReportElementTypedDict):
    """Immutable version of :class:`ValueBlockDict` (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[float] value: The numeric value of the block (guaranteed to be float).
    :param Required[str] hash_id: The unique hash identifier for the value block.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param NotRequired[str] timer: The name of the timer associated with this value.

    The ``__immutable__`` field is a class marker to indicate immutability
    for type-checking purposes. It should not be set or used at runtime.
    """
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    value: Required[float]  # Guaranteed to be float rather than int | float
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    timer: NotRequired[str]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability
