"""Typed dictionaries for the V1 ResultsInfo data structure.

This module defines four distinct dictionary types for handling ResultsInfo data,
all modeled on the JSON schema for version 1 ResultsInfo in
version 1: :class:`~simplebench.report.versions.v1.ResultsInfoSchema`.

    - :class:`ResultsInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - :class:`ImmutableResultsInfoData`: An immutable version of `ResultsInfoData`.
    - :class:`ResultsInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
    - :class:`ImmutableResultsInfoDict`: An immutable version of `ResultsInfoDict`.

    These types ensure proper validation and serialization of ResultsInfo data
"""

from simplebench.report.base import ReportElementTypedDict
from simplebench.simplebench_types import (
    CoreDataMappingType,
    ImmutableCoreDataMappingType,
    Never,
    NotRequired,
    Required,
    VariationMarks,
)

from ..metrics_object import MetricsObjectDict

__all__: list[str] = []

# --- For data used as INPUT (e.g., to `from_dict`) ---


class _RequiredResultsInfoData(ReportElementTypedDict, total=True):
    """Required fields for V1 ResultsInfoData data.

    :param Required[str] semantic_type: The semantic type of the results.
    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[VariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectDict] metrics: The metrics object data.
    :param Required[extra_info: CoreDataMappingType] extra_info: Additional information.
    """

    semantic_type: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    n: Required[float]
    variation_marks: Required[VariationMarks]
    metrics: Required[MetricsObjectDict]
    extra_info: Required[CoreDataMappingType]


class _ImmutableRequiredResultsInfoData(ReportElementTypedDict, total=True):
    """Required fields for Immutable V1 ResultsInfoData data.

    :param Required[str] semantic_type: The semantic type of the results.
    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[ImmutableVariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectDict] metrics: The metrics object data.
    :param Required[extra_info: ImmutableCoreDataMappingType] extra_info: Additional information.
    """

    semantic_type: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    n: Required[float]
    variation_marks: Required[VariationMarks]
    metrics: Required[MetricsObjectDict]
    extra_info: Required[ImmutableCoreDataMappingType]


class ResultsInfoData(_RequiredResultsInfoData, total=False):
    """Typed dictionary for V1 ResultsInfo data used as INPUT.

    All fields except `type`, `version`, `hash_id`, and `extra_info`
    are required (`total=False`).

    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[VariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectData] metrics: The metrics object data.
    :param NotRequired[CoreDataMappingType] extra_info: Additional information.
    :param NotRequired[str] hash_id: The unique hash identifier for the Results information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]


class ImmutableResultsInfoData(_ImmutableRequiredResultsInfoData, total=False):
    """Typed dictionary for Immutable V1 ResultsInfo data used as INPUT.

    All fields except `type`, `version`, `hash_id`are required (`total=False`).

    `__immutable__` is a class-level marker to signal immutability. It is
    typed as `NotRequired[Never]` so that it cannot be set on instances and
    should never appear in runtime data.

    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[ImmutableVariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectData] metrics: The metrics object data.
    :param NotRequired[str] hash_id: The unique hash identifier for the Results information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    __immutable__: NotRequired[Never]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class ResultsInfoDict(ReportElementTypedDict, total=True):
    """Required fields for V1 ResultsInfoDict OUTPUT data.

    :param Required[str] semantic_type: The semantic type of the results.
    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[VariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectDict] metrics: The metrics object data.
    :param Required[CoreDataMappingType] extra_info: Additional information.
    :param Required[str] hash_id: The unique hash identifier for the Results information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """

    semantic_type: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    n: Required[float]
    variation_marks: Required[VariationMarks]
    metrics: Required[MetricsObjectDict]
    extra_info: Required[CoreDataMappingType]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class _ImmutableRequiredResultsInfoDict(ReportElementTypedDict, total=True):
    """Required fields for Immutable V1 ResultsInfoDict OUTPUTdata.

    :param Required[str] semantic_type: The semantic type of the results.
    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[ImmutableVariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectDict] metrics: The metrics object data.
    :param Required[ImmutableCoreDataMappingType] extra_info: Additional information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the Results information.
    """

    semantic_type: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    n: Required[float]
    variation_marks: Required[VariationMarks]
    metrics: Required[MetricsObjectDict]
    extra_info: Required[ImmutableCoreDataMappingType]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableResultsInfoDict(_ImmutableRequiredResultsInfoDict, total=False):
    """Immutable Typed dictionary for the JSON representation of a V1 ResultsInfo (OUTPUT).

    :param Required[str] semantic_type: The semantic type of the results.
    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[VariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectDict] metrics: The metrics object data.
    :param Required[ImmutableCoreDataMappingType] extra_info: Additional information.
    :param Required[str] hash_id: The unique hash identifier for the Results information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[ImmutableCoreDataMappingType] extra_info: Additional information.

    """

    __immutable__: NotRequired[Never]
