"""Typed dictionaries for the V1 SystemInfo data structure.

(type stub version)

This is the type stub version of the type definitions for V1 SystemInfo data.

There are two versions (.pyi and .py) to accommodate different versions
of Python supporting different features in TypedDicts.

If you edit one of these files, please remember to update the other to
match.

The files are otherwise identical in structure and content.

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
from typing import NotRequired, Required, TypedDict

# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredSystemInfoData(TypedDict, total=True):
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

if sys.version_info >= (3, 12):
    class SystemInfoData(_RequiredSystemInfoData, total=False, closed=True):
        """Typed dictionary for V1 SystemInfo data used as INPUT.

        This type is lenient, allowing `type`, `version`, and `hash_id` to be
        omitted (`total=False`).

        .. note::
            This TypedDict uses `closed=True`, which is only supported in Python 3.12 and
            later. To maintain compatibility with earlier versions, an alternative
            definition without `closed=True` is provided automatically to older Python
            versions.

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

else:  # For Python versions < 3.12 where closed=True is not supported
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

class _RequiredSystemInfoDict(TypedDict, total=True):
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

if sys.version_info >= (3, 12):
    class SystemInfoDict(_RequiredSystemInfoDict, total=True, closed=True):
        """Typed dictionary for the JSON representation of a V1 SystemInfo (OUTPUT).

        This type is strict, requiring `type` and `version` to be present.

        All fields are required (`total=True`), and their types are immutable.
        No additional fields are allowed beyond those defined here (`closed=True`).

        .. note::
            This TypedDict uses `closed=True`, which is only supported in Python 3.12 and later.
            An alternative definition without `closed=True`is also provided automatically
            to older Python versions for compatibility.

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

else:  # For Python versions < 3.12 where closed=True is not supported
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
