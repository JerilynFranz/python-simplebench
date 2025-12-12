"""V1 JSONResults class"""
from typing import Any

from simplebench.reporters.json.report.base import StatsBlock as BaseStatsBlock


class StatsBlock(BaseStatsBlock):
    """Class representing JSON stats summary for V1 reports."""

    VERSION: int = 1
    """The JSON stats summary version number."""

    def __init__(self, results: list[dict[str, Any]]):  # pylint: disable=super-init-not-called
        """Initialize JSONStatsSummary with a list of result dictionaries.
        :param results: A list of dictionaries representing individual results.
        """
        self.results = results

    def to_dict(self) -> dict[str, Any]:
        """Convert JSONStatsSummary to a dictionary format.

        :return: A dictionary representation of the JSONStatsSummary.
        """
        return {
            "results": self.results
        }
