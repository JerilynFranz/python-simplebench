"""Typed dictionaries for the V1 StatsBlock data structure.

This module defines two distinct dictionary types for handling StatsBlock data,
both modeled on the JSON schema for version 1 StatsBlocks in
version 1: :class:`~simplebench.report.versions.v1.stats_block.stats_block_schema.StatsBlockSchema`.

    - `StatsBlockData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, accepting `int` or `float` for the `value` field and making `type` and `version` optional.
    - `StatsBlockDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `value` is a `float` and that `type` and `version` are present.

    These types ensure proper validation and serialization of StatsBlock data
"""
import sys
from typing import Sequence

from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired, Required
else:
    from typing_extensions import NotRequired, Required

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
    :param Required[float] rstdev: The relative standard deviation.
    :param Required[Sequence[str | float]] percentiles: The percentiles data.
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
    rstdev: Required[float]
    percentiles: Required[Sequence[str | float]]

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
    :param Required[float] rstdev: The relative standard deviation.
    :param Required[Sequence[str | float]] percentiles: The percentiles data.
    :param NotRequired[str] description: A description of the statistic.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] cpu_timer: The name of the CPU timer associated with this value.
    """
    description: NotRequired[str]
    timer: NotRequired[str]
    cpu_timer: NotRequired[str]

class StatsBlockData(_AllStatsBlockBase, total=False):
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
    :param NotRequired[str] cpu_timer: The name of the CPU timer associated with this value.
    :param NotRequired[str] description: A description of the statistic.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    type: NotRequired[str]
    version: NotRequired[int]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class StatsBlockDict(_AllStatsBlockBase, total=False):
    """Typed dictionary for the JSON representation of a V1 StatsBlock (OUTPUT).

    This type is strict, requiring `type` and`version`` to be present.
    `value` is guaranteed to be a `float`, `timer` is optional.

    All fields are immutable.

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
    :param Required[Sequence[str | float]] percentiles: The percentiles data.
    :param NotRequired[str] timer: The name of the timer associated with this value.
    :param NotRequired[str] cpu_timer: The name of the CPU timer associated with this value.
    :param NotRequired[str] description: A description of the statistic.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """
    type: Required[str]
    version: Required[int]
