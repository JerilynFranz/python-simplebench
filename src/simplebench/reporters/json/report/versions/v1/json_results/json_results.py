"""V1 JSONResults class"""
from typing import Any

from simplebench.reporters.json.report.base.json_results import JSONResults as BaseJSONResults


class JSONResults(BaseJSONResults):
    """Class representing JSON results for V1 reports."""

    VERSION: int = 1
    """The JSON results version number."""

    def __init__(self, results: list[dict[str, Any]]):  # pylint: disable=super-init-not-called
        """Initialize JSONResults with a list of result dictionaries.

        :param results: A list of dictionaries representing individual results.
        """
        self.results = results

    def to_dict(self) -> dict[str, Any]:
        """Convert JSONResults to a dictionary format.

        :return: A dictionary representation of the JSONResults.
        """
        return {
            "results": self.results
        }
