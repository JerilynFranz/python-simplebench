"""Immutable PythonInfo implementation.

It provides methods to convert to and from dictionary representations
and includes schema validation specific to version 1 reports.

The version 1 PythonInfo is the first stable version of the JSON PythonInfo format
and serves as a foundation for future versions.

As the foundational version, this class is considered immutable. Future versions
will inherit from this class to extend its functionality, but this implementation
will not be changed.
"""

import threading
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Any

from simplebench.report.base import BasePythonInfo, JSONSchema

from . import _validate
from .python_info_schema import PythonInfoSchema
from .typeddict_types import ImmutablePythonInfoDict, PythonInfoData

_LOCK = threading.Lock()

__all__ = []


class PythonInfo(BasePythonInfo):
    """Immutable class representing python execution environment in a report (V1)."""

    SCHEMA: type[JSONSchema] = PythonInfoSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON PythonInfo type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON PythonInfo version number."""

    ID: str = SCHEMA.ID
    """The JSON PythonInfo identifier property value for version 1 reports."""

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
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
        hash_id: str,
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

        :param str hash_id: The unique hash identifier for this PythonInfo. If an
            empty string is provided, a value will be automatically computed based on
            the other properties.
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
        self._hash_id = _validate.hash_id(hash_id)
        self._python_version = _validate.python_version(python_version)
        self._implementation = _validate.implementation(implementation)
        self._implementation_version = _validate.implementation_version(implementation_version)
        self._compiler = _validate.compiler(compiler)
        self._revision = _validate.revision(revision)
        self._buildno = _validate.buildno(buildno)
        self._builddate = _validate.builddate(builddate)
        self._command_line_flags = _validate.command_line_flags(command_line_flags)
        self._environment_variables = _validate.environment_variables(environment_variables)
        self._gc_is_enabled = _validate.gc_is_enabled(gc_is_enabled)
        self._gc_thresholds = _validate.gc_thresholds(gc_thresholds)
        self._thread_switch_interval = _validate.thread_switch_interval(thread_switch_interval)
        self._architecture_bits = _validate.architecture_bits(architecture_bits)
        self._architecture_linkage = _validate.architecture_linkage(architecture_linkage)
        self._from_dict: ImmutablePythonInfoDict | None = None

    @classmethod
    def from_dict(cls, data: PythonInfoData) -> 'PythonInfo':
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
            skip_fields={'version', 'type'},
            optional_fields={'hash_id', 'version', 'type'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutablePythonInfoDict:
        """Returns the PythonInfo as an immutable MappingProxyType dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`PythonInfoSchema`
        for the version 1 PythonInfo as mirrored by :class:`ImmutablePythonInfoDict`.

        The dictionary is cached after the first call to avoid redundant
        serialization work on subsequent calls. In effect, this makes the method
        idempotent and a lazy property of the instance.

        This method will raise an AttributeError if any required property
        is missing from the instance.

        The returned instance is of type :class:`MappingProxyType` to ensure immutability
        and will always reflect the state of the instance at the time of the first call.

        The exact same instance is returned on subsequent calls to ensure consistency
        and this is true even in multi-threaded scenarios.

        :return ImmutablePythonInfoDict: A dictionary representation of the PythonInfo.
        :raises AttributeError: If any required property is missing.
        """
        if self._from_dict is None:
            with _LOCK:
                # Double-checked in case another thread populated while waiting for the lock.
                if self._from_dict is not None:
                    return self._from_dict
                self._from_dict = self._to_dict_helper(ImmutablePythonInfoDict)
        return self._from_dict

    @property
    def compiler(self) -> str:
        """Get the compiler property.

        :return: The compiler string.
        """
        return self._compiler

    @property
    def implementation(self) -> str:
        """Get the implementation property.

        :return: The implementation string.
        """
        return self._implementation

    @property
    def implementation_version(self) -> str:
        """Get the implementation_version property.

        :return: The implementation_version string.
        """
        return self._implementation_version

    @property
    def python_version(self) -> str:
        """Get the python_version property.

        :return: The python_version string.
        """
        return self._python_version

    @property
    def buildno(self) -> str:
        """Get the build number property.

        :return: The build number string.
        """
        return self._buildno

    @property
    def builddate(self) -> str:
        """Get the build date property.

        :return: The build date string.
        """
        return self._builddate

    @property
    def command_line_flags(self) -> str:
        """Get the command_line_flags property.

        :return: The command_line_flags string.
        """
        return self._command_line_flags

    @property
    def environment_variables(self) -> MappingProxyType[str, str]:
        """Get the environment_variables property.

        :return: The environment_variables mapping.
        """
        return MappingProxyType(self._environment_variables)

    @property
    def gc_is_enabled(self) -> bool:
        """Get the gc_is_enabled property.

        :return: The gc_is_enabled boolean.
        """
        return self._gc_is_enabled

    @property
    def gc_thresholds(self) -> tuple[int, int, int]:
        """Get the gc_thresholds property.

        :return: The gc_thresholds tuple.
        """
        return self._gc_thresholds

    @property
    def thread_switch_interval(self) -> float:
        """Get the thread_switch_interval property.

        :return: The thread_switch_interval float.
        """
        return self._thread_switch_interval

    @property
    def architecture_bits(self) -> str:
        """Get the architecture_bits property.

        :return: The architecture_bits string.
        """
        return self._architecture_bits

    @property
    def architecture_linkage(self) -> str:
        """Get the architecture_linkage property.

        :return: The architecture_linkage string.
        """
        return self._architecture_linkage

    @property
    def revision(self) -> str:
        """Get the revision property.

        :return: The revision string.
        """
        return self._revision

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        It is lazily computed on first access if not provided during initialization.

        :return: The hash_id string.
        :raises SimpleBenchAttributeError: If any required property is missing.
        """
        if self._hash_id == '':
            self._hash_id = self._hash_id_helper(ImmutablePythonInfoDict)
        return self._hash_id

    def __repr__(self) -> str:
        """Get the string representation of the PythonInfo instance.

        :return: The string representation of the PythonInfo.
        """
        # Get the init parameters excluding 'type' and 'version'
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
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
