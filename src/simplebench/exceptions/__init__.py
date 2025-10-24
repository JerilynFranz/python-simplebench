# -*- coding: utf-8 -*-
"""Custom exceptions for the simplebench package."""
import argparse
from enum import Enum
from typing import Any, Generic, TypeVar

from .base import ErrorTag
from .case import CaseErrorTag
from .cli import CLIErrorTag
from .decorators import DecoratorsErrorTag
from .iteration import IterationErrorTag
from .results import ResultsErrorTag
from .runners import RunnersErrorTag
from .session import SessionErrorTag
from .si_units import SIUnitsErrorTag
from .utils import UtilsErrorTag
from .tasks import RichTaskErrorTag, RichProgressTasksErrorTag
from .validators import ValidatorsErrorTag

__all__ = [
    "TaggedException",
    "SimpleBenchTypeError",
    "SimpleBenchValueError",
    "SimpleBenchKeyError",
    "SimpleBenchRuntimeError",
    "SimpleBenchNotImplementedError",
    "SimpleBenchAttributeError",
    "SimpleBenchArgumentError",
    "SimpleBenchImportError",
    "ErrorTag",
    "CaseErrorTag",
    "CLIErrorTag",
    "DecoratorsErrorTag",
    "IterationErrorTag",
    "RichProgressTasksErrorTag",
    "RichTaskErrorTag",
    "ResultsErrorTag",
    "RunnersErrorTag",
    "SessionErrorTag",
    "SIUnitsErrorTag",
    "UtilsErrorTag",
    "ValidatorsErrorTag",
]


E = TypeVar('E', bound=Exception)


class TaggedException(Exception, Generic[E]):
    """
    A generic exception that can be specialized with a base exception type
    and requires a tag during instantiation.

    This class extends the built-in Exception class and adds a mandatory tag
    attribute. The tag is intended to provide additional context or categorization
    for the exception.

    The tag must be an instance of Enum to ensure a controlled set of possible tags and
    must be the first argument provided during instantiation if passed positionally.

    It is used by other exceptions in the simplebench package to provide
    standardized error tagging for easier identification and handling of specific error conditions.
    and is used to create exceptions with specific tags for error handling and identification.
    with this base class.

    Example:

    class MyTaggedException(TaggedException[ValueError]):
    '''A tagged exception that is a specialized ValueError.'''

    raise MyTaggedException("An error occurred", tag=MyErrorTags.SOME_ERROR)


    Args:
        tag (Enum, keyword): An Enum member representing the error code.
        *args: Positional arguments to pass to the base exception's constructor.
        **kwargs: Keyword arguments to pass to the base exception's constructor.

    Attributes:
        tag_code: Enum
    """
    def __init__(self, *args: Any, tag: Enum, **kwargs: Any) -> None:
        """
        Initializes the exception with a mandatory tag.

        Args:
            *args: Positional arguments to pass to the base exception's constructor.
            tag (Enum, keyword): An Enum member representing the error code.
            **kwargs: Keyword arguments to pass to the base exception's constructor.
        """
        if not isinstance(tag, Enum):
            raise TypeError("Missing or wrong type 'tag' argument (must be Enum)")
        self.tag_code = tag
        super().__init__(*args, **kwargs)


class SimpleBenchTypeError(TaggedException[ValueError]):
    """Base class for all SimpleBench type errors.

    It differs from a standard TypeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchTypeError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str, positional): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchTypeError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchValueError(TaggedException[ValueError]):
    """Base class for all SimpleBench value errors.

    It differs from a standard ValueError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchValueError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchKeyError(TaggedException[KeyError]):
    """Base class for all SimpleBench key errors.

    It differs from a standard KeyError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchKeyError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchKeyError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchRuntimeError(TaggedException[RuntimeError]):
    """Base class for all SimpleBench runtime errors.

    It differs from a standard RuntimeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchRuntimeError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchRuntimeError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchNotImplementedError(TaggedException[NotImplementedError]):
    """Base class for all SimpleBench not implemented errors.

    It differs from a standard NotImplementedError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchNotImplementedError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchNotImplementedError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)


class SimpleBenchAttributeError(TaggedException[AttributeError]):
    """Base class for all SimpleBench attribute errors.

    It differs from a standard AttributeError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchAttributeError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
        name (str | None): The attribute name.
        obj (object): The object the attribute was not found on.
    """
    def __init__(self, msg: str, *, tag: ErrorTag, name: str | None = None, obj: object = ..., ) -> None:
        """Raises a SimpleBenchAttributeError with the given message, name, obj, and tag.

        Args:
            msg (str): The error message.
            name (str | None): The attribute name.
            obj (object): The object the attribute was not found on.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag, name=name, obj=obj)


class SimpleBenchArgumentError(TaggedException[argparse.ArgumentError]):
    """Base class for re-raising all SimpleBench ArgumentError errors.

    It is designed to be used in places where an argparse.ArgumentError
    would be appropriate and for re-raising ArgumentErrors
    caught from argparse operations.

    It differs from a argparse.ArgumentError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support
    and by directly setting the argument_name property to the name of the
    argument that caused the error. This is because the argparse.ArgumentError
    constructor expects an argparse.Action instance as the first argument
    and that is not always available when re-raising the exception.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchArgumentError(argument_name="my-arg",
                                       message="An error occurred",
                                       tag=MyErrorTags.SOME_ERROR)

    Args:
        argument_name (str | None): The argument name.
        message (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, argument_name: str | None, message: str, *, tag: ErrorTag) -> None:
        # argparse.ArgumentError has a specific signature we must adapt to. It expects
        # to get an argparse.Action instance as the first argument to infer the
        # argument_name from, which we don't have here, and so must backfill the argument_name
        # after initialization.
        if tag.__doc__ is None:
            message = f"{message}: {tag.value}"
        else:
            message = f"{message}: {tag.__doc__}"
        super().__init__(None, message, tag=tag)
        self.argument_name = argument_name


class SimpleBenchImportError(TaggedException[ImportError]):
    """Base class for all SimpleBench import errors.

    It differs from a standard ImportError by the addition of a
    tag code used to very specifically identify where the error
    was thrown in the code for testing and development support.

    This tag code does not have a direct semantic meaning except to identify
    the specific code throwing the exception for tests.

    Usage:
        raise SimpleBenchImportError("An error occurred", tag=MyErrorTags.SOME_ERROR)

    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchImportError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        if tag.__doc__ is None:
            message = f"{msg}: {tag.value}"
        else:
            message = f"{msg}: {tag.__doc__}"
        super().__init__(message, tag=tag)
