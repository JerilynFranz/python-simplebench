"""Typed dictionaries for the V1 ValueBlock data structure.

This module defines two distinct dictionary types for handling ValueBlock data,
both modeled on the JSON schema for version 1 ValueBlocks in
version 1: :class:`~simplebench.report.versions.v1.value_block.value_block_schema.ValueBlockSchema`.

    - `ValueBlockData`: For use as INPUT (e.g., to `from_dict`). It is more
    lenient, accepting `int` or `float` for the `value` field and making `type` and `version` optional.
    - `ValueBlockDict`: For use as OUTPUT (e.g., from `to_dict`). It is
    stricter, guaranteeing that `value` is a `float` and that `type` and `version` are present.

    These types ensure proper validation and serialization of ValueBlock data"""
from simplebench.report.base import ValueBlockDataBase


# A base for fields that are always required and have the same type.
class _ValueBlockCore(ValueBlockDataBase, total=True):
    semantic_type: str
    unit: str
    scale: float

# --- For data used as INPUT (e.g., to `from_dict`) ---


class _RequiredValueBlockData(_ValueBlockCore, total=True):
    """Required fields for V1 ValueBlock data used as INPUT."""
    value: float | int  # Accepts int or float, as per JSON 'number' type


class ValueBlockData(_RequiredValueBlockData, total=False):
    """Typed dictionary for V1 ValueBlock data used as INPUT.

    This type is lenient, allowing `type`, `version`, and `timer` to be
    omitted, and accepting `int` or `float` for the `value` field.

    :param str semantic_type: The semantic type of the value.
    :param str unit: The unit of the value.
    :param float scale: The scaling factor for the value.
    :param int | float value: The numeric value of the block.
    :param str type: (optional) The type identifier for the block.
    :param int version: (optional) The version of the block's data structure.
    :param str timer: (optional) The name of the timer associated with this value.
    """
    type: str
    version: int
    timer: str


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class _RequiredValueBlockDict(_ValueBlockCore, total=True):
    """Required fields for V1 ValueBlock data used as OUTPUT."""
    type: str
    version: int
    value: float  # Guaranteed to be a float on output


class ValueBlockDict(_RequiredValueBlockDict, total=False):
    """Typed dictionary for the JSON representation of a V1 ValueBlock (OUTPUT).

    This type is strict, requiring `type` and `version` to be present and
    guaranteeing that `value` is a `float`. The `timer` field remains optional.

    :param str type: The type identifier for the block.
    :param int version: The version of the block's data structure.
    :param str semantic_type: The semantic type of the value.
    :param str unit: The unit of the value.
    :param float scale: The scaling factor for the value.
    :param float value: The numeric value of the block (guaranteed to be float).
    :param str timer: (optional) The name of the timer associated with this value.
    """
    timer: str
