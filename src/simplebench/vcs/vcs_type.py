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
    SVN = "svn"
    """Subversion (SVN) Version Control System."""
    PERFORCE = "perforce"
    """Perforce Version Control System."""
    TFVC = "tfvc"
    """Team Foundation Version Control (TFVC) System."""
    NONE = "none"
    """No Version Control System detected."""
