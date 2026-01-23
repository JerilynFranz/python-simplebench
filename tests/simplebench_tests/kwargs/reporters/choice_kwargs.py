"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""

from simplebench_tests.kwargs.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.reporter import Reporter


class ChoiceKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Choice instance.

    This class is primarily used to facilitate testing of the Choice class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Choice class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(
            self, *,
            reporter: Reporter | NoDefaultValue = NO_DEFAULT_VALUE,
            choice_conf: ChoiceConf | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Constructs a ChoiceKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choice instance in tests.

        :param reporter: An instance of a Reporter subclass.
        :type reporter: Reporter | NoDefaultValue
        :param choice_conf: An instance of ChoiceConf containing configuration for the Choice reporter.
        :type choice_conf: ChoiceConf | NoDefaultValue
        """
        super().__init__(call=Choice.__init__, kwargs=locals())
