"""Typed dictionaries for the V1 RawDataBlock data structure.

This module defines four distinct dictionary types for handling RawDataBlock data,
all modeled on the JSON schema for version 1 RawDataBlocks in
version 1: :class:`~simplebench.report.versions.v1.RawDataBlockSchema`.

    - `RawDataBlockData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, accepting `int` or `float` for the `value` field and making `type` and `version` optional.
    - `ImmutableRawDataBlockData`: An immutable version of `RawDataBlockData`.
    - `RawDataBlockDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `data` is a sequence of `float` values and that
    `type`, `version` and `hash_id` are present.
    - `ImmutableRawDataBlockDict`: An immutable version of `RawDataBlockDict`.

    These types ensure proper validation and serialization of RawDataBlock data
"""

from collections.abc import Sequence

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

__all__: list[str] = []

# --- For data used as INPUT (e.g., to `from_dict`) ---


class _RequiredRawDataBlockData(ReportElementTypedDict, total=True):
    """Required fields for V1 RawDataBlock data used as INPUT.

    The input type allows `value` to be either `int` or `float`.

    :param Required[str] name: The name of the values.
    :param Required[str] semantic_type: The semantic type of the values.
    :param Required[str] unit: The unit for the values.
    :param Required[float] scale: The scaling factor for the values.
    """

    name: Required[str]
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    rounds: Required[int]
    data: Required[Sequence[float | int]]


class RawDataBlockData(_RequiredRawDataBlockData, total=False):
    """Typed dictionary for V1 RawDataBlock data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `timer` to be
    omitted, and accepting either `int` or `float` for the `value` field.

    :param Required[str] name: The name of the values.
    :param Required[str] semantic_type: The semantic type of the values.
    :param Required[str] unit: The unit for the values.
    :param Required[float] scale: The scaling factor for the values.
    :param Required[int] rounds: The number of rounds each data point represents.
    :param Required[Sequence[float | int]] data: The numeric data values.
    :param NotRequired[str] description: The description of the value.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The hash identifier for the block.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    """

    description: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]
    timer: NotRequired[str]


class _RequiredImmutableRawDataBlockData(ReportElementTypedDict, total=True):
    """Immutable typed dictionary for V1 RawDataBlock data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `timer` to be
    omitted, and accepting either `int` or `float` for the `value` field.

    All fields are immutable.

    :param Required[str] name: The name of the values.
    :param Required[str] semantic_type: The semantic type of the values.
    :param Required[str] unit: The unit for the values.
    :param Required[float] scale: The scaling factor for the values.
    :param Required[int] rounds: The number of rounds each data point represents.
    :param Required[tuple[float | int, ...] data: The numeric data values.
    """

    name: Required[str]
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    rounds: Required[int]
    data: Required[tuple[float | int, ...]]


class ImmutableRawDataBlockData(_RequiredImmutableRawDataBlockData, total=False):
    """Immutable typed dictionary for V1 RawDataBlock data used as INPUT.

    The ``__immutable__`` marker identifies this as an immutable dictionary type.
    It is a class-level marker and does not correspond to any actual data field.
    It should never be set or included in instances of this type.

    .. note::
        Because this is an immutable type and the regular TypedDict constructor
        does not support immutability, this type must be instantiated using
        :func:`typing.cast` on a :class:`types.MappingProxyType` instance or
        similar methods to ensure immutability is respected at runtime.

    All fields are immutable.

    :param Required[str] name: The name of the values.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] rounds: The number of rounds each data point represents.
    :param Required[tuple[float | int, ...] data: The numeric data values.
    :param NotRequired[str] description: The description of the value.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The hash identifier for the block.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    """

    description: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]
    timer: NotRequired[str]
    __immutable__: NotRequired[Never]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class _RequiredRawDataBlock(ReportElementTypedDict, total=True):
    """Required fields for V1 RawDataBlock data used as OUTPUT.

    It requires that `type`, `version`, and `hash_id` are present.

    It is stricter than the input type.

    :param Required[str] name: The name of the values.
    :param Required[str] semantic_type: The semantic type of the values.
    :param Required[str] unit: The unit for the values.
    :param Required[float] scale: The scaling factor for the values.
    :param Required[int] rounds: The number of rounds each data point represents.
    :param Required[Sequence[float, ...]] data: The numeric data values.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash identifier for the block.
    """

    name: Required[str]
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    rounds: Required[int]
    data: Required[tuple[float, ...]]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class RawDataBlockDict(_RequiredRawDataBlock, total=False):
    """Typed dictionary for the JSON representation of a V1 RawDataBlock (OUTPUT).

    This type is strict, requiring `type` and`version` to be present.
    `value` is guaranteed to be a `float`, `timer` is optional.

    All fields are immutable.

    :param Required[str] name: The name of the value.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] rounds: The number of rounds each data point represents.
    :param Required[tuple[float, ...]] data: The numeric data values.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash identifier for the block.
    :param NotRequired[str] description: The description of the value.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    """

    description: NotRequired[str]
    timer: NotRequired[str]


class _RequiredImmutableRawDataBlockDict(ReportElementTypedDict, total=True):
    """Required fields for V1 RawDataBlock data used as OUTPUT.

    It requires that `type`, `version`, and `hash_id` are present and that
    `data` be a :class:`tuple` of :class:`float` values. It is stricter
    than the input type.

    All fields are immutable.

    :param Required[str] name: The name of the values.
    :param Required[str] semantic_type: The semantic type of the values.
    :param Required[str] unit: The unit for the values.
    :param Required[float] scale: The scaling factor for the values.
    :param Required[int] rounds: The number of rounds each data point represents.
    :param Required[tuple[float, ...]] data: The numeric data values.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash identifier for the block.
    """

    name: Required[str]
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    rounds: Required[int]
    data: Required[tuple[float, ...]]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableRawDataBlockDict(_RequiredImmutableRawDataBlockData, total=False):
    """Optional fields for V1 ImmutableRawDataBlock data used as OUTPUT.

    The ``__immutable__`` marker identifies this as an immutable dictionary type.
    It is a class-level marker and does not correspond to any actual data field.
    It should never be set or included in instances of this type.

    .. note::
        Because this is an immutable type and the regular TypedDict constructor
        does not support immutability, this type must be instantiated using
        :func:`typing.cast` on a :class:`types.MappingProxyType` instance or
        similar methods to ensure immutability is respected at runtime.

    All fields are immutable.

    :param Required[str] name: The name of the value.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] rounds: The number of rounds each data point represents.
    :param Required[tuple[float | int, ...] data: The numeric data values.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash identifier for the block.
    :param NotRequired[str] description: The description of the value.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    """

    description: NotRequired[str]
    timer: NotRequired[str]
    __immutable__: NotRequired[Never]
