"""KWArgs subclass for reports v1 PythonInfo()."""
from collections.abc import Mapping, Sequence

from simplebench.report.versions.v1 import PythonInfo
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class PythonInfoKWArgs(KWArgs):
    """KWArgs for report.versions.v1.PythonInfo()"""

    def __init__(
            self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            title: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            python_version: str | NoDefaultValue = NO_DEFAULT_VALUE,
            implementation: str | NoDefaultValue = NO_DEFAULT_VALUE,
            implementation_version: str | NoDefaultValue = NO_DEFAULT_VALUE,
            compiler: str | NoDefaultValue = NO_DEFAULT_VALUE,
            revision: str | NoDefaultValue = NO_DEFAULT_VALUE,
            buildno: str | NoDefaultValue = NO_DEFAULT_VALUE,
            builddate: str | NoDefaultValue = NO_DEFAULT_VALUE,
            command_line_flags: str | NoDefaultValue = NO_DEFAULT_VALUE,
            environment_variables: Mapping[str, str] | NoDefaultValue = NO_DEFAULT_VALUE,
            gc_is_enabled: bool | NoDefaultValue = NO_DEFAULT_VALUE,
            gc_thresholds: Sequence[int] | NoDefaultValue = NO_DEFAULT_VALUE,
            thread_switch_interval: float | NoDefaultValue = NO_DEFAULT_VALUE,
            architecture_bits: str | NoDefaultValue = NO_DEFAULT_VALUE,
            architecture_linkage: str | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize self."""
        super().__init__(PythonInfo.__init__, kwargs=locals(), globalns=globals())
