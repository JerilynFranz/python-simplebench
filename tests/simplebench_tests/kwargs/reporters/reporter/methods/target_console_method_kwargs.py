"""KWArgs for Reporter.target_console() method."""
# ruff: noqa: F401
# These imports are necessary for the class to run correctly as
# because we need them in the global namespace.
# Also, ruff will remove "unused" imports without the noqa directive.
from rich.table import Table
from rich.text import Text
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

from simplebench.reporters.reporter import Reporter, ReporterProtocol
from simplebench.session import Session


class TargetConsoleMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().target_console() method.

    This class is primarily used to facilitate testing of the Reporter target_console()
    instance method with various combinations of parameters, including those that are
    optional and those that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.

    :param session: The Session instance containing benchmark results.
    :type session: Session | None
    :param output: The report data to write to the console.
    :type output: str | bytes | Text | Table
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            session: Session | NoDefaultValue = NO_DEFAULT_VALUE,
            output: str | bytes | Text | Table | NoDefaultValue = NO_DEFAULT_VALUE,
    ) -> None:
        """Constructs a TargetConsoleMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().target_console()
        instance method in tests.

        :param session: The Session instance containing benchmark results.
        :type session: Session | None
        :param output: The report data to write to the console.
        :type output: str | bytes | Text | Table
        """
        super().__init__(call=Reporter.target_console, kwargs=locals(), globalns=globals())
