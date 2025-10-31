"""Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations
from typing import Sequence, TYPE_CHECKING

from tests.kwargs import NoDefaultValue

from simplebench.reporters.choices import Choices

if TYPE_CHECKING:
    from simplebench.reporters.choice import Choice


class ChoicesKWArgs(dict):
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
            choices: Sequence[Choice] | Choices | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ChoicesKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choices instance in tests.

        Args:
            choices (Sequence[Choice] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of Choice instances.
        """
        super().__init__(base_class=Choices, kwargs=locals())
