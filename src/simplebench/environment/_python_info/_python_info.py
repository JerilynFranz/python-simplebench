"""Python information utility functions.

This provides a PythonInfo class that gathers and exposes information
about the Python environment at the time of its creation using
the :module:`platform`, :module:`sys`, and :module:`os` modules.

It wraps several :func:`platform` module functions to provide a clean,
typed set of properties to access the :attr:`version`, :attr:`implementation`,
:attr:`compiler`, :attr:`revision`, and :attr:`build` details.

It also inspects :attr:`sys.flags` to provide a :attr:`command_line_flags` property
that summarizes the command line flags used to start the interpreter.

It also gathers information about the garbage collector settings
using the :module:`gc` module.

Exposed properties include:
- `version` - version number of the Python interpreter.
- `implementation` - name of the Python implementation.
- `implementation_version` - version of the Python implementation.
- `compiler` - compiler used to build the Python interpreter.
- `revision` - revision of the Python implementation.
- `buildno` - build number of the Python interpreter.
- `builddate` - build date of the Python interpreter.
- `command_line_flags` - command line flags used to start the interpreter.
- `gc_is_enabled` - whether the garbage collector is enabled.
- `gc_thresholds` - the garbage collection thresholds.
- `thread_switch_interval` - the thread switch interval in seconds.
"""

import gc
import platform
import sys
import sysconfig
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Final, Literal, cast

from simplebench.simplebench_types import CoreDataMapping

if TYPE_CHECKING:
    from simplebench.report.versions import v1 as report

_BUILDNO: Final[Literal[0]] = 0
"""Index for build number in platform.python_build() tuple."""
_BUILDDATE: Final[Literal[1]] = 1
"""Index for build date in platform.python_build() tuple."""

_BITS: Final[Literal[0]] = 0
"""Index for bits in platform.architecture() tuple."""
_LINKAGE: Final[Literal[1]] = 1
"""Index for linkage format in platform.architecture() tuple."""


class _NonExistentFlag:
    """Marker class for non-existent sys.flags attributes."""


_NO_FLAG_SET = _NonExistentFlag()
"""Marker instance for non-existent sys.flags attributes."""


