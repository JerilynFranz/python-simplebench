"""Mapping containers for variation cols used in SimpleBench.

This is an immutable mapping of variation field names to their corresponding string cols
for a specific variation.
"""

from collections.abc import Mapping

from simplebench.simplebench_types import CoreDataMapping

from . import _validate


class VariationCols(CoreDataMapping[str]):
    """Mapping container for variation cols used in SimpleBench.

    Maps variation field names to their corresponding string cols for a specific variation.

    Example:

    .. code-block:: python
        variation_cols = VariationCols({
            "input_size": "Input Size",
            "algorithm": "Algorithm",
        })

    """
    def __init__(self, cols: Mapping[str, str] | None = None) -> None:
        """Construct a VariationCols instance.

        If cols is None, creates an empty VariationCols.

        :param cols: The mapping of variation field names to their Cols.
        :type cols: Mapping[str, str] | None
        :raises SimpleBenchTypeError: If the cols argument is not a mapping of strings to strings, or
            if any keys are not valid identifiers.
        """
        data = _validate.data(cols or {})
        super().__init__(data)

    @classmethod
    def from_dict(cls, data: Mapping[str, str]) -> 'VariationCols':
        """Create a VariationCols instance from a dictionary.

        This is a compatability method for creating a VariationCols instance from a dictionary,
        such as when deserializing from JSON used by the Hydrate mechanism in the Report.from_dict method.

        :param data: The dictionary to create the VariationCols from.
        :type data: Mapping[str, str]
        :returns: A new VariationCols instance.
        :rtype: VariationCols
        :raises SimpleBenchTypeError: If the input data is not a mapping of strings to strings, or
            if any keys are not valid identifiers.
        """
        return cls(data)
