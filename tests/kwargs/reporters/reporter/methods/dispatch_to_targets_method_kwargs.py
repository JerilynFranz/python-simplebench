"""KWArgs for the Reporter.dispatch_to_targets method tests."""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from rich.table import Table
from rich.text import Text

from simplebench.case import Case
from simplebench.enums import Section
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.log.base.report_log_entry import ReportLogEntry
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter
from simplebench.session import Session

from ....kwargs import KWArgs, NoDefaultValue


class DispatchToTargetsMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().dispatch_to_targets() method.

    This class is primarily used to facilitate testing of the Reporter dispatch_to_targets()
    instance method with various combinations of parameters, including those that are
    optional and those that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            output: str | bytes | Text | Table | NoDefaultValue = NoDefaultValue(),
            filename_base: str | NoDefaultValue = NoDefaultValue(),
            log_metadata: ReportLogEntry | NoDefaultValue = NoDefaultValue(),
            args: Namespace | NoDefaultValue = NoDefaultValue(),
            choice: Choice | NoDefaultValue = NoDefaultValue(),
            case: Case | NoDefaultValue = NoDefaultValue(),
            section: Section | NoDefaultValue = NoDefaultValue(),
            path: Path | NoDefaultValue = NoDefaultValue(),
            session: Session | NoDefaultValue = NoDefaultValue(),
            callback: ReporterCallback | NoDefaultValue = NoDefaultValue(),
    ) -> None:
        """Constructs a DispatchToTargetsMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().dispatch_to_targets()
        instance method in tests.

        :param output: The report data to be dispatched to the specified targets.
        :type output: str | bytes | Text | Table
        :param filename_base: The base filename to use when saving report data to the filesystem.
                              Does not include file extension.
        :type filename_base: str
        :param args: The parsed command-line arguments.
        :type args: Namespace
        :param log_metadata: The report log metadata.
        :type log_metadata: ReportLogMetadata
        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :param case: The Case instance representing the benchmarked code.
        :type case: Case
        :param section: The Section instance specifying the report section.
        :type section: Section
        :param path: The path to the directory where the CSV file(s) will be saved.
        :type path: Path | None
        :param session: The Session instance containing benchmark results.
        :type session: Session | None
        :param callback: A callback function for additional processing of the report.
                         The function should accept two arguments: the Case instance and the CSV data as a string.
                         Leave as None if no callback is needed.
        :type callback: ReporterCallback | None
        """
        super().__init__(call=Reporter.dispatch_to_targets, kwargs=locals())
