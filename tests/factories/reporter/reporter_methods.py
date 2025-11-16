""""Factories for reporter method mocks used in tests.

It provides factory functions and mock classes to simulate and record
interactions with reporter methods such as rendering reports, writing to
the filesystem, outputting to the console, and invoking callbacks.
This is useful for testing the behavior of reporter classes without
performing actual I/O operations.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias, overload

from rich.table import Table
from rich.text import Text

from simplebench.reporters.protocols import ReporterCallback, ReportRenderer

from ...cache_factory import CacheId, cached_factory
from ...kwargs.reporters.reporter import RenderByCaseMethodKWArgs, RenderBySectionMethodKWArgs
from .. import case_factory, choice_factory, default_reporter_callback, namespace_factory, path_factory, session_factory

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.enums import Format, Section
    from simplebench.reporters.reporter.options import ReporterOptions
    from simplebench.session import Session

Output: TypeAlias = str | bytes | Text | Table


@overload
def render_by_case_kwargs_factory(
        *,
        kwargs: RenderByCaseMethodKWArgs | None = None) -> RenderByCaseMethodKWArgs:
    """Factory to create RenderByCaseMethodKWArgs with default values.

    This factory constructs a RenderByCaseMethodKWArgs instance populated with
    default values for testing the Reporter.render_by_case() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

     Defaults:
        renderer (ReportRenderer):
            `RenderRecorder()`
        args (Namespace):
            `namespace_factory(cache_id=cache_id)`
        case (Case):
            `case_factory(cache_id=cache_id)`
        choice (Choice):
            `choice_factory(cache_id=cache_id)`
        path (Path):
            `path_factory(cache_id=cache_id)`
        session (Session):
            `session_factory(cache_id=cache_id)`
        callback (ReporterCallback):
            `default_reporter_callback`

    Args:
        kwargs (RenderByCaseMethodKWArgs | None, default=None): Specific keyword arguments to override defaults.
        cache_id (CacheId, default=CACHE_DEFAULT): The cache identifier.

    Returns:
        RenderByCaseMethodKWArgs: The constructed keyword arguments dataclass.
    """


@overload
def render_by_case_kwargs_factory(
        *,
        kwargs: RenderByCaseMethodKWArgs | None = None,
        cache_id: CacheId = None) -> RenderByCaseMethodKWArgs:
    """Factory to create RenderByCaseMethodKWArgs with default values.

    This factory constructs a RenderByCaseMethodKWArgs instance populated with
    default values for testing the Reporter.render_by_case() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

     Defaults:
        renderer (ReportRenderer):
            `RenderRecorder()`
        args (Namespace):
            `namespace_factory(cache_id=cache_id)`
        case (Case):
            `case_factory(cache_id=cache_id)`
        choice (Choice):
            `choice_factory(cache_id=cache_id)`
        path (Path):
            `path_factory(cache_id=cache_id)`
        session (Session):
            `session_factory(cache_id=cache_id)`
        callback (ReporterCallback):
            `default_reporter_callback`

    Args:
        kwargs (RenderByCaseMethodKWArgs | None, default=None): Specific keyword arguments to override defaults.
        cache_id (CacheId, default=CACHE_DEFAULT): The cache identifier.

    Returns:
        RenderByCaseMethodKWArgs: The constructed keyword arguments dataclass.
    """


@cached_factory
def render_by_case_kwargs_factory(
    *,
    kwargs: RenderByCaseMethodKWArgs | None = None,
    cache_id: CacheId = None,
) -> RenderByCaseMethodKWArgs:
    """Factory to create RenderByCaseMethodKWArgs with default values.

    This factory constructs a RenderByCaseMethodKWArgs instance populated with
    default values for testing the Reporter.render_by_case() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        renderer (ReportRenderer):
            `RenderRecorder()`
        args (Namespace):
            `namespace_factory(cache_id=cache_id)`
        case (Case):
            `case_factory(cache_id=cache_id)`
        choice (Choice):
            `choice_factory(cache_id=cache_id)`
        path (Path):
            `path_factory(cache_id=cache_id)`
        session (Session):
            `session_factory(cache_id=cache_id)`
        callback (ReporterCallback):
            `default_reporter_callback`

    Args:
        kwargs (RenderByCaseMethodKWArgs | None, default=None): Specific keyword arguments to override defaults.
        cache_id (CacheId, default=CACHE_DEFAULT): The cache identifier.

    Returns:
        RenderByCaseMethodKWArgs: The constructed keyword arguments dataclass.
    """
    defaults = RenderByCaseMethodKWArgs(
        renderer=RenderSpy(),
        args=namespace_factory(),
        case=case_factory(cache_id=cache_id),
        choice=choice_factory(cache_id=cache_id),
        path=path_factory(cache_id=cache_id),
        session=session_factory(cache_id=cache_id),
        callback=default_reporter_callback,
    )
    return defaults if kwargs is None else RenderByCaseMethodKWArgs(**(defaults | kwargs))


@cached_factory
def render_by_section_kwargs_factory(
    *,
    kwargs: RenderBySectionMethodKWArgs | None = None,
    cache_id: CacheId = None,
) -> RenderBySectionMethodKWArgs:
    """Factory to create RenderBySectionMethodKWArgs with default values.

    This factory constructs a RenderBySectionMethodKWArgs instance populated with
    default values for testing the Reporter.render_by_section() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        renderer (ReportRenderer): `RenderSpy()`
        args (Namespace): `namespace_factory()`
        case (Case): `case_factory(cache_id=cache_id)`
        choice (Choice): `choice_factory(cache_id=cache_id)`
        path (Path): `path_factory(cache_id=cache_id)`
        session (Session): `session_factory(cache_id=cache_id)`
        callback (ReporterCallback): `default_reporter_callback`

    Args:
        kwargs (RenderBySectionMethodKWArgs | None, default=None): Specific keyword arguments to override defaults.
        cache_id (CacheId, default=None): The cache identifier.

    Returns:
        RenderBySectionMethodKWArgs: The constructed keyword arguments dataclass.
    """
    defaults = RenderBySectionMethodKWArgs(
        renderer=RenderSpy(),
        args=namespace_factory(),
        case=case_factory(cache_id=cache_id),
        choice=choice_factory(cache_id=cache_id),
        path=path_factory(cache_id=cache_id),
        session=session_factory(cache_id=cache_id),
        callback=default_reporter_callback,
    )
    return defaults if kwargs is None else RenderBySectionMethodKWArgs(**(defaults | kwargs))


@dataclass
class FileSystemCall:
    """Data class to store a filesystem target call.

    Attributes:
        path (Path): The path to the directory where the file will be saved.
        subdir (str): The subdirectory within the path.
        filename (str): The name of the file to be saved.
        output (Output): The content to be written to the file.
        unique (bool): Whether to ensure a unique filename.
        append (bool): Whether to append to the file if it exists.
    """
    path: Path
    subdir: str
    filename: str
    output: Output
    unique: bool
    append: bool


class FileSystemSpy:
    """Helper mock class to record calls to the filesystem target method.

    This class records each call made to the filesystem target method,
    storing the parameters in a list for later inspection.

    Attributes:
        calls (list[FileSystemCall]): List of recorded filesystem calls.
    """

    def __init__(self) -> None:
        self.calls: list[FileSystemCall] = []

    def __call__(self, *,
                 path: Path,
                 subdir: str,
                 filename: str,
                 output: Output,
                 unique: bool,
                 append: bool,) -> None:
        self.calls.append(
            FileSystemCall(
                path=path,
                subdir=subdir,
                filename=filename,
                output=output,
                unique=unique,
                append=append,
            ))

    @property
    def count(self) -> int:
        """Get the number of recorded filesystem calls.

        Returns:
            int: The count of recorded calls.
        """
        return len(self.calls)


@dataclass
class ConsoleCall:
    """Data class to store a console target call.

    Attributes:
        session (Session | None): The session instance, if any.
        output (Output): The content to be output to the console.
    """
    session: Session | None
    output: Output


class ConsoleSpy:
    """Helper mock class to record calls to a reporter console target method.

    This class records each call made to the console target method,
    storing the parameters in a list for later inspection.

    Attributes:
        calls (list[ConsoleCall]): List of recorded console calls.
    """

    def __init__(self) -> None:
        self.calls: list[ConsoleCall] = []

    def __call__(self, *,
                 session: Session | None,
                 output: Output) -> None:
        self.calls.append(
            ConsoleCall(
                session=session,
                output=output,
            ))

    @property
    def count(self) -> int:
        """Get the number of recorded console calls.

        Returns:
            int: The count of recorded calls.
        """
        return len(self.calls)


@dataclass
class CallbackCall:
    """Data class to store a callback target call.

    Attributes:
        callback (ReporterCallback): The callback function.
        case (Case): The Case instance.
        section (Section): The Section of the report.
        output_format (Format): The Format of the report.
        output (Any): The report data sent to the callback.
    """
    callback: ReporterCallback
    case: Case
    section: Section
    output_format: Format
    output: Any


class CallbackSpy():
    """Helper mock class to record calls to a reporter callback.

    This class records each call made to the callback target method,
    storing the parameters in a list for later inspection.

    Attributes:
        calls (list[CallbackCall]): List of recorded callback calls.
    """
    def __init__(self) -> None:
        self.calls: list[CallbackCall] = []

    # typed as a method to match the ReporterCallback signature
    def __call__(self, *,
                 callback: ReporterCallback,
                 case: Case,
                 section: Section,
                 output_format: Format,
                 output: Any) -> None:
        self.calls.append(
            CallbackCall(
                callback=callback,
                case=case,
                section=section,
                output_format=output_format,
                output=output,
            ))

    @property
    def count(self) -> int:
        """Get the number of recorded callback calls.

        Returns:
            int: The count of recorded calls.
        """
        return len(self.calls)


@dataclass
class RenderCall:
    """Data class to store a render method call.

    Attributes:
        case (Case): The Case instance.
        section (Section): The Section of the report.
        options (ReporterOptions): The ReporterOptions used for rendering.
    """
    case: Case
    section: Section
    options: ReporterOptions


class RenderSpy(ReportRenderer):
    """Helper mock class to record calls to a reporter render method.

    This class records each call made to the render method,
    storing the parameters in a list for later inspection.
    """
    def __init__(self) -> None:
        self.calls: list[RenderCall] = []

    def __call__(self, *,
                 case: Case,
                 section: Section,
                 options: ReporterOptions) -> Output:
        self.calls.append(
            RenderCall(
                case=case,
                section=section,
                options=options,
            ))
        return Text(f"Rendered report for case {case} in section {section}")

    @property
    def count(self) -> int:
        """Get the number of recorded render calls.

        Returns:
            int: The count of recorded calls.
        """
        return len(self.calls)
