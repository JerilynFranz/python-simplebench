"""KWArgs subclass for MemoryInfo.__init__."""

from simplebench.report.versions.v1.memory_info import MemoryInfo, SwapMemoryObject, VirtualMemoryObject
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class MemoryInfoKWArgs(KWArgs):
    """KWArgs for MemoryInfo()"""

    def __init__(
            self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            swap_memory: SwapMemoryObject | NoDefaultValue = NO_DEFAULT_VALUE,
            virtual_memory: VirtualMemoryObject | NoDefaultValue = NO_DEFAULT_VALUE,
) -> None:
        """Initialize kwargs for MemoryInfo.__init__."""
        super().__init__(MemoryInfo.__init__, kwargs=locals(), globalns=globals())
