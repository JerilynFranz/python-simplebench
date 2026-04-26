"""Environment variables report for simplebench."""
import re
from collections.abc import Mapping

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _EnvironmentInfoErrorTag
from simplebench.simplebench_types import CoreDataMapping

from ..environment_info import EnvironmentInfo

_KEY_REGEX = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

class EnvironmentVars(EnvironmentInfo):
    """Environment variables report for simplebench."""

    def __init__(self,
                 data: Mapping[str, str],
                 title: str,
                 description: str = '',
                 hash_id: str = '') -> None:
        """Initialize an EnvironmentVars instance.

        This is a specialized version of :class:`EnvironmentInfo` that is designed to hold environment variables
        as key-value pairs in the data mapping. The keys must be valid environment variable names
        (consisting of letters, digits, and underscores, and not starting with a digit), and the values must be strings.

        It has the semantic type 'simplebench::environment_vars' and a specific validation logic for the data mapping.

        If a 'hash_id' key is present in the input data mapping, its value is validated
        and used as the hash_id property. If not present, the hash_id is computed from the
        rest of the data mapping.

        If 'type' or 'version' keys are not present in the input data mapping, they are
        automatically added with the appropriate values for this class.

        :param data: A mapping representing environment variables.
        Each key-value pair corresponds to an environment variable name and its value.
        The values must be strings.
        :type data: Mapping[str, str]
        :param title: A human-readable title for this environment.
        :type title: str
        :param description: A human-readable description for this environment.
        :type description: str
        :param hash_id: The hash ID of the environment, a 64-character hexadecimal string.
        :type hash_id: str
        """
        super().__init__(title=title,
                         description=description,
                         semantic_type='simplebench::environment_vars',
                         data=_validate_data(data),
                         hash_id=hash_id)


def _validate_data(data: Mapping[str, str]) -> CoreDataMapping:
    """Validate the data mapping for EnvironmentVars.

    :param data: The data mapping to validate.
    :type data: Mapping[str, str]
    :return: A validated CoreDataMapping instance containing the environment variables.
    :rtype: CoreDataMapping
    :raises SimpleBenchTypeError: If the data is not a mapping, if any keys or values are not strings.
    :raises SimpleBenchValueError: If any keys are not valid environment variable names.
    """
    if not isinstance(data, Mapping):
        raise SimpleBenchTypeError('data must be a mapping type', tag=_EnvironmentInfoErrorTag.INVALID_DATA_TYPE)

    if not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise SimpleBenchTypeError('all keys and values in data must be strings',
                                   tag=_EnvironmentInfoErrorTag.INVALID_DATA_TYPE)

    if not all(_KEY_REGEX.match(k) for k in data.keys()):
        raise SimpleBenchValueError('all keys in data must be valid environment variable names',
                                   tag=_EnvironmentInfoErrorTag.INVALID_DATA_KEY)

    return CoreDataMapping(data)
