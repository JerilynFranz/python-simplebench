"""Validation functions for VirtualMemoryObject properties."""
from simplebench.report._error_tags import VirtualMemoryErrorTag
from simplebench.validators import validate_float_range, validate_non_negative_int


def total(value: int) -> int:
    """Validate total virtual memory.

    :param int value: The total virtual memory in bytes.
    :return int: The validated total virtual memory.
    """
    return validate_non_negative_int(
        value, 'total',
        VirtualMemoryErrorTag.INVALID_TOTAL_TYPE,
        VirtualMemoryErrorTag.INVALID_TOTAL_VALUE)

def available(value: int) -> int:
    """Validate available virtual memory.

    :param int value: The available virtual memory in bytes.
    :return int: The validated available virtual memory.
    """
    return validate_non_negative_int(
        value, 'available',
        VirtualMemoryErrorTag.INVALID_AVAILABLE_TYPE,
        VirtualMemoryErrorTag.INVALID_AVAILABLE_VALUE)

def percent(value: float) -> float:
    """Validate percentage of virtual memory used.

    :param float value: The percentage of virtual memory used.
    :return float: The validated percentage of virtual memory used.
    """
    return validate_float_range(
        value, 'percent',
        VirtualMemoryErrorTag.INVALID_PERCENT_TYPE,
        VirtualMemoryErrorTag.INVALID_PERCENT_OUT_OF_RANGE,
        min_value=0.0, max_value=100.0)

def used(value: int) -> int:
    """Validate used virtual memory.

    :param int value: The used virtual memory in bytes.
    :return int: The validated used virtual memory.
    """
    return validate_non_negative_int(
        value, 'used',
        VirtualMemoryErrorTag.INVALID_USED_TYPE,
        VirtualMemoryErrorTag.INVALID_USED_VALUE)

def free(value: int) -> int:
    """Validate free virtual memory.

    :param int value: The free virtual memory in bytes.
    :return int: The validated free virtual memory.
    """
    return validate_non_negative_int(
        value, 'free',
        VirtualMemoryErrorTag.INVALID_FREE_TYPE,
        VirtualMemoryErrorTag.INVALID_FREE_VALUE)
