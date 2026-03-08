"""Exception Error Tags for JSON Schema generation errors."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _JSONSchemaErrorTag(ErrorTag):
    """Error tags for JSON Schema generation errors."""

    SCHEMA_EXPORT_ERROR = auto()
    """Error exporting JSON schema as JSON."""
