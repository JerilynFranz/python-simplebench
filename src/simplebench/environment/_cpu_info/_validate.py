"""Validators for environment.cpu_info module.

Import module and access validators via imported _validate module.
"""
from collections.abc import Mapping
from typing import TYPE_CHECKING

from typeguard import check_type

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.validators import validate_core_data_mapping, validate_string

from ._error_tags import _CPUInfoErrorTag

if TYPE_CHECKING:
    from simplebench.report.versions import v1 as report

__all__: list[str] = []


def cpu_info(value: Mapping[str, dict[str, object]]) -> 'report.ImmutableCPUInfoData':
    """Validate the CPU information dictionary.

    It expects a mapping type (such as dict) that conforms to the
    :class:`~simplebench.report.versions.v1.CPUInfoData` structure.

    It returns the validated CPU information dictionary as an immutable
    :class:`~simplebench.simplebench_types.CoreDataMappingType` object
    cast as a :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`
    for static type checking purposes.

    :param value: The CPU information dictionary to validate.
    :type value: Mapping[str, dict[str, object]]
    :return: The validated CPU information dictionary.
    :rtype: CoreDataMappingType (cast as ImmutableCPUInfoData typed dict for static type checking)
    :raises SimpleBenchTypeError: If the value is not a valid CPUInfoData structure.
    """
    from simplebench.report.versions import v1 as report

    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            'CPU information data must be a mapping type (such as dict).',
            tag=_CPUInfoErrorTag.INVALID_CPUINFO_DATA)

    # Convert to dict for type checking
    value_as_dict = dict(value)
    try:
        validated_value = check_type(value_as_dict, report.CPUInfoData)

        # Validate core data mapping structure and return as immutable typed dict
        # static type cast for type checking purposes because checkers do not
        # understand the return type of validate_core_data_mapping as being dict
        # typed as ImmutableCPUInfoData. The ignore is needed to suppress mypy
        # complaints about the cast.
        return validate_core_data_mapping(validated_value, name='CPUInfo.info')  # type: ignore

    except TypeError as exc:
        raise SimpleBenchTypeError(
            'Invalid cpuinfo data that does not conform to the expected CPUInfoData structure.',
            tag=_CPUInfoErrorTag.INVALID_CPUINFO_DATA) from exc



def cache_key(value: str | None) -> str | None:
    """Validate the cache_key parameter.

    The cache_key must be a non-blank string containing only alphanumeric characters.

    :param str | None value: The cache_key string to validate.
    :return str | None: The validated cache_key string.
    :raises SimpleBenchTypeError: If the value is not a string or ``None``.
    :raises SimpleBenchValueError: If the value is not a non-blank alphanumeric string.
    """
    if value is None:
        return None
    return validate_string(
        value,
        'cache_key',
        _CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_TYPE,
        _CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_VALUE,
        strip=False,
        allow_empty=False,
        alphanumeric_only=True,
        message='cache_key must be a non-empty string containing only alphanumeric characters.',
    )
