# -*- coding: utf-8 -*-
"""Reporter for benchmark results using Rich tables on the console."""
from simplebench.reporters.reporter import ReporterOptions
from simplebench.validators import validate_int_range

from .exceptions import RichTableOptionsErrorTag


class RichTableOptions(ReporterOptions):
    """Class for holding Rich table reporter specific options in a Choice.

    This class provides additional configuration options specific to the JSON reporter.
    It is accessed via the ``options`` attribute of a
    :class:`~simplebench.reporters.choice.Choice` instance.

    :ivar virtual_width: The width of the Rich table output in characters when rendered
        to the filesystem or via callback. Must be between 80 and 1000 characters or
        ``None``. If ``None``, no width constraint is applied.

        The virtual width is used to determine how the table should be formatted when
        rendered to non-console outputs, such as files or callbacks. This allows for
        better control over the appearance of the table in different contexts.
    :vartype virtual_width: int, optional
    """
    def __init__(self,
                 virtual_width: int | None = None) -> None:
        """Create a RichTableOptions instance.

        :param virtual_width: The width of the Rich table output when rendered to the
            filesystem or via callback. Must be between 80 and 1000 characters or
            ``None``. If ``None``, no width constraint is applied. Defaults to ``None``.
        :type virtual_width: int, optional
        :raises ~simplebench.exceptions.SimpleBenchTypeError: If ``virtual_width`` is not
            an integer or ``None``.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If ``virtual_width`` is not
            between 80 and 10000 characters when specified.
        """
        if virtual_width is None:
            self._virtual_width = None
        else:
            self._virtual_width = validate_int_range(
                virtual_width, 'virtual_width',
                RichTableOptionsErrorTag.INVALID_VIRTUAL_WIDTH_TYPE,
                RichTableOptionsErrorTag.INVALID_VIRTUAL_WIDTH_VALUE,
                min_value=80, max_value=10000)

    @property
    def virtual_width(self) -> int | None:
        """Return the virtual width of the Rich table output.

        The virtual width is used when rendered to the filesystem or via callback.

        :return: The virtual width of the Rich table output in characters.
        :rtype: int, optional
        """
        return self._virtual_width
