"""KWArgs subclass for VirtualMemoryObject()."""

from simplebench.report.versions.v1.memory_info.virtual_memory.virtual_memory import VirtualMemoryObject
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class VirtualMemoryObjectKWArgs(KWArgs):
    """KWArgs for VirtualMemoryObject()"""

    def __init__(
            self, *,
            total: int | NoDefaultValue = NO_DEFAULT_VALUE,
            available: int | NoDefaultValue = NO_DEFAULT_VALUE,
            percent: float | NoDefaultValue = NO_DEFAULT_VALUE,
            used: int | NoDefaultValue = NO_DEFAULT_VALUE,
            free: int | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize self."""
        super().__init__(VirtualMemoryObject.__init__, kwargs=locals(), globalns=globals())

