"""Typed dictionaries for the V1 CPUInfo data structure.

(type stub version)

This is the type stub version of the type definitions for V1 Report data.

There are two versions (.pyi and .py) to accommodate different versions
of Python supporting different features in TypedDicts.

If you edit one of these files, please remember to update the other to
match.

The files are otherwise identical in structure and content.

This module defines two distinct dictionary types for handling CPUInfo data,
both modeled on the JSON schema for version 1 CPUInfo in
version 1: :class:`~simplebench.report.versions.v1.cpu_info.cpu_info_schema.CPUInfoSchema`.

    - `CPUInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `CPUInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.

    These types ensure proper validation and serialization of CPUInfo data
"""
import sys
from typing import NotRequired, Required, TypedDict

from simplebench.types import CoreDataMappingType

# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredCPUInfoData(TypedDict, total=True):
    """Required fields for V1 CPUInfo data used as INPUT.
    
    :param CoreDataMappingType data: The CPU information data.
    """
    data: Required[CoreDataMappingType]


if sys.version_info >= (3, 12):
    class CPUInfoData(_RequiredCPUInfoData, total=False, closed=True):
        """Typed dictionary for V1 CPUInfo data used as INPUT.

        This type is lenient, allowing `type`, `version`, and `hash_id` to be
        omitted (`total=False`).

        .. note::
            This TypedDict uses `closed=True`, which is only supported in Python 3.12 and
            later. To maintain compatibility with earlier versions, an alternative
            definition without `closed=True` is provided automatically to older Python
            versions.

        :param Required[CoreDataMappingType] data: The CPU information data.
        :param NotRequired[str] hash_id: The unique hash identifier for the CPU information.
        :param NotRequired[str] type: The type identifier for the block.
        :param NotRequired[int] version: The version of the block's data structure.
        """
        hash_id: NotRequired[str]
        type: NotRequired[str]
        version: NotRequired[int]

else:  # For Python versions < 3.12 where closed=True is not supported
    class CPUInfoData(_RequiredCPUInfoData, total=False):
        """Typed dictionary for V1 CPUInfo data used as INPUT.

        All fields except `type`, `version`, and `hash_id` are required (`total=False`).

        .. note::
            No additional fields are allowed beyond those defined here but
            `closed=True` is not being enforced due to Python version limitations
            before Python 3.12.

        :param Required[CoreDataMappingType] data: The CPU information data.
        :param NotRequired[str] hash_id: The unique hash identifier for the CPU information.
        :param NotRequired[str] type: The type identifier for the block.
        :param NotRequired[int] version: The version of the block's data structure.
        """
        hash_id: NotRequired[str]
        type: NotRequired[str]
        version: NotRequired[int]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredCPUInfoDict(TypedDict, total=True):
    """Required fields for V1 CPUInfo data used as OUTPUT.
    
    :param CoreDataMappingType data: The CPU information data.
    :param str hash_id: The unique hash identifier for the CPU information.
    :param str type: The type identifier for the block.
    :param int version: The version of the block's data structure.
    """
    data: Required[CoreDataMappingType]
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]

if sys.version_info >= (3, 12):
    class CPUInfoDict(_RequiredCPUInfoDict, total=False, closed=True):
        """Typed dictionary for the JSON representation of a V1 CPUInfo (OUTPUT).

        All fields except `type`, `version`, and `hash_id` are required (`total=False`).

        .. note::
            No additional fields are allowed beyond those defined here but
            `closed=True` is not being enforced due to Python version limitations
            before Python 3.12.

        :param Required[CoreDataMappingType] data: The CPU information data.
        :param Required[str] hash_id: The unique hash identifier for the CPU information.
        :param Required[str] type: The type identifier for the block.
        :param Required[int] version: The version of the block's data structure.
        """
else:  # For Python versions < 3.12 where closed=True is not supported
    class CPUInfoDict(_RequiredCPUInfoDict, total=False):
        """Typed dictionary for the JSON representation of a V1 CPUInfo (OUTPUT).

        All fields except `type`, `version`, and `hash_id` are required (`total=False`).

        .. note::
            No additional fields are allowed beyond those defined here but
            `closed=True` is not being enforced due to Python version limitations
            before Python 3.12.

    :param Required[CoreDataMappingType] data: The CPU information data.
    :param Required[str] hash_id: The unique hash identifier for the CPU information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """
