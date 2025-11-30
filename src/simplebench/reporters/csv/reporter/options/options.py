"""ReporerOptions subclass for CSV reporter specific options.

This module defines the :class:`~.CSVOptions` class, which is a subclass of
:class:`~simplebench.reporters.reporter.options.ReporterOptions` and is used
to hold options specific to the CSV reporter.
"""
from typing import Sequence

from simplebench.reporters.reporter import ReporterOptions
from simplebench.validators import validate_bool, validate_sequence_of_type

from .exceptions import _CSVOptionsErrorTag
from .fields import CSVField

_DEFAULT_RICH_TABLE_FIELDS: Sequence[CSVField] = [
    CSVField.N,
    CSVField.ITERATIONS,
    CSVField.ROUNDS,
    CSVField.ELAPSED_SECONDS,
    CSVField.MEAN,
    CSVField.MEDIAN,
    CSVField.MIN,
    CSVField.MAX,
    CSVField.P5,
    CSVField.P95,
    CSVField.STD_DEV,
    CSVField.RSD_PERCENT,
]


class CSVOptions(ReporterOptions):
    """Class for holding CSV reporter specific options in a Choice.

    This class provides additional configuration options specific to the JSON reporter.
    It is accessed via the ``options`` attribute of a
    :class:`~simplebench.reporters.choice.Choice` instance.

    :param fields: A tuple of CSV fields to include in the output.
        If none is specifically set, a predefined set of fields is used. The fields appear in the order
        specified in the sequence.

        If specified, all fields must be from the :class:`~.CSVField` enum.

        The default fields, in order, are:

        - :attr:`~.CSVField.N`
        - :attr:`~.CSVField.ITERATIONS`
        - :attr:`~.CSVField.ROUNDS`
        - :attr:`~.CSVField.ELAPSED_SECONDS`
        - :attr:`~.CSVField.MEAN`
        - :attr:`~.CSVField.MEDIAN`
        - :attr:`~.CSVField.MIN`
        - :attr:`~.CSVField.MAX`
        - :attr:`~.CSVField.P5`
        - :attr:`~.CSVField.P95`
        - :attr:`~.CSVField.STD_DEV`
        - :attr:`~.CSVField.RSD_PERCENT`

    :param variation_cols_last: Whether to place the variation columns (if any) at the end of the rows.
        Defaults to ``False`` - which places the variation columns at the start of the rows.
    :raises ~simplebench.exceptions.SimpleBenchTypeError: Any parameter is of an invalid type.
    :raises ~simplebench.exceptions.SimpleBenchValueError: If ``fields`` is an empty sequence."""
    def __init__(self,
                 fields: Sequence[CSVField] | None = None,
                 variation_cols_last: bool = False
                 ) -> None:
        """Initialize CSVOptions instance."""
        self._fields: tuple[CSVField, ...] = tuple(validate_sequence_of_type(
            fields if fields is not None else _DEFAULT_RICH_TABLE_FIELDS,
            CSVField, 'fields',
            _CSVOptionsErrorTag.INVALID_DEFAULT_FIELDS_TYPE,
            _CSVOptionsErrorTag.INVALID_DEFAULT_FIELDS_VALUE,
            allow_empty=False))
        self._variation_cols_last = validate_bool(
            variation_cols_last, 'variation_cols_last',
            _CSVOptionsErrorTag.INVALID_VARIATION_COLS_LAST_TYPE)

    @property
    def fields(self) -> tuple[CSVField, ...]:
        """Return the fields, in order, to include in the CSV table when rendering.

        :return: A tuple of CSVField enums representing the default fields.
        """
        return self._fields

    @property
    def variation_cols_last(self) -> bool:
        """Return whether variation columns are placed at the end of the rows.

        :return: True if variation columns are placed at the end, False if at the start.
        """
        return self._variation_cols_last
