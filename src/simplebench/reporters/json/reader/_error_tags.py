"""Exceptions for JSON report reader."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _JSONReaderErrorTag(ErrorTag):
    """Error tags for JSON reporter reader exceptions."""

    INVALID_DICTIONARY_PROPERTY_TYPE = auto()
    """Invalid type for dictionary property assignment."""
    INVALID_FILEPATH_PROPERTY_TYPE = auto()
    """Invalid type for filepath property assignment."""
    FILE_NOT_FOUND = auto()
    """File not found at specified filepath."""
    NOT_A_FILE = auto()
    """Specified filepath is not a file."""
    JSON_DECODE_ERROR = auto()
    """Error decoding JSON."""
    SCHEMA_LOAD_ERROR = auto()
    """Error loading JSON reporter schema."""
    SCHEMA_VALIDATION_ERROR = auto()
    """Error validating JSON reporter schema."""
