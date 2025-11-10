"""Mixin for target-related functionality for the Reporter class."""
from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table
from rich.text import Text

from simplebench.enums import Format, Section
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.validators import (validate_filename, validate_string,
                                    validate_type)

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session


class _ReporterTargetMixin:
    """Mixin for target-related functionality for the Reporter class."""

    def target_filesystem(self: ReporterProtocol, *,
                          path: Path | None,
                          subdir: str,
                          filename: str,
                          output: str | bytes | Text | Table,
                          unique: bool = False,
                          append: bool = False) -> None:
        """Helper method to output report data to the filesystem.

        path, subdir, and filename are combined to form the full path to the output file.

        If unique is True, the filename will be made unique by prepending a counter
        starting from 001 to the filename and counting up until a unique filename is found.
        E.g. 001_filename.txt, 002_filename.txt, etc.

        If append is True, the output will be appended to the file if it already exists.
        Otherwise, an exception will be raised if the file already exists. Note that
        append mode is not compatible with unique mode.

        The type signature for path is Path | None because the overall report() method
        accepts path as Optional[Path] because it is not always required. However,
        this method should only be called when a valid Path is provided and will
        raise an exception if it is not a Path instance.

        Args:
            path (Path | None): The path to the directory where output should be saved.
            subdir (str): The subdirectory within the path to save the file to.
            filename (str): The filename to save the output as.
            output (str | bytes | Text | Table): The report data to write to the file.
            unique (bool): If True, ensure the filename is unique by prepending a counter as needed.
            append (bool): If True, append to the file if it already exists. Otherwise, raise an error.

        Raises:
            SimpleBenchTypeError: If path is not a Path instance,
                or if subdir or filename are not strings.
            SimpleBenchValueError: If both append and unique are True. Or if the output file
                already exists and neither append nor unique options were specified.
        """
        path = validate_type(
            path, Path, 'path',
            ReporterErrorTag.TARGET_FILESYSTEM_INVALID_PATH_ARG_TYPE)
        subdir = validate_string(
            subdir, 'subdir',
            ReporterErrorTag.TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_TYPE,
            ReporterErrorTag.TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_VALUE,
            strip=False, allow_empty=True, allow_blank=False, alphanumeric_only=True)
        filename = validate_filename(filename)
        append = validate_type(
            append, bool, 'append',
            ReporterErrorTag.TARGET_FILESYSTEM_INVALID_APPEND_ARG_TYPE)
        unique = validate_type(
            unique, bool, 'unique',
            error_tag=ReporterErrorTag.TARGET_FILESYSTEM_INVALID_UNIQUE_ARG_TYPE)
        if not isinstance(output, (str, bytes, Text, Table)):
            raise SimpleBenchTypeError(
                "output must be of type str, bytes, Text, or Table",
                tag=ReporterErrorTag.TARGET_FILESYSTEM_INVALID_OUTPUT_ARG_TYPE)
        if append and unique:
            raise SimpleBenchValueError(
                "append and unique options are not compatible when writing to filesystem",
                tag=ReporterErrorTag.TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS)
        if unique:
            counter = 1
            while (path / subdir / f"{counter:03d}_{filename}").exists():
                counter += 1
            filename = f"{counter:03d}_{filename}"

        if isinstance(output, (Text, Table)):
            output = self.rich_text_to_plain_text(output)
        output_path = path / subdir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mode = 'wb' if isinstance(output, bytes) else 'w'
        if append:
            mode = 'ab' if isinstance(output, bytes) else 'a'
        if output_path.exists() and not append:
            raise SimpleBenchValueError(
                f"Output file already exists and neither append nor unique options were specified: {output_path}",
                tag=ReporterErrorTag.TARGET_FILESYSTEM_OUTPUT_FILE_EXISTS)
        with output_path.open(mode=mode) as f:
            f.write(output)

    def target_callback(self: ReporterProtocol,
                        callback: ReporterCallback | None,
                        case: Case,
                        section: Section,
                        output_format: Format,
                        output: str | bytes | Text | Table) -> None:
        """Helper method to send report data to a callback function.

        Args:
            callback (ReporterCallback | None): The callback function to send the output to.
            case (Case): The Case instance representing the benchmarked code.
            section (Section): The Section of the report.
            output_format (Format): The Format of the report.
            output (str | bytes | Text | Table): The report data to send to the callback.

        Returns:
            None
        """
        if isinstance(output, (Text, Table)):
            output = self.rich_text_to_plain_text(output)
        if callback is not None:
            callback(case=case, section=section, output_format=output_format, output=output)

    def target_console(self: ReporterProtocol, session: Session | None, output: str | bytes | Text | Table) -> None:
        """Helper method to output report data to the console.

        It uses the Rich Console instance from the Session if provided, otherwise
        it creates a new Console instance.

        It can accept output as a string, Rich Text, or Rich Table.

        Args:
            output (str | bytes | Text | Table): The report data to print to the console.

        Returns:
            None
        """
        console = session.console if session is not None else Console()
        console.print(output)

    def rich_text_to_plain_text(self: ReporterProtocol, rich_text: Text | Table) -> str:
        """Convert Rich Text or Table to plain text by stripping formatting.

        Applies a virtual console width to ensure proper line wrapping. The console
        width simulates how the text would appear in a terminal of the specified width.

        As rich text is normally mainly used for console output, this method
        provides a way to convert it to plain text while preserving the intended
        layout as much as possible for non-console output targets.

        Args:
            rich_text (Text | Table): The Rich Text or Table instance to convert.
        Returns:
            str: The plain text representation of the Rich Text.
        """
        if not isinstance(rich_text, (Text, Table)):
            raise SimpleBenchTypeError(
                f'rich_text argument is of invalid type: {type(rich_text)}. '
                f'Must be rich.Text or rich.Table.',
                tag=ReporterErrorTag.RICH_TEXT_TO_PLAIN_TEXT_INVALID_RICH_TEXT_ARG_TYPE)

        output_io = StringIO()  # just a string buffer to capture console output
        console = Console(file=output_io, width=None, record=True)
        console.print(rich_text)
        text_output = console.export_text(styles=False)
        output_io.close()

        return text_output
