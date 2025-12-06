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

from simplebench.enums import Format, Section
from simplebench.reporters.log.base.report_log_entry import ReportLogEntry
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer

from ...cache_factory import CacheId, cached_factory
from ...kwargs.reporters.reporter import (
    DispatchToTargetsMethodKWArgs,
    RenderByCaseMethodKWArgs,
    RenderBySectionMethodKWArgs,
    TargetCallbackMethodKWArgs,
    TargetConsoleMethodKWArgs,
    TargetFilesystemMethodKWArgs,
)
from .. import (
    case_factory,
    choice_factory,
    default_filename_base,
    default_format_plain,
    default_output,
    default_output_str,
    default_reporter_callback,
    default_section,
    default_subdir,
    namespace_factory,
    path_factory,
    report_log_metadata_factory,
    session_factory,
)

if TYPE_CHECKING:
    from simplebench.case import Case
    # from simplebench.reporters.choice.choice import Choice
    from simplebench.reporters.reporter.options import ReporterOptions
    from simplebench.session import Session

Output: TypeAlias = str | bytes | Text | Table


def target_callback_kwargs_factory(
        *,
        kwargs: dict[str, Any] | None = None,
        cache_id: CacheId = None) -> TargetCallbackMethodKWArgs:
    """Factory to create keyword arguments for the callback target method.

    This factory constructs a dictionary of keyword arguments populated with
    default values for testing the Reporter.target_callback() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        - callback (ReporterCallback): `default_reporter_callback()`
        - case (Case): `case_factory(cache_id=cache_id)`
        - section (Section): `default_section()`
        - output_format (Format): `default_format_plain()`
        - output (Output): `default_output_str()`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: dict[str, Any] | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments.
    :rtype: TargetCallbackMethodKWArgs
    """
    defaults = TargetCallbackMethodKWArgs(
        callback=default_reporter_callback,
        case=case_factory(cache_id=cache_id),
        section=default_section(),
        output_format=default_format_plain(),
        output=default_output_str(),
    )
    return defaults if kwargs is None else TargetCallbackMethodKWArgs(**(defaults | kwargs))


def target_console_kwargs_factory(
        *,
        kwargs: dict[str, Any] | None = None,
        cache_id: CacheId = None) -> TargetConsoleMethodKWArgs:
    """Factory to create keyword arguments for the console target method.

    This factory constructs a dictionary of keyword arguments populated with
    default values for testing the Reporter.target_console() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        - session (Session): `session_factory(cache_id=cache_id)`
        - output (Output): `default_output()`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: dict[str, Any] | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments.
    :rtype: TargetConsoleMethodKWArgs
    """
    defaults = TargetConsoleMethodKWArgs(
        session=session_factory(cache_id=cache_id),
        output=default_output(),
    )
    return defaults if kwargs is None else TargetConsoleMethodKWArgs(**(defaults | kwargs))


def target_filesystem_kwargs_factory(
        *,
        kwargs: dict[str, Any] | None = None,
        cache_id: CacheId = None) -> TargetFilesystemMethodKWArgs:
    """Factory to create keyword arguments for the filesystem target method.

    This factory constructs a dictionary of keyword arguments populated with
    default values for testing the Reporter.target_filesystem() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        - log_metadata (ReportLogMetadata): `report_log_metadata_factory()`
        - path (Path): `path_factory(cache_id=cache_id)`
        - subdir (str): `default_subdir()`
        - filename (str): `default_filename_base()`
        - output (Output): `default_output()`
        - unique (bool): `True`
        - append (bool): `False`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: dict[str, Any] | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments.
    :rtype: TargetFilesystemMethodKWArgs
    """
    defaults = TargetFilesystemMethodKWArgs(
        log_metadata=report_log_metadata_factory(),
        path=path_factory(cache_id=cache_id),
        subdir=default_subdir(),
        filename=default_filename_base(),
        output=default_output(),
        unique=True,
        append=False,
    )
    return defaults if kwargs is None else TargetFilesystemMethodKWArgs(**(defaults | kwargs))


