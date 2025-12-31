"""Typed dictionaries for the V1 SystemInfo data structure.

This module defines two distinct dictionary types for handling SystemInfo data,
both modeled on the JSON schema for version 1 SystemInfo in
version 1: :class:`~simplebench.report.versions.v1.system_info.system_info_schema.SystemInfoSchema`.

    - `SystemInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, making `type`, `version`, and `hash_id` optional.
    - `SystemInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `type`, `version`, and `hash_id` are present.

    These types ensure proper validation and serialization of SystemInfo data
"""
import sys

from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired, Required
else:
    from typing_extensions import NotRequired, Required

# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredSystemInfoData(ReportElementTypedDict, total=True):
    """Required fields for V1 SystemInfo data used as INPUT.

    All fields are required (`total=True`), except for those made optional
    in the main `SystemInfoData` definition.

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    """
    system: Required[str]
    system_version: Required[str]
    release: Required[str]
    machine: Required[str]

class SystemInfoData(_RequiredSystemInfoData, total=False):
    """Typed dictionary for V1 SystemInfo data used as INPUT.

    All fields except `type`, `version`, and `hash_id` are required (`total=False`).

    .. note::
        No additional fields are allowed beyond those defined here but
        `closed=True` is not being enforced due to Python version limitations
        before Python 3.12.

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    :param NotRequired[str] hash_id: The unique hash identifier for the system information.
    """
    type: NotRequired[str]
    version: NotRequired[int]
    hash_id: NotRequired[str]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredSystemInfoDict(ReportElementTypedDict, total=True):
    """Required fields for V1 SystemInfo data used as OUTPUT.

     All fields are required (`total=True`)

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the system information.
    """
    system: Required[str]
    system_version: Required[str]
    release: Required[str]
    machine: Required[str]
    type: Required[str]
    version: Required[int]
    hash_id: Required[str]

class SystemInfoDict(_RequiredSystemInfoDict, total=True):
    """Typed dictionary for the JSON representation of a V1 SystemInfo (OUTPUT).

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

    :param Required[str] system: The system OS identifier string.
    :param Required[str] system_version: The system version string.
    :param Required[str] release: The system release string.
    :param Required[str] machine: The machine type string.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    :param Required[str] hash_id: The unique hash identifier for the system information.
    """
