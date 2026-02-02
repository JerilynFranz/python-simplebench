"""simplebench.reporters.reporter.Reporter render_by_case() KWArgs package for SimpleBench tests."""

from argparse import Namespace  #
from pathlib import Path

from simplebench.case import Case
from simplebench.metadata import Metadata
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter import Reporter
from simplebench.session import Session

from ....kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class RenderByCaseMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().render_by_case() method.

    This class is primarily used to facilitate testing of the Reporter render_by_case()
    instance method with various combinations of parameters, including those that are
    optional and those that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.

    :param renderer: The method to be used for actually rendering the report.
    :type renderer: ReportRenderer
    :param args: The parsed command-line arguments.
    :type args: Namespace
    :param log_metadata: The report log metadata.
    :type log_metadata: ReportLogMetadata
    :param case: The Case instance representing the benchmarked code.
    :type case: Case
    :param choice: The Choice instance specifying the report configuration.
    :type choice: Choice
    :param path: The path to the directory where the CSV file(s) will be saved.
    :type path: Path | None
    :param session: The Session instance containing benchmark results.
    :type session: Session | None
    :param callback: A callback function for additional processing of the report.
                     The function should accept two arguments: the Case instance and the CSV data as a string.
                     Leave as None if no callback is needed.
    :type callback: ReporterCallback | None
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            renderer: ReportRenderer | NoDefaultValue = NO_DEFAULT_VALUE,
            log_metadata: Metadata | NoDefaultValue = NO_DEFAULT_VALUE,
            args: Namespace | NoDefaultValue = NO_DEFAULT_VALUE,
            case: Case | NoDefaultValue = NO_DEFAULT_VALUE,
            choice: Choice | NoDefaultValue = NO_DEFAULT_VALUE,
            path: Path | NoDefaultValue = NO_DEFAULT_VALUE,
            session: Session | NoDefaultValue = NO_DEFAULT_VALUE,
            callback: ReporterCallback | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Constructs a RenderByCaseMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().render_by_case()
        instance method in tests.

        :param renderer: The method to be used for actually rendering the report.
        :type renderer: ReportRenderer
        :param args: The parsed command-line arguments.
        :type args: Namespace
        :param log_metadata: The report log metadata.
        :type log_metadata: ReportLogMetadata
        :param case: The Case instance representing the benchmarked code.
        :type case: Case
        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :param path: The path to the directory where the CSV file(s) will be saved.
        :type path: Path | None
        :param session: The Session instance containing benchmark results.
        :type session: Session | None
        :param callback: A callback function for additional processing of the report.
                         The function should accept two arguments: the Case instance and the CSV data as a string.
                         Leave as None if no callback is needed.
        :type callback: ReporterCallback | None
        """
        super().__init__(call=Reporter.render_by_case, kwargs=locals(), globalns=globals())
