"""Exceptions for JSON reports and schemas."""
# ruff: noqa: F401

from ._cpu_info import _CPUInfoErrorTag
from ._environment_info import _EnvironmentInfoErrorTag
from ._extras_object import _ExtrasErrorTag
from ._machine_info import _MachineInfoErrorTag
from ._memory_info import _MemoryInfoErrorTag
from ._metric import _MetricErrorTag
from ._metric_type import _MetricTypeErrorTag
from ._metric_types import _MetricTypesErrorTag
from ._metrics import _MetricsErrorTag
from ._metrics_object import _MetricsObjectErrorTag
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

__all__: list[str] = []
