"""Base class for object <-> dictionary conversion and validation.

This module defines a base class `Hydrator` for objects, which includes methods
for initializing, converting to and from dictionaries, and validating against a
set of allowed parameters.
"""
import dataclasses
import inspect
from collections.abc import Mapping
from copy import copy
from functools import cache
from typing import Any, Callable, Iterable, get_type_hints, is_typeddict


from . import validate


class Hydrator:
    """Base class providing convience methods for processing a JSON object."""

    @classmethod
    @cache
    def init_params(cls) -> dict[str, Any]:
        """Return a dictionary of the parameters that can be passed to the constructor.

        It is used to help determine which fields are required for the constructor
        and what their types are.

        Only keyword-only parameters are included. It uses `get_type_hints` to
        resolve annotations, including simple and generic types.

        It is cached to avoid recomputing it every time it is called.
        """
        # TypedDict support
        if is_typeddict(cls):
            return dict(cls.__annotations__)

        # Dataclass support
        if dataclasses.is_dataclass(cls):
            return {field.name: field.type for field in dataclasses.fields(cls)}

        # Regular class logic (Python 3.10+)
        try:
            type_hints = get_type_hints(cls.__init__)
        except Exception:  # pylint: disable=broad-exception-caught
            return {}

        return {
            name: type_hints[name]
            for name, param in inspect.signature(cls.__init__).parameters.items()
            if param.kind == inspect.Parameter.KEYWORD_ONLY and name in type_hints
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
        process_as: Mapping[str, Callable[[Any], Any]] | None = None
    ) -> dict[str, Any]:
        """Process and validate the data dictionary.

        :param Mapping[str, Any] data: The data dictionary to process.
        :param Mapping[str, Any] allowed_fields: A dictionary of allowed input keys and their types. It cannot be empty.
        :param Iterable[str] | None skip_fields: A list of input keys to NOT include in the output.
                    Only keys that are present in the `allowed_fields` dictionary can be skipped.
        :param Iterable[str] | None optional_fields: An iterable of input keys that are optional and
                    that can be omitted from the output if missing. Only keys that are present in the
                    `allowed_fields` dictionary can be optional.
        :param Mapping[str, Any] | None defaults: A dictionary of default values for keys if they are not present.
                    If a key is present in the input data, the default value is not used.
                    If a value is set by the default, it is not considered missing.
                    Only keys that are present in the `optional_fields` dictionary can have default values.
        :param Mapping[str, Any] | None match_on: A dictionary of keys and values that must match the
                        corresponding keys in the input data. This is processed AFTER the default
                        values are applied. Only keys that are present in the `allowed_fields`
                        dictionary can have match_on rules.
        :param Mapping[str, Callable[[Any], Any]] | None process_as: A dictionary of keys and functions
                        to apply to the corresponding values in the input data before storing in the
                        output. This is processed AFTER the match_on rules for input are checked.
                        Only keys that are present in the `allowed_fields` dictionary can have
                        process_as rules.
        :return dict[str, Any]: The processed and validated data dictionary.
        :raises: SimpleBenchTypeError if the data does not match the rules.

        Raises:
            SimpleBenchValueError: If the data does not match the rules.
        """
        data = validate.data(data)
        allowed_fields_map = validate.allowed(allowed_fields)
        skip_fields_set = validate.skip(skip_fields or set(), allowed_fields_map)
        optional_fields_set = validate.optional(optional_fields or set(), allowed_fields_map)
        defaults_for_fields = validate.defaults(defaults or {}, optional_fields_set)
        match_on_fields = validate.match_on(match_on or {}, allowed_fields_map)
        process_as_handlers = validate.process_as(process_as or {}, allowed_fields_map)

        data = cls._apply_defaults(data, defaults_for_fields)
        validate.match_on_values(data, match_on_fields)
        validate.allowed_keys_against_data(data, allowed_fields_map)
        validate.required_keys_against_data(data, allowed_fields_map, optional_fields_set)
        output = copy(data)  # Shallow copy to avoid mutating input
        output = cls._apply_process_as_handlers(output, process_as_handlers)
        output = cls._remove_skipped_fields(output, skip_fields_set)
        validate.data_types(output, allowed_fields_map)
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
