"""simplebench.reporters.reporter.Reporter render_by_section() KWArgs package for SimpleBench tests."""

from argparse import Namespace
from pathlib import Path

from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

from simplebench.case import Case
from simplebench.metadata import Metadata
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter import Reporter
from simplebench.session import Session


class RenderByMetricMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().render_by_metric() method.

    This class is primarily used to facilitate testing of the Reporter render_by_metric()
    instance method with various combinations of parameters.
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
        """Constructs a RenderByMetricMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().render_by_metric()
        instance method in tests.
        """
        super().__init__(
            call=Reporter.render_by_metric, kwargs=locals(), globalns=globals())
