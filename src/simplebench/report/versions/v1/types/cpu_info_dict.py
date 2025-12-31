"""Typed dictionaries for the V1 CPUInfo data structure.

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

from simplebench.report.base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import CoreDataMappingType

if sys.version_info >= (3, 11):
    from typing import NotRequired, Required
else:
    from typing_extensions import NotRequired, Required



# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredCPUInfoData(ReportElementTypedDict, total=True):
    """Required fields for V1 CPUInfo data used as INPUT.
    
    :param CoreDataMappingType data: The CPU information data.
    """
    data: Required[CoreDataMappingType]


class CPUInfoData(_RequiredCPUInfoData, total=False):
    """Typed dictionary for V1 CPUInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).

    :param Required[CoreDataMappingType] data: The CPU information data.
    :param NotRequired[str] hash_id: The unique hash identifier for the CPU information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredCPUInfoDict(ReportElementTypedDict, total=True):
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

class CPUInfoDict(_RequiredCPUInfoDict, total=False):
    """Typed dictionary for the JSON representation of a V1 CPUInfo (OUTPUT).

:param Required[CoreDataMappingType] data: The CPU information data.
:param Required[str] hash_id: The unique hash identifier for the CPU information.
:param Required[str] type: The type identifier for the block.
:param Required[int] version: The version of the block's data structure.
"""
