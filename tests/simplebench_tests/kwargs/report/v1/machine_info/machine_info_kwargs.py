"""KWArgs subclass for MachineInfo.__init__."""
# ruff: noqa: F401
from collections.abc import Sequence

from simplebench.report.versions.v1 import CPUInfo, EnvironmentInfo, MachineInfo, MemoryInfo, SystemInfo
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue, report


class MachineInfoKWArgs(KWArgs):
    """KWArgs for MachineInfo.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            node: str | NoDefaultValue = NO_DEFAULT_VALUE,
            cpu: CPUInfo | NoDefaultValue = NO_DEFAULT_VALUE,
            memory: MemoryInfo | NoDefaultValue = NO_DEFAULT_VALUE,
            system: SystemInfo | NoDefaultValue = NO_DEFAULT_VALUE,
            environment: Sequence[EnvironmentInfo] | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize JSONMachineInfo.

        :param str hash_id: The unique hash identifier for the machine information.
        :param str node: The node string.
        :param CPUInfo cpu: The CPU information.
        :param MemoryInfo memory: The memory information.
        :param SystemInfo system: The system information.
        :param Sequence[EnvironmentInfo] environment: The execution environment information.
        :raises SimpleBenchTypeError: If any of the parameters are of incorrect type.
        :raises SimpleBenchValueError: If any of the parameters have invalid values."""
        super().__init__(MachineInfo.__init__, kwargs=locals(), globalns=globals())
