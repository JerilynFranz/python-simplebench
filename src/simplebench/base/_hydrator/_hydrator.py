"""Base class for object <-> dictionary conversion and validation.

This module defines a base class `Hydrator` for objects, which includes methods
for initializing, converting to and from dictionaries, and validating against a
set of allowed parameters.
"""
import dataclasses
import inspect
from collections.abc import Callable, Iterable, Mapping
from copy import copy
from functools import cache
from typing import Any, Union, get_args, get_origin, get_type_hints, is_typeddict

from simplebench._log import _log

from .._typed_dict_key_info import TypedDictKeyInfo
from . import _validate

__all__: list[str] = []


class Hydrator:
    """Base class providing convenience methods for processing data dictionaries
    for object import operations for containers such as dataclasses or TypedDicts.
    It handles parameter introspection, data validation, default value application,
    and type processing for nested objects.

    It is intended to be used as a base class for other classes that need to
    import/export data from/to dictionaries with validation such as dataclasses
    or TypedDicts being serialized/deserialized to/from dictionaries where
    the data needs to be validated and processed into complex nested objects.

    It is not intended to be used for cases where simple **kwargs unpacking
    is sufficient, or where deep type checking is required beyond basic validation
    and processing.

    This class provides two main functionalities:
    1. Initializing a mapping of constructor parameters and their types (`init_params`)
       for a class using keyword-only arguments, and
    2. Importing and validating data from a dictionary based on allowed fields,
       optional fields, default values, matching rules, and processing functions. (`import_data`).

    Subclasses can utilize these methods to facilitate data import/export operations
    and ensure that the data conforms to expected formats and types.

    It is designed to allow easy import of complex nested data structures by allowing
    custom processing functions for specific fields during the import process (via
    the `process_as` parameter) while allowing customization of import rules. This includes
    specifying fields to be skipped, providing default values, specifying optional fields,
    and matching rules for fields during import.

    It uses type hints to determine the expected types of fields for validation purposes
    during import. Because it is mainly intended to be used for data serialization/deserialization
    of dictionaries using only basic Python types such as dictionaries, lists, and primitives,
    it does not implement deep type checking beyond what is necessary for basic validation
    and processing.

    Example usage:

    .. code-block:: python3
        :caption: Example of using Hydrator as a base class for data import/export.
        from typing import Any
        from simplebench.base.hydrator.hydrator import Hydrator

        data: dict[str, Any] = {'field1': 42, 'field2': {'some': 'data'}, 'field3': 3.14}

        MyDataClassInstance = MyDataClass.from_dict(data)


        class MyDataClass(Hydrator):
            '''A simple data class unpacking nested objects from dicts.'''

            def __init__(self, *, field1: int, field2: AnotherClass, field3: float = 0.0, field4: AThirdClass):
                self.field1 = field1
                self.field2 = field2
                self.field3 = field3
                self.field4 = field4

            @classmethod
            def from_dict(cls, data: dict[str, Any]) -> 'MyDataClass':
                allowed_fields = cls.init_params()

                def process_field4(value: dict) -> AThirdClass:
                    return AThirdClass(**value)

                validated_data = cls.import_data(
                    data=data,
                    allowed_fields=allowed_fields,
                    optional_fields=['field3'],
                    defaults={'field3': 0.0},
                    process_as={'field2': AnotherClass.from_dict, 'field4': process_field4},
                )
                return cls(**validated_data)

            def to_dict(self) -> dict[str, Any]:
                return {
                    'field1': self.field1,
                    'field2': self.field2.to_dict(),
                    'field3': self.field3,
                    'field4': {'value': self.field4.value},
                }


        class AThirdClass:
            '''Another simple class to demonstrate nested object processing
            of an unrelated class that can be constructed using a helper function
            shim to illustrate custom processing during data import.
            '''

            def __init__(self, *, value: float):
                self.value = value


        class AnotherClass:
            '''A simple class to demonstrate nested object processing

            This is a simple class that can be constructed from a dictionary
            using **kwargs unpacking to illustrate nested object handling
            in the Hydrator base class.

            It is the kind of class that might be used as a field by a Hydrator subclass
            but does not itself need to inherit from Hydrator.
            '''

            def __init__(self, *, some: str):
                self.some = some

            @classmethod
            def from_dict(cls, data: dict[str, Any]) -> 'AnotherClass':
                return cls(**data)

            def to_dict(self) -> dict[str, Any]:
                return {'some': self.some}


    """

    @classmethod
    @cache
    def init_params(cls, target_cls: type | None = None) -> dict[str, Any]:
        """Return a dictionary of the parameters and their types that can be
        passed to the constructor.

        It inspects the target class's `__init__` method to extract the keyword-only
        parameters and their type annotations and returns them as a dictionary.

        If the class is a TypedDict or a dataclass, it extracts the fields
        and their types accordingly.

        To use with TypedDicts, pass the TypedDict class itself as the `cls` parameter:

        .. code-block:: python3

            from typing import TypedDict


            class MyTypedDict(TypedDict):
                field1: int
                field2: str


            params = Hydrator.init_params(MyTypedDict)
            # params will be {'field1': int, 'field2': str}
            value = MyTypedDict(**params)

        It is used to help determine which fields are required for the constructor
        and what their types are during data import/export operations.

        Only keyword-only parameters are included. It uses `get_type_hints` to
        resolve annotations, including simple and generic types.

        It is cached to avoid recomputing it every time it is called.

        :param type | None target_cls: (optional) The target class to inspect. If None, uses the current class.
        :return dict[str, Any]: A dictionary mapping parameter names for the __init__ method to their types.
        """
        if target_cls is None:
            target_cls = cls

        # TypedDict support
        if is_typeddict(target_cls):
            return cls.init_params_for_typeddict(target_cls)

        # Dataclass support
        if dataclasses.is_dataclass(target_cls):
            return {field.name: field.type for field in dataclasses.fields(target_cls)}

        # Regular class logic (Python 3.10+)
        try:
            type_hints = get_type_hints(
                target_cls.__init__,
                globalns=vars(inspect.getmodule(target_cls)),
                localns=dict(vars(target_cls))
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return {}

        return {  # __immutable__ is internal marker for Immutable TypedDicts
            name: type_hints[name]
            for name, param in inspect.signature(target_cls.__init__).parameters.items()
            if name != '__immutable__' and param.kind == inspect.Parameter.KEYWORD_ONLY and name in type_hints
        }

    @classmethod
    def import_data(
        cls,
        *,
        data: Mapping[str, Any],
        allowed_fields: Mapping[str, Any],
        skip_fields: Iterable[str] | None = None,
        optional_fields: Iterable[str] | None = None,
        defaults: Mapping[str, Any] | None = None,
        match_on: Mapping[str, Any] | None = None,
        process_as: Mapping[str, Callable[[Any], Any]] | None = None,
    ) -> dict[str, Any]:
        """Process and validate the data dictionary.

        :param Mapping[str, Any] data: The data dictionary to process.
        :param Mapping[str, Any] allowed_fields: A dictionary of allowed input keys and their types.
                    It cannot be empty. The types must in the form suitable for isinstance checks.
                    e.g., str, int, list, dict, or (class, otherclass, ...) for multiple allowed types.

        :param Iterable[str] | None skip_fields: (optional) A list of input keys to NOT include in the output.
                    Only keys that are present in the `allowed_fields` dictionary can be skipped.
        :param Iterable[str] | None optional_fields: (optional) An iterable of input keys that are optional and
                    that can be omitted from the output if missing. Only keys that are present in the
                    `allowed_fields` dictionary can be optional.
        :param Mapping[str, Any] | None defaults: (optional) A dictionary of default values for keys
                    if they are not present.
                    If a key is present in the input data, the default value is not used.
                    If a value is set by the default, it is not considered missing.
                    Only keys that are present in the `optional_fields` dictionary can have default values.
        :param Mapping[str, Any] | None match_on: (optional) A dictionary of keys and values that must match the
                        corresponding keys in the input data. This is processed AFTER the default
                        values are applied. Only keys that are present in the `allowed_fields`
                        dictionary can have match_on rules.
        :param Mapping[str, Callable[[Any], Any]] | None process_as: (optional) A dictionary of keys and functions
                        to apply to the corresponding values in the input data before storing in the
                        output. This is processed AFTER the match_on rules for input are checked.
                        Only keys that are present in the `allowed_fields` dictionary can have
                        process_as rules.
        :return dict[str, Any]: The processed and validated data dictionary.
        :raises: SimpleBenchTypeError if the data does not match the rules.

        """
        data = _validate.data(data)
        allowed_fields_map = _validate.allowed(allowed_fields)
        skip_fields_set = _validate.skip(skip_fields or set(), allowed_fields_map)
        optional_fields_set = _validate.optional(optional_fields or set(), allowed_fields_map)
        defaults_for_fields = _validate.defaults(defaults or {}, optional_fields_set)
        match_on_fields = _validate.match_on(match_on or {}, allowed_fields_map)
        process_as_handlers = _validate.process_as(process_as or {}, allowed_fields_map)

        data = cls._apply_defaults(data, defaults_for_fields)
        _log.debug("Data after applying defaults: %s", data)
        _validate.match_on_values(data, match_on_fields)
        _log.debug("Data after match_on validation: %s", data)
        _validate.allowed_keys_against_data(data, allowed_fields_map)
        _log.debug("Data after allowed keys validation: %s", data)
        _validate.required_keys_against_data(data, allowed_fields_map, optional_fields_set)
        _log.debug("Data after required keys validation: %s", data)
        output = cls._apply_process_as_handlers(data, process_as_handlers)
        _log.debug("Data after applying process_as handlers: %s", output)
        output = cls._remove_skipped_fields(output, skip_fields_set)
        _log.debug("Data after removing skipped fields: %s", output)
        _validate.data_types(output, allowed_fields_map)
        _log.debug("Data after data types validation: %s", output)
        return output

    @staticmethod
    def _apply_defaults(data: dict[str, Any], defaults: Mapping[str, Any]) -> dict[str, Any]:
        """Apply default values to the data dictionary.

        :param dict[str, Any] data: The data dictionary to apply defaults to.
        :param Mapping[str, Any] defaults: The default values to apply.
        :return dict[str, Any]: The data dictionary with defaults applied.
        """
        output = copy(data)  # Shallow copy to avoid mutating input
        for field, default_value in defaults.items():
            if field not in output:
                output[field] = default_value
        return output

    @staticmethod
    def _apply_process_as_handlers(data: dict[str, Any], process_as_handlers: Mapping[str, Any]) -> dict[str, Any]:
        """Apply process_as functions to the output dictionary.

        :param dict[str, Any] data: The data dictionary to process.
        :param Mapping[str, Any] process_as_handlers: The process_as functions to apply.
        :return dict[str, Any]: A copy of the data dictionary with process_as functions applied.
        """
        output = copy(data)  # Shallow copy to avoid mutating input
        for field, process_func in process_as_handlers.items():
            if field in output:
                output[field] = process_func(output[field])
        return output

    @staticmethod
    def _remove_skipped_fields(data: dict[str, Any], skip_fields_set: set[str]) -> dict[str, Any]:
        """Remove skipped fields from the output dictionary.

        :param dict[str, Any] data: The data dictionary to process.
        :param set[str] skip_fields_set: The set of fields to skip.
        :return dict[str, Any]: The data dictionary with skipped fields removed.
        """
        output = copy(data)  # Shallow copy to avoid mutating input
        for field in skip_fields_set:
            if field in output:
                del output[field]
        return output

    @classmethod
    def init_params_for_typeddict(cls, typeddict_cls: type) -> dict[str, Any]:
        """Return a dictionary of the parameters and their types for a TypedDict class.

        It takes a TypedDict class as input and returns a dictionary mapping
        parameter names to their types based on the TypedDict's annotations.

        :param type typeddict_cls: The TypedDict class to inspect.
        :return dict[str, Any]: A dictionary mapping parameter names for the TypedDict to their types.
        """
        output: dict[str, Any] = {}
        _log.debug("Initializing TypedDict parameters for %s", typeddict_cls.__name__)
        if not is_typeddict(typeddict_cls):
            raise TypeError(f"Provided class {typeddict_cls.__name__} is not a TypedDict.")
        try:
            signature = inspect.signature(typeddict_cls)
        except ValueError:
            signature = None
        _log.debug("TypedDict %s signature: %s", typeddict_cls.__name__, signature)
        annotations = get_type_hints(typeddict_cls,
                                     globalns=vars(inspect.getmodule(typeddict_cls)),
                                     localns=dict(vars(typeddict_cls)))
        _log.debug("TypedDict %s annotations: %s", typeddict_cls.__name__, annotations)
        for key in annotations:
            if key == '__immutable__':
                continue
            value_info = TypedDictKeyInfo(key, typeddict_cls)
            value_type = value_info.value_type
            output[key] = cls._unwrap_typeddict_type(value_type)
        _log.debug("TypedDict %s: %s", typeddict_cls.__name__, output)
        return output

    @classmethod
    def _unwrap_typeddict_type(cls, tp: Any) -> Any:
        """Unwrap a type annotation to its base type for isinstance checks.

        - For generics (e.g., list[str]), returns the base type (list, dict, set, tuple, etc.).
        - For TypedDict, returns dict.
        - For primitives, returns the primitive type.
        - For unions, returns a tuple of the base types.
        - For Literal, returns a tuple of the literal values.
        - Otherwise, returns the type itself.

        :param Any tp: The type annotation to unwrap.
        :return Any: The base type suitable for isinstance checks.
        """
        if is_typeddict(tp):
            return dict

        origin = get_origin(tp)
        if origin is not None:
            # Handle Union types
            if (
                origin is getattr(__import__('typing'), 'Union', None)
                or origin is getattr(__import__('types'), 'UnionType', None)
                or origin is Union
            ):
                args = get_args(tp)
                return tuple(cls._unwrap_typeddict_type(arg) for arg in args)
            # Handle Literal types
            if origin is getattr(__import__('typing'), 'Literal', None):
                return get_args(tp)
            return origin

        return tp  # Fallback: return the type itself
