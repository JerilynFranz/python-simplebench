"""The tagged exception base class.

This module defines the TaggedException base class, which extends the built-in Exception class
and adds a mandatory tag attribute. The tag is intended to provide additional context or categorization
for the exception. The tag is an instance of Enum to ensure a controlled set of possible tags.
This ensures that the tag is always valid and can be used to categorize exceptions in a consistent
and meaningful way.

There is only one public class in this module, :class:`TaggedException`, which is
designed to be subclassed by other exceptions in the simplebench package
to provide standardized error tagging for easier identification and handling
of specific error conditions.

"""

from typing import Any

from .error_tag import ErrorTag

# __all__ is empty because this module is designed for explicit imports only.
__all__: list[str] = []


class TaggedException(Exception):
    """
    A generic exception that can be specialized with a base exception type
    and requires a tag during instantiation.

    This class extends the built-in Exception class and adds a mandatory tag
    attribute. The tag is intended to provide additional context or categorization
    for the exception.

    The tag must be an instance of ErrorTag to ensure a controlled set of possible tags and
    must be the first argument provided during instantiation if passed positionally.

    It is used by other exceptions in the simplebench package to provide
    standardized error tagging for easier identification and handling of specific error conditions.
    and is used to create exceptions with specific tags for error handling and identification.
    with this base class.

    Example:

    .. code-block:: python

        from enum import auto
        from simplebench.doc_utils import enum_docstrings
        from simplebench.exceptions import ErrorTag, TaggedException


        @enum_docstrings
        class MyErrorTags(ErrorTag):
            SOME_ERROR = auto()
            '''Some error occurred.'''
            ANOTHER_ERROR = auto()
            '''Another error occurred.'''

        class MyTaggedException(TaggedException, ValueError):
            '''A tagged exception that is a specialized ValueError.'''

        raise MyTaggedException("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        tag (ErrorTag): An ErrorTag Enum member representing the error code.
        *args: Positional arguments to pass to the base exception's constructor.
        **kwargs: Keyword arguments to pass to the base exception's constructor.

    Attributes:
        tag_code: ErrorTag Enum member representing the error code associated with
        this exception.
    """

    def __init__(self, *args: Any, tag: ErrorTag, **kwargs: Any) -> None:
        """
        Initializes the exception with a mandatory tag.

        Args:
            *args: Positional arguments to pass to the base exception's constructor.
            tag (ErrorTag): An ErrorTag Enum member representing the error code.
            **kwargs: Keyword arguments to pass to the base exception's constructor.
        """
        if not isinstance(tag, ErrorTag):
            raise TypeError(f'tag argument must be an instance of ErrorTag, got {type(tag).__name__}')
        self.tag_code = tag
        super().__init__(*args, **kwargs)
