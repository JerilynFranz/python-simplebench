"""Error tags for machine info utilities."""
from simplebench.exceptions import ErrorTag
from simplebench.doc_utils import enum_docstrings


@enum_docstrings
class _MachineInfoErrorTag(ErrorTag):
    """Error tags for machine info utilities."""
    INVALID_NODE_PARAM = 'INVALID_NODE_PARAM'
    """Invalid 'node' parameter for MachineInfo initialization."""
