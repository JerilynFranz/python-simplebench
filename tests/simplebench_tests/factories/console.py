"""Factory functions for creating consoles for testing purposes."""
from io import StringIO
from typing import overload

from rich.console import Console

from ..cache_factory import CacheId, uncached_factory


# overloads provide a tooltip assist for the decorated function and IDE tooltips
# This is necessary because the cache_factory decorators create a function
# with a confusing tooltip (inherently).
@overload
def console_factory() -> Console:
    """Return a default Console instance for testing purposes.

    It is uncached by default to ensure that each call returns a fresh Console instance,
    preventing unintended side effects from shared state when using consoles across
    multiple tests.

    The console is created with default parameters that DO NOT produce screen output.

    It is configured as follows:
    - file: StringIO() (in-memory stream)
    - quiet: True
    - record: True
    - force_terminal: False
    - width: None
    - color_system: None
    - legacy_windows: False

    The default configuration ensures that the console does not attempt to
    write to the actual terminal and making it possible to retrieve the output
    using `rich.console.Console().export_text()`, making it suitable for use in
    automated tests.

    :return: A Console instance with default test parameters.
    :rtype: Console
    """


@overload
def console_factory(*, cache_id: CacheId = None) -> Console:
    """Return a default Console instance for testing purposes.

    It is uncached by default to ensure that each call returns a fresh Console instance,
    preventing unintended side effects from shared state when using consoles across
    multiple tests.

    The console is created with default parameters that DO NOT produce screen output.

    It is configured as follows:
    - file: StringIO() (in-memory stream)
    - quiet: True
    - record: True
    - force_terminal: False
    - width: None
    - color_system: None
    - legacy_windows: False

    The default configuration ensures that the console does not attempt to
    write to the actual terminal and making it possible to retrieve the output
    using `rich.console.Console().export_text()`, making it suitable for use in
    automated tests.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Console instance with default test parameters.
    :rtype: Console
    """


@uncached_factory
def console_factory(*, cache_id: CacheId = None) -> Console:  # pylint: disable=unused-argument
    """Return a default Console instance for testing purposes.

    It is uncached by default to ensure that each call returns a fresh Console instance,
    preventing unintended side effects from shared state when using consoles across
    multiple tests.

    The console is created with default parameters that DO NOT produce screen output.

    It is configured as follows:
    - file: StringIO() (in-memory stream)
    - quiet: True
    - record: True
    - force_terminal: False
    - width: None
    - color_system: None
    - legacy_windows: False

    The default configuration ensures that the console does not attempt to
    write to the actual terminal and making it possible to retrieve the output
    using `rich.console.Console().export_text()`, making it suitable for use in
    automated tests.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Console instance with default test parameters.
    :rtype: Console
    """
    return Console(file=StringIO(),
                   quiet=True,
                   record=True,
                   force_terminal=False,
                   width=None,
                   color_system=None,
                   legacy_windows=False)
