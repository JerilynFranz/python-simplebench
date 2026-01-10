"""Exceptions for JSON reports and schemas."""
from ._cpu_info import _CPUInfoErrorTag
from ._memory_info import _MemoryInfoErrorTag
from ._python_info import _PythonInfoErrorTag
from ._swap_memory import _SwapMemoryErrorTag
from ._system_info import _SystemInfoErrorTag
from ._virtual_memory import _VirtualMemoryErrorTag
from .execution_environment import _ExecutionEnvironmentErrorTag
from .json_schema import _JSONSchemaErrorTag
from .machine_info import _MachineInfoErrorTag
from .metrics import _MetricsErrorTag
from .raw_data_block import _RawDataBlockErrorTag
from .report import _ReportErrorTag
from .results_info import _ResultsInfoErrorTag
from .stats_block import _StatsBlockErrorTag
from .value_block import _ValueBlockErrorTag
from .vcs_info import _VCSInfoErrorTag

__all__ = [
    "_CPUInfoErrorTag",
    "_ExecutionEnvironmentErrorTag",
    "_JSONSchemaErrorTag",
    "_MachineInfoErrorTag",
    "_MemoryInfoErrorTag",
    "_MetricsErrorTag",
    "_PythonInfoErrorTag",
    "_RawDataBlockErrorTag",
    "_ReportErrorTag",
    "_ResultsInfoErrorTag",
    "_StatsBlockErrorTag",
    "_SwapMemoryErrorTag",
    "_SystemInfoErrorTag",
    "_ValueBlockErrorTag",
    "_VirtualMemoryErrorTag",
    "_VCSInfoErrorTag",
]
