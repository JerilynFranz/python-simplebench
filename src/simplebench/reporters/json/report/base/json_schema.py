"""Base for JSON Schema classes."""
import json
from abc import ABC, abstractmethod
from functools import cache
from io import StringIO

from simplebench.exceptions import SimpleBenchTypeError

from ..exceptions import _JSONSchemaErrorTag


class JSONSchema(ABC):
    """Abstract Base class representing a JSON schema."""

    @classmethod
    @abstractmethod
    def as_dict(cls) -> dict:
        """Return the JSON schema as a dictionary.

        :return: JSON schema dictionary.
        """
        raise NotImplementedError("json_schema_dict must be implemented in subclasses.")

    @classmethod
    @cache
    def as_string(cls) -> str:
        """Return the JSON schema as a JSON formatted string.

        Usage:
            json_schema = JSONSchema.as_string()
        """
        schema_dict = cls.as_dict()
        with StringIO() as jsonfile:
            try:
                json.dump(schema_dict, jsonfile, indent=2)
                jsonfile.seek(0)
            # If an error occurs during dumping, it will be caught below
            # and is pretty much certain to be some version of type error
            # because the schema is a static dict. Bad programmer, no cookie.
            except Exception as exc:
                raise SimpleBenchTypeError(
                    f'Error generating JSON output for JSON Reporter schema: {exc}',
                    tag=_JSONSchemaErrorTag.SCHEMA_EXPORT_ERROR) from exc
            schema_text = jsonfile.read()
        return schema_text
