"""Mapping container for extras used in SimpleBench.

This is an immutable mapping of extra field names to their corresponding core data types.

This restricts the types of extras that can be stored to only those core data types supported by SimpleBench.

This allows for better type safety and consistency when handling extras within the SimpleBench framework.
"""

from collections.abc import Mapping

from simplebench.simplebench_types import CoreDataMapping, CoreDataTypes


class Extras(CoreDataMapping):
    """Mapping container for extras used in SimpleBench.

    Extras are additional metadata fields that can be associated with various
    SimpleBench entities such as benchmarks, test cases, and results.

    They are represented as a mapping from string keys to core data types
    where the keys are the names of the extra fields and the values are their
    corresponding core data values.

    The keys are restricted to be of type :class:`str` and conform to
    :func:`str.isidentifier` and the values must be of type :class:`CoreDataTypes`.
    """
    def __init__(self, __mapping: Mapping[str, CoreDataTypes]) -> None:
        """Construct an Extras instance.

        :param __mapping: The mapping of keys to core data types.
        :type __mapping: Mapping[str, CoreDataTypes]
        :raises SimpleBenchTypeError: If the __mapping argument is not a mapping of strings
            to core data types.
        :raises SimpleBenchTypeError: If any keys are not of type :class:`str` and a :func:`str.isidentifier`.
        :raises SimpleBenchTypeError: If any values are not of type :class:`CoreDataTypes`.
        """
        super().__init__(__mapping)
