"""JSONReport version 1 class."""
from typing import Any

from simplebench.exceptions import SimpleBenchValueError
from simplebench.reporters.json.report.base_json_report import JSONReport as BaseJSONReport

from .exceptions import _JSONReportErrorTag


class JSONReport(BaseJSONReport):
    """Class representing a JSON report version 1."""

    JSON_SCHEMA_URI: str = "https://json-schema.org/draft/2020-12/schema"
    """The JSON Schema URI for version 1 reports."""
    VERSION: int = 1
    """The JSON report version number."""

    @classmethod
    def from_dict(cls, data: dict) -> "JSONReport":
        """Create a JSONReport instance from a dictionary.

        :param data: Dictionary containing the JSON report data.
        :return: JSONReport instance.
        :raises SimpleBenchValueError: If the version is not 1.
        """
        if not isinstance(data, dict):
            raise SimpleBenchValueError(
                "Input data must be a dictionary",
                tag=_JSONReportErrorTag.INVALID_INPUT_DATA_TYPE)
        if not all(isinstance(key, str) for key in data.keys()):
            raise SimpleBenchValueError(
                "All keys in input data must be strings",
                tag=_JSONReportErrorTag.INVALID_INPUT_DATA_KEYS_TYPE)

        BaseJSONReport.validate_schema_uri(data.get('$schema'))
        BaseJSONReport.validate_version(data.get('version'))
        BaseJSONReport.validate_type(data.get('type'), 'Case')
        report = cls(
            group=data.get('group'),  # type: ignore[reportArgumentType]
            title=data.get('title'),  # type: ignore[reportArgumentType]
            description=data.get('description'),  # type: ignore[reportArgumentType]
            variation_cols=data.get('variation_cols'),  # type: ignore[reportArgumentType]
            results=data.get('results')  # type: ignore[reportArgumentType]
        )

        return report

    __slots__ = ('_group', '_title', '_description', '_variation_cols', '_results')

    def __init__(self, *,  # pylint: disable=super-init-not-called
                 group: str,
                 title: str,
                 description: str,
                 variation_cols: dict[str, str],
                 results: list[dict[str, Any]]) -> None:
        """Initialize a JSONReport v1 instance."""
        self.group = group
        self.title = title
        self.description = description
        self.variation_cols = variation_cols
        self.results = results
