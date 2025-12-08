"""VCS Types enumeration."""
from enum import Enum
from simplebench.enums import enum_docstrings


@enum_docstrings
class VCSType(str, Enum):
    """Enumeration of supported Version Control System types."""

    GIT = "git"
    """Git Version Control System."""
    HG = "hg"
    """Mercurial (Hg) Version Control System."""
    NONE = "none"
    """No Version Control System detected."""
