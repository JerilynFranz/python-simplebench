"""System information utility functions.

This provides a SystemInfo class that gathers and exposes information
about the System environment at the time of its creation using
the :module:`platform` module.

It wraps several :module:`platform` module functions to provide a clean,
typed set of properties to access system, release, version, machine, and node.

"""

import dataclasses
import platform
from types import MappingProxyType
from typing import TYPE_CHECKING, cast

from simplebench.report.versions.v1 import ImmutableSystemInfoData

if TYPE_CHECKING:
    from typing import ClassVar


@dataclasses.dataclass(frozen=True)
class SystemInfo:
    """Create a SystemInfo facade for the system related :module:`platform` functions.

    It is a typed object-oriented representation of the System environment
    andcleanly exposes the following :module:`platform` functions
    as properties:

    - :func:`platform.system` - name of the operating system.
    - :func:`platform.release` - release of the operating system.
    - :func:`platform.version` - version of the operating system.
    - :func:`platform.machine` - machine type, e.g. 'x86_64'.

    By 'snapshotting' this information at initialization, the SystemInfo class provides
    a consistent view of the System environment that can be easily passed around and used
    in other parts of the application or reporting tools and makes it possible to
    serialize (such as by pickling) this information if needed.
    """

    system: str
    """The System OS identifier string.

    Examples include 'Linux', 'Windows', 'Darwin' (for macOS), etc.

    May be blank or empty if the system could not be identified.
    """
    release: str
    """The System release string."""
    system_version: str
    """The System version string."""
    machine: str
    """The machine type, e.g. 'x86_64' or 'arm64'."""

    _singleton_cache: 'ClassVar[SystemInfo | None]' = None
    """The cached singleton of the SystemInfo instance."""

    __slots__ = ('system', 'release', 'system_version', 'machine', '_dict_cache')

    def __init__(self) -> None:
        """Create a SystemInfo facade for the System :module:`platform` functions.

        This is used to gather information about the current System version, implementation,
        compiler, revision, and build details. This constructor accepts no arguments
        and always reflects the environment in which it was originally created.
        """
        cls = self.__class__
        if cls._singleton_cache is None:
            # Uses object.__setattr__ because the class is frozen
            uname = platform.uname()
            object.__setattr__(self, 'system', uname.system)
            object.__setattr__(self, 'release', uname.release)
            object.__setattr__(self, 'system_version', uname.version)
            object.__setattr__(self, 'machine', uname.machine)

            # Prerender the dict cache
            output: dict[str, object] = {}
            fields: tuple[dataclasses.Field, ...] = dataclasses.fields(self)
            for field in fields:
                name = field.name
                output[name] = getattr(self, name)
            dict_instance = MappingProxyType(output)
            object.__setattr__(self, '_dict_cache', dict_instance)
            cls._singleton_cache = self

        else:
            object.__setattr__(self, 'system', cls._singleton_cache.system)
            object.__setattr__(self, 'release', cls._singleton_cache.release)
            object.__setattr__(self, 'system_version', cls._singleton_cache.system_version)
            object.__setattr__(self, 'machine', cls._singleton_cache.machine)
            object.__setattr__(self, '_dict_cache', cls._singleton_cache._dict_cache)

    def to_dict(self) -> ImmutableSystemInfoData:
        """Convert the SystemInfo to an immutable dictionary representation.

        This is useful for serialization or reporting purposes.

        :return ImmutableSystemInfoData: An immutable dictionary representation of the SystemInfo.
        """
        return cast(ImmutableSystemInfoData, getattr(self, '_dict_cache'))
