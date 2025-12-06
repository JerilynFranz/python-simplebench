"""KWArgs for the Reporter.target_filesystem method tests."""
from __future__ import annotations

from pathlib import Path

from rich.table import Table
from rich.text import Text

from simplebench.reporters.log.base.report_log_entry import ReportLogEntry
from simplebench.reporters.reporter import Reporter

from ....kwargs import KWArgs, NoDefaultValue


class TargetFilesystemMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().target_filesystem() method.

    This class is primarily used to facilitate testing of the Reporter target_filesystem()
    instance method with various combinations of parameters, including those that are
    optional and those that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            log_metadata: ReportLogEntry | NoDefaultValue = NoDefaultValue(),
            path: Path | NoDefaultValue = NoDefaultValue(),
            subdir: str | NoDefaultValue = NoDefaultValue(),
            filename: str | NoDefaultValue = NoDefaultValue(),
            output: str | bytes | Text | Table | NoDefaultValue = NoDefaultValue(),
            unique: bool | NoDefaultValue = NoDefaultValue(),
            append: bool | NoDefaultValue = NoDefaultValue(),
    ) -> None:
        """Constructs a TargetFilesystemMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().target_filesystem()
        instance method in tests.

        :param log_metadata: The report log metadata.
        :type log_metadata: ReportLogMetadata | None
        :param path: The path to the directory where the CSV file(s) will be saved.
        :type path: Path | None
        :param subdir: The subdirectory within the path to save the file to.
        :type subdir: str
        :param filename: The filename to save the output as.
        :type filename: str
        :param output: The report data to write to the file.
        :type output: str | bytes | Text | Table
        :param unique: If True, ensure the filename is unique by prepending a counter as needed.
        :type unique: bool
        :param append: If True, append to the file if it already exists. Otherwise, raise an error.
        :type append: bool
        """
        super().__init__(call=Reporter.target_filesystem, kwargs=locals())
