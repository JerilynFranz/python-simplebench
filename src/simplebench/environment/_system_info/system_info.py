"""System information utility functions.

This provides a SystemInfo class that gathers and exposes information
about the System environment at the time of its creation using
the :module:`platform` module.

It wraps several :module:`platform` module functions to provide a clean,
typed set of properties to access system, release, version, machine, and node.

"""

import platform
from typing import TYPE_CHECKING, cast

from simplebench.simplebench_types import CoreDataMapping


if TYPE_CHECKING:
    from typing import ClassVar
    from simplebench.report.versions import v1 as report


class SystemInfo:
    """Create a SystemInfo facade for the system related :module:`platform` functions.

    It is a typed object-oriented representation of the System environment
    and cleanly exposes the following :module:`platform` functions
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

    _singleton_cache: 'ClassVar[SystemInfo | None]' = None
    """The cached singleton of the SystemInfo instance."""

    __slots__ = ('_system', '_release', '_system_version', '_machine', '_dict_cache')

    def __init__(self) -> None:
        """Create a SystemInfo facade for the System :module:`platform` functions.

        This is used to gather information about the current System version, implementation,
        compiler, revision, and build details. This constructor accepts no arguments
        and always reflects the environment in which it was originally created.
        """
        cls = self.__class__
        self._system: str
        self._release: str
        self._system_version: str
        self._machine: str
        self._dict_cache: report.ImmutableSystemInfoData

        if cls._singleton_cache is None:
            uname = platform.uname()
            self._system = uname.system
            self._release = uname.release
            self._system_version = uname.version
            self._machine = uname.machine

            # Prerender the dict cache
            output: dict[str, str] = {}
            for field in cls.__slots__:
                name = field.lstrip('_')
                output[name] = getattr(self, field)
            self._dict_cache = cast('report.ImmutableSystemInfoData', CoreDataMapping(output))
            cls._singleton_cache = self

        for field in cls.__slots__:
            name = field.lstrip('_')
            setattr(self, field, getattr(cls._singleton_cache, field))

    def to_dict(self) -> 'report.ImmutableSystemInfoData':
        """Convert the SystemInfo to an immutable dictionary representation.

        This is useful for serialization or reporting purposes.

        :return report.ImmutableSystemInfoData: An immutable dictionary representation of the SystemInfo.
        """
        return self._dict_cache
