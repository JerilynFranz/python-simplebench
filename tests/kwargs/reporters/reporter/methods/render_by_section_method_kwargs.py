"""simplebench.reporters.reporter.Reporter render_by_section() KWArgs package for SimpleBench tests."""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from simplebench.case import Case
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.log.report_log_metadata import ReportLogMetadata
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter import Reporter
from simplebench.session import Session

from ....kwargs import KWArgs, NoDefaultValue


class RenderBySectionMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().render_by_section() method.

    This class is primarily used to facilitate testing of the Reporter render_by_section()
    instance method with various combinations of parameters.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            renderer: ReportRenderer | NoDefaultValue = NoDefaultValue(),
            args: Namespace | NoDefaultValue = NoDefaultValue(),
            log_metadata: ReportLogMetadata | NoDefaultValue = NoDefaultValue(),
            case: Case | NoDefaultValue = NoDefaultValue(),
            choice: Choice | NoDefaultValue = NoDefaultValue(),
            path: Path | NoDefaultValue = NoDefaultValue(),
            session: Session | NoDefaultValue = NoDefaultValue(),
            callback: ReporterCallback | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a RenderBySectionMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().render_by_section()
        instance method in tests.
        """
        super().__init__(call=Reporter.render_by_section, kwargs=locals())
