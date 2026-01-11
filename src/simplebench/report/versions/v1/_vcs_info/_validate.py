"""Validation functions for VCSInfo version 1 data."""
import re

from simplebench.report._error_tags import _VCSInfoErrorTag
from simplebench.validators import validate_bool, validate_iso8601_datetime, validate_string, validate_string_with_regex

_HASH_ID_REGEX = re.compile(r'^[a-fA-F0-9]{64}$')

def hash_id(value: str) -> str:
    """Validate the hash_id string.

    An empty string is allowed, which indicates that the hash_id should be
    computed automatically.

    :param value: The unique hash identifier for the vcs information.
    :return: The validated hash_id string.
    :raises SimpleBenchTypeError: If the hash_id value is not a string.
    """
    value = validate_string(
            value, "hash_id",
            _VCSInfoErrorTag.INVALID_HASH_ID_TYPE,
            _VCSInfoErrorTag.INVALID_HASH_ID_VALUE,
            allow_empty=True, strip=True)

    return validate_string_with_regex(
            value, "hash_id", _HASH_ID_REGEX,
            _VCSInfoErrorTag.INVALID_HASH_ID_STRUCTURE,  # can't trigger type error here
            _VCSInfoErrorTag.INVALID_HASH_ID_STRUCTURE)

def vcs(value: str) -> str:
    """Validate the VCS type string.

    Validates that the VCS type is a non-empty/non-blank string.

    :param value: The version control system string.
    :return: The validated VCS type string.
    :raises SimpleBenchValueError: If the value type is empty or blank.
    :raises SimpleBenchTypeError: If the value type is not a string.
    """
    return validate_string(
            value, "vcs",
            _VCSInfoErrorTag.INVALID_VCS_TYPE,
            _VCSInfoErrorTag.INVALID_VCS_VALUE,
            strip=True, allow_empty=False)


def commit_id(value: str) -> str:
    """Validate the commit ID string.

    Validates that the commit ID is a non-empty/non-blank string.

    :param value: The unique identifier of the current revision.
    :return: The validated commit ID string. It cannot be blank or empty.
    :raises SimpleBenchValueError: If the commit ID is blank or empty.
    :raises SimpleBenchTypeError: If the commit ID is not a string.
    """
    return validate_string(
            value, "commit_id",
            _VCSInfoErrorTag.INVALID_COMMIT_ID_TYPE,
            _VCSInfoErrorTag.INVALID_COMMIT_ID_VALUE,
            strip=True, allow_empty=False)


def commit_datetime(value: str) -> str:
    """Validate the commit datetime string.

    :param value: The datetime of the commit in ISO 8601 format.
    :return: The validated commit datetime string.
    :raises SimpleBenchValueError: If the datetime string is not in valid ISO 8601 format.
    :raises SimpleBenchTypeError: If the datetime value is not a string.
    """
    return validate_iso8601_datetime(
            value, "commit_datetime",
            _VCSInfoErrorTag.INVALID_COMMIT_DATETIME_TYPE,
            _VCSInfoErrorTag.INVALID_COMMIT_DATETIME_VALUE)


def branch(value: str) -> str:
    """Validate the branch name string.

    It only checks that the value is a non-empty/non-blank string.

    :param value: The current branch name.
    :return: The validated branch name string. It cannot be blank or empty.
    :raises SimpleBenchTypeError: If the branch name is not a string.
    """
    return validate_string(
            value, "branch",
            _VCSInfoErrorTag.INVALID_BRANCH_TYPE,
            _VCSInfoErrorTag.INVALID_BRANCH_TYPE,  # can't trigger value error here
            strip=True, allow_empty=False)


def repository_url(value: str) -> str:
    """Validate the repository URL string.

    It only checks that the value is a string. An empty string is allowed.

    :param value: The URL of the primary remote repository or an empty string.
    :return: The validated repository URL string.
    :raises SimpleBenchTypeError: If the repository URL is not a string.
    """
    return validate_string(
            value, "repository_url",
            _VCSInfoErrorTag.INVALID_REPOSITORY_URL_TYPE,
            _VCSInfoErrorTag.INVALID_REPOSITORY_URL_TYPE,  # can't trigger value error here
            strip=True, allow_empty=True)


def is_dirty(value: bool) -> bool:
    """Validate the is_dirty boolean value.

    :param value: Whether there are uncommitted changes.
    :return: The validated is_dirty boolean value.
    :raises SimpleBenchTypeError: If the is_dirty value is not a boolean.
    """
    return validate_bool(
            value, "is_dirty",
            _VCSInfoErrorTag.INVALID_IS_DIRTY_TYPE)
