"""KWArgs for the Reporter.target_filesystem method tests."""
# ruff: noqa: F401
# These imports are necessary for the class to run correctly
# because we need them in the global namespace.
# Also, ruff will remove "unused" imports without the noqa directive.
from pathlib import Path

from rich.table import Table
from rich.text import Text
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

from simplebench.metadata import Metadata
from simplebench.reporters.reporter import Reporter, ReporterProtocol


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
            log_metadata: Metadata | NoDefaultValue = NO_DEFAULT_VALUE,
            path: Path | NoDefaultValue = NO_DEFAULT_VALUE,
            subdir: str | NoDefaultValue = NO_DEFAULT_VALUE,
            filename: str | NoDefaultValue = NO_DEFAULT_VALUE,
            output: str | bytes | Text | Table | NoDefaultValue = NO_DEFAULT_VALUE,
            unique: bool | NoDefaultValue = NO_DEFAULT_VALUE,
            append: bool | NoDefaultValue = NO_DEFAULT_VALUE,
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
        super().__init__(call=Reporter.target_filesystem, kwargs=locals(), globalns=globals())