class PythonInfo:
    """Create a PythonInfo facade for the Python :module:`platform` functions.

    It is a typed object-oriented representation of the Python environment
    where it was created and cleanly exposes the following :module:`platform`
    derived information. It is NOT a direct mapping of :module:`platform` functions,
    but rather a higher-level abstraction that provides the following properties
    after gathering and processing the relevant data to account for different
    Python implementations:

    - `version` - version number of the Python interpreter.
    - `implementation` - name of the Python implementation.
    - `implementation_version` - version of the Python implementation.
    - `compiler` - compiler used to build the Python interpreter.
    - `revision` - revision of the Python implementation.
    - `buildno` - build number of the Python interpreter.
    - `builddate` - build date of the Python interpreter.
    - `command_line_flags` - command line flags used to start the interpreter.

    It unpacks the :func:`platform.python_build()` tuple into separate string attributes for easier
    access and type casts :func:`platform.python_version()` to a string for static typing tools
    because there is no type hint for it in the :module:`platform` module and static analysis tools
    sometimes get confused by it.

    It also inspects :attr:`sys.flags` to construct a string representation of the command line flags
    used to start the interpreter.

    By 'snapshotting' this information at initialization, the PythonInfo class provides
    a consistent view of the Python environment that can be easily passed around and used
    in other parts of the application or reporting tools and makes it possible to
    serialize (such as by pickling) this information if needed.
    """
    _cached_proto: 'PythonInfo | None' = None
    """A cached instance of PythonInfo for reuse in future instances to optimize performance."""

    __slots__ = (
        '_python_version',
        '_implementation',
        '_implementation_version',
        '_compiler',
        '_revision',
        '_buildno',
        '_builddate',
        '_command_line_flags',
        '_gc_is_enabled',
        '_gc_thresholds',
        '_thread_switch_interval',
        '_architecture_bits',
        '_architecture_linkage',
        '_xoptions',
        '_sys_flags',
        '_gil_is_enabled',
        '_abiflags',
        '_config_args',
        '_py_debug',
        '_with_pymalloc',
        '_dict_cache',
    )

    def __init__(self) -> None:
        """Create a PythonInfo facade for the Python :module:`platform` functions.

        This is used to gather information about the current Python version, implementation,
        compiler, revision, and build details.

        It caches information that would not change during a run (like version, implementation,
        compiler, etc.) in a class-level variable for future instances to reuse and optimize
        performance, while still re-evaluating fields that could change during a run
        (like garbage collector settings, and thread switch interval)
        """
        cls = self.__class__
        if cls._cached_proto is None:
            architecture = platform.architecture()
            self._architecture_bits = architecture[_BITS]
            self._architecture_linkage = architecture[_LINKAGE]
            self._python_version = str(platform.python_version())
            self._implementation = platform.python_implementation()
            self._compiler = platform.python_compiler()
            self._implementation_version = self._python_implementation_version()
            self._revision = platform.python_revision()
            build_info = platform.python_build()
            self._buildno = build_info[_BUILDNO]
            self._builddate = build_info[_BUILDDATE]
            self._command_line_flags = self._python_command_line_flags()
            self._gc_is_enabled = gc.isenabled()
            self._gc_thresholds = gc.get_threshold()
            self._thread_switch_interval = sys.getswitchinterval()
            self._xoptions = self._python_xoptions()
            self._sys_flags = self._python_sys_flags()
            self._gil_is_enabled = self._python_gil_is_enabled()
            self._abiflags = getattr(sys, 'abiflags', '')
            self._config_args = self._sysconfig_config_args()
            self._py_debug = self._sysconfig_flag('Py_DEBUG')
            self._with_pymalloc = self._sysconfig_flag('WITH_PYMALLOC')
            self._dict_cache: None | MappingProxyType[str, object] = None
            cls._cached_proto = self

        for field in cls.__slots__:
            self.__setattr__(field, getattr(cls._cached_proto, field))

        self._gc_is_enabled = gc.isenabled()
        self._gc_thresholds = gc.get_threshold()
        self._thread_switch_interval = sys.getswitchinterval()
        self._gil_is_enabled = self._python_gil_is_enabled()

        output: dict[str, object] = {}
        fields = cls.__slots__
        for field in fields:
            if field == '_dict_cache':
                continue
            name = field.lstrip('_')
            output[name] = getattr(self, field)
        self._dict_cache = MappingProxyType(output)
        return

    @property
    def python_version(self) -> str:
        """Return the Python version string."""
        return self._python_version

    @property
    def implementation(self) -> str:
        """Return the Python implementation name."""
        return self._implementation

    @property
    def implementation_version(self) -> str:
        """Return the Python implementation version string."""
        return self._implementation_version

    @property
    def compiler(self) -> str:
        """Return the Python compiler string."""
        return self._compiler

    @property
    def revision(self) -> str:
        """Return the Python implementation revision string."""
        return self._revision

    @property
    def buildno(self) -> str:
        """Return the Python build number."""
        return self._buildno

    @property
    def builddate(self) -> str:
        """Return the Python build date."""
        return self._builddate

    @property
    def command_line_flags(self) -> str:
        """Return the command line flags used to start the interpreter."""
        return self._command_line_flags

    @property
    def gc_is_enabled(self) -> bool:
        """Return a boolean indicating if the garbage collector is enabled."""
        return self._gc_is_enabled

    @property
    def gc_thresholds(self) -> tuple[int, int, int]:
        """Return a tuple of the garbage collection thresholds."""
        return self._gc_thresholds

    @property
    def thread_switch_interval(self) -> float:
        """Return the thread switch interval in seconds."""
        return self._thread_switch_interval

    @property
    def architecture_bits(self) -> str:
        """Return a string containing the architecture bits."""
        return self._architecture_bits

    @property
    def architecture_linkage(self) -> str:
        """Return a string containing the architecture linkage format."""
        return self._architecture_linkage

    @property
    def xoptions(self) -> CoreDataMapping[str | bool]:
        return self._xoptions

    def _python_implementation_version(self) -> str:
        """Return the Python implementation revision.

        This handles special cases for different Python implementations.

        For CPython, this is the same as :func:`platform.python_version`.
        For PyPy, this is the PyPy version (e.g., '7.3.5').

        :return str : The Python implementation version.
        """
        python_implementation: str = platform.python_implementation()
        py_implementation_version: str = platform.python_version()
        if python_implementation == 'PyPy':
            version_info = getattr(sys, 'pypy_version_info', None)
            if version_info is not None:
                py_implementation_version = (
                    f'{version_info.major:d}.{version_info.minor:d}.{version_info.micro:d}'
                    f'-{version_info.releaselevel}{version_info.serial:d}'
                )
            else:
                py_implementation_version = 'unknown'
        return py_implementation_version

    def _python_command_line_flags(self) -> str:
        """Return the Python command line flags used to start the interpreter.

        This inspects :attr:`sys.flags` and constructs a string representation
        of the command line flags that were used when starting the Python interpreter.

        :return str: The command line flags as a string.
        """
        active_flags = set()
        sys_flags = sys.flags
        flag_map = self._flag_map()

        for flag_name in sorted(flag_map.keys()):
            flag_value = getattr(sys_flags, flag_name, _NO_FLAG_SET)

            if flag_value is _NO_FLAG_SET or not flag_value:
                continue

            arg = flag_map[flag_name]
            if callable(arg):
                # Special cases like -v and -O that depend on the flag's value.
                active_flags.add(arg(flag_value))
            else:
                active_flags.add(str(arg))

        return ' '.join(sorted(list(active_flags)))

    def _flag_map(self) -> dict[str, str | bool | int | Callable[[Any], str]]:
        """Return a mapping of sys.flags attribute names to command-line representations.

        This is used internally to construct the command line flags string.

        :return: A dictionary mapping flag names to their command-line representation.
        """
        flag_map: dict[str, str | bool | int | Callable[[Any], str]] = {
            'bytes_warning': '-b',
            'context_aware_warnings': '-X context_aware_warnings',
            'debug': '-d',
            'dev_mode': '-X dev',
            'dont_write_bytecode': '-B',
            'gil': '-X gil',
            'hash_randomization': '-R',
            'ignore_environment': '-E',
            'inspect': '-i',
            'int_max_str_digits': '-X int_max_str_digits',
            'isolated': '-I',
            'no_site': '-S',
            'no_user_site': '-s',
            'optimize': lambda v: f'-O{v}' if v > 1 else '-O',
            'quiet': '-q',
            'safe_path': '-P',
            'thread_inherit_context': '-X thread_inherit_context',
            'utf8_mode': '-X utf8',
            'verbose': lambda v: '-v' * v,
            'warn_default_encoding': '-X warn_default_encoding',
        }
        return flag_map

    def to_dict(self) -> 'report.ImmutablePythonInfoData':
        """Get the Python information dictionary.

        This dictionary contains all the Python information gathered from the
        :module:`pythoninfo` module at the time of the instance's creation.
        :return report.ImmutablePythonInfoData: An immutable dictionary containing all
            the Python information.
        """
        return cast('report.ImmutablePythonInfoData', self._dict_cache)

    def _python_xoptions(self) -> CoreDataMapping[str | bool]:
        xoptions = getattr(sys, '_xoptions', {})
        output: dict[str, str | bool] = {}
        for key, value in sorted(xoptions.items()):
            output[str(key)] = value
        return CoreDataMapping(output)

    def _python_sys_flags(self) -> CoreDataMapping[int]:
        output: dict[str, int] = {}
        sys_flags = sys.flags

        for flag_name in sorted(self._flag_map().keys()):
            flag_value: int | _NonExistentFlag = getattr(sys_flags, flag_name, _NO_FLAG_SET)
            if isinstance(flag_value, _NonExistentFlag):
                continue
            output[flag_name] = int(flag_value)

        return CoreDataMapping(output)

    def _python_gil_is_enabled(self) -> bool | None:
            gil_state = getattr(sys, '_is_gil_enabled', None)
            if callable(gil_state):
                return bool(gil_state())
            return None

    def _sysconfig_config_args(self) -> str | None:
        config_args = sysconfig.get_config_var('CONFIG_ARGS')
        if config_args is None:
            return None
        return str(config_args)

    def _sysconfig_flag(self, name: str) -> bool | None:
        value = sysconfig.get_config_var(name)
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return value != 0
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized == '':
                return None
            if normalized in {'0', 'false', 'no', 'off'}:
                return False
            if normalized in {'1', 'true', 'yes', 'on'}:
                return True
        return bool(value)
