"""execution environment module

This provides an ExecutionEnvironment class that gathers and exposes information
about the Execution Environment at the time of its creation/
"""
from types import MappingProxyType
from typing import cast

from simplebench.report.versions.v1 import ImmutableExecutionEnvironmentData

from .._python_info import PythonInfo


class ExecutionEnvironment:
    """Create an ExecutionEnvironment instance gathering execution environment information.
    It currently only gathers Python interpreter information via the PythonInfo class.
    """
    __slots__ = ('_python', '_dict_cache')

    def __init__(self) -> None:
        """Create an ExecutionEnvironment instance gathering execution environment information.

        It currently only gathers Python interpreter information via the PythonInfo class.
        """
        self._python: PythonInfo = PythonInfo()
        self._dict_cache: ImmutableExecutionEnvironmentData = cast(ImmutableExecutionEnvironmentData,
            MappingProxyType({
                'python': self.python.to_dict(),
            }))

    def to_dict(self) -> ImmutableExecutionEnvironmentData:
        """Convert the ExecutionEnvironment to an immutable dictionary representation.

        This is useful for serialization or reporting purposes.

        :return ImmutableExecutionEnvironmentData: An immutable dictionary representation of the ExecutionEnvironment.
        """
        return self._dict_cache

    @property
    def python(self) -> PythonInfo:
        """The Python interpreter information."""
        return self._python
