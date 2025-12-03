"""Reporter for benchmark results using Rich tables on the console."""
from typing import Sequence

from simplebench.reporters.reporter import ReporterOptions
from simplebench.validators import validate_bool, validate_int_range, validate_sequence_of_type

from .exceptions import _PytestOptionsErrorTag
from .fields import PytestField

_DEFAULT_RICH_TABLE_FIELDS: Sequence[PytestField] = [
    PytestField.N,
    PytestField.ITERATIONS,
    PytestField.ROUNDS,
    PytestField.ELAPSED_SECONDS,
    PytestField.MEAN,
    PytestField.MEDIAN,
    PytestField.MIN,
    PytestField.MAX,
    PytestField.P5,
    PytestField.P95,
    PytestField.STD_DEV,
    PytestField.RSD_PERCENT,
]


class PytestOptions(ReporterOptions):
    """Class for holding Rich table reporter specific options in a Choice.

    This class provides additional configuration options specific to the JSON reporter.
    It is accessed via the ``options`` attribute of a
    :class:`~simplebench.reporters.choice.Choice` instance.

    :param virtual_width: The width of the Rich table output in characters when rendered
        to the filesystem or via callback. Must be between 80 and 1000 characters or
        ``None``. If ``None``, no width constraint is applied.

        The virtual width is used to determine how the table should be formatted when
        rendered to non-console outputs, such as files or callbacks. This allows for
        better control over the appearance of the table in different contexts.
    :param fields: A tuple of Rich Table fields to include in the output.
        If none is specifically set, a predefined set of fields is used. The fields appear in the order
        specified in the sequence.

        If specified, all fields must be from the :class:`~.PytestField` enum.

        The default fields, in order, are:

        - :attr:`~.PytestField.N`
        - :attr:`~.PytestField.ITERATIONS`
        - :attr:`~.PytestField.ROUNDS`
        - :attr:`~.PytestField.ELAPSED_SECONDS`
        - :attr:`~.PytestField.MEAN`
        - :attr:`~.PytestField.MEDIAN`
        - :attr:`~.PytestField.MIN`
        - :attr:`~.PytestField.MAX`
        - :attr:`~.PytestField.P5`
        - :attr:`~.PytestField.P95`
        - :attr:`~.PytestField.STD_DEV`
        - :attr:`~.PytestField.RSD_PERCENT`

    :param variation_cols_last: Whether to place the variation columns (if any) at the end of the rows.
        Defaults to ``False`` - which places the variation columns at the start of the rows.
    :raises ~simplebench.exceptions.SimpleBenchTypeError: If any parameter is of an invalid type.
    :raises ~simplebench.exceptions.SimpleBenchValueError: If ``virtual_width`` is not
        between 80 and 10000 characters when specified or if ``fields`` is an empty sequence.
    """
    def __init__(self,
                 virtual_width: int | None = None,
                 fields: Sequence[PytestField] | None = None,
                 variation_cols_last: bool = False
                 ) -> None:
        """Initialize PytestOptions instance."""
        if virtual_width is None:
            self._virtual_width = None
        else:
            self._virtual_width = validate_int_range(
                virtual_width, 'virtual_width',
                _PytestOptionsErrorTag.INVALID_VIRTUAL_WIDTH_TYPE,
                _PytestOptionsErrorTag.INVALID_VIRTUAL_WIDTH_VALUE,
                min_value=80, max_value=10000)
        self._fields: tuple[PytestField, ...] = tuple(validate_sequence_of_type(
            fields if fields is not None else _DEFAULT_RICH_TABLE_FIELDS,
            PytestField, 'fields',
            _PytestOptionsErrorTag.INVALID_DEFAULT_FIELDS_TYPE,
            _PytestOptionsErrorTag.INVALID_DEFAULT_FIELDS_VALUE,
            allow_empty=False))
        self._variation_cols_last = validate_bool(
            variation_cols_last, 'variation_cols_last',
            _PytestOptionsErrorTag.INVALID_VARIATION_COLS_LAST_TYPE)

    @property
    def virtual_width(self) -> int | None:
        """Return the virtual width of the Rich table output.

        The virtual width is used when rendered to the filesystem or via callback.

        :return: The virtual width of the Rich table output in characters.
        """
        return self._virtual_width

    @property
    def fields(self) -> tuple[PytestField, ...]:
        """Return the fields, in order, to include in the Rich table when rendering.

        :return: A tuple of PytestField enums representing the default fields.
        """
        return self._fields

    @property
    def variation_cols_last(self) -> bool:
        """Return whether variation columns are placed at the end of the rows.

        :return: True if variation columns are placed at the end, False if at the start.
        """
        return self._variation_cols_last
