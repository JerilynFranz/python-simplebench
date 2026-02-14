"""KWArgs subclass for SystemInfo.__init__."""

from simplebench.report.versions.v1 import SystemInfo
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class SystemInfoKWArgs(KWArgs):
    """KWArgs for SystemInfo.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            system: str | NoDefaultValue = NO_DEFAULT_VALUE,
            system_version: str | NoDefaultValue = NO_DEFAULT_VALUE,
            release: str | NoDefaultValue = NO_DEFAULT_VALUE,
            machine: str | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize the SystemInfo instance.

        :param str hash_id: The unique hash identifier for the system info.
        :param str system: The system OS identifier string.
        :param str system_version: The system version string.
        :param str release: The system release string.
        :param str machine: The machine type string."""
        super().__init__(SystemInfo.__init__, kwargs=locals(), globalns=globals())
