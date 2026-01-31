"""Validation functions for ReporterConfig."""

from simplebench.enums import Format, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import MetricsSelection
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.simplebench_types import ElementCollection, is_element_collection
from simplebench.validators import validate_dirname, validate_string, validate_type

from ._error_tags import _ReporterConfigErrorTag


def name(value: str) -> str:
    """Validate ReporterConfig name.

    :param value: The name to validate.
    :type value: str
    :return: The validated name.
    :rtype: str
    :raises SimpleBenchValueError: If the name is invalid.
    :raises SimpleBenchTypeError: If the name is not a string.
    """
    return validate_string(
        value,
        'name',
        type_error_tag=_ReporterConfigErrorTag.INVALID_NAME_TYPE,
        value_error_tag=_ReporterConfigErrorTag.INVALID_NAME_VALUE,
        allow_empty=False,
        allow_blank=False,
    )

def description(value: str) -> str:
    """Validate ReporterConfig description.

    :param value: The description to validate.
    :type value: str
    :return: The validated description.
    :rtype: str
    :raises SimpleBenchValueError: If the description is invalid.
    :raises SimpleBenchTypeError: If the description is not a string.
    """
    return validate_string(
        value,
        'description',
        type_error_tag=_ReporterConfigErrorTag.INVALID_DESCRIPTION_TYPE,
        value_error_tag=_ReporterConfigErrorTag.INVALID_DESCRIPTION_VALUE,
        allow_empty=False,
        allow_blank=False)


def metrics(value: MetricsSelection) -> MetricsSelection:
    """Validate ReporterConfig metrics selection.

    :param value: The MetricsSelection to validate.
    :type value: MetricsSelection
    :return: The validated MetricsSelection.
    :rtype: MetricsSelection
    :raises SimpleBenchTypeError: If the value is not a MetricsSelection.
    """
    return validate_type(
        value, MetricsSelection, 'metrics',
        _ReporterConfigErrorTag.INVALID_METRICS_TYPE)


def targets(value: ElementCollection[Target]) -> frozenset[Target]:
    """Validate ReporterConfig targets.

    Must be a non-empty ElementCollection of Target enums.

    :param value: The list of Targets to validate.
    :type value: ElementCollection[Target]
    :return: The validated frozenset of Targets.
    :rtype: frozenset[Target]
    :raises SimpleBenchTypeError: If the value is not an ElementCollection of Target enums, or is empty.
    :raises SimpleBenchTypeError: If any element in the collection is not a Target enum.
    :raises SimpleBenchValueError: If the collection is empty.
    """
    if not is_element_collection(value):
        raise SimpleBenchTypeError(
            f'Invalid type for targets: expected ElementCollection[Target], got {type(value).__name__}.',
            tag=_ReporterConfigErrorTag.INVALID_TARGETS_TYPE)
    if len(value) == 0:
        raise SimpleBenchTypeError(
            'Invalid value for targets: iterable is empty.',
            tag=_ReporterConfigErrorTag.INVALID_TARGETS_VALUE)
    if not all(isinstance(item, Target) for item in value):
        raise SimpleBenchTypeError(
            'Invalid element type in targets: all elements must be of type Target.',
            tag=_ReporterConfigErrorTag.INVALID_TARGETS_ELEMENT_TYPE)
    if isinstance(value, frozenset):
        return value
    return frozenset(value)


def default_targets(value: ElementCollection[Target]) -> frozenset[Target]:
    """Validate ReporterConfig default targets.

    Must be an ElementCollection of Target enums. It may be empty.

    :param value: The list of default Targets to validate.
    :type value: list[Target]
    :return: The validated frozenset of default Targets.
    :rtype: frozenset[Target]
    :raises SimpleBenchTypeError: If the value is not an ElementCollection of Target enums, or is empty.
    :raises SimpleBenchTypeError: If any element in the collection is not a Target enum.
    """
    if not is_element_collection(value):
        raise SimpleBenchTypeError(
            f'Invalid type for default_targets: expected ElementCollection[Target], got {type(value).__name__}.',
            tag=_ReporterConfigErrorTag.INVALID_DEFAULT_TARGETS_TYPE)

    if not all(isinstance(item, Target) for item in value):
        raise SimpleBenchTypeError(
            'Invalid element type in default_targets: all elements must be of type Target.',
            tag=_ReporterConfigErrorTag.INVALID_DEFAULT_TARGETS_ELEMENT_TYPE)
    if isinstance(value, frozenset):
        return value
    return frozenset(value)


def formats(value: ElementCollection[Format]) -> frozenset[Format]:
    """Validate ReporterConfig formats.

    Must be a non-empty ElementCollection of Format enums.

    :param value: The list of Formats to validate.
    :type value: ElementCollection[Format]
    :return: The validated frozenset of Formats.
    :rtype: frozenset[Format]
    :raises SimpleBenchTypeError: If the value is not an ElementCollection of Format enums.
    :raises SimpleBenchValueError: If the collection is empty.
    """
    if not is_element_collection(value):
        raise SimpleBenchTypeError(
            f'Invalid type for formats: expected ElementCollection[Format], got {type(value).__name__}.',
            tag=_ReporterConfigErrorTag.INVALID_FORMATS_TYPE)
    if len(value) == 0:
        raise SimpleBenchTypeError(
            'Invalid value for formats: iterable is empty.',
            tag=_ReporterConfigErrorTag.INVALID_FORMATS_ELEMENT_TYPE)
    if not all(isinstance(item, Format) for item in value):
        raise SimpleBenchTypeError(
            'Invalid element type in formats: all elements must be of type Format.',
            tag=_ReporterConfigErrorTag.INVALID_FORMATS_ELEMENT_TYPE)
    if isinstance(value, frozenset):
        return value
    return frozenset(value)


