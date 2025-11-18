"""Choice KWArgs package for SimpleBench tests."""
from typing import Iterable

from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices import ChoicesConf
from tests.kwargs import KWArgs, NoDefaultValue


class ChoicesConfKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a ChoicesConf instance.

    This class is primarily used to facilitate testing of the ChoicesConf class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the ChoicesConf class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            choices: Iterable[ChoiceConf] | ChoicesConf | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ChoicesKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choices instance in tests.

        :param choices: An iterable of ChoiceConf instances.
        :type choices: Iterable[ChoiceConf] | ChoicesConf | NoDefaultValue
        """
        super().__init__(call=ChoicesConf.__init__, kwargs=locals())
