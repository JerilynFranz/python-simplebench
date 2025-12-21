"""Error tags for machine info utilities."""
from simplebench.exceptions import ErrorTag
from simplebench.doc_utils import enum_docstrings


@enum_docstrings
class _MachineInfoErrorTag(ErrorTag):
    """Error tags for machine info utilities.

    :param GET_MACHINE_INFO_ERROR: Error occurred while getting machine info.
    :param CPU_INFO_ERROR: Error occurred while getting CPU info.
    """
    INVALID_NODE_PARAM = 'INVALID_NODE_PARAM'
    """Invalid 'node' parameter for MachineInfo initialization."""
