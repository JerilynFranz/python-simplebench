# -*- coding: utf-8 -*-
"""Custom exceptions for the simplebench package."""
import argparse
import re
from enum import Enum
from textwrap import dedent
from typing import Any, Generic, TypeVar

from .base import ErrorTag
from .case import _CaseErrorTag
from .cli import _CLIErrorTag
from .decorators import _DecoratorsErrorTag
from .iteration import _IterationErrorTag
from .results import _ResultsErrorTag
from .runners import _RunnersErrorTag
from .session import _SessionErrorTag
from .si_units import _SIUnitsErrorTag
from .tasks import _RichProgressTasksErrorTag, _RichTaskErrorTag
from .utils import _UtilsErrorTag

__all__ = [
    "TaggedException",
    "SimpleBenchBenchmarkError",
    "SimpleBenchTypeError",
    "SimpleBenchValueError",
    "SimpleBenchKeyError",
    "SimpleBenchRuntimeError",
    "SimpleBenchNotImplementedError",
    "SimpleBenchAttributeError",
    "SimpleBenchArgumentError",
    "SimpleBenchImportError",
    "ErrorTag",
    "_CaseErrorTag",
    "_CLIErrorTag",
    "_DecoratorsErrorTag",
    "_IterationErrorTag",
    "_RichProgressTasksErrorTag",
    "_RichTaskErrorTag",
    "_ResultsErrorTag",
    "_RunnersErrorTag",
    "_SessionErrorTag",
    "_SIUnitsErrorTag",
    "_UtilsErrorTag",
]


E = TypeVar('E', bound=Exception)


def dedent_and_normalize_whitespace(text: str) -> str:
    """Dedent and and normalize whitespace.

    * \\n and \\t characters are removed.
    * Leading and trailing whitespace is removed.
    * Multiple consecutive whitespace characters are reduced to a single space.

    Args:
        text (str): The text to dedent and strip.

    Returns:
        str: The dedented and normalized text.
    """
    dedented_text = dedent(text)
    no_newlines_tabs = dedented_text.replace('\n', ' ').replace('\t', ' ')
    normalized_whitespace = re.sub(re.compile(r'\s+'), ' ', no_newlines_tabs)
    return normalized_whitespace.strip()


def generate_message(msg: str, tag: ErrorTag) -> str:
    """Generate an error message with the given tag.

    Args:
        msg (str): The base error message.
        tag (ErrorTag): The error tag.

    Returns:
        str: The generated error message.
    """
    if tag.__doc__ is None:
        message = f"{msg}: {tag.value}"
    else:
        message = f"{msg}: {dedent_and_normalize_whitespace(tag.__doc__)}"
    return message.replace('\n', '')


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
        message = generate_message(msg, tag)
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
        """Raises a SimpleBenchValueError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        message = generate_message(msg, tag)
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
        message = generate_message(msg, tag)
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
        message = generate_message(msg, tag)
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
        message = generate_message(msg, tag)
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
        message = generate_message(msg, tag)
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
        message = generate_message(message, tag)
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
        message = generate_message(msg, tag)
        super().__init__(message, tag=tag)


class SimpleBenchTimeoutError(TaggedException[TimeoutError]):
    """Exceptions raised for timeout implementations.

    Usage:
        raise SimpleBenchTimeoutError("An error occurred",
                                       tag=MyErrorTags.SOME_ERROR,
                                       func_name="my_function")
    Args:
        msg (str): The error message.
        func_name (str | None): The name of the function that timed out.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag, func_name: str | None = None) -> None:
        """Raises a SimpleBenchTimeoutError with the given message and tag.

        Args:
            msg (str): The error message.
            func_name (str | None): The name of the function that timed out.
            tag (ErrorTag): The tag code.
        """
        message = generate_message(msg, tag)
        super().__init__(message, tag=tag)
        self.func_name: str | None = func_name


class SimpleBenchUsageError(TaggedException[RuntimeError]):
    """Exceptions raised for CLI usage errors.

    Usage:
        raise SimpleBenchUsageError("An error occurred",
                                    tag=MyErrorTags.SOME_ERROR)
    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchTimeoutError with the given message and tag.

        Args:
            msg (str): The error message.
            func_name (str | None): The name of the function that timed out.
            tag (ErrorTag): The tag code.
        """
        message = generate_message(msg, tag)
        super().__init__(message, tag=tag)


class SimpleBenchBenchmarkError(TaggedException[RuntimeError]):
    """Exceptions raised for benchmark execution errors.

    If an exception occurs during the execution of a benchmark,
    it can be wrapped in a SimpleBenchBenchmarkError to provide
    additional context and tagging.

    Usage:
        raise SimpleBenchBenchmarkError("An error occurred",
                                        tag=MyErrorTags.SOME_ERROR)
    Args:
        msg (str): The error message.
        tag (ErrorTag): The tag code.
    """
    def __init__(self, msg: str, *, tag: ErrorTag) -> None:
        """Raises a SimpleBenchBenchmarkError with the given message and tag.

        Args:
            msg (str): The error message.
            tag (ErrorTag): The tag code.
        """
        message = generate_message(msg, tag)
        super().__init__(message, tag=tag)