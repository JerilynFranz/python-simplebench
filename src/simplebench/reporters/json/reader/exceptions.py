"""Exceptions for JSON report reader."""

from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _JSONReaderErrorTag(ErrorTag):
    """Error tags for JSON reporter reader exceptions."""
    INVALID_DICTIONARY_PROPERTY_TYPE = 'INVALID_DICTIONARY_PROPERTY_TYPE'
    """Invalid type for dictionary property assignment."""
    INVALID_FILEPATH_PROPERTY_TYPE = 'INVALID_FILEPATH_PROPERTY_TYPE'
    """Invalid type for filepath property assignment."""
    FILE_NOT_FOUND = 'FILE_NOT_FOUND'
    """File not found at specified filepath."""
    NOT_A_FILE = 'NOT_A_FILE'
    """Specified filepath is not a file."""
    JSON_DECODE_ERROR = 'JSON_DECODE_ERROR'
    """Error decoding JSON."""
    SCHEMA_LOAD_ERROR = 'SCHEMA_LOAD_ERROR'
    """Error loading JSON reporter schema."""
    SCHEMA_VALIDATION_ERROR = 'SCHEMA_VALIDATION_ERROR'
    """Error validating JSON reporter schema."""
