"""Immutable PythonInfo implementation.

It provides methods to convert to and from dictionary representations
and includes schema validation specific to version 1 reports.

The version 1 PythonInfo is the first stable version of the JSON PythonInfo format
and serves as a foundation for future versions.

As the foundational version, this class is considered immutable. Future versions
will inherit from this class to extend its functionality, but this implementation
will not be changed.
"""

from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Any

from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import CoreDataMapping

from . import _validate
from .python_info_schema import PythonInfoSchema
from .typeddict_types import ImmutablePythonInfoDict, PythonInfoData

__all__: list[str] = []


class PythonInfo(report.EnvironmentInfo):
    """Immutable class representing python execution environment in a report (V1)."""

    SCHEMA = PythonInfoSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON PythonInfo type property value for version 1 reports."""

    SEMANTIC_TYPE: str = SCHEMA.SEMANTIC_TYPE
    """The semantic type of the python environment information, formatted as 'namespace::type_name'."""

    VERSION: int = SCHEMA.VERSION
    """The JSON PythonInfo version number."""

    ID: str = SCHEMA.ID
    """The JSON PythonInfo identifier property value for version 1 reports."""

    _init_params_cache: MappingProxyType[str, Any] | None = None
    """Cache for the constructor parameters of the ResultsInfo class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(PythonInfoData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    def __init__(
        self,
        *,
        hash_id: str = '',
        python_version: str,
        implementation: str,
        implementation_version: str,
        compiler: str,
        revision: str,
        buildno: str,
        builddate: str,
        command_line_flags: str,
        environment_variables: Mapping[str, str],
        gc_is_enabled: bool,
        gc_thresholds: Sequence[int],
        thread_switch_interval: float,
        architecture_bits: str,
        architecture_linkage: str,
    ) -> None:
        """Initialize a PythonInfo instance.

        :param hash_id: (default = '') The unique hash identifier for this PythonInfo. If an
            empty string is provided, a value will be automatically computed based on
            the other properties.
        :type hash_id: str
        :param str python_version: The Python version string.
        :param str implementation: The Python implementation name.
        :param str implementation_version: The Python implementation version string.
        :param str compiler: The compiler used to build Python.
        :param str revision: The Python source code revision identifier.
        :param str buildno: The Python build number.
        :param str builddate: The Python build date string.
        :param str command_line_flags: The command line flags used to start Python.
        :param Mapping[str, str] environment_variables: The Python-specific environment variables.
        :param bool gc_is_enabled: Whether the garbage collector is enabled.
        :param Sequence[int] gc_thresholds: The garbage collection thresholds.
        :param float | int thread_switch_interval: The thread switch interval in seconds.
        :param str architecture_bits: The architecture bits (e.g., '32bit', '64bit').
        :param str architecture_linkage: The architecture linkage (e.g., 'ELF', 'WindowsPE').
        """
        data = {
            'python_version': _validate.python_version(python_version),
            'implementation': _validate.implementation(implementation),
            'implementation_version': _validate.implementation_version(implementation_version),
            'compiler': _validate.compiler(compiler),
            'revision': _validate.revision(revision),
            'buildno': _validate.buildno(buildno),
            'builddate': _validate.builddate(builddate),
            'command_line_flags': _validate.command_line_flags(command_line_flags),
            'environment_variables': _validate.environment_variables(environment_variables),
            'gc_is_enabled': _validate.gc_is_enabled(gc_is_enabled),
            'gc_thresholds': _validate.gc_thresholds(gc_thresholds),
            'thread_switch_interval': _validate.thread_switch_interval(thread_switch_interval),
            'architecture_bits': _validate.architecture_bits(architecture_bits),
            'architecture_linkage': _validate.architecture_linkage(architecture_linkage)
        }
        super().__init__(data=data,
                         semantic_type=self.SEMANTIC_TYPE,
                         hash_id=hash_id,
                         title='Python Environment',
                         description='Information about the Python execution environment')

    @classmethod
    def from_dict(cls, data: PythonInfoData) -> 'PythonInfo':  # type: ignore[override]
        """Create a PythonInfo instance from a dictionary.

        .. code-block:: python3
           :caption: Example

            python_info = PythonInfo.from_dict(data)

        The dictionary must conform to the expected structure for the PythonInfo
        representation. The 'version' and 'type' properties are validated
        against the class's VERSION and TYPE attributes if they are present.

        :param data: The dictionary containing PythonInfo information.
        :return: A PythonInfo instance.
        """
        allowed_keys = cls._data_params()
        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type', 'semantic_type', 'title', 'description'},
            optional_fields={'hash_id', 'version', 'type', 'semantic_type', 'description'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
        )
        unwrapped_data = kwargs.pop('data', {})
        kwargs.update(unwrapped_data)
        return cls(**kwargs)

    def to_dict(self) -> ImmutablePythonInfoDict:  # type: ignore[override]
        """Returns the PythonInfo as an immutable CoreDataMapping dictionary
        suitable for JSON serialization.

        This includes all properties defined in the :class:`PythonInfoSchema`
        for the version 1 PythonInfo as mirrored by :class:`ImmutablePythonInfoDict`.

        The returned instance is of type :class:`CoreDataMapping` to ensure immutability
        and will always reflect the state of the instance at the time of the first call.

        The exact same instance is returned on all calls.

        :return ImmutablePythonInfoDict: A dictionary representation of the PythonInfo.
        :raises AttributeError: If any required property is missing.
        """
        return super().to_dict()  # type: ignore[return-value]

    @property
    def compiler(self) -> str:
        """Get the compiler property.

        :return: The compiler string.
        """
        return self.data['compiler']  # type: ignore

    @property
    def implementation(self) -> str:
        """Get the implementation property.

        :return: The implementation string.
        """
        return self.data['implementation']  # type: ignore

    @property
    def implementation_version(self) -> str:
        """Get the implementation_version property.

        :return: The implementation_version string.
        """
        return self.data['implementation_version']  # type: ignore

    @property
    def python_version(self) -> str:
        """Get the python_version property.

        :return: The python_version string.
        """
        return self.data['python_version']  # type: ignore

    @property
    def buildno(self) -> str:
        """Get the build number property.

        :return: The build number string.
        """
        return self.data['buildno']  # type: ignore

    @property
    def builddate(self) -> str:
        """Get the build date property.

        :return: The build date string.
        """
        return self.data['builddate']  # type: ignore

    @property
    def command_line_flags(self) -> str:
        """Get the command_line_flags property.

        :return: The command_line_flags string.
        """
        return self.data['command_line_flags']  # type: ignore

    @property
    def environment_variables(self) -> CoreDataMapping[str]:
        """Get the environment_variables property.

        :return: The environment_variables mapping.
        """
        return self.data['environment_variables']  # type: ignore

    @property
    def gc_is_enabled(self) -> bool:
        """Get the gc_is_enabled property.

        :return: The gc_is_enabled boolean.
        """
        return self.data['gc_is_enabled']  # type: ignore

    @property
    def gc_thresholds(self) -> tuple[int, int, int]:
        """Get the gc_thresholds property.

        :return: The gc_thresholds tuple.
        """
        return self.data['gc_thresholds']  # type: ignore

    @property
    def thread_switch_interval(self) -> float:
        """Get the thread_switch_interval property.

        :return: The thread_switch_interval float.
        """
        return self.data['thread_switch_interval']  # type: ignore

    @property
    def architecture_bits(self) -> str:
        """Get the architecture_bits property.

        :return: The architecture_bits string.
        """
        return self.data['architecture_bits']  # type: ignore

    @property
    def architecture_linkage(self) -> str:
        """Get the architecture_linkage property.

        :return: The architecture_linkage string.
        """
        return self.data['architecture_linkage']  # type: ignore

    @property
    def revision(self) -> str:
        """Get the revision property.

        :return: The revision string.
        """
        return self.data['revision']  # type: ignore

    def for_json(self) -> ImmutablePythonInfoDict:  # type: ignore[override]
        """Get the JSON-serializable dictionary representation of this PythonInfo.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this PythonInfo.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this PythonInfo.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this PythonInfo.
        """
        return self.to_dict().as_json()  # type: ignore

    def __repr__(self) -> str:
        """Get the string representation of the PythonInfo instance.

        :return: The string representation of the PythonInfo.
        """
        init_params = self.data.thaw()
        init_params['hash_id'] = self.hash_id
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the PythonInfo instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two PythonInfo instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, PythonInfo):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'PythonInfo':
        """Return the same instance since PythonInfo is immutable."""
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'PythonInfo':
        """Return the same instance since PythonInfo is immutable."""
        return self
