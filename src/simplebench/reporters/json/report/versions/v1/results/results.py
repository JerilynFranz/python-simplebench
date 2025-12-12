"""V1 Results object class

The V1 Results object represents the results section of a version 1 JSON report.

"""
from simplebench.reporters.json.report.base import Results as BaseResults


class Results(BaseResults):
    """Class representing JSON results object for V1 reports."""

    VERSION: int = 1
    """The JSON results object version number for version 1 results."""

    TYPE: str = "SimpleBenchResults::V1"
    """The JSON results object type for version 1 results."""

    
