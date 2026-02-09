"""Reporter base class.

This module defines the Reporter abstract base class, which serves as the foundation
for all reporter implementations in the SimpleBench benchmarking framework.

It handles common functionality such as validating input arguments, configuring argparse CLI arguments,
managing default options, sending reports to various targets, and orchestrating report generation.

To create a new reporter, a developer must subclass `Reporter` and implement the abstract
`render()` method. For most reporters, the default `run_report()` implementation, which
renders a report for each metric, is sufficient.

A `Reporter` is responsible for generating reports based on benchmark results from a `Session` and `Case`.
Reporters can produce reports in various formats and output them to different targets.
"""
# ruff: noqa: B009,B010

from abc import ABC, abstractmethod
from argparse import Namespace
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias, TypeVar

from rich.table import Table
from rich.text import Text

from simplebench.case.results import Results
from simplebench.enums import Format, Target
from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchTypeError
from simplebench.metrics import Metric, MetricsSelection
from simplebench.options.reporter.options import ReporterOptions
from simplebench.reporters.choices.choices import Choices
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter._config import ReporterConfig
from simplebench.reporters.reporter._error_tags import _ReporterErrorTag
from simplebench.reporters.reporter._mixins import (
    _ReporterArgparseMixin,
    _ReporterOrchestrationMixin,
    _ReporterPrioritizationMixin,
    _ReporterTargetMixin,
)
from simplebench.reporters.reporter.protocols import ReporterProtocol

from . import _validate

Options: TypeAlias = ReporterOptions

T = TypeVar('T')


if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.metadata import Metadata
    from simplebench.reporters.choice.choice import Choice
    from simplebench.session import Session
    from simplebench.simplebench_types import ElementCollection

__all__: list[str] = []


