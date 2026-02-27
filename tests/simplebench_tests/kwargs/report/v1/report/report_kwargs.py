"""KWArgs subclass for Report.__init__."""
from collections.abc import Sequence

from simplebench.report.versions.v1 import MachineInfo, Report, ResultsInfo
from simplebench.simplebench_types import VariationCols
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class ReportKWArgs(KWArgs):
    """KWArgs for Report.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            timestamp: str | NoDefaultValue = NO_DEFAULT_VALUE,
            group: str | NoDefaultValue = NO_DEFAULT_VALUE,
            title: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            variation_cols: VariationCols | NoDefaultValue = NO_DEFAULT_VALUE,
            results: Sequence[ResultsInfo] | NoDefaultValue = NO_DEFAULT_VALUE,
            machine: MachineInfo | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize a Report instance.

        :param str hash_id: The unique hash identifier for the report.
        :param str timestamp: ISO 8601 formatted timestamp string.
        :param str group: Group of the benchmark.
        :param str title: Title of the benchmark.
        :param str description: Description of the benchmark.
        :param VariationCols variation_cols: Variation columns dictionary.
        :param Sequence[ResultsInfo] results: Sequence of ResultsInfo instances.
        :param MachineInfo machine: MachineInfo instance."""
        super().__init__(Report.__init__, kwargs=locals(), globalns=globals())

