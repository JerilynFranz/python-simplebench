"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations
from typing import TYPE_CHECKING

from tests.kwargs import NoDefaultValue, KWArgs

from simplebench.reporters.choice import Choice, ChoiceConf

if TYPE_CHECKING:
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
    def __init__(  # pylint: disable=unused-argument
            self, *,
            reporter: Reporter | NoDefaultValue = NoDefaultValue(),
            choice_conf: ChoiceConf | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ChoiceKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choice instance in tests.

        Args:
            reporter (Reporter| NoDefaultValue, default=NoDefaultValue()):
                An instance of a Reporter subclass.
            choice_conf (ChoiceConf | NoDefaultValue, default=NoDefaultValue()):
                An instance of ChoiceConf containing configuration for the Choice reporter.
        """
        super().__init__(call=Choice.__init__, kwargs=locals())
