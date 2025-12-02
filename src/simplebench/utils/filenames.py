"""Utility functions for file names."""
import re

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from .exceptions import _UtilsErrorTag

# Finds all characters that are not a-z, A-Z, 0-9, _ (underline), or - (dash)
_SANITIZE_FILENAME_RE = re.compile(r'[^-a-zA-Z0-9_]+')
# Finds one or more sequential _ (underline) characters
_COLLAPSE_UNDERSCORES_RE = re.compile(r'_+')


def sanitize_filename(name: str) -> str:
    """Sanitizes a filename by replacing invalid characters with _ (underline).

    Only a-z, A-Z, 0-9, _  (underline), and - (dash) characters are allowed. All other
    characters are replaced with _ and multiple sequential _ characters are then
    collapsed to single _ characters. Leading and trailing _ and - characters are removed.


    Examples:

    .. code-block:: python3

        sanitize_filename("My File-Name.txt")  # returns "My_File-Name_txt"
        sanitize_filename("Invalid/Chars\\In:Name*?")  # returns "Invalid_Chars_In_Name"
        sanitize_filename("   Leading and Trailing   ")  # returns "Leading_and_Trailing"
        sanitize_filename("!!!")  # returns "_"

    .. note::
        This function does not check for reserved filenames on any operating system.

        It is the caller's responsibility to ensure the sanitized filename is valid
        for the target filesystem.

        If a filename becomes completely empty after sanitization, the function will return
        a single underscore ('_') character. This is the one exception to the rule that
        leading and trailing _ and - characters are removed.

    :param name: The filename to sanitize.
    :type name: str
    :return: The sanitized filename.
    :rtype: str
    :raises SimpleBenchTypeError: If the ``name`` arg is not a str.
    :raises SimpleBenchValueError: If the ``name`` arg is an empty string.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            "name arg must be a str",
            tag=_UtilsErrorTag.SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE)
    if name == '':
        raise SimpleBenchValueError(
            "name arg must not be an empty string",
            tag=_UtilsErrorTag.SANITIZE_FILENAME_EMPTY_NAME_ARG)
    first_pass: str = re.sub(_SANITIZE_FILENAME_RE, '_', name)
    second_pass: str = re.sub(_COLLAPSE_UNDERSCORES_RE, '_', first_pass)
    third_pass: str = second_pass.strip('_-')
    return '_' if third_pass == '' else third_pass
