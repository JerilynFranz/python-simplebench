"""KWArgs subclass for Environment.__init__."""

from collections.abc import Mapping
from typing import Any

from simplebench.report.versions.v1 import Environment
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class EnvironmentKWArgs(KWArgs):
    """KWArgs for GenericEnvironment.__init__"""

    def __init__(self, *, data: Mapping[str, Any] | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize a GenericEnvironment instance.

        If a 'hash_id' key is present in the input data mapping, its value is validated
        and used as the hash_id property. If not present, the hash_id is computed from the
        rest of the data mapping.

        If 'type' or 'version' keys are not present in the input data mapping, they are
        automatically added with the appropriate values for this class.

        :param data: Keyword arguments representing environment properties.
        Each key-value pair corresponds to a property name and its value.
        The values must be of core data types."""
        super().__init__(Environment.__init__, kwargs=locals(), globalns=globals())
