"""V1 Results object class

The V1 Results object represents the results section of a version 1 JSON report.

It provides methods to co

"""
from typing import Any

from simplebench.reporters.json.report.base import Results as BaseResults


class Results(BaseResults):
    """Class representing JSON results object for V1 reports."""

    VERSION: int = 1
    """The JSON results object version number for version 1 results."""

    TYPE: str = "SimpleBenchResults::V1"
    """The JSON results object type for version 1 results."""

    def to_dict(self) -> dict[str, Any]:
        """Convert Results to a dictionary format.

        :return: A dictionary representation of the Results.
        """
        return {
            "results": self.results
        }
