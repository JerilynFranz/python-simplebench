# -*- coding: utf-8 -*-
"""Reporter for benchmark results using JSON files."""
from simplebench.reporters.reporter import ReporterOptions


class JSONOptions(ReporterOptions):
    """Class for holding JSON reporter specific options in a Choice or Case.

    This class provides additional configuration options specific to the JSON reporter.
    It is accessed via the ``options`` attribute of a
    :class:`~simplebench.reporters.choice.Choice` or :class:`~simplebench.case.Case`
    instance.

    :ivar full_data: Whether to include full data in the JSON output.
    :vartype full_data: bool
    """
    def __init__(self, *,
                 full_data: bool = False) -> None:
        """Initialize JSONChoiceOptions with default targets and subdirectory.

        :param full_data: Whether to include full data in the JSON output.
            Defaults to ``False``.
        :type full_data: bool
        """
        self._full_data: bool = full_data

    @property
    def full_data(self) -> bool:
        """Return whether to include full data in the JSON output.

        :return: Whether to include full data in the JSON output.
        :rtype: bool
        """
        return self._full_data
