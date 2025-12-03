"""Utility functions for significant figures handling."""
import math

from simplebench.defaults import DEFAULT_SIGNIFICANT_FIGURES
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from .exceptions import _UtilsErrorTag


def sigfigs(number: float, figures: int = DEFAULT_SIGNIFICANT_FIGURES) -> float:
    """Rounds a floating point number to the specified number of significant figures.

    If the number of significant figures is not specified, it defaults to
    :data:`~.defaults.DEFAULT_SIGNIFICANT_FIGURES`.

    * 14.2 to 2 digits of significant figures becomes 14
    * 0.234 to 2 digits of significant figures becomes 0.23
    * 0.0234 to 2 digits of significant figures becomes 0.023
    * 14.5 to 2 digits of significant figures becomes 15
    * 0.235 to 2 digits of significant figures becomes 0.24

    :param number: The number to round.
    :type number: float
    :param figures: The number of significant figures to round to.
    :type figures: int
    :raises TypeError: If the ``number`` arg is not a float or the ``figures`` arg is not an int.
    :raises ValueError: If the ``figures`` arg is not at least 1.
    :return: The rounded number as a float.
    :rtype: float
    """
    if not isinstance(number, float):
        raise SimpleBenchTypeError(
            "number arg must be a float",
            tag=_UtilsErrorTag.SIGFIGS_INVALID_NUMBER_ARG_TYPE)
    if not isinstance(figures, int):
        raise SimpleBenchTypeError(
            "figures arg must be an int",
            tag=_UtilsErrorTag.SIGFIGS_INVALID_FIGURES_ARG_TYPE)
    if figures < 1:
        raise SimpleBenchValueError(
            "figures arg must be at least 1",
            tag=_UtilsErrorTag.SIGFIGS_INVALID_FIGURES_ARG_VALUE)

    if number == 0.0:
        return 0.0
    return round(number, figures - int(math.floor(math.log10(abs(number)))) - 1)
