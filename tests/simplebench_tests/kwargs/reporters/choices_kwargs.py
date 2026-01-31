"""Choice KWArgs package for SimpleBench tests."""
from simplebench.reporters.choice import Choice
from simplebench.reporters.choices import Choices
from simplebench.simplebench_types import ElementCollection

from ..kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class ChoicesKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Choices instance.

    This class is primarily used to facilitate testing of the Choices class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Choices class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(
            self,
            choices: ElementCollection[Choice] | Choices | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Constructs a ChoicesKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choices instance in tests.

        :param choices: An iterable of Choice instances.
        :type choices: ElementCollection[Choice] | Choices | NoDefaultValue
        """
        super().__init__(call=Choices.__init__, kwargs=locals(), globalns=globals())
