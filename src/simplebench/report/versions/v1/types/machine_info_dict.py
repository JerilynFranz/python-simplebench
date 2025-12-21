"""Typed dictionaries for the V1 MachineInfo data structure.

This module defines two distinct dictionary types for handling MachineInfo data,
both modeled on the JSON schema for version 1 MachineInfo in
version 1: :class:`~simplebench.report.versions.v1.machine_info.machine_info_schema.MachineInfoSchema`.

    - `MachineInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `MachineInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.

    These types ensure proper validation and serialization of MachineInfo data"""
from typing import TypedDict

from .cpu_info_dict import CPUInfoData, CPUInfoDict
from .execution_environment_dict import ExecutionEnvironmentData, ExecutionEnvironmentDict


# A base for fields that are always required and have the same type.
class _MachineInfoCore(TypedDict, total=True):
    processor: str
    machine: str
    system: str
    release: str
    node: str


# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredMachineInfoData(_MachineInfoCore, total=True):
    """Required fields for V1 MachineInfo data used as INPUT."""
    execution_environment: ExecutionEnvironmentData
    cpu: CPUInfoData


class MachineInfoData(_RequiredMachineInfoData, total=False):
    """Typed dictionary for V1 MachineInfo data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `hash_id` to be
    omitted.

    :param str processor: The processor string.
    :param str machine: The machine string.
    :param str system: The operating system name.
    :param str release: The operating system release.
    :param str node: The node string.
    :param ExecutionEnvironmentData execution_environment: The execution environment information.
    :param CPUInfoData cpu: The CPU information.
    :param str hash_id: (optional) The unique hash identifier for the machine information.
    :param str type: (optional) The type identifier for the block.
    :param int version: (optional) The version of the block's data structure.
    """
    hash_id: str
    type: str
    version: int


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredMachineInfoDict(_MachineInfoCore, total=True):
    """Required fields for V1 MachineInfo data used as OUTPUT."""
    type: str
    version: int
    hash_id: str
    execution_environment: ExecutionEnvironmentDict
    cpu: CPUInfoDict


class MachineInfoDict(_RequiredMachineInfoDict, total=False):
    """Typed dictionary for the JSON representation of a V1 MachineInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, and `hash_id` to be present.

    :param str type: The type identifier for the block.
    :param int version: The version of the block's data structure.
    :param str hash_id: The unique hash identifier for the machine information.
    :param str processor: The processor string.
    :param str machine: The machine string.
    :param str system: The operating system name.
    param str release: The operating system release.
    :param str node: The node string.
    :param ExecutionEnvironmentDict execution_environment: The execution environment information.
    :param CPUInfoDict cpu: The CPU information.
    """
