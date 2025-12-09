"""Factory method for ReportLogMetadata objects for testing purposes."""

from pathlib import Path
from typing import TYPE_CHECKING

from simplebench.case import Case
from simplebench.metadata import Metadata

from ...factories import case_factory, default_timestamp, output_path_factory, reports_log_path_factory
from ...kwargs import NoDefaultValue

_DEFERRED_IMPORTED = False
if TYPE_CHECKING:
    from simplebench.reporters.choice import Choice

    from ...factories import choice_factory
    _DEFERRED_IMPORTED = True
else:
    choice_factory = None  # pylint: disable=invalid-name
    Choice = None  # pylint: disable=invalid-name


def deferred_imports():
    """Perform deferred imports to avoid circular dependencies."""
    global Choice, choice_factory, _DEFERRED_IMPORTED  # pylint: disable=global-statement
    if not _DEFERRED_IMPORTED:
        from simplebench.reporters.choice import Choice  # pylint: disable=import-outside-toplevel

        from ...factories import choice_factory  # pylint: disable=import-outside-toplevel
        _DEFERRED_IMPORTED = True


def report_log_filepath_factory() -> Path:
    """Create a default filepath for testing.

    :return: A Path instance representing the default filepath.
    """
    deferred_imports()
    return output_path_factory() / "0000001" / 'subdir' / 'a_file.txt'


def report_log_metadata_factory(  # pylint: disable=unused-argument
    *,
    filepath: Path | NoDefaultValue = NoDefaultValue(),
    timestamp: float | NoDefaultValue = NoDefaultValue(),
    reports_log_path: Path | NoDefaultValue = NoDefaultValue(),
    case: Case | NoDefaultValue = NoDefaultValue(),
    choice: Choice | NoDefaultValue = NoDefaultValue(),
) -> Metadata:
    """Create a ReportLogMetadata instance for testing.

    :param filepath: The path to the generated report file. If None, no file path is set.
    :param timestamp: The timestamp of the report generation.
    :param reports_log_path: The path to the reports log file.
    :param case: The Case instance containing benchmark results. If None, a default Case is created.
    :param choice: The Choice instance specifying the report configuration. If None, a default Choice is created.
    :return: A ReportLogMetadata instance.
    """
    deferred_imports()
    kwargs = {
        'filepath': report_log_filepath_factory(),
        'case': case_factory(),
        'choice': choice_factory(),
        'reports_log_path': reports_log_path_factory(),
        'timestamp': default_timestamp(),
    }
    for key in kwargs:
        if not isinstance(locals()[key], NoDefaultValue):
            kwargs[key] = locals()[key]

    return Metadata(**kwargs)  # type: ignore[arg-type]
