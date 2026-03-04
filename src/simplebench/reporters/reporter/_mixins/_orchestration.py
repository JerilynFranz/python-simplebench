"""Mixin for orchestration-related functionality for the Reporter class.

It provides methods to orchestrate the rendering of reports by case or by metric,
handling the dispatching of outputs to various targets such as filesystem, console,
or callback functions.
"""
from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING

from rich.table import Table
from rich.text import Text

from simplebench.enums import Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric
from simplebench.metrics._metrics_selection import MetricsCollection
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter import Prioritized, ReporterProtocol, _ReporterErrorTag
from simplebench.type_proxies import is_case, is_choice, is_session
from simplebench.utils import sanitize_filename
from simplebench.validators import validate_string, validate_type

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.metadata import Metadata
    from simplebench.reporters.choice import Choice
    from simplebench.session import Session



class _ReporterOrchestrationMixin:
    """Mixin for orchestration-related functionality for the Reporter class.

    It provides methods to orchestrate the rendering of reports by case or by metric,
    handling the dispatching of outputs to various targets such as filesystem, console,
    or callback functions.

    This makes writing reporters easier by providing common orchestration logic that
    can be reused across different reporter implementations.

    :ivar render_by_case: Render the report for an entire case at once across all applicable metrics.
    :vartype render_by_case: meth
    :ivar render_by_metric: Render a report for each metric and case individually and dispatch to targets.
    :vartype render_by_metric: meth
    """

    def _validate_render_by_args(
        self: ReporterProtocol,
        *,
        renderer: ReportRenderer | None,
        log_metadata: 'Metadata',
        args: Namespace,
        case: 'Case',
        choice: 'Choice',
        path: Path | None = None,
        session: 'Session | None' = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Validate common arguments for render_by_case and render_by_metric methods.

        Checks that the provided arguments are of the expected types. Raises exceptions
        if any argument is of an incorrect type.

        :param renderer: The method to be used for actually rendering the report.
        :type renderer: ReportRenderer | None
        :param log_metadata: The metadata for the report log.
        :type log_metadata: ReportLogMetadata
        :param args: The parsed command-line arguments.
        :type args: Namespace
        :param case: The Case instance representing the benchmarked code.
        :type case: Case
        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :param path: The path to the directory where the CSV file(s) will be saved.
        :type path: Path | None
        :param session: The Session instance containing benchmark results.
        :type session: Session | None
        :param callback: A callback function for additional processing of the report.
        :type callback: ReporterCallback | None
        :raises SimpleBenchTypeError: If any of the provided arguments are not of the expected types.
        """
        if renderer is not None and not callable(renderer):
            raise SimpleBenchTypeError(
                'renderer must be a callable ReportRenderer or None',
                tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_RENDERER_ARG_TYPE,
            )
        from simplebench.metadata import Metadata

        validate_type(
            log_metadata,
            Metadata,
            'log_metadata',
            _ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_LOG_METADATA_ARG_TYPE,
        )

        args = validate_type(args, Namespace, 'args', _ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_ARGS_ARG_TYPE)

        if path is not None:
            path = validate_type(path, Path, 'path', _ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_PATH_ARG_TYPE)

        # is_* checks handle deferred import runtime type checking for Case, Choice, and Session
        if not is_case(case):
            raise SimpleBenchTypeError(
                'Expected a Case instance for case argument',
                tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CASE_ARG_TYPE,
            )

        if not is_choice(choice):
            raise SimpleBenchTypeError(
                'Expected a Choice instance for choice argument',
                tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CHOICE_ARG_TYPE,
            )

        if Target.FILESYSTEM in choice.targets:
            if not isinstance(path, Path):
                raise SimpleBenchTypeError(
                    f'Path must be provided for FILESYSTEM target in {type(self)} when rendering by metric/case',
                    tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_MISSING_PATH_FOR_FILESYSTEM_TARGET,
                )
            if not isinstance(log_metadata.reports_log_path, Path):
                raise SimpleBenchTypeError(
                    f'log_metadata.reports_log_path must be provided for FILESYSTEM target in {type(self)}'
                    'when rendering by metric/case',
                    tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_MISSING_REPORTS_LOG_PATH_FOR_FILESYSTEM_TARGET,
                )

        if not is_session(session) and session is not None:
            raise SimpleBenchTypeError(
                'session must be a Session instance if provided',
                tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_SESSION_ARG_TYPE,
            )

        if callback is not None and not isinstance(callback, ReporterCallback):
            raise SimpleBenchTypeError(
                'callback must be a callable ReporterCallback if provided',
                tag=_ReporterErrorTag.VALIDATE_RENDER_BY_ARGS_INVALID_CALLBACK_ARG_TYPE,
            )

    def render_by_case(
        self: ReporterProtocol,
        *,
        renderer: ReportRenderer | None = None,
        log_metadata: 'Metadata',
        args: Namespace,
        case: 'Case',
        choice: 'Choice',
        path: Path | None = None,
        session: 'Session | None' = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Render the report for an entire case at once across all applicable metrics.

        This method is called by the subclass's run_report() method to run one report per case
        that is then processed according to the specified targets.

        It calls the subclass's render() method to actually generate the report output.

        Usage of this method is appropriate when the report output encompasses
        all metrics in a single output, such as a summary table or comprehensive report.

        Usage:

        .. code-block:: python

            from typing import TYPE_CHECKING

            from simplebench.reporters.reporter.reporter import Reporter, ReporterOptions

            if TYPE_CHECKING:
                from simplebench.case import Case
                from simplebench.reporters.choice.choice import Choice
                from simplebench.session import Session

            class MyReporter(Reporter):
                def __init__(self, ...):
                    ...

                def run_report(self, case: Case, choice: Choice, session: Session | None = None) -> None:
                    self.render_by_case(renderer=self.render,
                                        log_metadata=log_metadata,
                                        args=self._args,
                                        case=case,
                                        choice=choice,
                                        path=self._path,
                                        session=session,
                                        callback=self._callback)

                def render(self, *, case: Case, metric: Metric, options: ReporterOptions) -> str:
                    '''Render the report output for the entire case across all metrics.'''
                    ...

        :param renderer: The rendering function to use. If not provided,
            defaults to `self.render`.
        :type renderer: ReportRenderer | None
        :param timestamp: The timestamp for the report.
        :type log_metadata: ReportLogMetadata
        :param args: The parsed command-line arguments.
        :type args: Namespace
        :param case: The Case instance representing the benchmarked code.
        :type case: Case
        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :param path: The path to the directory where the CSV file(s) will be saved.
        :type path: Path | None
        :param session: The Session instance containing benchmark results.
        :type session: Session | None
        :param callback:
            A callback function for additional processing of the report.
            The function should accept two arguments: the Case instance and the CSV data as a string.
            Leave as None if no callback is needed.
        :type callback: ReporterCallback | None
        :raises SimpleBenchTypeError: If the provided arguments are not of the expected types or if
            required arguments are missing. Also raised if the callback is not callable when
            provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
            target is specified.
        :raises SimpleBenchValueError: If an unsupported metric or target is specified in the choice.
        """
        log_metadata.case = case
        log_metadata.choice = choice
        actual_renderer = renderer if renderer is not None else self.render
        self._validate_render_by_args(
            renderer=actual_renderer,
            log_metadata=log_metadata,
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback,
        )

        prioritized = Prioritized(reporter=self, choice=choice, case=case)
        self.dispatch_to_targets(
            output=actual_renderer(case=case, metric=None, options=prioritized.options),
            filename_base=case.title,
            log_metadata=log_metadata,
            args=args,
            choice=choice,
            case=case,
            metric=None,
            path=path,
            session=session,
            callback=callback,
        )

    def render_by_metric(
        self: ReporterProtocol,
        *,
        renderer: ReportRenderer | None = None,
        log_metadata: 'Metadata',
        args: Namespace,
        case: 'Case',
        choice: 'Choice',
        path: Path | None = None,
        session: 'Session | None' = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Render a report for each metric and dispatch to targets.

        This method is called by the subclass's run_report() method to run one report per metric
        that is then processed according to the specified targets.

        It calls the subclass's render() method to actually generate the report output.

        Usage of this method is appropriate when the report output divides each case by
        metric, such as separate files or outputs for each metric of the report.

        Usage:

        .. code-block:: python

            from simplebench.reporters.reporter.reporter import Reporter, ReporterOptions

            if TYPE_CHECKING:
                from simplebench.case import Case
                from simplebench.reporters.choice.choice import Choice
                from simplebench.session import Session


            class MyReporter(Reporter):
                def __init__(self, ...):
                    ...

                def run_report(self, case: Case, choice: Choice, session: Session | None = None) -> None:
                    self.render_by_metric(
                                        renderer=self.render,
                                        args=self._args,
                                        case=case,
                                        choice=choice,
                                        path=self._path,
                                        session=session,
                                        callback=self._callback)

                def render(self, *, case: Case, metric: Metric, options: ReporterOptions) -> str:
                    '''Render the report output for the entire case across all metrics.'''
                    ...

        :param renderer: The rendering function to use. If not provided,
            defaults to `self.render`.
        :type renderer: ReportRenderer | None
        :param log_metadata: The metadata for logging the report.
        :type log_metadata: ReportLogMetadata
        :param args: The parsed command-line arguments.
        :type args: Namespace
        :param case: The Case instance representing the benchmarked code.
        :type case: Case
        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :param path: The path to the directory where the CSV file(s) will be saved.
        :type path: Path | None
        :param session: The Session instance containing benchmark results.
        :type session: Session | None
        :param callback:
            A callback function for additional processing of the report.
            The function should accept two arguments: the Case instance and the CSV data as a string.
            Leave as None if no callback is needed.
        :type callback: ReporterCallback | None
        :raises SimpleBenchTypeError: If the provided arguments are not of the expected types or if
            required arguments are missing. Also raised if the callback is not callable when
            provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
            target is specified.
        :raises SimpleBenchValueError: If an unsupported metric or target is specified in the choice.
        """
        actual_renderer = renderer if renderer is not None else self.render
        self._validate_render_by_args(
            renderer=actual_renderer,
            log_metadata=log_metadata,
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback,
        )
        metrics = choice.metrics
        if not isinstance(metrics, MetricsCollection):
            raise SimpleBenchTypeError(
                'choice.metrics must be a MetricsCollection instance for render_by_metric',
                tag=_ReporterErrorTag.RENDER_BY_METRIC_NOT_A_METRICS_COLLECTION)
        prioritized = Prioritized(reporter=self, choice=choice, case=case)
        log_metadata.case = case
        log_metadata.choice = choice
        for metric in metrics:
            output = actual_renderer(case=case, metric=metric, options=prioritized.options)
            metric_value = getattr(metric, 'value', str(metric))
            self.dispatch_to_targets(
                output=output,
                log_metadata=log_metadata,
                filename_base=f'{case.title}-{metric_value}',
                args=args,
                choice=choice,
                case=case,
                metric=metric,
                path=path,
                session=session,
                callback=callback,
            )

    def dispatch_to_targets(  # pylint: disable=too-many-arguments,too-many-locals
        self: ReporterProtocol,
        *,
        output: str | bytes | Text | Table,
        log_metadata: 'Metadata',
        filename_base: str,
        args: Namespace,
        choice: 'Choice',
        case: 'Case',
        metric: Metric | None,
        path: Path | None = None,
        session: 'Session | None' = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Deliver the rendered output to the specified targets.

        This helper method takes the rendered output and dispatches it to the
        appropriate targets based on the prioritized options.

        This method handles the logic for delivering the report output to the possible targets:
        - FILESYSTEM: Writes the output to a file in the specified path and subdirectory.
        - CALLBACK: Sends the output to a provided callback function for further processing.
        - CONSOLE: Outputs the report directly to the console.

        :param output: The rendered report output.
        :param log_metadata: The metadata for logging the report.
        :param filename_base: The base filename to use for filesystem outputs.
            This is the filename without any suffixes or extensions.
        :param args: The parsed command-line arguments.
        :param choice: The Choice instance specifying the report configuration.
        :param case: The Case instance representing the benchmarked code.
        :param metric: The Metric of the report.
        :param path: The path to the directory where the CSV file(s) will be saved.
        :param session: The Session instance containing benchmark results.
        :param callback: A callback function for additional processing of the report.
        :raises SimpleBenchValueError: If an unsupported target is specified in the choice.
        """
        from simplebench.metadata import Metadata

        output = validate_type(
            output, (str, bytes, Text, Table), 'output', _ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_OUTPUT_ARG_TYPE
        )
        log_metadata = validate_type(
            log_metadata, Metadata, 'log_metadata', _ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_LOG_METADATA_ARG_TYPE
        )
        filename_base = validate_string(
            filename_base,
            'filename_base',
            _ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_FILENAME_BASE_ARG_TYPE,
            _ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_FILENAME_BASE_ARG_VALUE,
            allow_empty=False,
            strip=True,
            alphanumeric_only=False,
            allow_blank=False,
        )
        args = validate_type(args, Namespace, 'args', _ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_ARGS_ARG_TYPE)
        if not is_case(case):
            raise SimpleBenchTypeError(
                'Expected a Case instance for case argument',
                tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_CASE_ARG_TYPE,
            )
        log_metadata.case = case
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                'Expected a Choice instance for choice argument',
                tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_CHOICE_ARG_TYPE,
            )
        log_metadata.choice = choice
        if not is_session(session) and session is not None:
            raise SimpleBenchTypeError(
                'session must be a Session instance if provided',
                tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_SESSION_ARG_TYPE,
            )

        if metric is not None and not isinstance(metric, Metric):
            raise SimpleBenchTypeError(
                f'metric must be a Metric instance or None for dispatch_to_targets: found type {type(metric)}',
                tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_METIC_ARG_TYPE)

        if callback is not None and not isinstance(callback, ReporterCallback):
            raise SimpleBenchTypeError(
                'callback must be a callable ReporterCallback if provided',
                tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_CALLBACK_ARG_TYPE,
            )
        if path is not None:
            path = validate_type(path, Path, 'path', _ReporterErrorTag.DISPATCH_TO_TARGETS_INVALID_PATH_ARG_TYPE)

        prioritized = Prioritized(reporter=self, choice=choice, case=case)
        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=prioritized.default_targets
        )

        if Target.FILESYSTEM in targets:
            if not isinstance(path, Path):
                raise SimpleBenchTypeError(
                    f'Path must be a Path instance for FILESYSTEM target in {type(self)}, got {type(path)}',
                    tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_PATH_TYPE,
                )
            if not isinstance(log_metadata.reports_log_path, Path):
                raise SimpleBenchTypeError(
                    f'log_metadata.reports_log_path must be a Path instance for FILESYSTEM target in {type(self)}, '
                    f'got {type(log_metadata.reports_log_path)}',
                    tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_LOG_METADATA_REPORTS_LOG_PATH_TYPE,
                )

        output_as_text = output
        if isinstance(output, (Text, Table)):
            output_as_text = self.rich_text_to_plain_text(output)
        filename: str = sanitize_filename(filename_base)
        if prioritized.file_suffix:
            filename += f'.{prioritized.file_suffix}'

        for output_target in targets:
            match output_target:
                case Target.FILESYSTEM:
                    self.target_filesystem(
                        log_metadata=log_metadata,
                        path=path,
                        subdir=prioritized.subdir,
                        filename=filename,
                        output=output_as_text,
                        unique=prioritized.file_unique,
                        append=prioritized.file_append,
                    )

                case Target.CALLBACK:
                    self.target_callback(
                        callback=callback,
                        case=case,
                        metric=metric,
                        output_format=choice.output_format,
                        output=output_as_text,
                    )

                case Target.CONSOLE:
                    self.target_console(session=session, output=output)

                case _:
                    raise SimpleBenchValueError(
                        f'Unsupported target for {type(self)}: {output_target}',
                        tag=_ReporterErrorTag.DISPATCH_TO_TARGETS_UNSUPPORTED_TARGET,
                    )
