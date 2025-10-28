# -*- coding: utf-8 -*-
"""Reporter for benchmark results using JSON files."""
from simplebench.reporters.reporter import ReporterOptions


class JSONOptions(ReporterOptions):
    """Class for holding JSON reporter specific options in a Choice or Case.

    This class provides additional configuration options specific to the JSON reporter.
    It is accessed via the `options` attribute of a Choice or Case instance.

    Attributes:
        full_data (bool): Whether to include full data in the JSON output.

    """
    def __init__(self, *,
                 full_data: bool = False) -> None:
        """Initialize JSONChoiceOptions with default targets and subdirectory.

        Args:
            full_data (bool, default=False): Whether to include full data in the JSON output.
        """
        self._full_data: bool = full_data

    @property
    def full_data(self) -> bool:
        """Return whether to include full data in the JSON output.

        Returns:
            bool: Whether to include full data in the JSON output.
        """
        return self._full_data
