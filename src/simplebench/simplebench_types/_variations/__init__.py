"""Variations package

""Types used by SimpleBench for variations

- :class:`VariationCols` for variation columns used in SimpleBench.
- :class:`VariationMarks` all fields for parameterizing a single variation.
- :class:`KWArgsVariations` for multiple variations of fields for benchmark cases.

"""
# ruff: noqa F401

from ._variation_cols import VariationCols
from ._variation_marks import VariationMarks
from ._kwargs_variations import KWArgsVariations

# No * imports
__all__ = []
