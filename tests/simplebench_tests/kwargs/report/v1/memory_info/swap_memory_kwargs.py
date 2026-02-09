"""KWArgs subclass for SwapMemoryObject()."""

from simplebench.report.versions.v1.memory_info import SwapMemoryObject
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class SwapMemoryObjectKWArgs(KWArgs):
    """KWArgs for SwapMemoryObject()"""

    def __init__(self, *,
            total: int | NoDefaultValue = NO_DEFAULT_VALUE,
            used: int | NoDefaultValue = NO_DEFAULT_VALUE,
            free: int | NoDefaultValue = NO_DEFAULT_VALUE,
            percent: float | NoDefaultValue = NO_DEFAULT_VALUE,
            swap_in: int | NoDefaultValue = NO_DEFAULT_VALUE,
            swap_out: int | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize."""
        super().__init__(SwapMemoryObject.__init__, kwargs=locals(), globalns=globals())
