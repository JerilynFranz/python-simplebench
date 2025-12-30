"""Typed dictionaries for the V1 Report data structure.

This module defines two distinct dictionary types for handling Report data,
both modeled on the JSON schema for version 1 Reports in
version 1: :class:`~simplebench.report.versions.v1.report.report_schema.ReportSchema`.

    - `ReportData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type` and `version` optional.
    - `ReportDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type` and `version` are present.

    These types ensure proper validation and serialization of Report data
"""
from typing import NotRequired, Required, Sequence

from simplebench.report.base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import ImmutableVariationColsType, VariationColsType

from .machine_info_dict import MachineInfoData, MachineInfoDict
from .results_info_dict import ResultsInfoData, ResultsInfoDict


# A base for fields that are always required and have the same type.
class _ReportBase(ReportElementTypedDict, total=True):
    """Core required fields for V1 Report data.
    
    :param Required[str] timestamp: The timestamp of the report.
    :param Required[str] group: The benchmark reporting group.
    :param Required[str] title: The title of the benchmark case.
    :param Required[str] description: A brief description of the benchmark case.
    """
    timestamp: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]


# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredReportData(_ReportBase, total=True):
    """Required fields for V1 Report data used as INPUT.
    
    :param Required[list[ResultsInfoData]] results: A list of benchmark results.
    :param Required[MachineInfoData] machine: Information about the machine running the benchmark.
    :param Required[VariationColsType] variation_cols: Columns for keyword argument variations.
    """
    results: Required[Sequence[ResultsInfoData]]
    machine: Required[MachineInfoData]
    variation_cols: Required[VariationColsType]

class ReportData(_RequiredReportData, total=False):
    """Typed dictionary for V1 Report data used as INPUT.

    All fields except `type` and `version` are required (`total=False`).

    :param Required[str] timestamp: The timestamp of the report.
    :param Required[str] group: The benchmark reporting group.
    :param Required[str] title: The title of the benchmark case.
    :param Required[str] description: A brief description of the benchmark case.
    :param Required[VariationColsType] variation_cols: Columns for keyword argument variations.
    :param Required[Sequence[ResultsInfoData]] results: A list of benchmark results.
    :param Required[MachineInfoData] machine: Information about the machine running the benchmark.
    :param NotRequired[str] type: The type identifier for the report.
    :param NotRequired[int] version: The version of the report's data structure.
    """
    type: NotRequired[str]
    version: NotRequired[int]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredReportDict(_ReportBase, total=True):
    """Required fields for V1 Report data used as OUTPUT.
    
    :param Required[tuple[ResultsInfoDict, ...]] results: A tuple of benchmark results.
    :param Required[MachineInfoDict] machine: Information about the machine running the benchmark.
    :param Required[ImmutableVariationColsType] variation_cols: Columns for keyword argument variations.
    :param Required[str] type: The type identifier for the report.
    :param Required[int] version: The version of the report's data structure.
    """
    type: Required[str]
    version: Required[int]
    results: Required[tuple[ResultsInfoDict, ...]]
    machine: Required[MachineInfoDict]
    variation_cols: Required[ImmutableVariationColsType]

class ReportDict(_RequiredReportDict, total=True):
    """TypedDict of immutable types for the JSON representation of a V1 Report (OUTPUT).

    This type is strict, requiring `type` and `version` to be present.

    All fields are required (`total=True`), and their types are immutable.

    The type asserts to type checkers that all required fields are present and
    that all fields are of the correct immutable types, but cannot enforce
    immutability of the instance itself (Python limitation).

    :param Required[str] type: The type identifier for the report.
    :param Required[int] version: The version of the report's data structure.
    :param Required[str] timestamp: The timestamp of the report.
    :param Required[str] group: The benchmark reporting group.
    :param Required[str] title: The title of the benchmark case.
    :param Required[str] description: A brief description of the benchmark case.
    :param Required[ImmutableVariationColsType] variation_cols: Columns for keyword argument variations.
    :param Required[tuple[ResultsInfoDict, ...]] results: A tuple of benchmark results.
    :param Required[MachineInfoDict] machine: Information about the machine running the benchmark.
    """
    type: Required[str]
    version: Required[int]
