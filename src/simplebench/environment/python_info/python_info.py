"""Python information utility functions.

This provides a PythonInfo class that gathers and exposes information
about the Python environment at the time of its creation using
the :module:`platform`, :module:`sys`, and :module:`os` modules.

It wraps several :func:`platform` module functions to provide a clean,
typed set of properties to access the :attr:`version`, :attr:`implementation`,
:attr:`compiler`, :attr:`revision`, and :attr:`build` details.

It also inspects :attr:`sys.flags` to provide a :attr:`command_line_flags` property
that summarizes the command line flags used to start the interpreter and a
:attr:`environment_variables` property that exposes a read-only mapping of
Python-specific environment variables that are set.

It also gathers information about the garbage collector settings
using the :module:`gc` module.
"""
import gc
import os
import platform
import sys
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Final, Literal

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


_NoFlagSet = _NonExistentFlag()
"""Marker instance for non-existent sys.flags attributes."""


@dataclass(frozen=True, slots=True)
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
    - `environment_variables` - Python-specific environment variables that are set.

    It unpacks the :func:`platform.python_build()` tuple into separate string attributes for easier
    access and type casts :func:`platform.python_version()` to a string for static typing tools
    because there is no type hint for it in the :module:`platform` module and static analysis tools
    sometimes get confused by it.

    It also inspects :attr:`sys.flags` to construct a string representation of the command line flags
    used to start the interpreter and gathers a read-only mapping of Python-specific environment variables
    that are set in the current environment. Both of the are sorted for consistency in
    representation and comparison.

    By 'snapshotting' this information at initialization, the PythonInfo class provides
    a consistent view of the Python environment that can be easily passed around and used
    in other parts of the application or reporting tools and makes it possible to
    serialize (such as by pickling) this information if needed.
    """
    version: str
    """The Python version string."""
    implementation: str
    """The Python implementation name."""
    implementation_version: str
    """The Python implementation version string."""
    compiler: str
    """The Python compiler string."""
    revision: str
    """The Python implementation revision string."""
    buildno: str
    """The Python build number."""
    builddate: str
    """The Python build date."""
    command_line_flags: str
    """The command line flags used to start the interpreter."""
    environment_variables: MappingProxyType[str, str]
    """A read-only dictionary of set Python-specific environment variables."""
    gc_is_enabled: bool
    """A boolean indicating if the garbage collector is enabled."""
    gc_thresholds: tuple[int, int, int]
    """A tuple of the garbage collection thresholds."""
    thread_switch_interval: float
    """The thread switch interval in seconds."""

    def __init__(self) -> None:
        """Create a PythonInfo facade for the Python :module:`platform` functions.

        This is used to gather information about the current Python version, implementation,
        compiler, revision, and build details. This constructor accepts no arguments
        and always reflects the environment in which it was originally created.
        """
        # Uses object.__setattr__ because the class is frozen
        architecture = platform.architecture()
        object.__setattr__(self, 'architecture_bits', architecture[_BITS])
        object.__setattr__(self, 'architecture_linkage', architecture[_LINKAGE])
        object.__setattr__(self, 'version', str(platform.python_version()))
        object.__setattr__(self, 'implementation', platform.python_implementation())
        object.__setattr__(self, 'compiler', platform.python_compiler())
        object.__setattr__(self, 'implementation_version', self._python_implementation_version())
        object.__setattr__(self, 'revision', platform.python_revision())
        build_info = platform.python_build()
        object.__setattr__(self, 'buildno', build_info[_BUILDNO])
        object.__setattr__(self, 'builddate', build_info[_BUILDDATE])
        object.__setattr__(self, 'command_line_flags', self._command_line_flags())
        object.__setattr__(self, 'environment_variables', self._environment_variables())
        object.__setattr__(self, 'gc_is_enabled', gc.isenabled())
        object.__setattr__(self, 'gc_thresholds', gc.get_threshold())
        object.__setattr__(self, 'thread_switch_interval', sys.getswitchinterval())

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
                    f'-{version_info.releaselevel}{version_info.serial:d}')
            else:
                py_implementation_version = 'unknown'
        return py_implementation_version

    def _command_line_flags(self) -> str:
        """Return the Python command line flags used to start the interpreter.

        This inspects :attr:`sys.flags` and constructs a string representation
        of the command line flags that were used when starting the Python interpreter.

        :return str: The command line flags as a string.
        """
        active_flags = set()
        sys_flags = sys.flags
        flag_map = self._flag_map()

        for flag_name in sorted(flag_map.keys()):
            flag_value = getattr(sys_flags, flag_name, _NoFlagSet)

            if flag_value is _NoFlagSet or not flag_value:
                continue

            arg = flag_map[flag_name]
            if callable(arg):
                # Special cases like -v and -O that depend on the flag's value.
                active_flags.add(arg(flag_value))
            else:
                active_flags.add(arg)

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

    def _environment_variables(self) -> MappingProxyType[str, str]:
        """Return a read-only dictionary of set Python environment variables.

        This inspects :attr:`os.environ` for a predefined list of variables
        that can influence Python's behavior.

        :return: A mapping proxy of the set environment variables.
        """
        # A comprehensive list of Python-specific environment variables.
        python_vars = (
            'PYTHONHOME', 'PYTHONPATH', 'PYTHONSAFEPATH', 'PYTHONPLATLIBDIR',
            'PYTHONSTARTUP', 'PYTHONOPTIMIZE', 'PYTHONBREAKPOINT', 'PYTHONDEBUG',
            'PYTHONINSPECT', 'PYTHONUNBUFFERED', 'PYTHONVERBOSE', 'PYTHONCASEOK',
            'PYTHONDONTWRITEBYTECODE', 'PYTHONPYCACHEPREFIX', 'PYTHONHASHSEED',
            'PYTHONINTMAXSTRDIGITS', 'PYTHONIOENCODING', 'PYTHONNOUSERSITE',
            'PYTHONUSERBASE', 'PYTHONEXECUTABLE', 'PYTHONWARNINGS',
            'PYTHONFAULTHANDLER', 'PYTHONTRACEMALLOC', 'PYTHONPROFILEIMPORTTIME',
            'PYTHONASYNCIODEBUG', 'PYTHONMALLOC', 'PYTHONMALLOCSTATS',
            'PYTHONLEGACYWINDOWSFSENCODING', 'PYTHONLEGACYWINDOWSSTDIO',
            'PYTHONCOERCECLOCALE', 'PYTHONDEVMODE', 'PYTHONUTF8',
            'PYTHONWARNDEFAULTENCODING', 'PYTHONNODEBUGRANGES', 'PYTHONPERFSUPPORT',
            'PYTHON_PERF_JIT_SUPPORT', 'PYTHON_DISABLE_REMOTE_DEBUG',
            'PYTHON_CPU_COUNT', 'PYTHON_FROZEN_MODULES', 'PYTHON_COLORS',
            'PYTHON_BASIC_REPL', 'PYTHON_HISTORY', 'PYTHON_GIL',
            'PYTHON_THREAD_INHERIT_CONTEXT', 'PYTHON_CONTEXT_AWARE_WARNINGS',
            'PYTHON_JIT', 'PYTHON_TLBC', 'PYTHONDUMPREFS', 'PYTHONDUMPREFSFILE',
            'PYTHON_PRESITE'
        )

        env_data = {}
        for var_name in sorted(python_vars):
            value = os.getenv(var_name)
            if value is not None:
                env_data[var_name] = value

        return MappingProxyType(env_data)
