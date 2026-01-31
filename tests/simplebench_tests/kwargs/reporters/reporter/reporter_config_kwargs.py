"""simplebench.reporters.reporter.Reporter KWArgs package for SimpleBench tests."""
from collections.abc import Iterable

from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

from simplebench.enums import Format, Target
from simplebench.metrics import MetricsSelection
from simplebench.reporters.choice import ChoiceConf
from simplebench.reporters.choices import ChoicesConf
from simplebench.reporters.reporter import ReporterConfig


class ReporterConfigKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a ReporterConfig instance.

    This class is primarily used to facilitate testing of the ReporterConfig class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the ReporterConfig class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(
            self,
            *,
            name: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            metrics: MetricsSelection | NoDefaultValue = NO_DEFAULT_VALUE,
            targets: Iterable[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
            default_targets: Iterable[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
            subdir: str | NoDefaultValue = NO_DEFAULT_VALUE,
            file_suffix: str | NoDefaultValue = NO_DEFAULT_VALUE,
            file_unique: bool | NoDefaultValue = NO_DEFAULT_VALUE,
            file_append: bool | NoDefaultValue = NO_DEFAULT_VALUE,
            formats: Iterable[Format] | NoDefaultValue = NO_DEFAULT_VALUE,
            choices: Iterable[ChoiceConf] | ChoicesConf | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Constructs a ReporterKWArgs instance. This class is used to hold keyword arguments for
        initializing a Reporter instance in tests.

        :param name: The unique identifying name of the reporter. Must be a non-empty string.
        :type name: str
        :param description: A brief description of the reporter. Must be a non-empty string.
                            or None if no specific options are defined.
        :type description: str
        :param sections: The set of all Metrics supported by the reporter.
        :type sections: set[Metric]
        :param targets: The set of all Targets supported by the reporter.
        :type targets: set[Target]
        :param default_targets: The default set of Targets for the reporter.
        :type default_targets: set[Target] | None
        :param subdir: The subdirectory where report files will be saved.
        :type subdir: str
        :param file_suffix: An optional file suffix for reporter output files.
                            - May be an empty string ('')
                            - Cannot contain non-alphanumeric characters (characters other than A-Z, a-z, 0-9).
                            - Cannot be longer than 10 characters.
        :type file_suffix: str
        :param file_unique: Whether output files should have unique names.
        :type file_unique: bool
        :param file_append: Whether output files should be appended to.
        :type file_append: bool
        :param formats: The set of Formats supported by the reporter.
        :type formats: set[Format]
        :param choices: A Choices instance defining the sections, output targets,
                        and formats supported by the reporter. Must have at least one Choice.
        :type choices: Iterable[ChoiceConf] | Choices
        """
        super().__init__(call=ReporterConfig.__init__, kwargs=locals())