def choices(value: ChoicesConf) -> ChoicesConf:
    """Validate ReporterConfig choices configuration.

    :param value: The ChoicesConf to validate.
    :type value: ChoicesConf
    :return: The validated ChoicesConf.
    :rtype: ChoicesConf
    :raises SimpleBenchTypeError: If the value is not a ChoicesConf.
    """
    return validate_type(
        value, ChoicesConf, 'choices',
        _ReporterConfigErrorTag.INVALID_CHOICES_TYPE)


def file_suffix(value: str) -> str:
    """Validate ReporterConfig file suffix.

    :param value: The file suffix to validate.
    :type value: str
    :return: The validated file suffix.
    :rtype: str
    :raises SimpleBenchValueError: If the file suffix is blank, empty,
        or contains invalid characters or is too long (more than 10 characters).
    :raises SimpleBenchTypeError: If the file suffix is not a string.
    """
    validated_suffix = validate_string(
        value,
        'file_suffix',
        type_error_tag=_ReporterConfigErrorTag.INVALID_FILE_SUFFIX_TYPE,
        value_error_tag=_ReporterConfigErrorTag.INVALID_FILE_SUFFIX_VALUE,
        allow_empty=False,
        allow_blank=False,
        alphanumeric_only=True,
    )
    if len(validated_suffix) > 10:
        raise SimpleBenchTypeError(
            'Invalid value for file_suffix: exceeds maximum length of 10 characters.',
            tag=_ReporterConfigErrorTag.INVALID_FILE_SUFFIX_VALUE_TOO_LONG)
    return validated_suffix


def file_unique(value: bool) -> bool:
    """Validate ReporterConfig file_unique flag.

    :param value: The file_unique flag to validate.
    :type value: bool
    :return: The validated file_unique flag.
    :rtype: bool
    :raises SimpleBenchTypeError: If the file_unique flag is not a boolean.
    """
    return validate_type(
        value, bool, 'file_unique',
        _ReporterConfigErrorTag.INVALID_FILE_UNIQUE_TYPE)


def file_append(value: bool) -> bool:
    """Validate ReporterConfig file_append flag.

    :param value: The file_append flag to validate.
    :type value: bool
    :return: The validated file_append flag.
    :rtype: bool
    :raises SimpleBenchTypeError: If the file_append flag is not a boolean.
    """
    return validate_type(
        value, bool, 'file_append',
        _ReporterConfigErrorTag.INVALID_FILE_APPEND_TYPE)


def validate_file_append_file_unique_combination(
        file_append_value: bool, file_unique_value: bool) -> None:
    """Validate that file_append and file_unique combination is valid.

    One, and only one, of file_append and file_unique must be True.

    :param file_append_value: The file_append flag.
    :type file_append_value: bool
    :param file_unique_value: The file_unique flag.
    :type file_unique_value: bool
    :raises SimpleBenchValueError: If both file_append and file_unique are True.
    :raises SimpleBenchValueError: If both file_append and file_unique are False.
    """

    # Check for (False, False) case first for clarity
    if not file_append_value and not file_unique_value:
        raise SimpleBenchValueError(
            'One of file_append or file_unique must be True.',
            tag=_ReporterConfigErrorTag.INVALID_FILE_APPEND_FILE_UNIQUE_ONE_MUST_BE_TRUE,
        )
    # If the first check passes, this check now correctly isolates the (True, True) case
    if file_append_value and file_unique_value:
        raise SimpleBenchValueError(
            'file_append and file_unique cannot both be True.',
            tag=_ReporterConfigErrorTag.INVALID_FILE_APPEND_FILE_UNIQUE_COMBINATION,
        )


def subdir(value: str) -> str:
    """Validate ReporterConfig subdir.

    It validates that:
        - The directory name is a string.
        - The directory name is made of alphanumeric characters,
          underscores, or dashes, and is at least one character long.
        - The directory name does not start or end with an underscore or dash.
        - If allow_empty is False, that the directory name is not an empty string. If
          allow_empty is True, an empty string is considered to be a valid dirname (default is
        - The total directory name length does not exceed 255 characters.

    :param value: The subdir to validate.
    :type value: str
    :return: The validated subdir.
    :rtype: str
    :raises SimpleBenchTypeError: If the subdir is not a string.
    :raises SimpleBenchValueError: If the subdir is too long, contains invalid characters,
        or starts/ends with a slash.
    """
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid type for subdir: expected str, got {type(value).__name__}.',
            tag=_ReporterConfigErrorTag.INVALID_SUBDIR_TYPE)

    return validate_dirname(value, allow_empty=True)


def default_targets_are_subset_of_targets(
        default_targets_value: frozenset[Target],
        targets_value: frozenset[Target],
        ) -> None:
    """Validate that default_targets is a subset of targets.

    :param default_targets_value: The default_targets collection.
    :type default_targets_value: ElementCollection[Target]
    :param targets_value: The targets collection.
    :type targets_value: ElementCollection[Target]
    :raises SimpleBenchValueError: If default_targets is not a subset of targets.
    """
    if not default_targets_value.issubset(targets_value):
        raise SimpleBenchValueError(
            'default_targets must be a subset of targets.',
            tag=_ReporterConfigErrorTag.INVALID_DEFAULT_TARGETS_TYPE)
