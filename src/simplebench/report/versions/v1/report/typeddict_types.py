"""Typed dictionaries for the V1 Report data structure.

This module defines four distinct dictionary types for handling Report data,
all modeled on the JSON schema for version 1 Reports in
version 1: :class:`~simplebench.report.versions.v1.report.report_schema.ReportSchema`.

    - :class:`ReportData`: For use as INPUT (e.g., to `from_dict`). It is more
        lenient, making `type`, `version`, and `hash_id` optional.
    - :class:`ImmutableReportData`: An immutable variant of `ReportData` for
        type-checking purposes.
    - :class:`ReportDict`: For use as OUTPUT (e.g., from `to_dict`). It is
        stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
    - :class:`ImmutableReportDict`: An immutable variant of `ReportDict` for
        type-checking purposes.

    These types ensure proper validation and serialization of Report data
"""

from collections.abc import Mapping, Sequence

from simplebench.report.base import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required, VariationCols

from ..machine_info import ImmutableMachineInfoData, ImmutableMachineInfoDict, MachineInfoData, MachineInfoDict
from ..results_info import ImmutableResultsInfoData, ImmutableResultsInfoDict, ResultsInfoData, ResultsInfoDict

__all__: list[str] = []

# --- For data used as INPUT (e.g., to `from_dict`) ---

class ReportData(ReportElementTypedDict):
    """Typed dictionary for V1 Report data used as INPUT.

    All fields except `hash_id`, `type`, and `version` are required.

    :param Required[str] timestamp: The timestamp of the report.
    :param Required[str] group: The benchmark reporting group.
    :param Required[str] title: The title of the benchmark case.
    :param Required[str] description: A brief description of the benchmark case.
    :param Required[Mapping[str, str]] variation_cols: Columns for keyword argument variations.
    :param Required[Sequence[ResultsInfoData]] results: A list of benchmark results.
    :param Required[MachineInfoData] machine: Information about the machine running the benchmark.
    :param NotRequired[str] type: The type identifier for the report.
    :param NotRequired[int] version: The version of the report's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the report.
    """
    timestamp: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    variation_cols: Required[Mapping[str, str]]
    results: Required[Sequence[ResultsInfoData]]
    machine: Required[MachineInfoData]
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]


class ImmutableReportData(ReportElementTypedDict):
    """Typed dictionary for immutable V1 Report data used as INPUT.

    All fields except `hash_id`, `type`, and `version` are required.

    The `__immutable__` field is included to signal that this dictionary
    is intended to be immutable. It is not used at runtime but serves
    as a class-level marker for type checkers and developers. It should never be set
    to any value.

    :param Required[str] timestamp: The timestamp of the report.
    :param Required[str] group: The benchmark reporting group.
    :param Required[str] title: The title of the benchmark case.
    :param Required[str] description: A brief description of the benchmark case.
    :param Required[VariationCols] variation_cols: Columns for keyword argument variations.
    :param Required[tuple[ImmutableResultsInfoData, ...]] results: A tuple of benchmark results.
    :param Required[ImmutableMachineInfoData] machine: Information about the machine running the benchmark.
    :param NotRequired[str] type: The type identifier for the report.
    :param NotRequired[int] version: The version of the report's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the report.
    """
    timestamp: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    variation_cols: Required[VariationCols]
    results: Required[tuple[ImmutableResultsInfoData, ...]]
    machine: Required[ImmutableMachineInfoData]
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]
    __immutable__: NotRequired[Never]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class ReportDict(ReportElementTypedDict):
    """Required fields for V1 Report data used as OUTPUT.

    :param Required[str] timestamp: The timestamp of the report.
    :param Required[str] group: The benchmark reporting group.
    :param Required[str] title: The title of the benchmark case.
    :param Required[str] description: A brief description of the benchmark case.
    :param Required[tuple[ResultsInfoDict, ...]] results: A tuple of benchmark results.
    :param Required[MachineInfoDict] machine: Information about the machine running the benchmark.
    :param Required[VariationCols] variation_cols: Columns for keyword argument variations.
    :param Required[str] type: The type identifier for the report.
    :param Required[int] version: The version of the report's data structure.
    :param Required[str] hash_id: The unique hash identifier for the report.
    """
    timestamp: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    results: Required[tuple[ResultsInfoDict, ...]]
    machine: Required[MachineInfoDict]
    variation_cols: Required[VariationCols]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableReportDict(ReportElementTypedDict):
    """Required fields for immutable V1 Report data used as OUTPUT.

    The immutable variant ensures that the data cannot be modified after creation.

    :param Required[str] timestamp: The timestamp of the report.
    :param Required[str] group: The benchmark reporting group.
    :param Required[str] title: The title of the benchmark case.
    :param Required[str] description: A brief description of the benchmark case.
    :param Required[tuple[ImmutableResultsInfoDict, ...]] results: A tuple of benchmark results.
    :param Required[ImmutableMachineInfoDict] machine: Information about the machine running the benchmark.
    :param Required[VariationCols] variation_cols: Columns for keyword argument variations.
    :param Required[str] type: The type identifier for the report.
    :param Required[int] version: The version of the report's data structure.
    :param Required[str] hash_id: The unique hash identifier for the report.
    """
    timestamp: Required[str]
    group: Required[str]
    title: Required[str]
    description: Required[str]
    results: Required[tuple[ImmutableResultsInfoDict, ...]]
    machine: Required[ImmutableMachineInfoDict]
    variation_cols: Required[VariationCols]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    __immutable__: NotRequired[Never]
