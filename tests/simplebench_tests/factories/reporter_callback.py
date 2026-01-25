"""Factory for ReporterCallback conformant callback functions for testing purposes.

Separately defined to avoid circular imports.
"""
from typing import Any

from simplebench.case import Case
from simplebench.enums import Format
from simplebench.metrics import Metric


def default_reporter_callback(  # pylint: disable=unused-argument
        *, case: Case, metric: Metric, output_format: Format, output: Any) -> None:
    """A default ReporterCallback conformant callback function for testing purposes.

    .. code-block:: python

        def default_reporter_callback(
                *, case: Case, section: Metric, output_format: Format, output: Any) -> None:
            return None
    """
    return None  # pragma: no cover
