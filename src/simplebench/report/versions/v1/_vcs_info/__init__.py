"VCSInfo related classes and types for version 1 reports."

from ._typeddict_types import ImmutableVCSInfoData, ImmutableVCSInfoDict, VCSInfoData, VCSInfoDict
from ._vcs_info import VCSInfo
from ._vcs_info_schema import VCSInfoSchema

__all__ = ['VCSInfo', 'VCSInfoSchema', 'VCSInfoData', 'VCSInfoDict', 'ImmutableVCSInfoData', 'ImmutableVCSInfoDict']
