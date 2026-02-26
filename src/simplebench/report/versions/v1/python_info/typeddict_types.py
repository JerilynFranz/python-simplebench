"""Typed dictionaries for the V1 PythonInfo data structure.

This module defines three distinct dictionary types for handling PythonInfo data,
both modeled on the JSON schema for version 1 PythonInfo in
version 1: :class:`~simplebench.report.versions.v1.PythonInfoSchema`.

- `PythonInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
lenient, making `type`, `version`, and `hash_id` optional.
- `PythonInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
- `ImmutablePythonInfoDict`: An immutable subclass of `PythonInfoDict` for
type-checking purposes.

These types ensure proper validation and serialization of PythonInfo data
"""
from collections.abc import Mapping, Sequence

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence, Never, NotRequired, Required

__all__: list[str] = []


class PythonInfoEnv(ReportElementTypedDict):
    python_version: Required[str]
    implementation: Required[str]
    implementation_version: Required[str]
    compiler: Required[str]
    revision: Required[str]
    buildno: Required[str]
    builddate: Required[str]
    command_line_flags: Required[str]
    environment_variables: Required[Mapping[str, str]]
    gc_is_enabled: Required[bool]
    gc_thresholds: Required[Sequence[int]]
    thread_switch_interval: Required[float]
    architecture_bits: Required[str]
    architecture_linkage: Required[str]

class ImmutablePythonInfoEnv(ReportElementTypedDict):
    python_version: Required[str]
    implementation: Required[str]
    implementation_version: Required[str]
    compiler: Required[str]
    revision: Required[str]
    buildno: Required[str]
    builddate: Required[str]
    command_line_flags: Required[str]
    environment_variables: Required[CoreDataMapping[str]]
    gc_is_enabled: Required[bool]
    gc_thresholds: Required[CoreDataSequence[int]]
    thread_switch_interval: Required[float]
    architecture_bits: Required[str]
    architecture_linkage: Required[str]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability

# --- For data used as INPUT (e.g., to `from_dict`) ---

class PythonInfoData(ReportElementTypedDict):
    """Typed dictionary for V1 PythonInfo data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `hash_id` to be
    omitted.

    :param hash_id: The unique hash identifier for the python information.
    :type NotRequired[str]
    :param type: The type identifier for the block.
    :type type: NotRequired[str]
    :param version: The version of the block's data structure.
    :type version: NotRequired[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
    :type semantic_type: NotRequired[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[PythonInfoEnv]
    """
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    semantic_type: NotRequired[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[PythonInfoEnv]


class ImmutablePythonInfoData(ReportElementTypedDict):
    """Immutable version of :class:`PythonInfoData` (INPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`~simplebench.simplebench_types.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~simplebench.simplebench_types.Immutable`.

    Because it inherits from `PythonInfoData`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param hash_id: The unique hash identifier for the python information.
    :type hash_id: NotRequired[str]
    :param type: The type identifier for the block.
    :type type: NotRequired[str]
    :param version: The version of the block's data structure.
    :type version: NotRequired[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
    :type semantic_type: NotRequired[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[ImmutablePythonInfoEnv]
    """
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    semantic_type: NotRequired[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[ImmutablePythonInfoEnv]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class PythonInfoDict(ReportElementTypedDict):
    """Typed dictionary for the JSON representation of a V1 PythonInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, and `hash_id` to be present.

    :param hash_id: The unique hash identifier for the python information.
    :type hash_id: Required[str]
    :param type: The type identifier for the block.
    :type type: Required[str]
    :param version: The version of the block's data structure.
    :type version: Required[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
    :type semantic_type: Required[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[PythonInfoEnv]
    """
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    semantic_type: Required[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[PythonInfoEnv]


class ImmutablePythonInfoDict(ReportElementTypedDict):
    """Immutable version of :class:`PythonInfoDict` (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`~simplebench.simplebench_types.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~simplebench.simplebench_types.Immutable`.

    Because it inherits from `PythonInfoDict`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param hash_id: The unique hash identifier for the python information.
    :type hash_id: Required[str]
    :param type: The type identifier for the block.
    :type type: Required[str]
    :param version: The version of the block's data structure.
    :type version: Required[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
    :type semantic_type: Required[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[ImmutablePythonInfoEnv]
    """
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    semantic_type: Required[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[ImmutablePythonInfoEnv]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability
