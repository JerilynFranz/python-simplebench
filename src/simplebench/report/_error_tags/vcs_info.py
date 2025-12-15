"""Error tags for VCSInfo reporter base class."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VCSInfoErrorTag(ErrorTag):
    """Error tags for VCSInfo reporter base class."""
    JSON_SCHEMA_VALIDATION_ERROR = "JSON_SCHEMA_VALIDATION_ERROR"
    """The JSON data does not conform to the expected schema."""
    INVALID_VERSION_TYPE = "INVALID_VERSION_TYPE"
    """The 'version' property is not of type 'int'."""
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    """The 'version' property is an unsupported version number."""
    INVALID_HASH_ID_PROPERTY_TYPE = "INVALID_HASH_ID_PROPERTY_TYPE"
    """The 'hash_id' property is not of type 'str'."""
    INVALID_HASH_ID_PROPERTY_VALUE = "INVALID_HASH_ID_PROPERTY_VALUE"
    """The 'hash_id' property is not a valid hash ID."""
