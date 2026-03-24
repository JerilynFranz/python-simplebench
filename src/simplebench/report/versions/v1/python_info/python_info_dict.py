"""Typed dictionaries for the V1 PythonInfo data structure.

This module defines dictionary types for handling PythonInfo data modeled on
:class:`~simplebench.report.versions.v1.PythonInfoSchema`.

- :class:`PythonInfoEnv`: Raw Python runtime/environment payload used in ``data``.
- :class:`ImmutablePythonInfoEnv`: Immutable counterpart of :class:`PythonInfoEnv`.
- :class:`PythonInfoData`: Input shape (e.g., for ``from_dict``) with relaxed optional metadata.
- :class:`ImmutablePythonInfoData`: Immutable counterpart of :class:`PythonInfoData`.
- :class:`PythonInfoDict`: Output shape (e.g., from ``to_dict``) with required metadata.
- :class:`ImmutablePythonInfoDict`: Immutable counterpart of :class:`PythonInfoDict`.

These types support validation-oriented typing for ingestion and serialization.
"""
from collections.abc import Mapping, Sequence

from simplebench.report.base import ReportElementTypedDict
from simplebench.simplebench_types import CoreDataSequence, Never, NotRequired, Required

__all__: list[str] = []


class PythonInfoEnv(ReportElementTypedDict):
    """Typed dictionary for the raw PythonInfo environment data collected from the system.

    :param python_version: The version of the Python interpreter.
    :type python_version: str
    :param implementation: The Python implementation (e.g., CPython, PyPy).
    :type implementation: str
    :param implementation_version: The version of the Python implementation.
    :type implementation_version: str
    :param compiler: The compiler used to build the Python interpreter.
    :type compiler: str
    :param revision: The revision identifier for the Python interpreter build.
    :type revision: str
    :param buildno: The build number for the Python interpreter.
    :type buildno: str
    :param builddate: The build date for the Python interpreter.
    :type builddate: str
    :param command_line_flags: The command line flags used when running the Python interpreter.
    :type command_line_flags: str
    :param gc_is_enabled: Whether garbage collection is enabled in the Python interpreter.
    :type gc_is_enabled: bool
    :param gc_thresholds: The garbage collection thresholds for the Python interpreter.
    :type gc_thresholds: Sequence[int]
    :param gc_counts: The garbage collection counts for the Python interpreter.
    :type gc_counts: Sequence[int]
    :param thread_switch_interval: The thread switch interval for the Python interpreter.
    :type thread_switch_interval: float
    :param architecture_bits: The architecture bits of the Python interpreter (e.g., '32bit', '64bit').
    :type architecture_bits: str
    :param architecture_linkage: The architecture linkage of the Python interpreter (e.g., 'ELF', 'WindowsPE').
    :type architecture_linkage: str
    :param xoptions: The xoptions used when running the Python interpreter.
    :type xoptions: Mapping[str, str | bool | int]
    :param sys_flags: The sys_flags used when running the Python interpreter.
    :type sys_flags: Mapping[str, int]
    :param gil_is_enabled: Whether the Global Interpreter Lock is enabled in the Python interpreter.
    :type gil_is_enabled: bool | None
    :param abiflags: The ABIFlags used by the Python interpreter.
    :type abiflags: str
    :param config_args: The configuration arguments used by the Python interpreter.
    :type config_args: str | None
    :param py_debug: Whether the Python interpreter is in debug mode.
    :type py_debug: bool | None
    :param with_pymalloc: Whether the Python interpreter is using PyMalloc.
    :type with_pymalloc: bool | None
    """
    python_version: Required[str]
    implementation: Required[str]
    implementation_version: Required[str]
    compiler: Required[str]
    revision: Required[str]
    buildno: Required[str]
    builddate: Required[str]
    command_line_flags: Required[str]
    gc_is_enabled: Required[bool]
    gc_thresholds: Required[Sequence[int]]
    gc_counts: Required[Sequence[int]]
    thread_switch_interval: Required[float]
    architecture_bits: Required[str]
    architecture_linkage: Required[str]
    xoptions: Required[Mapping[str, str | bool | int]]
    sys_flags: Required[Mapping[str, int]]
    gil_is_enabled: Required[bool | None]
    abiflags: Required[str]
    config_args: Required[str | None]
    py_debug: Required[bool | None]
    with_pymalloc: Required[bool | None]