class Reporter(
    ABC,
    _ReporterArgparseMixin,
    _ReporterOrchestrationMixin,
    _ReporterPrioritizationMixin,
    _ReporterTargetMixin,
    ReporterProtocol,
):
    """Base class for Reporter classes.

    A :class:`~.Reporter` is responsible for generating reports based on benchmark results
    from a :class:`~simplebench.session.Session` and :class:`~simplebench.case.Case`.
    Reporters can produce reports in various formats and output them to different targets.

    All :class:`~.Reporter` subclasses must implement the methods defined in this interface.
    Reporters should handle their own output, whether to console, file system,
    HTTP endpoint, display device, via a callback or other output.

    The :class:`~.Reporter` interface ensures that all reporters provide a consistent
    set of functionalities, making it easier to manage and utilize different

    reporting options within the SimpleBench framework.
    """
    @classmethod
    def get_hardcoded_default_options(cls) -> Any:
        """Get the built-in hardcoded default options for the reporter.

        This abstract method must be implemented by all :class:`~.Reporter` subclasses.
        It defines the base class default options for a reporter and must
        be available in all :class:`~.Reporter` subclasses.

        It returns the hardcoded default :class:`~.ReporterOptions` sub-class instance
        specific to the reporter.

        Sub-classes must implement the following class variables:

            _OPTIONS_TYPE: ClassVar[type[MyOptions]] = MyOptions
            _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {...}

        or the method will raise an exception.

        :return: The built-in hardcoded default :class:`~.ReporterOptions` instance.
        :raises SimpleBenchNotImplementedError: If required class variables are not implemented
            or are of incorrect types.
        """
        _validate.subclass_config(cls)
        if '_HARDCODED_DEFAULT_OPTIONS' not in cls.__dict__:
            options_type: type[ReporterOptions] = getattr(cls, '_OPTIONS_TYPE')
            options_kwargs: dict[str, Any] = getattr(cls, '_OPTIONS_KWARGS')
            setattr(cls, '_HARDCODED_DEFAULT_OPTIONS', options_type(**options_kwargs))
        return getattr(cls, '_HARDCODED_DEFAULT_OPTIONS')

    @classmethod
    def set_default_options(cls, options: Options | None = None) -> None:
        """Set the default options for the reporter.

        :param options: The options to set as the default, defaults to None
        :type options: :class:`~.ReporterOptions` or None, optional
        """
        _validate.subclass_config(cls)
        options_type = getattr(cls, '_OPTIONS_TYPE')
        if options.__class__ is ReporterOptions:
            raise SimpleBenchTypeError(
                'Invalid type for options argument in set_default_options(). '
                'Expected ReporterOptions subclass instance or None and got ReporterOptions base class instance.',
                tag=_ReporterErrorTag.SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE_BASE_CLASS_INSTANCE,
            )
        if not isinstance(options, options_type) and options is not None:
            raise SimpleBenchTypeError(
                'Invalid type for options argument in set_default_options(). '
                f'Expected {options_type} or None and got {type(options)}.',
                tag=_ReporterErrorTag.SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE,
            )
        setattr(cls, '_DEFAULT_OPTIONS', options)

    @classmethod
    def get_default_options(cls) -> Options:
        """Get the default options for the reporter.

        Returns the default options set via :meth:`~.set_default_options` if set,
        otherwise returns the built-in hardcoded default options from
        :meth:`~.get_hardcoded_default_options`.

        :return: The default options.
        :rtype: :class:`~.ReporterOptions`
        """
        _validate.subclass_config(cls)
        if '_DEFAULT_OPTIONS' in cls.__dict__:
            user_default = getattr(cls, '_DEFAULT_OPTIONS')
            if user_default is not None:
                return user_default
        return cls.get_hardcoded_default_options()

    def __init__(self, config: ReporterConfig) -> None:
        """Initialize the Reporter instance.

        :param config: The configuration object for the reporter.
        :type config: ReporterConfig
        :raises SimpleBenchTypeError: If the provided config is not a ReporterConfig instance.
        """
        from simplebench.reporters.choice import Choice
        _validate.subclass_config(self.__class__)
        self._config: ReporterConfig = _validate.config(config, 'config')

        choices_list: list[Choice] = []
        for item in self.config.choices.values():
            choices_list.append(Choice(reporter=self, choice_conf=item))

        self._choices = Choices(choices_list)
        """An instance of `Choices` containing the `Choice` instances for the `Reporter`.

        This is constructed from an iterable of `Choice` instances (private backing field)"""

    @staticmethod
    def find_options_by_type(
            options: 'ElementCollection[ReporterOptions] | None',
            cls: type[T]) -> T | None:
        """Retrieve the first instance of type ``cls`` (if present) from a collection of :class:`~.ReporterOptions`.

        This is used to extract reporter specific options from an iterable container of generic
        :class:`~.ReporterOptions` such as those associated with a
        :class:`~simplebench.reporters.choice.choice.Choice` or :class:`~simplebench.case.Case`.

        For example, a :class:`~simplebench.reporters.csv.CSVReporter` may define
        a :class:`~simplebench.reporters.csv.CSVReporterOptions` class
        that extends :class:`~.ReporterOptions` and use this method to extract
        a :class:`~simplebench.reporters.csv.CSVReporterOptions` instance
        from the options :class:`~simplebench.simplebench_types.ElementCollection`
        associated with a :class:`~simplebench.case.Case`:

        .. code-block:: python

            options = Reporter.find_options_by_type(case.options, CSVReporterOptions)

        :param options: A collection of :class:`~.ReporterOptions` instances.
        :type options: ElementCollection[:class:`~.ReporterOptions`] | None
        :param cls: The specific subclass type of :class:`~.ReporterOptions` to find.
        :type cls: type[T]
        :return: The instance of the class ``cls`` if found, otherwise ``None``.
        :rtype: T | None
        :raises SimpleBenchTypeError: If ``cls`` is not a type.
        :raises SimpleBenchTypeError: If ``options`` is not a
            :class:`~simplebench.simplebench_types.ElementsCollection` of :class:`~.ReporterOptions`
        """
        _validate.cls_type(cls, 'cls')

        if options is None:
            return None

        validated_options = _validate.reporter_options(options, 'options')
        for item in validated_options:
            if isinstance(item, cls):
                return item
        return None

    def report(
        self,  # pylint: disable=too-many-arguments  # noqa: C901
        *,
        log_metadata: 'Metadata',
        args: Namespace,
        case: 'Case',
        choice: 'Choice',
        path: Path | None = None,
        session: 'Session | None' = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Generate a report based on the benchmark results.

        This method performs validation and then calls the subclass's :meth:`~.run_report` method.

        :param log_metadata: The metadata for the report log.
        :type log_metadata: :class:`~simplebench.reporters.log.report_log_metadata.ReportLogMetadata`
        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param case: The :class:`~simplebench.case.Case` instance containing benchmark results.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance specifying
                       the report configuration.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param path: The path to the directory where the report can be saved if needed.
                     Leave as ``None`` if not saving to the filesystem. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance containing benchmark results.
                        Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: A callback function for additional processing of the report. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
        _validate.log_metadata(log_metadata, 'log_metadata')
        _validate.reports_log_path(log_metadata, 'log_metadata.reports_log_path')
        _validate.args(args, 'args')
        _validate.case(case, 'case')
        _validate.path(path, 'path')
        _validate.session(session, 'session')
        _validate.choice(choice, 'choice')
        _validate.callback(callback, 'callback')
        _validate.supported_metrics(choice.metrics, self.supported_metrics, 'choice.metrics')
        _validate.supported_targets(choice.targets, self.supported_targets, 'choice.targets')
        _validate.supported_formats(choice.output_format, self.supported_formats, 'choice.output_format')
        _validate.callback_in_targets(choice.targets, callback, 'CALLBACK in choice.targets, callback argument')
        _validate.filesystem_in_targets(choice.targets, path, 'FILESYSTEM in choice.targets, path argument')

        # Only proceed if there are results to report
        # TODO: THINK ABOUT THIS MORE. SHOULD WE RAISE AN EXCEPTION INSTEAD?
        results = case.results
        if not results:
            return

        # If we reach this point, all validation has passed and execution
        # will pass through to the hook method, either the default implementation
        # or an overridden implementation in the subclass
        self.run_report(
            args=args,
            log_metadata=log_metadata,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback,
        )

    @abstractmethod
    def render(self, *,
               case: 'Case', metric: 'Metric | None', options: 'ReporterOptions') -> str | bytes | Text | Table:
        """Render the report for a specific case and metric.

        This abstract method must be implemented by all :class:`~.Reporter` subclasses.
        It is responsible for generating the actual report content for a given case and metric,
        based on the provided options.

        The output can be a string, bytes, or a Rich object (:class:`~rich.text.Text` or
        :class:`~rich.table.Table`).

        :param case: The :class:`~simplebench.case.Case` instance containing the benchmark results.
        :type case: :class:`~simplebench.case.Case`
        :param metric: The specific :class:`~simplebench.metric.Metric` of the results to render.
        :type metric: :class:`~simplebench.metric.Metric` | None
        :param options: The reporter-specific :class:`~.ReporterOptions` for rendering.
        :type options: :class:`~.ReporterOptions`
        :return: The rendered report content.
        :rtype: str | bytes | :class:`~rich.text.Text` | :class:`~rich.table.Table`
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        raise SimpleBenchNotImplementedError(
            'Reporter subclasses must implement the render method', tag=_ReporterErrorTag.RENDER_NOT_IMPLEMENTED
        )

    def run_report(
        self,
        *,
        args: Namespace,
        log_metadata: 'Metadata',
        case: 'Case',
        choice: 'Choice',
        path: Path | None = None,
        session: 'Session | None' = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Orchestration hook for report generation.

        This method is the primary customization point for controlling how a report is generated.
        It is called by the public :meth:`~.report` method after all inputs have been validated.

        The default implementation calls :meth:`~._ReporterOrchestrationMixin.render_by_metric`,
        which is suitable for most reporters. Subclasses can override this method to provide
        alternative orchestration, such as calling
        :meth:`~._ReporterOrchestrationMixin.render_by_case` for reports that are generated
        once per case.

        .. note::
            This is also the correct place to implement custom logic for non-standard
            targets like :attr:`~simplebench.enums.Target.CUSTOM`.

        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param log_metadata: The metadata for the report log.
        :type log_metadata: :class:`~simplebench.reporters.log.report_log_metadata.Report
        :param case: The :class:`~simplebench.case.Case` instance representing the benchmarked code.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance specifying
                       the report configuration.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param path: The path to the directory where report files will be saved. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance containing benchmark results.
                        Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: A callback function for additional processing. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
        self.render_by_metric(
            log_metadata=log_metadata,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback,
            args=args,
        )

    def add_choice(self, choice: 'Choice') -> None:
        """Add a :class:`~simplebench.reporters.choice.choice.Choice` to the reporter's choices.

        If the choice's metrics, targets, or formats are not supported by the reporter,
        a :class:`~simplebench.exceptions.SimpleBenchValueError` is raised

        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance to add.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :raises SimpleBenchTypeError: If the provided choice is not a
            :class:`~simplebench.reporters.choice.choice.Choice` instance.
        :raises SimpleBenchValueError: If the choice's metrics, targets, or formats
            are not supported by the reporter.
        """
        _validate.choice(choice, 'choice')
        _validate.supported_metrics(choice.metrics, self.supported_metrics, 'choice.metrics')
        _validate.supported_targets(choice.targets, self.supported_targets, 'choice.targets')
        _validate.supported_formats(choice.output_format, self.supported_formats, 'choice.output_format')
        self.choices.add(choice)

    @property
    def config(self) -> ReporterConfig:
        """The configuration object for the reporter."""
        return self._config

    @property
    def choices(self) -> Choices:
        """The :class:`~simplebench.reporters.choices.choices.Choices` for the reporter.

        The :class:`~simplebench.reporters.choices.choices.Choices` instance contains one or more
        :class:`~simplebench.reporters.choice.choice.Choice` instances, each representing a
        specific combination of metrics, targets, and formats, command line flags,
        and descriptions.

        This property allows access to the reporter's choices for generating reports
        and customizing report output and available options.

        :return: The :class:`~simplebench.reporters.choices.choices.Choices` instance for the reporter.
        :rtype: :class:`~simplebench.reporters.choices.choices.Choices`
        """
        return self._choices

    @property
    def name(self) -> str:
        """The unique identifying name of the reporter."""
        return self.config.name

    @property
    def description(self) -> str:
        """A brief description of the reporter."""
        return self.config.description

    @property
    def options_type(self) -> type[Options]:
        """The specific :class:`~.ReporterOptions` subclass associated with this reporter."""
        return self.__class__.get_default_options().__class__

    @property
    def subdir(self) -> str:
        """The subdirectory where report files will be saved."""
        return self.config.subdir

    @property
    def default_targets(self) -> frozenset[Target]:
        """The default set of Targets for the reporter."""
        return self.config.default_targets

    @property
    def file_suffix(self) -> str:
        """The file suffix for reporter output files."""
        return self.config.file_suffix

    @property
    def file_unique(self) -> bool:
        """Whether output files should have unique names."""
        return self.config.file_unique

    @property
    def file_append(self) -> bool:
        """Whether output files should be appended to."""
        return self.config.file_append

    @property
    def supported_metrics(self) -> MetricsSelection:
        """The set of supported :class:`~simplebench.metric.Metric` for the reporter.

        This is the set of :class:`~simplebench.metric.Metric` that the reporter can include
        in its reports.

        Defined :class:`~simplebench.reporters.choice.choice.Choice` can only include
        :class:`~simplebench.metric.Metric` that are declared in this set.
        """
        return self.config.metrics

    @property
    def supported_targets(self) -> frozenset[Target]:
        """The set of supported :class:`~simplebench.enums.Target` for the reporter.

        This is the set of :class:`~simplebench.enums.Target` that the reporter can output to.

        Defined :class:`~simplebench.reporters.choice.choice.Choice` can only include
        :class:`~simplebench.enums.Target` that are declared in this set.
        """
        return self.config.targets

    @property
    def supported_formats(self) -> frozenset[Format]:
        """The set of supported :class:`~simplebench.enums.Format` for the reporter.

        This is the set of :class:`~simplebench.enums.Format` that the reporter can output in.

        Defined :class:`~simplebench.reporters.choice.choice.Choice` can only include
        :class:`~simplebench.enums.Format` that are declared in this set.
        """
        return self.config.formats

    def get_all_stats_values(self, results: Sequence[Results], metric: Metric) -> list[float]:
        """Gathers all primary statistical values for a given metric across multiple results.

        It collects mean, median, minimum, maximum, 5th percentile, and 95th percentile,
        from each :class:`~simplebench.case.Results` instance for the specified metric.

        This method is useful in determining appropriate scaling factors or units
        for reporting by analyzing the range of values across all results.

        Adjusted standard deviation is not included in this collection because it can
        be ``NaN`` for results with insufficient data points, or orders of magnitude different
        from the other statistics, which can skew scaling calculations.

        :param results: A list of :class:`~simplebench.case.Results` instances to gather
                        statistics from.
        :type results: list[:class:`~simplebench.case.Results`]
        :param metric: The metric to gather statistics for.
        :type metric: :class:`~simplebench.metric.Metric`
        :return: A list of all gathered statistical values.
        :rtype: list[float]
        """
        all_numbers = []
        for result in results:
            stats = result.stats(metric)
            all_numbers.extend(
                [stats.mean, stats.median, stats.minimum, stats.maximum, stats.percentiles[5], stats.percentiles[95]]
            )
        return all_numbers

    @property
    def schema_version(self) -> int:
        """Get the schema version number for the reporter.

        This method returns the schema version number that indicates
        the version of the report schema used by the reporter.

        This defaults to ``1`` and can be overridden by subclasses
        if they implement a different schema version.

        :return: The schema version number.
        """
        return 1
