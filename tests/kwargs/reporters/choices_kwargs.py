"""Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from simplebench.reporters.choices import Choices

from ..kwargs import KWArgs, NoDefaultValue

if TYPE_CHECKING:
    from simplebench.reporters.choice import Choice


class ChoicesKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Choices instance.

    This class is primarily used to facilitate testing of the Choices class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Choices class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            choices: Iterable[Choice] | Choices | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ChoicesKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choices instance in tests.

        Args:
            choices (Iterable[Choice] | Choices | NoDefaultValue, default=NoDefaultValue()):
                An iterable of Choice instances.
        """
        super().__init__(call=Choices.__init__, kwargs=locals())
