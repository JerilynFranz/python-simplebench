"""KWArgs for Reporter.target_callback() method."""
from simplebench.case import Case
from simplebench.enums import Format, Section
from simplebench.reporters.protocols.reporter_callback import ReporterCallback
from simplebench.reporters.reporter import Reporter

from ....kwargs import KWArgs, NoDefaultValue


class TargetCallbackMethodKWArgs(KWArgs):
    """A class to hold keyword arguments for calling the Reporter().target_callback() method.

    This class is primarily used to facilitate testing of the Reporter target_callback()
    instance method with various combinations of parameters, including those that are
    optional and those that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.

    :param callback: The callback function to send the output to.
    :type callback: ReporterCallback | None
    :param case: The Case instance representing the benchmarked code.
    :type case: Case
    :param section: The Section of the report.
    :type section: Section
    :param output_format: The Format of the report.
    :type output_format: Format
    :param output: The report data to pass to the callback function.
    :type output: str | bytes
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            callback: ReporterCallback | NoDefaultValue = NoDefaultValue(),
            case: Case | NoDefaultValue = NoDefaultValue(),
            section: Section | NoDefaultValue = NoDefaultValue(),
            output_format: Format | NoDefaultValue = NoDefaultValue(),
            output: str | bytes | NoDefaultValue = NoDefaultValue(),
    ) -> None:
        """Constructs a TargetCallbackMethodKWArgs instance.

        This class is used to hold keyword arguments for calling the Reporter().target_callback()
        instance method in tests.

        :param callback: The callback function to send the output to.
        :type callback: ReporterCallback | None
        :param case: The Case instance representing the benchmarked code.
        :type case: Case
        :param section: The Section of the report.
        :type section: Section
        :param output_format: The Format of the report.
        :type output_format: Format
        :param output: The report data to pass to the callback function.
        :type output: str | bytes
        """
        super().__init__(call=Reporter.target_callback, kwargs=locals())
