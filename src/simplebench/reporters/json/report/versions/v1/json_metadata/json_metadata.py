"""V1 JSONResults class"""
from typing import Any

from simplebench.reporters.json.report.base.json_metadata import JSONMetadata as BaseMetadata


class JSONMetadata(BaseMetadata):
    """Class representing JSON metadata for V1 reports."""

    VERSION: int = 1
    """The JSON metadata version number."""

    def __init__(self, results: list[dict[str, Any]]):  # pylint: disable=super-init-not-called
        """Initialize JSONMetadata with a list of result dictionaries.
        :param results: A list of dictionaries representing individual results.
        """
        self.results = results

    def to_dict(self) -> dict[str, Any]:
        """Convert JSONMetadata to a dictionary format.

        :return: A dictionary representation of the JSONMetadata.
        """
        return {
            "results": self.results
        }
