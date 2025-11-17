"""KWArgs for Reporter.target_console() method."""
from rich.table import Table
from rich.text import Text

from simplebench.reporters.reporter import Reporter
from simplebench.session import Session

from ....kwargs import KWArgs, NoDefaultValue


class TargetConsoleMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().target_console() method.

    This class is primarily used to facilitate testing of the Reporter target_console()
    instance method with various combinations of parameters, including those that are
    optional and those that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.

    Args:
        session (Optional[Session]): The Session instance containing benchmark results.
        output (str | bytes | Text | Table): The report data to write to the console.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            session: Session | NoDefaultValue = NoDefaultValue(),
            output: str | bytes | Text | Table | NoDefaultValue = NoDefaultValue(),
    ) -> None:
        """Constructs a TargetConsoleMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().target_console()
        instance method in tests.

        Args:
            session (Optional[Session]): The Session instance containing benchmark results.
            output (str | bytes | Text | Table): The report data to write to the console.
        """
        super().__init__(call=Reporter.target_console, kwargs=locals())
