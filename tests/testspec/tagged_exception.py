"""TestSpec testing framework - tagged exceptions."""
from enum import Enum
from typing import Any, Generic, TypeVar

E = TypeVar('E', bound=Exception)


class TaggedException(Exception, Generic[E]):
    """
    A generic exception that can be specialized with a base exception type
    and requires a tag during instantiation.

    This helper class extends the built-in Exception class and adds a mandatory tag
    attribute usable by the testspec framework. The testspec framework uses this class
    to create exceptions with specific tags for error handling and identification.

    Tagged exceptions are intended to provide additional context or categorization
    for the exception when testing but are not mandatory when testing exceptions.

    To create a tagged exception, subclass this class with the desired base exception type.
    The base exception type must be a subclass of Exception.
    The subclassed tagged exception can then be raised like a normal exception,

    The tag must be an instance of Enum to ensure a controlled set of possible tags.

    It is used by other exceptions in the typechecked package to provide
    standardized error tagging for easier identification and handling of specific error conditions.
    and is used to create exceptions with specific tags for error handling and identification.
    with this base class.

    Example:

        from testspec import TaggedException

        class MyTaggedValueError(TaggedException[ValueError]):
        '''A tagged exception that is a specialized ValueError.'''

        raise MyTaggedValueError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    :param args: Positional arguments to pass to the base exception's constructor.
    :type args: Any
    :param tag: An Enum member representing the error code.
    :type tag: Enum
    :param kwargs: Keyword arguments to pass to the base exception's constructor.
    :type kwargs: Any
    :ivar tag_code: The tag code for the exception.
    :vartype tag_code: Enum
    """
    __test__ = False  # Prevent pytest from trying to collect this class as a test case

    def __init__(self, *args: Any, tag: Enum, **kwargs: Any) -> None:
        """
        Initializes the exception with a mandatory tag.

        :param args: Positional arguments to pass to the base exception's constructor.
        :type args: Any
        :param tag: An Enum member representing the error code.
        :type tag: Enum
        :param kwargs: Keyword arguments to pass to the base exception's constructor.
        :type kwargs: Any
        """
        if not isinstance(tag, Enum):
            raise TypeError("Missing or wrong type 'tag' argument (must be Enum)")
        self.tag_code = tag
        super().__init__(*args, **kwargs)