def dispatch_to_targets_kwargs_factory(
    *,
    kwargs: DispatchToTargetsMethodKWArgs | None = None,
    cache_id: CacheId = None,
) -> DispatchToTargetsMethodKWArgs:
    """Factory to create DispatchToTargetsMethodKWArgs with default values.

    This factory constructs a DispatchToTargetsMethodKWArgs instance populated with
    default values for testing the Reporter.dispatch_to_targets() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        - args (Namespace): `namespace_factory(cache_id=cache_id)`
        - reports_log_path (Path): `path_factory(cache_id=cache_id)`
        - timestamp (Timestamp): `default_timestamp()`
        - case (Case): `case_factory(cache_id=cache_id)`
        - choice (Choice): `choice_factory(cache_id=cache_id)`
        - path (Path): `path_factory(cache_id=cache_id)`
        - session (Session): `session_factory(cache_id=cache_id)`
        - section (Section): `default_section()`
        - callback (ReporterCallback): `default_reporter_callback()`
        - output (Output): `default_output()`
        - filename_base (str): `default_filename_base()`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: DispatchToTargetsMethodKWArgs | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments dataclass.
    :rtype: DispatchToTargetsMethodKWArgs
    """
    defaults = DispatchToTargetsMethodKWArgs(
        args=namespace_factory(),
        case=case_factory(cache_id=cache_id),
        choice=choice_factory(cache_id=cache_id),
        path=path_factory(cache_id=cache_id),
        log_metadata=report_log_metadata_factory(),
        session=session_factory(cache_id=cache_id),
        section=default_section(),
        callback=default_reporter_callback,
        output=default_output(),
        filename_base=default_filename_base(),
    )
    return defaults if kwargs is None else DispatchToTargetsMethodKWArgs(**(defaults | kwargs))


