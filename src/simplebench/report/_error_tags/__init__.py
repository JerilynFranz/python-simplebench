"""Exceptions for JSON reports and schemas."""

from ._cpu_info import _CPUInfoErrorTag
from ._environment_info import _EnvironmentInfoErrorTag
from ._execution_environment import _ExecutionEnvironmentErrorTag
from ._extras_object import _ExtrasErrorTag
from ._machine_info import _MachineInfoErrorTag
from ._memory_info import _MemoryInfoErrorTag
from ._metrics import _MetricsErrorTag
from ._python_info import _PythonInfoErrorTag
from ._raw_data_block import _RawDataBlockErrorTag
from ._stats_block import _StatsBlockErrorTag
from ._swap_memory import _SwapMemoryErrorTag
from ._system_info import _SystemInfoErrorTag
from ._value_block import _ValueBlockErrorTag
from ._vcs_info import _VCSInfoErrorTag
from ._virtual_memory import _VirtualMemoryErrorTag
from .json_schema import _JSONSchemaErrorTag
from .report import _ReportErrorTag
from .results_info import _ResultsInfoErrorTag

__all__ = [
    '_CPUInfoErrorTag',
    '_ExtrasErrorTag',
    '_ExecutionEnvironmentErrorTag',
    '_EnvironmentInfoErrorTag',
    '_JSONSchemaErrorTag',
    '_MachineInfoErrorTag',
    '_MemoryInfoErrorTag',
    '_MetricsErrorTag',
    '_PythonInfoErrorTag',
    '_RawDataBlockErrorTag',
    '_ReportErrorTag',
    '_ResultsInfoErrorTag',
    '_StatsBlockErrorTag',
    '_SwapMemoryErrorTag',
    '_SystemInfoErrorTag',
    '_ValueBlockErrorTag',
    '_VirtualMemoryErrorTag',
    '_VCSInfoErrorTag',
]
