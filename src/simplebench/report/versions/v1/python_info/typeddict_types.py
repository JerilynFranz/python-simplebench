"""Typed dictionaries for the V1 PythonInfo data structure.

This module defines three distinct dictionary types for handling PythonInfo data,
both modeled on the JSON schema for version 1 PythonInfo in
version 1: :class:`~simplebench.report.versions.v1.PythonInfoSchema`.

- `PythonInfoData`: For use as INPUT (e.g., to `from_dict`). It is more
lenient, making `type`, `version`, and `hash_id` optional.
- `PythonInfoDict`: For use as OUTPUT (e.g., from `to_dict`). It is
stricter, guaranteeing that `type`, `version`, and `hash_id` are present.
- `ImmutablePythonInfoDict`: An immutable subclass of `PythonInfoDict` for
type-checking purposes.

These types ensure proper validation and serialization of PythonInfo data
"""

from simplebench.report.base._report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

__all__ = []


# A base for fields that are always required and have the same type.
class _PythonInfoCore(ReportElementTypedDict, total=True):
    compiler: Required[str]
    implementation: Required[str]
    implementation_version: Required[str]
    python_version: Required[str]
    build: Required[str]
    release: Required[str]
    system: Required[str]


# --- For data used as INPUT (e.g., to `from_dict`) ---


class PythonInfoData(_PythonInfoCore, total=False):
    """Typed dictionary for V1 PythonInfo data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `hash_id` to be
    omitted.

    :param Required[str] compiler: The compiler string.
    :param Required[str] implementation: The implementation string.
    :param Required[str] implementation_version: The implementation_version string.
    :param Required[str] python_version: The python_version string.
    :param Required[str] build: The build string.
    :param Required[str] release: The release string.
    :param Required[str] system: The system string.
    :param NotRequired[str] hash_id: The unique hash identifier for the python information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]


class ImmutablePythonInfoData(PythonInfoData, total=False):
    """Immutable version of :class:`PythonInfoData` (INPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`typechecked.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~typechecked.Immutable`.

    Because it inherits from `PythonInfoData`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[str] compiler: The compiler string.
    :param Required[str] implementation: The implementation string.
    :param Required[str] implementation_version: The implementation_version string.
    :param Required[str] python_version: The python_version string.
    :param Required[str] build: The build string.
    :param Required[str] release: The release string.
    :param Required[str] system: The system string.
    :param NotRequired[str] hash_id: The unique hash identifier for the python information.
    :param NotRequired[str] type: The type identifier for the block.
    :param NotRequired[int] version: The version of the block's data structure.
    """

    __immutable__: NotRequired[Never]  # Marker to indicate immutability


# --- For data used as OUTPUT (e.g., from `to_dict`) ---


class PythonInfoDict(_PythonInfoCore, total=True):
    """Typed dictionary for the JSON representation of a V1 PythonInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, and `hash_id` to be present.

    :param Required[str] compiler: The compiler string.
    :param Required[str] implementation: The implementation string.
    :param Required[str] implementation_version: The implementation_version string.
    :param Required[str] python_version: The python_version string.
    :param Required[str] build: The build string.
    :param Required[str] release: The release string.
    :param Required[str] system: The system string.
    :param Required[str] hash_id: The unique hash identifier for the python information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """

    type: Required[str]
    version: Required[int]
    hash_id: Required[str]


class ImmutablePythonInfoDict(PythonInfoDict, total=False):
    """Immutable version of :class:`PythonInfoDict` (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`typechecked.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~typechecked.Immutable`.

    Because it inherits from `PythonInfoDict`, all fields are the same and it
    can be used interchangeably where immutability is not a concern.

    :param Required[str] compiler: The compiler string.
    :param Required[str] implementation: The implementation string.
    :param Required[str] implementation_version: The implementation_version string.
    :param Required[str] python_version: The python_version string.
    :param Required[str] build: The build string.
    :param Required[str] release: The release string.
    :param Required[str] system: The system string.
    :param Required[str] hash_id: The unique hash identifier for the python information.
    :param Required[str] type: The type identifier for the block.
    :param Required[int] version: The version of the block's data structure.
    """

    __immutable__: NotRequired[Never]  # Marker to indicate immutability