@overload
def render_by_case_kwargs_factory(
        *,
        kwargs: RenderByCaseMethodKWArgs | None = None) -> RenderByCaseMethodKWArgs:
    """Factory to create RenderByCaseMethodKWArgs with default values.

    This factory constructs a RenderByCaseMethodKWArgs instance populated with
    default values for testing the Reporter.render_by_case() method.

    Defaults can be overridden by providing specific arguments in the kwargs parameter.

    Defaults:
        - renderer (ReportRenderer): `RenderRecorder()`
        - args (Namespace): `namespace_factory(cache_id=cache_id)`
        - case (Case): `case_factory(cache_id=cache_id)`
        - choice (Choice): `choice_factory(cache_id=cache_id)`
        - path (Path): `path_factory(cache_id=cache_id)`
        - session (Session): `session_factory(cache_id=cache_id)`
        - callback (ReporterCallback): `default_reporter_callback`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: RenderByCaseMethodKWArgs | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments dataclass.
    :rtype: RenderByCaseMethodKWArgs
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
        - renderer (ReportRenderer): `RenderRecorder()`
        - args (Namespace): `namespace_factory(cache_id=cache_id)`
        - case (Case): `case_factory(cache_id=cache_id)`
        - choice (Choice): `choice_factory(cache_id=cache_id)`
        - path (Path): `path_factory(cache_id=cache_id)`
        - session (Session): `session_factory(cache_id=cache_id)`
        - callback (ReporterCallback): `default_reporter_callback`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: RenderByCaseMethodKWArgs | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments dataclass.
    :rtype: RenderByCaseMethodKWArgs
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
        - renderer (ReportRenderer): `RenderRecorder()`
        - timestamp (Timestamp): `default_timestamp()`
        - args (Namespace): `namespace_factory(cache_id=cache_id)`
        - case (Case): `case_factory(cache_id=cache_id)`
        - choice (Choice): `choice_factory(cache_id=cache_id)`
        - path (Path): `path_factory(cache_id=cache_id)`
        - session (Session): `session_factory(cache_id=cache_id)`
        - callback (ReporterCallback): `default_reporter_callback`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: RenderByCaseMethodKWArgs | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments dataclass.
    :rtype: RenderByCaseMethodKWArgs
    """
    defaults = RenderByCaseMethodKWArgs(
        renderer=RenderSpy(),
        log_metadata=report_log_metadata_factory(),
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
        - renderer (ReportRenderer): `RenderSpy()`
        - log_metadata (ReportLogMetadata): `report_log_metadata_factory()`
        - args (Namespace): `namespace_factory()`
        - case (Case): `case_factory(cache_id=cache_id)`
        - choice (Choice): `choice_factory(cache_id=cache_id)`
        - path (Path): `path_factory(cache_id=cache_id)`
        - reports_log_path (Path): `reports_log_path_factory(cache_id=cache_id)`
        - session (Session): `session_factory(cache_id=cache_id)`
        - callback (ReporterCallback): `default_reporter_callback`

    :param kwargs: Specific keyword arguments to override defaults.
    :type kwargs: RenderBySectionMethodKWArgs | None
    :param cache_id: The cache identifier.
    :type cache_id: CacheId, optional
    :return: The constructed keyword arguments dataclass.
    :rtype: RenderBySectionMethodKWArgs
    """
    defaults = RenderBySectionMethodKWArgs(
        renderer=RenderSpy(),
        log_metadata=report_log_metadata_factory(),
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

    :ivar log_metadata: The report log metadata.
    :vartype log_metadata: ReportLogMetadata
    :ivar path: The path to the directory where the file will be saved.
    :vartype path: Path
    :ivar subdir: The subdirectory within the path.
    :vartype subdir: str
    :ivar filename: The name of the file to be saved.
    :vartype filename: str
    :ivar output: The content to be written to the file.
    :vartype output: Output
    :ivar unique: Whether to ensure a unique filename.
    :vartype unique: bool
    :ivar append: Whether to append to the file if it exists.
    :vartype append: bool
    """
    log_metadata: ReportLogEntry
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

    :ivar calls: List of recorded filesystem calls.
    :vartype calls: list[FileSystemCall]
    """

    def __init__(self) -> None:
        self.calls: list[FileSystemCall] = []

    def __call__(self, *,
                 path: Path,
                 log_metadata: ReportLogEntry,
                 subdir: str,
                 filename: str,
                 output: Output,
                 unique: bool,
                 append: bool,) -> None:
        self.calls.append(
            FileSystemCall(
                path=path,
                log_metadata=log_metadata,
                subdir=subdir,
                filename=filename,
                output=output,
                unique=unique,
                append=append,
            ))

    @property
    def count(self) -> int:
        """Get the number of recorded filesystem calls.

        :return: The count of recorded calls.
        :rtype: int
        """
        return len(self.calls)


@dataclass
class ConsoleCall:
    """Data class to store a console target call.

    :ivar session: The session instance, if any.
    :vartype session: Session | None
    :ivar output: The content to be output to the console.
    :vartype output: Output
    """
    session: Session | None
    output: Output


class ConsoleSpy:
    """Helper mock class to record calls to a reporter console target method.

    This class records each call made to the console target method,
    storing the parameters in a list for later inspection.

    :ivar calls: List of recorded console calls.
    :vartype calls: list[ConsoleCall]
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

        :return: The count of recorded calls.
        :rtype: int
        """
        return len(self.calls)


@dataclass
class CallbackCall:
    """Data class to store a callback target call.

    :ivar callback: The callback function.
    :vartype callback: ReporterCallback
    :ivar case: The Case instance.
    :vartype case: Case
    :ivar section: The Section of the report.
    :vartype section: Section
    :ivar output_format: The Format of the report.
    :vartype output_format: Format
    :ivar output: The report data sent to the callback.
    :vartype output: Any
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

    :ivar calls: List of recorded callback calls.
    :vartype calls: list[CallbackCall]
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

        :return: The count of recorded calls.
        :rtype: int
        """
        return len(self.calls)


@dataclass
class RenderCall:
    """Data class to store a render method call.

    :ivar case: The Case instance.
    :vartype case: Case
    :ivar section: The Section of the report.
    :vartype section: Section
    :ivar options: The ReporterOptions used for rendering.
    :vartype options: ReporterOptions
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

        :return: The count of recorded calls.
        :rtype: int
        """
        return len(self.calls)
