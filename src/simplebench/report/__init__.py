"""JSON Report public API."""

from types import ModuleType

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from ._error_tags import _ReportErrorTag
from .versions import v1

CURRENT: ModuleType = v1


def get_report_version(version: int) -> ModuleType:
    """Get the report module for the specified version.

    :param version: The report version number.
    :return: The report module corresponding to the version.
    :raises TypeError: If the version is not an integer.
    :raises ValueError: If the version is unsupported.
    """
    if not isinstance(version, int):
        raise SimpleBenchTypeError('version must be an integer', tag=_ReportErrorTag.INVALID_VERSION_TYPE)

    match version:
        case 1:
            return v1
        case _:
            raise SimpleBenchValueError(
                f'Unsupported report version: {version}', tag=_ReportErrorTag.UNSUPPORTED_VERSION
            )


__all__: list[str] = []
