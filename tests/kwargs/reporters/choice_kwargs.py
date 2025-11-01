"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""
from __future__ import annotations
from typing import Any, Sequence, TYPE_CHECKING

from tests.kwargs import NoDefaultValue, KWArgs

from simplebench.reporters.choice import Choice

if TYPE_CHECKING:
    from simplebench.reporters.reporter import Reporter
    from simplebench.enums import Section, Target, Format, FlagType
    from simplebench.reporters.reporter import ReporterOptions


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
        """Constructs a ChoiceKWArgs instance. This class is used to hold keyword arguments for
        initializing a Choice instance in tests.

        Args:
            reporter (Reporter| NoDefaultValue, default=NoDefaultValue()):
                An instance of a Reporter subclass.
            flags (Sequence[str] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of command-line flags associated with the choice.
            flag_type (FlagType | NoDefaultValue, default=NoDefaultValue()):
                The type of flag (e.g., boolean, string) associated with the choice.
            name (str | NoDefaultValue, default=NoDefaultValue()):
                A unique name for the choice.
            description (str | NoDefaultValue, default=NoDefaultValue()):
                A brief description of the choice.
            subdir (str | NoDefaultValue, default=NoDefaultValue()):
                The subdirectory for output files.
            sections (Sequence[Section] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of Section enums to include in the report.
            targets (Sequence[Target] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of Target enums for output.
            default_targets (Sequence[Target] | NoDefaultValue, default=NoDefaultValue()):
                A sequence of default Target enums for output.
            file_suffix (str | NoDefaultValue, default=NoDefaultValue()):
                The file suffix for output files.
            file_unique (bool | NoDefaultValue, default=NoDefaultValue()):
                Whether the output files should be unique.
            file_append (bool | NoDefaultValue, default=NoDefaultValue()):
                Whether to append to existing output files.
            output_format (Format | NoDefaultValue, default=NoDefaultValue()):
                A Format enums for output.
            options (ReporterOptions | NoDefaultValue, default=NoDefaultValue()):
                Options for the choice.
            extra (Any | NoDefaultValue, default=NoDefaultValue()):
                Any additional metadata associated with the choice. Defaults to None.
        """
        super().__init__(base_class=Choice, kwargs=locals())
