"""simplebench.reporters.reporter.Reporter KWArgs package for SimpleBench tests."""
from __future__ import annotations

from typing import Iterable

from simplebench.enums import Format, Section, Target
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter import Reporter

from ..kwargs import KWArgs, NoDefaultValue


class ReporterKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Reporter instance.

    This class is primarily used to facilitate testing of the Reporter class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            name: str | NoDefaultValue = NoDefaultValue(),
            description: str | NoDefaultValue = NoDefaultValue(),
            sections: Iterable[Section] | NoDefaultValue = NoDefaultValue(),
            targets: Iterable[Target] | NoDefaultValue = NoDefaultValue(),
            default_targets: Iterable[Target] | NoDefaultValue = NoDefaultValue(),
            subdir: str | NoDefaultValue = NoDefaultValue(),
            file_suffix: str | NoDefaultValue = NoDefaultValue(),
            file_unique: bool | NoDefaultValue = NoDefaultValue(),
            file_append: bool | NoDefaultValue = NoDefaultValue(),
            formats: Iterable[Format] | NoDefaultValue = NoDefaultValue(),
            choices: Iterable[ChoiceConf] | ChoicesConf | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a ReporterKWArgs instance. This class is used to hold keyword arguments for
        initializing a Reporter instance in tests.

        Args:
            name (str):
                The unique identifying name of the reporter. Must be a non-empty string.
            description (str):
                A brief description of the reporter. Must be a non-empty string.
                or None if no specific options are defined.
            sections (set[Section]):
                The set of all Sections supported by the reporter.
            targets (set[Target]):
                The set of all Targets supported by the reporter.
            default_targets (set[Target] | None, default=None):
                The default set of Targets for the reporter.
            subdir (str, default=''):
                The subdirectory where report files will be saved.
            file_suffix (str):
                An optional file suffix for reporter output files.
                - May be an empty string ('')
                - Cannot contain non-alphanumeric characters (characters other than A-Z, a-z, 0-9).
                - Cannot be longer than 10 characters.
            file_unique (bool):
                Whether output files should have unique names.
            file_append (bool):
                Whether output files should be appended to.
            formats (set[Format]):
                The set of Formats supported by the reporter.
            choices (Iterable[ChoiceConf] | Choices):
                A Choices instance defining the sections, output targets,
                and formats supported by the reporter. Must have at least one Choice."""
        super().__init__(call=Reporter.__init__, kwargs=locals())
