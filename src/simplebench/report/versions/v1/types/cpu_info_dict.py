"""Typed dictionaries for the V1 CPUInfo data structure.

This module defines two distinct dictionary types for handling CPUInfo data,
both modeled on the JSON schema for version 1 CPUInfo in
version 1: :class:`~simplebench.report.versions.v1.cpu_info.cpu_info_schema.CPUInfoSchema`.

    - `CPUInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `CPUInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.

    These types ensure proper validation and serialization of CPUInfo data"""
from typing import TypedDict


# A base for fields that are always required and have the same type.
class _CPUInfoCore(TypedDict, total=True):
    arch: str
    bits: int
    count: int
    arch_string_raw: str
    brand_raw: str


# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredCPUInfoData(_CPUInfoCore, total=True):
    """Required fields for V1 CPUInfo data used as INPUT."""


class CPUInfoData(_RequiredCPUInfoData, total=False):
    """Typed dictionary for V1 CPUInfo data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `hash_id` to be
    omitted.

    :param str arch: The CPU architecture.
    :param int bits: The CPU bitness (e.g., 32 or 64).
    :param int count: The number of CPU cores.
    :param str arch_string_raw: The raw architecture string.
    :param str brand_raw: The raw brand string.
    :param str hash_id: (optional) The unique hash identifier for the CPU information.
    :param str type: (optional) The type identifier for the block.
    :param int version: (optional) The version of the block's data structure.
    """
    hash_id: str
    type: str
    version: int


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredCPUInfoDict(_CPUInfoCore, total=True):
    """Required fields for V1 CPUInfo data used as OUTPUT."""
    type: str
    version: int
    hash_id: str


class CPUInfoDict(_RequiredCPUInfoDict, total=False):
    """Typed dictionary for the JSON representation of a V1 CPUInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, and `hash_id` to be present.

    :param str type: The type identifier for the block.
    :param int version: The version of the block's data structure.
    :param str hash_id: The unique hash identifier for the CPU information.
    :param str arch: The CPU architecture.
    :param int bits: The CPU bitness (e.g., 32 or 64).
    :param int count: The number of CPU cores.
    :param str arch_string_raw: The raw architecture string.
    :param str brand_raw: The raw brand string.
    """
