"""Typed dictionaries for the V1 VCSInfo data structure.

This module defines four distinct dictionary types for handling VCSInfo data,
all modeled on the JSON schema for version 1 VCSInfo in
version 1: :class:`~simplebench.report.versions.v1.VCSInfoSchema`.

- `VCSInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
lenient, making `type`, `version`, and `hash_id` optional.
- `ImmutableVCSInfoData`: An immutable subclass of `VCSInfoData` for
type-checking purposes.
- `VCSInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
- `ImmutableVCSInfoDict`: An immutable subclass of `VCSInfoDict` for
type-checking purposes.

These types ensure proper validation and serialization of VCSInfo data
"""

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

__all__ = []


# A base for fields that are always required and have the same type.
class _VCSInfoCore(ReportElementTypedDict, total=True):
    """
    Typed dictionary base required fields for V1 VCSInfo data structure.

    :param Required[str] vcs: The version control system string.
    :param Required[str] commit_id: The unique identifier of the current revision.
    :param Required[str] branch: The current branch name.
    :param Required[str] repository_url: The URL of the primary remote repository or empty string.
    :param Required[bool] is_dirty: Whether there are uncommitted changes.
    :param Required[str] commit_datetime: The datetime of the commit in ISO 8601 format.
    """

    vcs: Required[str]
    commit_id: Required[str]
    commit_datetime: Required[str]
    branch: Required[str]
    repository_url: Required[str]
    is_dirty: Required[bool]


# --- For data used as INPUT (e.g., to `from_dict`) ---


class VCSInfoData(_VCSInfoCore, total=False):
    """Typed dictionary for V1 VCSInfo data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `hash_id` to be
    omitted.

    :param Required[str] vcs: The version control system string.
    :param Required[str] commit_id: The unique identifier of the current revision.
    :param Required[str] commit_datetime: The datetime of the commit in ISO 8601 format.
    :param Required[str] branch: The current branch name.
    :param Required[str] repository_url: The URL of the primary remote repository or empty string.
    :param Required[bool] is_dirty: Whether there are uncommitted changes.
    :param NotRequired[str] hash_id: The unique hash identifier for the vcs information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]


class ImmutableVCSInfoData(VCSInfoData, total=False):
    """Immutable version of :class:`VCSInfoData` (INPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The ``__immutable__`` field is a class marker to indicate immutability
    for type-checking purposes. It should not be set or used at runtime.

    Because it inherits from `VCSInfoData`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[str] vcs: The version control system string.
    :param Required[str] commit_id: The unique identifier of the current revision.
    :param Required[str] branch: The current branch name.
    :param Required[str] repository_url: The URL of the primary remote repository or empty string.
    :param Required[bool] is_dirty: Whether there are uncommitted changes.
    :param Required[str] commit_datetime: The datetime of the commit in ISO 8601 format.
    :param NotRequired[str] hash_id: The unique hash identifier for the vcs information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    __immutable__: NotRequired[Never]  # Marker to indicate immutability


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class VCSInfoDict(_VCSInfoCore, total=True):
    """Typed dictionary for the JSON representation of a V1 VCSInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, and `hash_id` to be present.

    :param Required[str] vcs: The version control system string.
    :param Required[str] commit_id: The unique identifier of the current revision.
    :param Required[str] branch: The current branch name.
    :param Required[str] repository_url: The URL of the primary remote repository or empty string.
    :param Required[bool] is_dirty: Whether there are uncommitted changes.
    :param Required[str] commit_datetime: The datetime of the commit in ISO 8601 format.
    :param Required[str] hash_id: The unique hash identifier for the vcs information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """

    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutableVCSInfoDict(VCSInfoDict, total=False):
    """Immutable version of :class:`VCSInfoDict` (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    Because it inherits from `VCSInfoDict`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    The ``__immutable__`` field is a class marker to indicate immutability
    for type-checking purposes. It should not be set or used at runtime.

    :param Required[str] vcs: The version control system string.
    :param Required[str] commit_id: The unique identifier of the current revision.
    :param Required[str] branch: The current branch name.
    :param Required[str] repository_url: The URL of the primary remote repository.
    :param Required[bool] is_dirty: Whether there are uncommitted changes.
    :param Required[str] commit_datetime: The datetime of the commit in ISO 8601 format.
    :param Required[str] hash_id: The unique hash identifier for the vcs information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """

    __immutable__: NotRequired[Never]  # Marker to indicate immutability
