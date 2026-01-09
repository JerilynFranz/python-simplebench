"""Validation functions for SwapMemoryObject properties."""
from simplebench.report._error_tags import SwapMemoryErrorTag
from simplebench.validators import validate_float_range, validate_non_negative_int


def total(value: int) -> int:
    """Validate the total swap memory in bytes.

    :param value: The total swap memory in bytes.
    :return int: The validated total swap memory in bytes.
    :raises SimpleBenchTypeError: If the value is not an int.
    :raises SimpleBenchValueError: If the value is negative.
    """
    return validate_non_negative_int(
        value, "total",
        SwapMemoryErrorTag.INVALID_TOTAL_TYPE,
        SwapMemoryErrorTag.INVALID_TOTAL_VALUE)

def used(value: int) -> int:
    """Validate the used swap memory in bytes.

    :param value: The used swap memory in bytes.
    :return int: The validated used swap memory in bytes.
    :raises SimpleBenchTypeError: If the value is not an int.
    :raises SimpleBenchValueError: If the value is negative.
    """
    return validate_non_negative_int(
        value, "used",
        SwapMemoryErrorTag.INVALID_USED_TYPE,
        SwapMemoryErrorTag.INVALID_USED_VALUE)

def free(value: int) -> int:
    """Validate the free swap memory in bytes.

    :param value: The free swap memory in bytes.
    :return: The validated free swap memory in bytes.
    :raises ValueError: If the value is negative.
    """
    return validate_non_negative_int(
        value, "free",
        SwapMemoryErrorTag.INVALID_FREE_TYPE,
        SwapMemoryErrorTag.INVALID_FREE_VALUE)

def percent(value: float) -> float:
    """Validate the percentage of swap memory used.

    :param value: The percentage of swap memory used.
    :return: The validated percentage of swap memory used.
    :raises ValueError: If the value is not between 0 and 100.
    """
    return validate_float_range(
        value, "percent",
        SwapMemoryErrorTag.INVALID_SWAP_PERCENT_TYPE,
        SwapMemoryErrorTag.INVALID_SWAP_PERCENT_OUT_OF_RANGE,
        min_value=0.0, max_value=100.0)

def swap_in(value: int) -> int:
    """Validate the swap memory sent to disk in bytes.

    :param value: The swap memory sent to disk in bytes.
    :return: The validated swap memory sent to disk in bytes.
    :raises ValueError: If the value is negative.
    """
    return validate_non_negative_int(
        value, "swap_in",
        SwapMemoryErrorTag.INVALID_SWAP_IN_TYPE,
        SwapMemoryErrorTag.INVALID_SWAP_IN_VALUE)

def swap_out(value: int) -> int:
    """Validate the swap memory received from disk in bytes.

    :param value: The swap memory received from disk in bytes.
    :return: The validated swap memory received from disk in bytes.
    :raises ValueError: If the value is negative.
    """
    return validate_non_negative_int(
        value, "swap_out",
        SwapMemoryErrorTag.INVALID_SWAP_OUT_TYPE,
        SwapMemoryErrorTag.INVALID_SWAP_OUT_VALUE)
