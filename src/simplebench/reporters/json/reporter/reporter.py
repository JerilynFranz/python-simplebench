"""Reporter for benchmark results using JSON files."""
from __future__ import annotations

import json
from argparse import Namespace
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias

from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.metadata import Metadata
from simplebench.reporters.protocols.reporter_callback import ReporterCallback
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.type_proxies import is_case
from simplebench.utils import get_machine_info
from simplebench.validators import validate_type

from .config import JSONConfig
from .exceptions import _JSONReporterErrorTag
from .options import JSONOptions
from simplebench.reporters.json.report.versions import CURRENT_VERSION

Options: TypeAlias = JSONOptions


if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.session import Session


class JSONReporter(Reporter):
    """Class for outputting benchmark results to JSON files.

    It supports reporting statistics for various sections,
    either separately or together, to the filesystem, via a callback function,
    or to the console in JSON format.

    The JSON files are tagged with metadata comments including the case title,
    description, and units for clarity.

    **Defined command-line flags:**

    * ``--json: {filesystem, console, callback}`` (default=filesystem) Outputs statistical
      results to JSON.
    * ``--json-data: {filesystem, console, callback}`` (default=filesystem) Outputs results
      to JSON with full data.

    **Example usage:**

    .. code-block:: none

        program.py --json               # Outputs results to JSON files in the filesystem (default).
        program.py --json filesystem    # Outputs results to JSON files in the filesystem.
        program.py --json console       # Outputs results to the console in JSON format.
        program.py --json callback      # Outputs results via a callback function in JSON format.
        program.py --json filesystem console  # Outputs results to both JSON files and the console.

    :ivar name: The unique identifying name of the reporter.
    :vartype name: str
    :ivar description: A brief description of the reporter.
    :vartype description: str
    :ivar choices: A collection of :class:`~simplebench.reporters.choices.Choices` instances
        defining the reporter instance, CLI flags, :class:`~simplebench.reporters.choice.Choice`
        name, supported :class:`~simplebench.enums.Section` objects, supported output
        :class:`~simplebench.enums.Target` objects, and supported output
        :class:`~simplebench.enums.Format` objects for the reporter.
    :vartype choices: ~simplebench.reporters.choices.Choices
    :ivar targets: The supported output targets for the reporter.
    :vartype targets: set[~simplebench.enums.Target]
    :ivar formats: The supported output formats for the reporter.
    :vartype formats: set[~simplebench.enums.Format]
    """
    _OPTIONS_TYPE: ClassVar[type[JSONOptions]] = JSONOptions  # type: ignore[reportIncompatibleVariableOveride]
    """:ivar: The type of :class:`~.ReporterOptions` used by the :class:`~.JSONReporter`.
    :vartype: ~typing.ClassVar[type[~.JSONOptions]]
    """
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {'full_data': False}
    """:ivar: The default keyword arguments for the :class:`~.JSONReporter` options.

    .. code-block:: python

        {"full_data": False}

    :vartype: ~typing.ClassVar[dict[str, ~typing.Any]]
    """

    def __init__(self, config: JSONConfig | None = None) -> None:
        """Initialize the JSONReporter.

        .. note::

            The exception documentation below refers to validation of subclass configuration
            class variables ``_OPTIONS_TYPE`` and ``_OPTIONS_KWARGS``. These must be correctly
            defined in any subclass of :class:`~.JSONReporter` to ensure proper functionality.

        :param config: An optional configuration object to override default reporter settings.
                       If not provided, default settings will be used.
        :type config: JSONConfig | None

        :raises ~simplebench.exceptions.SimpleBenchTypeError: If the subclass configuration
            types are invalid.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If the subclass configuration
            values are invalid.
        """
        if config is None:
            config = JSONConfig()

        super().__init__(config)

    def run_report(self,
                   *,
                   args: Namespace,
                   log_metadata: Metadata,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None
                   ) -> None:
        """Output the benchmark results to a file as tagged JSON if available.

        This method is called by the base class's :meth:`~.Reporter.report` method after
        validation. The base class handles validation of the arguments, so subclasses can
        assume the arguments are valid without a large amount of boilerplate code. The base
        class also handles lazy loading of the reporter classes, so subclasses can assume
        any required imports are available.

        The :meth:`~.run_report` method's main responsibilities are to select the appropriate
        output method (``render_by_case()`` in this case) based on the provided arguments
        and to pass the actual rendering method to be used (the :meth:`~.render` method in
        this case). The rendering method must conform with the
        :class:`~simplebench.reporters.protocols.reporter_renderer.ReportRenderer` protocol.

        :param args: The parsed command-line arguments.
        :param log_metadata: The :class:`~.ReportLogMetadata` instance containing metadata
            about the report being generated.
        :param case: The :class:`~simplebench.case.Case` instance representing the
            benchmarked code.
        :param choice: The :class:`~simplebench.reporters.choice.Choice` instance specifying
            the report configuration.
        :param path: The path to the directory where the JSON file(s) will be saved.
        :param reports_log_path: The path to the reports log file.
        :param session: The :class:`~simplebench.session.Session` instance containing
            benchmark results.
        :param callback: A callback function for additional processing of the report.
            The function should accept two arguments: the :class:`~simplebench.case.Case`
            instance and the JSON data as a string. Leave as ``None`` if no callback is
            needed.
        """
        self.render_by_case(
            renderer=self.render,
            log_metadata=log_metadata,
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
        """Convert the Case data for all sections to a JSON string.

        Machine info is included in the JSON output under the 'metadata' key.

        :param case: The :class:`~simplebench.case.Case` instance holding the benchmarked
            code statistics.
        :param section: The :class:`~simplebench.enums.Section` to render (ignored, all
            sections are included).
        :param options: The :class:`~.JSONOptions` instance specifying rendering options
            or ``None`` if not provided. (:class:`~.JSONOptions` is a subclass of
            :class:`~.ReporterOptions`.)
        :return: The JSON string representation of the :class:`~simplebench.case.Case` data.
        """
        # is_* checks provide deferred import validation to avoid circular imports
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"'case' argument must be a Case instance, got {type(case)}",
                tag=_JSONReporterErrorTag.RENDER_INVALID_CASE)
        section = validate_type(section, Section, 'section',
                                _JSONReporterErrorTag.RENDER_INVALID_SECTION)
        options = validate_type(options, Options, 'options',
                                _JSONReporterErrorTag.RENDER_INVALID_OPTIONS)

        full_data: bool = options.full_data if isinstance(options, Options) else False
        with StringIO() as jsonfile:
            case_dict = case.as_dict(full_data=full_data)
            try:
                case_dict['version'] = self.schema_version
                case_dict['metadata'] = get_machine_info()
                json.dump(case_dict, jsonfile, indent=4)
                jsonfile.seek(0)
            except Exception as exc:
                raise SimpleBenchTypeError(
                    f'Error generating JSON output for case {case.title}: {exc}',
                    tag=_JSONReporterErrorTag.JSON_OUTPUT_ERROR) from exc
            return jsonfile.read()

    @property
    def schema_version(self) -> int:
        """The current schema version for the JSON reporter."""
        return CURRENT_VERSION
