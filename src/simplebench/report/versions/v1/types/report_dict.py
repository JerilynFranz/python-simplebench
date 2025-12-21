"""Typed dictionaries for the V1 Report data structure.

This module defines two distinct dictionary types for handling Report data,
both modeled on the JSON schema for version 1 Reports in
version 1: :class:`~simplebench.report.versions.v1.report.report_schema.ReportSchema`.

    - `ReportData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type` and `version` optional.
    - `ReportDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type` and `version` are present.

    These types ensure proper validation and serialization of Report data"""
from typing import TypedDict

from .machine_info_dict import MachineInfoData, MachineInfoDict
from .results_info_dict import ResultsInfoData, ResultsInfoDict


# A base for fields that are always required and have the same type.
class _ReportCore(TypedDict, total=True):
    timestamp: str
    group: str
    title: str
    description: str
    variation_cols: dict[str, str]


# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredReportData(_ReportCore, total=True):
    """Required fields for V1 Report data used as INPUT."""
    results: list[ResultsInfoData]
    machine: MachineInfoData


class ReportData(_RequiredReportData, total=False):
    """Typed dictionary for V1 Report data used as INPUT.

    This type is lenient, allowing `type` and `version` to be
    omitted.

    :param str timestamp: The timestamp of the report.
    :param str group: The benchmark reporting group.
    :param str title: The title of the benchmark case.
    :param str description: A brief description of the benchmark case.
    :param dict[str, str] variation_cols: Columns for keyword argument variations.
    :param list[ResultsInfoData] results: A list of benchmark results.
    :param MachineInfoData machine: Information about the machine running the benchmark.
    :param str type: (optional) The type identifier for the report.
    :param int version: (optional) The version of the report's data structure.
    """
    type: str
    version: int


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredReportDict(_ReportCore, total=True):
    """Required fields for V1 Report data used as OUTPUT."""
    type: str
    version: int
    results: list[ResultsInfoDict]
    machine: MachineInfoDict


class ReportDict(_RequiredReportDict, total=False):
    """Typed dictionary for the JSON representation of a V1 Report (OUTPUT).

    This type is strict, requiring `type` and `version` to be present.

    :param str type: The type identifier for the report.
    :param int version: The version of the report's data structure.
    :param str timestamp: The timestamp of the report.
    :param str group: The benchmark reporting group.
    :param str title: The title of the benchmark case.
    :param str description: A brief description of the benchmark case.
    :param dict[str, str] variation_cols: Columns for keyword argument variations.
    :param list[ResultsInfoDict] results: A list of benchmark results.
    :param MachineInfoDict machine: Information about the machine running the benchmark.
    """
