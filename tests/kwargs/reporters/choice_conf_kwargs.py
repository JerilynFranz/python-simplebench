"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

from simplebench.reporters.choice.choice_conf import ChoiceConf
from tests.kwargs import KWArgs, NoDefaultValue

if TYPE_CHECKING:
    from simplebench.enums import FlagType, Format, Section, Target
    from simplebench.reporters.reporter import ReporterOptions


class ChoiceConfKWArgs(KWArgs):
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
            flags: Sequence[str] | NoDefaultValue = NoDefaultValue(),
            flag_type: FlagType | NoDefaultValue = NoDefaultValue(),
            name: str | NoDefaultValue = NoDefaultValue(),
            description: str | NoDefaultValue = NoDefaultValue(),
            subdir: str | NoDefaultValue = NoDefaultValue(),
            sections: Sequence[Section] | NoDefaultValue = NoDefaultValue(),
            targets: Sequence[Target] | NoDefaultValue = NoDefaultValue(),
            default_targets: Sequence[Target] | NoDefaultValue = NoDefaultValue(),
            output_format: Format | NoDefaultValue = NoDefaultValue(),
            file_suffix: str | NoDefaultValue = NoDefaultValue(),
            file_unique: bool | NoDefaultValue = NoDefaultValue(),
            file_append: bool | NoDefaultValue = NoDefaultValue(),
            options: ReporterOptions | NoDefaultValue = NoDefaultValue(),
            extra: Any | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ChoiceConfKWArgs instance. This class is used to hold keyword arguments for
        initializing a ChoiceConf instance in tests.

        :param flags: A sequence of command-line flags associated with the choice.
        :type flags: Sequence[str] | NoDefaultValue
        :param flag_type: The type of flag (e.g., boolean, string) associated with the choice.
        :type flag_type: FlagType | NoDefaultValue
        :param name: A unique name for the choice.
        :type name: str | NoDefaultValue
        :param description: A brief description of the choice.
        :type description: str | NoDefaultValue
        :param subdir: The subdirectory for output files.
        :type subdir: str | NoDefaultValue
        :param sections: A sequence of Section enums to include in the report.
        :type sections: Sequence[Section] | NoDefaultValue
        :param targets: A sequence of Target enums for output.
        :type targets: Sequence[Target] | NoDefaultValue
        :param default_targets: A sequence of default Target enums for output.
        :type default_targets: Sequence[Target] | NoDefaultValue
        :param file_suffix: The file suffix for output files.
        :type file_suffix: str | NoDefaultValue
        :param file_unique: Whether the output files should be unique.
        :type file_unique: bool | NoDefaultValue
        :param file_append: Whether to append to existing output files.
        :type file_append: bool | NoDefaultValue
        :param output_format: A Format enums for output.
        :type output_format: Format | NoDefaultValue
        :param options: Options for the choice.
        :type options: ReporterOptions | NoDefaultValue
        :param extra: Any additional metadata associated with the choice. Defaults to None.
        :type extra: Any | NoDefaultValue
        """
        super().__init__(call=ChoiceConf.__init__, kwargs=locals())
