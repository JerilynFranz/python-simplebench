"""Math-related utilities for SimpleBench."""
from collections.abc import Iterable


def smallest_abs(numbers: Iterable[float]) -> float:
    """Returns the smallest absolute value from the given sequence of numbers.

    :param numbers: A sequence of floating-point numbers to evaluate.
    :type numbers: Sequence[float]
    :return: The smallest absolute value, or None if there are no positive numbers.
    :rtype: float
    """
    return min([abs(n) for n in numbers if n != 0], default=0.0)
