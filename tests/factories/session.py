""""Factories for creating Session instances for testing purposes."""
from argparse import ArgumentParser
from typing import overload

from simplebench.enums import Verbosity
from simplebench.session import Session

from ..cache_factory import CACHE_DEFAULT, CacheId, cached_factory, uncached_factory
from ..kwargs import SessionKWArgs
from . import case_factory, console_factory, output_path_factory, runner_factory

# The overloads provide a tooltip assist for the decorated function and IDE tooltips
# This is necessary because the cache_factory decorators create a function
# with a confusing tooltip (inherently).

# See https://github.com/JerilynFranz/python-simplebench/issues/4 for context.


@overload
def session_factory() -> Session:
    """Return a default Session instance for testing purposes.

    The Session is initialized with default attributes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Session instance.
    :rtype: Session
    """


@overload
def session_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Session:
    """Return a default Session instance for testing purposes.

    The Session is initialized with default attributes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Session instance.
    :rtype: Session
    """


@cached_factory
def session_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Session:
    """Return a default Session instance for testing purposes.

    The Session is initialized with default attributes and cached by default.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A Session instance.
    :rtype: Session
    """
    return Session(cases=[case_factory(cache_id=cache_id)], verbosity=Verbosity.QUIET)


# The overloads provide a tooltip assist for the decorated function and IDE tooltips
# This is necessary because the cache_factory decorators create a function
# with a confusing tooltip (inherently).
@overload
def session_kwargs_factory() -> SessionKWArgs:
    """Return a dictionary of default Session keyword arguments for testing purposes.

    By default, this function is uncached to ensure fresh instances are returned.

    The dictionary contains default attributes for initializing a Session instance.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A dictionary with default Session keyword arguments.
    :rtype: SessionKWArgs
    """


@overload
def session_kwargs_factory(*, cache_id: CacheId = None) -> SessionKWArgs:
    """Return a dictionary of default Session keyword arguments for testing purposes.

    By default, this function is uncached to ensure fresh instances are returned.

    The dictionary contains default attributes for initializing a Session instance.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A dictionary with default Session keyword arguments.
    :rtype: SessionKWArgs
    """


@uncached_factory
def session_kwargs_factory(cache_id: CacheId = None) -> SessionKWArgs:
    """Return a dictionary of default Session keyword arguments for testing purposes.

    By default, this function is uncached to ensure fresh instances are returned.

    The dictionary contains default attributes for initializing a Session instance:

    Defaults:
        - cases: A list containing a single case created by `case_factory()`.
        - default_runner: A runner created by `runner_factory()`.
        - args_parser: An ArgumentParser instance with program name 'simplebench'.
        - verbosity: Verbosity.QUIET
        - progress: A rich Progress instance created by `progress_factory()`.
        - output_path: A Path instance created by `output_path_factory()`.
        - console: A Console instance created by `console_factory()`.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A dictionary with default Session keyword arguments.
    :rtype: SessionKWArgs
    """
    return SessionKWArgs(cases=tuple([case_factory(cache_id=cache_id)]),
                         default_runner=runner_factory(cache_id=cache_id),
                         args_parser=ArgumentParser(prog='simplebench'),
                         verbosity=Verbosity.QUIET,
                         show_progress=False,  # NOT the 'Progress' instance
                         output_path=output_path_factory(cache_id=cache_id),
                         console=console_factory(cache_id=cache_id))
