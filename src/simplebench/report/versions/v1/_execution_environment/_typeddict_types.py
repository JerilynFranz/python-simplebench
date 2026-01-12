"""Typed dictionaries for the V1 ExecutionEnvironment data structure.

This module defines four distinct dictionary types for handling ExecutionEnvironment data/

    - `ExecutionEnvironmentData`: For use as INPUT (e.g., to `from_dict`).
    - `ImmutableExecutionEnvironmentData`: An immutable version of `ExecutionEnvironmentData`.
    - `ExecutionEnvironmentDict`: For use as OUTPUT (e.g., from `to_dict`).
    - `ImmutableExecutionEnvironmentDict`: An immutable version of `ExecutionEnvironmentDict`.

    These types ensure proper validation and serialization of ExecutionEnvironment data
"""
from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired

# Imports are directly from the specific sub-modules to avoid accidentally creating circular dependencies
from .._python_info._typeddict_types import PythonInfoData, PythonInfoDict

__all__ = [
    "ExecutionEnvironmentData",
    "ImmutableExecutionEnvironmentData",
    "ExecutionEnvironmentDict",
    "ImmutableExecutionEnvironmentDict",
]

# --- For data used as INPUT (e.g., to `from_dict`) ---

class ExecutionEnvironmentData(ReportElementTypedDict, total=False):
    """Typed dictionary for V1 ExecutionEnvironment data used as INPUT.

    .. warning:: :class:`ImmutableExecutionEnvironmentData` does **NOT** inherit from :class:`ExecutionEnvironmentData`
        because of peculiarities of TypedDict inheritance and immutability signaling with extra_items.

        If it is needed to be used interchangeably with :class:`ExecutionEnvironmentDict`
        specify both types ``ExecutionEnvironmentDict | ImmutableExecutionEnvironmentDict``
        in the type annotations.

    The python property is optional here to allow for future extensions where other
    execution environments may be added. However, at least one property must be present.

    Any additional properties must conform to the :class:`CoreDataMappingType` type.

    This amounts to a mapping of string keys to arbitrary JSON-serializable values
    but excludes types that do not serialize cleanly to JSON.

    :param NotRequired[PythonInfoData] python: Information about the Python interpreter.
    """
    python: NotRequired[PythonInfoData]


class ImmutableExecutionEnvironmentData(ReportElementTypedDict, total=False):
    """Immutable typed dictionary for V1 ExecutionEnvironment data used as INPUT.
    
    .. warning::
        This class does **NOT** inherit from :class:`ExecutionEnvironmentData` because
        of peculiarities of TypedDict inheritance and immutability signaling with extra_items.

        If it is needed to be used interchangeably with :class:`ExecutionEnvironmentData`
        specify both types ``ExecutionEnvironmentData | ImmutableExecutionEnvironmentData``
        in the type annotations.

    The python property is optional here to allow for future extensions where other
    execution environments may be added. However, at least one property must be present.

    Additional properties declaring execution environments are allowed but not
    required. At least one property must be present (this is not enforced by the TypedDict itself
    but is a requirement of the JSON schema).

    Any additional properties must conform to the :class:`CoreDataMappingType` type.

    This amounts to a mapping of string keys to arbitrary JSON-serializable values
    but excludes types that do not serialize cleanly to JSON.

    The `__immutable__` class field is used to signal immutability to type checkers.
    Because it is typed as `NotRequired[Never]`, it cannot be set on instances and should never
    appear in runtime data.

    Python itself does not enforce immutability of dictionary instances, so it is the
    responsibility of the developer to ensure that constructed instances are composed
    solely of immutable types and containers. The TypedDict itself should actually be
    a :class:`MappingProxyType` or similar read-only view if runtime immutability is required.

    :param NotRequired[PythonInfoDict] python: Information about the Python interpreter.
    """
    __immutable__: NotRequired[Never]
    python: NotRequired[PythonInfoData]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class ExecutionEnvironmentDict(ReportElementTypedDict, total=False):
    """Typed dictionary for the JSON representation of a V1 ExecutionEnvironment (OUTPUT).

    This is a container for execution environment information.

    Additional properties declaring execution environments are allowed but not
    required. At least one property must be present (this is not enforced by the TypedDict itself
    but is a requirement of the JSON schema).

    Any additional properties must conform to the :class:`CoreDataMappingType` type. This
    is a mapping of string keys to arbitrary JSON-serializable values
    but excludes types that do not serialize cleanly to JSON.

    .. warning::
        :class:`ImmutableExecutionEnvironmentDict` does **NOT** inherit from :class:`ExecutionEnvironmentDict`
        because of peculiarities of :class:`TypedDict` inheritance and immutability signaling with extra_items.

        If it is needed to be used interchangeably with :class:`ExecutionEnvironmentDict`
        specify both types ``ExecutionEnvironmentDict | ImmutableExecutionEnvironmentDict``
        in the type annotations.

    :param NotRequired[PythonInfoDict] python: Information about the Python interpreter.
    """
    python: NotRequired[PythonInfoDict]


class ImmutableExecutionEnvironmentDict(ReportElementTypedDict, total=False):
    """Immutable typed dictionary for V1 ExecutionEnvironment data used as OUTPUT.

    ... warning::
        This class does **NOT** inherit from :class:`ExecutionEnvironmentDict` because
        of peculiarities of TypedDict inheritance and immutability signaling with extra_items.

        If it is needed to be used interchangeably with :class:`ExecutionEnvironmentDict`
        specify both types: ``ExecutionEnvironmentDict | ImmutableExecutionEnvironmentDict``.

    :param NotRequired[PythonInfoDict] python   : Information about the Python interpreter.
    """
    __immutable__: NotRequired[Never]
    python: NotRequired[PythonInfoDict]
