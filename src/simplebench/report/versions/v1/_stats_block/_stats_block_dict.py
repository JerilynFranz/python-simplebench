"""Typed dictionaries for the V1 StatsBlock data structure.

This module defines four distinct dictionary types for handling StatsBlock data,
all modeled on the JSON schema for version 1 StatsBlocks in
version 1: :class:`~simplebench.report.versions.v1.StatsBlockSchema`.

    - :class:`StatsBlockData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, accepting `int` or `float` for the `value` field and making `type` and `version` optional.
    - :class:`ImmutableStatsBlockData`: An immutable variation of :class:`StatsBlockData` for
    type-checking purposes.
    - :class:`StatsBlockDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `value` is a `float` and that `type` and `version` are present.
    - :class:`ImmutableStatsBlockDict`: An immutable variation of :class:`StatsBlockDict` for
    type-checking purposes.

    These types ensure proper validation and serialization of StatsBlock data
"""

from typing import Sequence

from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

__all__ = []

# --- For data used as INPUT (e.g., to `from_dict`) ---


class _RequiredStatsBlockBase(ReportElementTypedDict, total=True):
    """Required base fields for V1 StatsBlock

    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] relative_stdev: The relative standard deviation.
    """

    name: Required[str]
    semantic_type: Required[str]
    unit: Required[str]
    scale: Required[float]
    iterations: Required[int]
    rounds: Required[int]
    mean: Required[float]
    median: Required[float]
    minimum: Required[float]
    maximum: Required[float]
    stdev: Required[float]
    relative_stdev: Required[float]


class _AllStatsBlockBase(_RequiredStatsBlockBase, total=False):
    """All base fields for V1 StatsBlock data.

    This adds the optional base fields to the required base fields.

    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] relative_stdev: The relative standard deviation.
    :param NotRequired[str] description: A description of the statistic.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    """

    description: NotRequired[str]
    timer: NotRequired[str]


class _StatsBlockData(_AllStatsBlockBase, total=False):
    """Typed dictionary for V1 StatsBlock data used as INPUT.

    This type is lenient, allowing `type` and `version` to be omitted
    because the system can often infer them contextually.

    i.e. if calling a 'v1' schema's `from_dict`, it can assume `version=1`
    if not provided and the type can be inferred from the connected schema
    for the parent object.

    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] rstdev: The relative standard deviation.
    :param Required[Sequence[str | float]] percentiles: The percentiles data.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] description: A description of the statistic.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The hash ID of the block (64-character hex string).
    """

    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]


class StatsBlockData(_StatsBlockData, total=True):
    """Typed dictionary for V1 StatsBlock data used as INPUT (lenient).

    This type is lenient, allowing `type` and `version` to be omitted
    because the system can often infer them contextually.

    i.e. if calling a 'v1' schema's `from_dict`, it can assume `version=1`
    if not provided and the type can be inferred from the connected schema
    for the parent object.

    percentiles is defined here as `Sequence[float]` to allow
    both mutable and immutable sequences, but only of floats.

    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash ID of the block (64-character hex string).
    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] relative_stdev: The relative standard deviation.
    :param Required[Sequence[float]] percentiles: The percentiles data.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] description: A description of the statistic.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    percentiles: Required[Sequence[float]]


class _StatsBlockDict(_AllStatsBlockBase, total=True):
    """Typed dictionary for V1 StatsBlock data used as OUTPUT.

    This type is strict, required `type`, `version`, and `hash_id` to be present.
    All fields are immutable.

    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash ID of the block (64-character hex string).
    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] rstdev: The relative standard deviation.
    :param Required[tuple[float, ...]] percentiles: The percentiles data (101-item tuple).
    """

    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    percentiles: Required[tuple[float, ...]]


class _ImmutableStatsBlockDataWithImmutablePercentiles(_StatsBlockData, total=True):
    """Immutable typed dictionary for V1 StatsBlock data used as INPUT (lenient).

    This type is lenient, allowing `type` and `version` to be omitted
    because the system can often infer them contextually.

    i.e. if calling a 'v1' schema's `from_dict`, it can assume `version=1`
    if not provided and the type can be inferred from the connected schema
    for the parent object.

    All fields are immutable.

    percentiles is defined here as `tuple[float, ...]` to allow
    only an immutable sequences of floats.
    """

    percentiles: Required[tuple[float, ...]]


class ImmutableStatsBlockData(_StatsBlockData, total=False):
    """Immutable typed dictionary for V1 StatsBlock data used as INPUT (lenient).

    This type is lenient, allowing `type` and `version` to be omitted
    because the system can often infer them contextually.

    i.e. if calling a 'v1' schema's `from_dict`, it can assume `version=1`
    if not provided and the type can be inferred from the connected schema
    for the parent object.

    All fields are immutable.

    percentiles is defined here as `tuple[float, ...]` to allow
    only an immutable sequences of floats.

    ``__immutable__`` is defined as a class variable to mark the entire
    dictionary as immutable for type-checking purposes. It is not
    intended to be used at runtime and should never be set on instances.

    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] relative_stdev: The relative standard deviation.
    :param Required[tuple[float, ...]] percentiles: The percentiles data.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] description: A description of the statistic.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    __immutable__: NotRequired[Never]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class StatsBlockDict(_AllStatsBlockBase, total=True):
    """Typed dictionary for the JSON representation of a V1 StatsBlock (OUTPUT).

    This type is strict, requiring `type`, `version`, `hash_id` to be present.

    All fields are immutable.

    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash ID of the block (64-character hex string).
    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] relative_stdev: The relative standard deviation.
    :param Required[Sequence[float]] percentiles: The percentiles data (101 values).
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] description: A description of the statistic.

    """

    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    percentiles: Required[Sequence[float]]


class _ImmutableStatsBlockDictBase(_AllStatsBlockBase, total=True):
    """Immutable typed dictionary for the JSON representation of a V1 StatsBlock (OUTPUT).

    This type is strict, requiring `type`, `version`, `hash_id` to be present.

    All fields are immutable.

    percentiles is defined here as `tuple[float, ...]` to allow
    only an immutable sequences of floats.
    """

    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    percentiles: Required[tuple[float, ...]]


class ImmutableStatsBlockDict(_ImmutableStatsBlockDictBase, total=False):
    """Immutable typed dictionary for the JSON representation of a V1 StatsBlock (OUTPUT).

    This type is strict, requiring `type`, `version`, `hash_id` to be present.

    All fields are immutable.

    percentiles is defined here as `tuple[float, ...]` to allow
    only an immutable sequences of floats.

    ``__immutable__`` is defined as a class variable to mark the entire
    dictionary as immutable for type-checking purposes. It is not
    intended to be used at runtime and should never be set on instances.

    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The hash ID of the block (64-character hex string).
    :param Required[str] name: The name of the statistic.
    :param Required[str] semantic_type: The semantic type of the value.
    :param Required[str] unit: The unit of the value.
    :param Required[float] scale: The scaling factor for the value.
    :param Required[int] iterations: The number of iterations.
    :param Required[int] rounds: The number of rounds.
    :param Required[float] mean: The mean value.
    :param Required[float] median: The median value.
    :param Required[float] minimum: The minimum value.
    :param Required[float] maximum: The maximum value.
    :param Required[float] stdev: The standard deviation.
    :param Required[float] relative_stdev: The relative standard deviation.
    :param Required[tuple[float, ...]] percentiles: The percentiles data.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] description: A description of the statistic.
    """

    __immutable__: NotRequired[Never]
