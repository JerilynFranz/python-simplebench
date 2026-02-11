"""KWArgs subclass for CPUInfo()."""

from simplebench import environment
from simplebench.report.versions.v1 import CPUInfo, CPUInfoData
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class CPUInfoKWArgs(KWArgs):
    """KWArgs for report.versions.v1.CPUInfo()"""

    def __init__(
            self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            data: environment.CPUInfo | CPUInfoData | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize self."""
        super().__init__(CPUInfo.__init__, kwargs=locals(), globalns=globals())

