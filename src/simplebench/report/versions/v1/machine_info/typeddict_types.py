"""Typed dictionaries for the V1 MachineInfo data structure.

This module defines four distinct dictionary types for handling MachineInfo data,
both modeled on the JSON schema for version 1 MachineInfo in
version 1: :class:`~simplebench.report.versions.v1.MachineInfoSchema`.

    - `MachineInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `ImmutableMachineInfoData`: An immutable variant of `MachineInfoData`.
    - `MachineInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
    - `ImmutableMachineInfoDict`: An immutable variant of `MachineInfoDict`.

    These types ensure proper validation and serialization of MachineInfo data\
"""
from collections.abc import Sequence

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.simplebench_types import Never, NotRequired, Required

from ..cpu_info.typeddict_types import CPUInfoData, CPUInfoDict, ImmutableCPUInfoData, ImmutableCPUInfoDict
from ..environment_info.typeddict_types import (
    EnvironmentInfoData,
    EnvironmentInfoDict,
    ImmutableEnvironmentInfoData,
    ImmutableEnvironmentInfoDict,
)
from ..memory_info.typeddict_types import (
    ImmutableMemoryInfoData,
    ImmutableMemoryInfoDict,
    MemoryInfoData,
    MemoryInfoDict,
)
from ..python_info.typeddict_types import (
    ImmutablePythonInfoData,
    ImmutablePythonInfoDict,
    PythonInfoData,
    PythonInfoDict,
)
from ..system_info.typeddict_types import (
    ImmutableSystemInfoData,
    ImmutableSystemInfoDict,
    SystemInfoData,
    SystemInfoDict,
)

# Imports are directly from the specific sub-modules to avoid accidentally creating circular dependencies

__all__: list[str] = []

# --- For data used as INPUT (e.g., to `from_dict`) ---

class MachineInfoData(ReportElementTypedDict):
    """Typed dictionary for V1 MachineInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required.

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.

    :param Required[str] node: The node string.
    :param Required[CPUInfoData] cpu: The CPU information.
    :param Required[MemoryInfoData] memory: The operating system release.
    :param Required[SystemInfoData] system: The system name.
    :param Required[Sequence[EnvironmentInfoData | PythonInfoData]] environment: The
        execution environment information.
    :param NotRequired[str] hash_id: The unique hash identifier for the machine information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    node: Required[str]
    cpu: Required[CPUInfoData]
    memory: Required[MemoryInfoData]
    system: Required[SystemInfoData]
    environment: Required[Sequence[EnvironmentInfoData | PythonInfoData]]
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]


class ImmutableMachineInfoData(ReportElementTypedDict):
    """Immutable typed dictionary for V1 MachineInfo data used as INPUT.

    :param Required[str] node: The node string.
    :param Required[ImmutableCPUInfoData] cpu: The CPU information.
    :param Required[ImmutableMemoryInfoData] memory: The operating system release.
    :param Required[ImmutableSystemInfoData] system: The system name.
    :param Required[Sequence[ImmutableEnvironmentInfoData | ImmutablePythonInfoData]] environment: The
        execution environment information.
    :param NotRequired[str] hash_id: The unique hash identifier for the machine information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    node: Required[str]
    cpu: Required[ImmutableCPUInfoData]
    memory: Required[ImmutableMemoryInfoData]
    system: Required[ImmutableSystemInfoData]
    environment: Required[Sequence[ImmutableEnvironmentInfoData | ImmutablePythonInfoData]]
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    __immutable__: NotRequired[Never]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class MachineInfoDict(ReportElementTypedDict, total=True):
    """Required fields for V1 MachineInfo data used as OUTPUT

    This type is strict, requiring all fields, including `type`, `version`,
    and `hash_id`, to be present to strictly conform with the JSON schema and
    all sub-objects to also be in their strict OUTPUT forms as well.

    :param Required[str] node: The node string.
    :param Required[CPUInfoDict] cpu: The CPU information.
    :param Required[MemoryInfoDict] memory: The operating system release.
    :param Required[SystemInfoDict] system: The system name.
    :param Required[Sequence[EnvironmentInfoDict | PythonInfoDict]] environment: The
        execution environment information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the machine information.
    """
    node: Required[str]
    cpu: Required[CPUInfoDict]
    memory: Required[MemoryInfoDict]
    system: Required[SystemInfoDict]
    environment: Required[Sequence[EnvironmentInfoDict | PythonInfoDict]]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableMachineInfoDict(ReportElementTypedDict):
    """Immutable typed dictionary for V1 MachineInfo data used as OUTPUT.

    :param Required[str] node: The node string.
    :param Required[ImmutableCPUInfoDict] cpu: The CPU information.
    :param Required[ImmutableMemoryInfoDict] memory: The operating system release.
    :param Required[ImmutableSystemInfoDict] system: The system name.
    :param Required[Sequence[ImmutableEnvironmentInfoDict | ImmutablePythonInfoDict]] environment: The
        execution environment information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the machine information.
    """
    node: Required[str]
    cpu: Required[ImmutableCPUInfoDict]
    memory: Required[ImmutableMemoryInfoDict]
    system: Required[ImmutableSystemInfoDict]
    environment: Required[Sequence[ImmutableEnvironmentInfoDict | ImmutablePythonInfoDict]]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    __immutable__: NotRequired[Never]
