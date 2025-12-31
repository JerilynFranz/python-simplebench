"""Typed dictionaries for the V1 ResultsInfo data structure.

This module defines two distinct dictionary types for handling ResultsInfo data,
both modeled on the JSON schema for version 1 ResultsInfo in
version 1: :class:`~simplebench.report.versions.v1.results_info.results_info_schema.ResultsInfoSchema`.

    - `ResultsInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `ResultsInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.

    These types ensure proper validation and serialization of ResultsInfo data
"""
import sys

from simplebench.report.base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import (
    CoreDataMappingType,
    ImmutableCoreDataMappingType,
    ImmutableVariationMarksType,
    VariationMarksType,
)

from .metrics_object_dict import MetricsObjectDict

if sys.version_info >= (3, 11):
    from typing import NotRequired, Required
else:
    from typing_extensions import NotRequired, Required

# -- Common base for both INPUT and OUTPUT --

class _ResultsInfoBase(ReportElementTypedDict, total=True):
    """Base fields for V1 ResultsInfo data.

    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[MetricsObjectDict] metrics: The metrics object data.
    """
    group: Required[str]
    title: Required[str]
    description: Required[str]
    n: Required[float]
    metrics: Required[MetricsObjectDict]

# --- For data used as INPUT (e.g., to `from_dict`) ---

class ResultsInfoData(_ResultsInfoBase, total=False):
    """Typed dictionary for V1 ResultsInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).
        
    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[VariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectData] metrics: The metrics object data.
    :param NotRequired[str] hash_id: The unique hash identifier for the Results information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param Required[CoreDataMappingType] extra_info: Additional information.
    
    """
    variation_marks: Required[VariationMarksType]
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    extra_info: Required[CoreDataMappingType]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class ResultsInfoDict(_ResultsInfoBase, total=True):
    """Typed dictionary for the JSON representation of a V1 ResultsInfo (OUTPUT).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.

    :param Required[str] group: The group for the results.
    :param Required[str] title: The title of the results.
    :param Required[str] description: The description of the results.
    :param Required[float] n: The n-complexity value.
    :param Required[VariationMarksType] variation_marks: The variation marks mapping.
    :param Required[MetricsObjectDict] metrics: The metrics object data.
    :param Required[str] hash_id: The unique hash identifier for the Results information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[ImmutableCoreDataMappingType] extra_info: Additional information.
"""
    variation_marks: Required[ImmutableVariationMarksType]
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    extra_info: Required[ImmutableCoreDataMappingType]

