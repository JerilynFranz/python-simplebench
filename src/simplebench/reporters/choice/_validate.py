"""Validation functions for simplebench.reporters.choice package."""
from collections.abc import Hashable, Sequence
from typing import Any

from simplebench._log import _log
from simplebench.enums import FlagType, Format, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics.metrics_selection import MetricsSelection
from simplebench.options.reporter.options import ReporterOptions
from simplebench.simplebench_types import is_immutable
from simplebench.validators import (
    validate_iterable_of_type,
    validate_sequence_of_str,
    validate_string,
    validate_type,
)

from ._error_tags import _ChoiceConfErrorTag


def flags(value: Any) -> frozenset[str]:
    """Validate that a value is a sequence of FlagType enums for a flags parameter.

    :param value: The value to validate.
    :type value: Any
    :return frozenset[str]: A frozenset of validated flag strings.
    :raises SimpleBenchTypeError: If the value is not a sequence of strings.
    :raises SimpleBenchValueError: If one or more items in the flags argument is an empty string,
        blank string, or whitespace-only string.
    """
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise SimpleBenchTypeError(
            'The flags argument is not a Sequence of strings.',
            tag=_ChoiceConfErrorTag.FLAGS_INVALID_ARG_TYPE,
        )
    _log.debug('Validating flags: %r', value)
    return frozenset(
            validate_sequence_of_str(
                value,
                'flags',
                _ChoiceConfErrorTag.FLAGS_INVALID_ARG_TYPE,
                _ChoiceConfErrorTag.FLAGS_INVALID_ARGS_VALUE,
                allow_empty=False,
                allow_blank=False,
                allow_whitespace=False,
            )
        )


def flag_type(value: Any) -> FlagType:
    """Validate that a value is of type bool for a flag parameter.

    :param value: The value to validate.
    :type value: Any
    :return FlagType: The validated FlagType enum value.
    :raises SimpleBenchTypeError: The flag_type argument is not a :class:`~simplebench.enums.FlagType` enum value.
    """
    return validate_type(
            value, FlagType,
            'flag_type', _ChoiceConfErrorTag.FLAG_TYPE_INVALID_ARG_TYPE
        )


def name(value: Any) -> str:
    """Validate that a value is a non-empty, non-blank string for a name parameter.

    :param value: The value to validate.
    :type value: Any
    :return: The validated name string.
    :rtype: str
    :raises SimpleBenchTypeError: If the value is not a string.
    :raises SimpleBenchValueError: If the value is an empty string or blank string.
    """
    return validate_string(
            value,
            'name',
            _ChoiceConfErrorTag.NAME_INVALID_ARG_TYPE,
            _ChoiceConfErrorTag.NAME_INVALID_ARG_VALUE,
            allow_empty=False,
            allow_blank=False,
        )


def description(value: Any) -> str:
    """Validate that a value is a non-empty, non-blank string for a description parameter.

    :param value: The value to validate.
    :type value: Any
    :return: The validated description string.
    :rtype: str
    :raises SimpleBenchTypeError: If the value is not a string.
    :raises SimpleBenchValueError: If the value is an empty string or blank string.
    """
    return validate_string(
            value,
            'description',
            _ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
            _ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_VALUE,
            allow_empty=False,
            allow_blank=False,
        )


def metrics(value: Any) -> MetricsSelection:
    """Validate that a value is of type MetricsSelection for a metrics parameter.

    :param value: The value to validate.
    :type value: Any
    :return: The validated MetricsSelection instance.
    :rtype: MetricsSelection
    :raises SimpleBenchTypeError: If the value is not a MetricsSelection instance.
    """
    return validate_type(
            value,
            MetricsSelection,
            'metrics',
            _ChoiceConfErrorTag.METRICS_INVALID_ARG_TYPE,
        )

def targets(value: Any) -> frozenset[Target]:
    """Validate that a value is a sequence of Target enums for a targets parameter.

    :param value: The value to validate.
    :type value: Any
    :return: A frozenset of validated target enums.
    :rtype: frozenset[Target]
    :raises SimpleBenchTypeError: If the value is not a sequence of Target enums.
    :raises SimpleBenchValueError: If one or more items in the targets argument is not a Target enum value,
        or the targets argument is an empty sequence.
    """
    return frozenset(
        validate_iterable_of_type(
            value,
            Target,
            'targets',
            _ChoiceConfErrorTag.TARGETS_INVALID_ARG_TYPE,
            _ChoiceConfErrorTag.TARGETS_INVALID_ARG_VALUE,
            allow_empty=False,
        )
    )

def default_targets(value: Any) -> frozenset[Target]:
    """Validate that a value is a sequence of Target enums for a default_targets parameter.

    If the value is :obj:`None`, an empty frozenset is returned.

    :param value: The value to validate.
    :type value: Any
    :return: A frozenset of validated target enums.
    :rtype: frozenset[Target]
    :raises SimpleBenchTypeError: If the value is not a sequence of Target enums.
    :raises SimpleBenchValueError: If one or more items in the default_targets argument is not a Target enum value.
    """
    if value is None:
        return frozenset()

    return frozenset(
        validate_iterable_of_type(
            value,
            Target,
            'default_targets',
            _ChoiceConfErrorTag.DEFAULT_TARGETS_INVALID_ARG_TYPE,
            _ChoiceConfErrorTag.DEFAULT_TARGETS_INVALID_ARG_VALUE,
            allow_empty=True,
        )
    )


