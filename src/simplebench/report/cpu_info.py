"""JSON cpu info classes"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ._error_tags import _CPUInfoErrorTag

_DEFERRED_IMPORTS_LOADED: bool = False

if TYPE_CHECKING:
    from ._base import BaseCPUInfo
    from .versions.__notinit__ import json_class
    _DEFERRED_IMPORTS_LOADED = True  # To avoid import issues during type checking

else:
    json_class = None   # pylint: disable=invalid-name

def _load_deferred_imports() -> None:
    """Load deferred imports."""
    global _DEFERRED_IMPORTS_LOADED, json_class  # pylint: disable=global-statement
    if not _DEFERRED_IMPORTS_LOADED:
        from .versions.__notinit__ import json_class  # pylint: disable=import-outside-toplevel
        _DEFERRED_IMPORTS_LOADED = True


def cpu_info_by_version(version: int) -> type[BaseCPUInfo]:
    """Retrieve a CPUInfo instance for the specified version.

    :param version: The JSON report version number.
    :return: A CPUInfo class for the specified version.
    """
    _load_deferred_imports()

    return json_class(
        version,
        BaseCPUInfo,
        _CPUInfoErrorTag.INVALID_VERSION_TYPE,
        _CPUInfoErrorTag.UNSUPPORTED_VERSION
    )
