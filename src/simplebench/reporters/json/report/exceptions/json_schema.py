"""Exception Error Tags for JSON Schema generation errors."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _JSONSchemaErrorTag(ErrorTag):
    """Error tags for JSON Schema generation errors."""
    SCHEMA_EXPORT_ERROR = 'SCHEMA_EXPORT_ERROR'
    """Error exporting JSON schema as JSON."""