def subdir(value: Any) -> str | None:
    """Validate that a value is a valid subdirectory string for a subdir parameter.

    It must be alphanumeric, no longer than 64 characters, and
    cannot be a whitespace only string. It can be an empty string.

    If the value is :obj:`None`, it is considered valid.

    :param value: The value to validate.
    :type value: Any
    :return: The validated subdirectory string or None.
    :rtype: str | None
    :raises SimpleBenchTypeError: If the value is not a string or None.
    :raises SimpleBenchValueError: If the value is not alphanumeric or is a whitespace only string.
    :raises SimpleBenchValueError: If the value is longer than 64 characters.
    """
    if value is None:
        return None

    subdir_str = validate_string(
            value,
            'subdir',
            _ChoiceConfErrorTag.SUBDIR_INVALID_ARG_TYPE,
            _ChoiceConfErrorTag.SUBDIR_INVALID_ARG_VALUE,
            allow_empty=True,
            allow_blank=False,
            alphanumeric_only=True,
        )
    if len(subdir_str) > 64:
        raise SimpleBenchValueError(
            'The subdir argument is longer than 64 characters.',
            tag=_ChoiceConfErrorTag.SUBDIR_TOO_LONG,
        )
    return subdir_str


def file_suffix(value: Any) -> str | None:
    """Validate that a value is a valid file suffix string for a file_suffix parameter.

    It must be alphanumeric, no longer than 10 characters, and
    cannot be a whitespace only string. It can be an empty string.

    If the value is :obj:`None`, it is considered valid.

    :param value: The value to validate.
    :type value: Any
    :return: The validated file suffix string or None.
    :rtype: str | None
    :raises SimpleBenchTypeError: If the value is not a string or None.
    :raises SimpleBenchValueError: If the value is not alphanumeric or is a whitespace only string.
    :raises SimpleBenchValueError: If the value is longer than 10 characters.
    """
    if value is None:
        return None

    file_suffix_str = validate_string(
            value,
            'file_suffix',
            _ChoiceConfErrorTag.FILE_SUFFIX_INVALID_ARG_TYPE,
            _ChoiceConfErrorTag.FILE_SUFFIX_INVALID_ARG_VALUE,
            allow_empty=True,
            allow_blank=False,
            alphanumeric_only=True,
        )
    if len(file_suffix_str) > 10:
        raise SimpleBenchValueError(
            'The file_suffix argument is longer than 10 characters.',
            tag=_ChoiceConfErrorTag.FILE_SUFFIX_TOO_LONG,
        )
    return file_suffix_str


def file_unique(value: Any) -> bool | None:
    """Validate that a value is of type bool or None for a file_unique parameter.

    If the value is :obj:`None`, it is considered valid.

    :param value: The value to validate.
    :type value: Any
    :return: The validated boolean value or None.
    :rtype: bool | None
    :raises SimpleBenchTypeError: If the value is not a boolean or None.
    """
    if value is None:
        return None

    return validate_type(
            value,
            bool,
            'file_unique',
            _ChoiceConfErrorTag.FILE_UNIQUE_INVALID_ARG_TYPE,
        )

def file_append(value: Any) -> bool | None:
    """Validate that a value is of type bool or None for a file_append parameter.

    If the value is :obj:`None`, it is considered valid.

    :param value: The value to validate.
    :type value: Any
    :return: The validated boolean value or None.
    :rtype: bool | None
    :raises SimpleBenchTypeError: If the value is not a boolean or None.
    """
    if value is None:
        return None

    return validate_type(
            value,
            bool,
            'file_append',
            _ChoiceConfErrorTag.FILE_APPEND_INVALID_ARG_TYPE,
        )


def output_format(value: Any) -> Format:
    """Validate that a value is of type Format for an output_format parameter.

    :param value: The value to validate.
    :type value: Any
    :return: The validated Format enum value.
    :rtype: Format
    :raises SimpleBenchTypeError: If the value is not a Format enum value.
    """
    return validate_type(
            value,
            Format,
            'output_format',
            _ChoiceConfErrorTag.OUTPUT_FORMAT_INVALID_ARG_TYPE,
        )


def options(value: Any) -> ReporterOptions | None:
    """Validate that a value is of type ReporterOptions or None for an options parameter.

    If the value is :obj:`None`, it is considered valid.

    :param value: The value to validate.
    :type value: Any
    :return: The validated ReporterOptions instance or None.
    :rtype: ReporterOptions | None
    :raises SimpleBenchTypeError: If the value is not a ReporterOptions instance or None.
    """
    if value is None:
        return None

    return validate_type(
            value,
            ReporterOptions,
            'options',
            _ChoiceConfErrorTag.OPTIONS_INVALID_ARG_TYPE,
        )

def extra(value: Any) -> Hashable | None:
    """Validate that a value is Hashable and immutable or None for an extra parameter.

    If the value is :obj:`None`, it is considered valid.

    :param value: The value to validate.
    :type value: Any
    :return: The validated Hashable instance or None.
    :rtype: Hashable | None
    :raises SimpleBenchTypeError: If the value is not hashable and immutable or None.
    """
    if value is None:
        return None

    try:
        hash(value)
    except TypeError:
        raise SimpleBenchValueError(
            'The extra argument is not hashable.',
            tag=_ChoiceConfErrorTag.OPTIONS_INVALID_ARG_VALUE,
        ) from None

    try:
        if not is_immutable(value):
            raise SimpleBenchValueError(
                'The extra argument is not immutable.',
                tag=_ChoiceConfErrorTag.OPTIONS_INVALID_ARG_VALUE_NOT_IMMUTABLE)
    except (TypeError, RecursionError, ValueError) as e:
        raise SimpleBenchValueError(
            'The extra argument cannot be determined to be immutable.',
            tag=_ChoiceConfErrorTag.OPTIONS_INVALID_ARG_VALUE_NOT_IMMUTABLE) from e
    return value
