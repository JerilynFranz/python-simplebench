"""Typed dictionaries for the V1 ResultsInfo data structure."""
from typing import TypedDict

from .value_block_dict import ValueBlockData, ValueBlockDict


# A base for fields that are always required and have the same type.
class _ResultsInfoCore(TypedDict, total=True):
    kwargs: dict[str, str]
    stats: dict[str, ValueBlockDict]


# --- For data used as INPUT (e.g., to `from_dict`) ---

class _RequiredResultsInfoData(_ResultsInfoCore, total=True):
    """Required fields for V1 ResultsInfo data used as INPUT."""


class ResultsInfoData(_RequiredResultsInfoData, total=False):
    """Typed dictionary for V1 ResultsInfo data used as INPUT.

    :param dict[str, str] kwargs: Keyword argument variations for this result.
    :param dict[str, ValueBlockData] stats: Statistical results.
    :param list[ValueBlockData] raw_results: (optional) Raw timing results.
    """
    raw_results: list[ValueBlockData]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredResultsInfoDict(_ResultsInfoCore, total=True):
    """Required fields for V1 ResultsInfo data used as OUTPUT."""


class ResultsInfoDict(_RequiredResultsInfoDict, total=False):
    """Typed dictionary for the JSON representation of a V1 ResultsInfo (OUTPUT).

    :param dict[str, str] kwargs: Keyword argument variations for this result.
    :param dict[str, ValueBlockDict] stats: Statistical results.
    :param list[ValueBlockDict] raw_results: (optional) Raw timing results.
    """
    raw_results: list[ValueBlockDict]
