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
from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

from ._cpu_info_dict import CPUInfoData, CPUInfoDict
from ._memory_info_dict import MemoryInfoData, MemoryInfoDict
from ._system_info_dict import SystemInfoData, SystemInfoDict
from .execution_environment_dict import ExecutionEnvironmentData, ExecutionEnvironmentDict

__all__ = [
    "MachineInfoData",
    "ImmutableMachineInfoData",
    "MachineInfoDict",
    "ImmutableMachineInfoDict",
]

# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredMachineInfoData(ReportElementTypedDict, total=True):
    """Required fields for V1 MachineInfo data used as INPUT.

    :param Required[str] node: The node string.
    :param Required[CPUInfoData] cpu: The CPU information.
    :param Required[MemoryInfoData] memory: The operating system release.
    :param Required[SystemInfoData] system: The system name.
    :param Required[ExecutionEnvironmentData] execution_environment: The execution environment information.
    """
    node: Required[str]
    cpu: Required[CPUInfoData]
    memory: Required[MemoryInfoData]
    system: Required[SystemInfoData]
    execution_environment: Required[ExecutionEnvironmentData]

class MachineInfoData(_RequiredMachineInfoData, total=False):
    """Typed dictionary for V1 MachineInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.

            :param Required[str] node: The node string.

    :param Required[str] node: The node string.
    :param Required[CPUInfoData] cpu: The CPU information.
    :param Required[MemoryInfoData] memory: The operating system release.
    :param Required[SystemInfoData] system: The system name.
    :param Required[ExecutionEnvironmentData] execution_environment: The execution environment information.
    :param NotRequired[str] hash_id: The unique hash identifier for the machine information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]


class ImmutableMachineInfoData(MachineInfoData, total=False):
    """Immutable typed dictionary for V1 MachineInfo data used as INPUT.

    :param Required[str] node: The node string.
    :param Required[CPUInfoData] cpu: The CPU information.
    :param Required[MemoryInfoData] memory: The operating system release.
    :param Required[SystemInfoData] system: The system name.
    :param Required[ExecutionEnvironmentData] execution_environment: The execution environment information.
    :param NotRequired[str] hash_id: The unique hash identifier for the machine information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    __immutable__: NotRequired[Never]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class MachineInfoDict(ReportElementTypedDict, total=True):
    """Required fields for V1 MachineInfo data used as OUTPUT.

    This type is strict, requiring `type`, `version`, and `hash_id` to be
    present

    All fields are required (`total=True`), and their types are immutable.
    No additional fields are allowed beyond those defined here (`closed=True`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.

    The type asserts to type checkers that all required fields are present and
    that all fields are of the correct immutable types, but cannot enforce
    immutability of the instance itself (Python limitation).
    
    :param Required[str] node: The node string.
    :param Required[CPUInfoDict] cpu: The CPU information.
    :param Required[MemoryInfoDict] memory: The operating system release.
    :param Required[SystemInfoDict] system: The system name.
    :param Required[ExecutionEnvironmentDict] execution_environment: The execution environment information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the machine information.

    """
    node: Required[str]
    cpu: Required[CPUInfoDict]
    memory: Required[MemoryInfoDict]
    system: Required[SystemInfoDict]
    execution_environment: Required[ExecutionEnvironmentDict]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableMachineInfoDict(MachineInfoDict, total=False):
    """Immutable typed dictionary for V1 MachineInfo data used as OUTPUT.

    :param Required[str] node: The node string.
    :param Required[CPUInfoDict] cpu: The CPU information.
    :param Required[MemoryInfoDict] memory: The operating system release.
    :param Required[SystemInfoDict] system: The system name.
    :param Required[ExecutionEnvironmentDict] execution_environment: The execution environment information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the machine information.
    """
    __immutable__: NotRequired[Never]
