"""Typed dictionaries for the V1 MachineInfo data structure.

This module defines two distinct dictionary types for handling MachineInfo data,
both modeled on the JSON schema for version 1 MachineInfo in
version 1: :class:`~simplebench.report.versions.v1.machine_info.machine_info_schema.MachineInfoSchema`.

    - `MachineInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `MachineInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.

    These types ensure proper validation and serialization of MachineInfo data\
"""
import sys

from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict

from ._cpu_info_dict import CPUInfoData, CPUInfoDict
from .execution_environment_dict import ExecutionEnvironmentData, ExecutionEnvironmentDict
from ._memory_info_dict import MemoryInfoData, MemoryInfoDict
from ._system_info_dict import SystemInfoData, SystemInfoDict

if sys.version_info >= (3, 11):
    from typing import NotRequired, Required
else:
    from typing_extensions import NotRequired, Required

# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredMachineInfoData(ReportElementTypedDict, total=True):
    """Required fields for V1 MachineInfo data used as INPUT.

    :param Required[ExecutionEnvironmentData] execution_environment: The execution environment information.
    :param Required[CPUInfoData] cpu: The CPU information.
    """
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

    :param Required[str] processor: The processor string.
    :param Required[str] machine: The machine string.
    :param Required[str] system: The operating system name.
    :param Required[str] release: The operating system release.
    :param Required[str] node: The node string.
    :param Required[ExecutionEnvironmentData] execution_environment: The execution environment information.
    :param Required[CPUInfoData] cpu: The CPU information.
    :param NotRequired[str] hash_id: The unique hash identifier for the machine information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredMachineInfoDict(ReportElementTypedDict, total=True):
    """Required fields for V1 MachineInfo data used as OUTPUT.

    All fields are required (`total=True`), and their values are immutable types.
    
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the machine information.
    :param Required[ExecutionEnvironmentDict] execution_environment: The execution environment information.
    :param Required[CPUInfoDict] cpu: The CPU information.
    """
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]
    node: Required[str]
    cpu: Required[CPUInfoDict]
    memory: Required[MemoryInfoDict]
    system: Required[SystemInfoDict]
    execution_environment: Required[ExecutionEnvironmentDict]

class MachineInfoDict(_RequiredMachineInfoDict, total=True):
    """Typed dictionary for the JSON representation of a V1 MachineInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, `node`, and `hash_id` to be
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

    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the machine information.
    :param Required[str] node: The node string.
    :param Required[CPUInfoDict] cpu: The CPU information.
    :param Required[MemoryInfoDict] memory: The operating system release.
    :param Required[SystemInfoDict] system: The system name.
    :param Required[ExecutionEnvironmentDict] execution_environment: The execution environment information.
    """