class ImmutablePythonInfoEnv(ReportElementTypedDict):
    """Immutable version of :class:`PythonInfoEnv` for type-checking purposes.

    :param python_version: The version of the Python interpreter.
    :type python_version: str
    :param implementation: The Python implementation (e.g., CPython, PyPy).
    :type implementation: str
    :param implementation_version: The version of the Python implementation.
    :type implementation_version: str
    :param compiler: The compiler used to build the Python interpreter.
    :type compiler: str
    :param revision: The revision identifier for the Python interpreter build.
    :type revision: str
    :param buildno: The build number for the Python interpreter.
    :type buildno: str
    :param builddate: The build date for the Python interpreter.
    :type builddate: str
    :param command_line_flags: The command line flags used when running the Python interpreter.
    :type command_line_flags: str
    :param gc_is_enabled: Whether garbage collection is enabled in the Python interpreter.
    :type gc_is_enabled: bool
    :param gc_thresholds: The garbage collection thresholds for the Python interpreter.
    :type gc_thresholds: Sequence[int]
    :param gc_counts: The garbage collection counts for the Python interpreter.
    :type gc_counts: Sequence[int]
    :param thread_switch_interval: The thread switch interval for the Python interpreter.
    :type thread_switch_interval: float
    :param architecture_bits: The architecture bits of the Python interpreter (e.g., '32bit', '64bit').
    :type architecture_bits: str
    :param architecture_linkage: The architecture linkage of the Python interpreter (e.g., 'ELF', 'WindowsPE').
    :type architecture_linkage: str
    """
    python_version: Required[str]
    implementation: Required[str]
    implementation_version: Required[str]
    compiler: Required[str]
    revision: Required[str]
    buildno: Required[str]
    builddate: Required[str]
    command_line_flags: Required[str]
    gc_is_enabled: Required[bool]
    gc_thresholds: Required[CoreDataSequence[int]]
    thread_switch_interval: Required[float]
    architecture_bits: Required[str]
    architecture_linkage: Required[str]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability

# --- For data used as INPUT (e.g., to `from_dict`) ---

class PythonInfoData(ReportElementTypedDict):
    """Input TypedDict for PythonInfo data (e.g., ``from_dict``).

    This input shape is intentionally permissive for metadata fields:

    :param hash_id: The unique hash identifier for the python information.
    :type hash_id: NotRequired[str]
    :param type: The type identifier for the block.
    :type type: NotRequired[str]
    :param version: The version of the block's data structure.
    :type version: NotRequired[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
        It is optional, but always must be 'simplebench::python_info' for PythonInfo V1 data if present
    :type semantic_type: NotRequired[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[PythonInfoEnv]
    """
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    semantic_type: NotRequired[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[PythonInfoEnv]


class ImmutablePythonInfoData(ReportElementTypedDict):
    """Immutable version of :class:`PythonInfoData` (INPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`~simplebench.simplebench_types.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~simplebench.simplebench_types.Immutable`.

    :param hash_id: The unique hash identifier for the python information.
    :type hash_id: NotRequired[str]
    :param type: The type identifier for the block.
    :type type: NotRequired[str]
    :param version: The version of the block's data structure.
    :type version: NotRequired[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
        It is optional, but always must be 'simplebench::python_info' for PythonInfo V1 data if present
    :type semantic_type: NotRequired[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[ImmutablePythonInfoEnv]
    """
    hash_id: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[int]
    semantic_type: NotRequired[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[ImmutablePythonInfoEnv]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class PythonInfoDict(ReportElementTypedDict):
    """Typed dictionary for the JSON representation of a V1 PythonInfo (OUTPUT).

    This type is strict, requiring `type`, `version`, `hash_id`, and `semantic_type` to be present.

    :param hash_id: The unique hash identifier for the python information.
    :type hash_id: Required[str]
    :param type: The type identifier for the block.
    :type type: Required[str]
    :param version: The version of the block's data structure.
    :type version: Required[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
    :type semantic_type: Required[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[PythonInfoEnv]
    """
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    semantic_type: Required[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[PythonInfoEnv]


class ImmutablePythonInfoDict(ReportElementTypedDict):
    """Immutable version of :class:`PythonInfoDict` (OUTPUT).

    This marks the dictionary as immutable for type-checking purposes. During runtime,
    it should be constructed so as to enforce immutability.

    The :func:`~simplebench.simplebench_types.is_immutable` function will recognize this marker
    and treat instances of this type as :class:`~simplebench.simplebench_types.Immutable`.

    It is a stricter version of :class:`PythonInfoDict` that requires `data` to be an
    :class:`ImmutablePythonInfoEnv` (not just a :class:`PythonInfoEnv`).

    :param hash_id: The unique hash identifier for the python information.
    :type hash_id: Required[str]
    :param type: The type identifier for the block.
    :type type: Required[str]
    :param version: The version of the block's data structure.
    :type version: Required[int]
    :param semantic_type: The semantic type of the python information, formatted as 'namespace::type_name'.
        This dictates how the data should be interpreted. Users can define custom types using their own namespace
    :type semantic_type: Required[str]
    :param title: A human-readable title for this python information block.
    :type title: Required[str]
    :param description: A human-readable description for this python information block.
    :type description: NotRequired[str]
    :param data: The raw PythonInfo environment data collected from the system.
    :type data: Required[ImmutablePythonInfoEnv]
    """
    hash_id: Required[str]
    type: Required[str]
    version: Required[int]
    semantic_type: Required[str]
    title: Required[str]
    description: NotRequired[str]
    data: Required[ImmutablePythonInfoEnv]
    __immutable__: NotRequired[Never]  # Marker to indicate immutability
