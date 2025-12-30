"""Typed dictionaries for the V1 PythonInfo data structure."""
from simplebench.report.base.report_element_typed_dict import ReportElementTypedDict


# A base for fields that are always required and have the same type.
class _PythonInfoCore(ReportElementTypedDict, total=True):
    compiler: str
    implementation: str
    implementation_version: str
    python_version: str
    build: str
    release: str
    system: str


# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredPythonInfoData(_PythonInfoCore, total=True):
    """Required fields for V1 PythonInfo data used as INPUT."""


class PythonInfoData(_RequiredPythonInfoData, total=False):
    """Typed dictionary for V1 PythonInfo data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `hash_id` to be
    omitted.

    :param str compiler: The compiler string.
    :param str implementation: The implementation string.
    :param str implementation_version: The implementation_version string.
    :param str python_version: The python_version string.
    :param str build: The build string.
    :param str release: The release string.
    :param str system: The system string.
    :param str hash_id: (optional) The unique hash identifier for the python information.
    :param str type: (optional) The type identifier for the block.
    :param int version: (optional) The version of the block's data structure.
    """
    hash_id: str
    type: str
    version: int


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredPythonInfoDict(_PythonInfoCore, total=True):
    """Required fields for V1 PythonInfo data used as OUTPUT."""
    type: str
    version: int
    hash_id: str


class PythonInfoDict(_RequiredPythonInfoDict, total=False):
    """Typed dictionary for the JSON representation of a V1 PythonInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, and `hash_id` to be present.

    :param str type: The type identifier for the block.
    :param int version: The version of the block's data structure.
    :param str hash_id: The unique hash identifier for the python information.
    :param str compiler: The compiler string.
    :param str implementation: The implementation string.
    :param str implementation_version: The implementation_version string.
    :param str python_version: The python_version string.
    :param str build: The build string.
    :param str release: The release string.
    :param str system: The system string.
    """
