"""Mixin for prioritization-related functionality for the Reporter class."""
from __future__ import annotations

from typing import TYPE_CHECKING

from simplebench.enums import Target
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.type_proxies import is_case, is_choice

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.reporters.reporter.protocols import ReporterProtocol


class _ReporterPrioritizationMixin:
    """Mixin for prioritization-related functionality for the Reporter class."""

    def get_prioritized_options(self: ReporterProtocol, case: Case, choice: Choice) -> ReporterOptions:
        """Get the reporter-specific options from the case, choice, or default options.

        This method retrieves reporter-specific options of type `options_cls` by
        checking the `case` options first, then the `choice` options, and finally
        falling back to the reporter's default options if none are found.

        The actual type of `ReporterOptions` to retrieve is determined by the
        reporter's `options_type` property - it will always be a specific subclass
        of `ReporterOptions` defined by the reporter.

        :param case: The Case instance containing benchmark results.
        :type case: Case
        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :return: The prioritized instance of the class `ReporterOptions`.
            More specifically, it will be an instance of the reporter's specific
            `ReporterOptions` subclass as defined by the reporter's `options_type` property.
        :rtype: ReporterOptions
        :raises SimpleBenchNotImplementedError: If no ReporterOptions instance can be found.
        """
        # is_* checks handle deferred import runtime type checking for Case and Choice
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"Invalid case argument: expected Case instance, got {type(case).__name__}",
                tag=ReporterErrorTag.GET_PRIORITIZED_OPTIONS_INVALID_CASE_ARG_TYPE)
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                f"Invalid choice argument: expected Choice instance, got {type(choice).__name__}",
                tag=ReporterErrorTag.GET_PRIORITIZED_OPTIONS_INVALID_CHOICE_ARG_TYPE)

        cls = self.__class__
        options_cls = self._OPTIONS_TYPE
        # case.options is a list of ReporterOptions because Case.options is used
        # for all reporters. Thus, we need to filter by the specific type here
        # to find the reporter-specific options.
        case_options = cls.find_options_by_type(options=case.options, cls=options_cls)
        if isinstance(case_options, options_cls):
            return case_options

        if isinstance(choice.options, options_cls):
            return choice.options

        return cls.get_default_options()

    def get_prioritized_default_targets(self: ReporterProtocol, choice: Choice) -> frozenset[Target]:
        """Get the prioritized default targets from the choice or reporter defaults.

        This method retrieves the default targets for the reporter by first checking
        the `choice` default_targets, and if none are found, falling back to the reporter's
        default targets.

        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :return: The set of default targets.
        :rtype: frozenset[Target]
        """
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                f"Invalid choice argument: expected Choice instance, got {type(choice).__name__}",
                tag=ReporterErrorTag.GET_PRIORITIZED_DEFAULT_TARGETS_INVALID_CHOICE_ARG_TYPE)
        if choice.default_targets:
            return choice.default_targets
        return self.default_targets

    def get_prioritized_subdir(self: ReporterProtocol, choice: Choice) -> str:
        """Get the prioritized subdirectory from the choice or reporter defaults.

        The prioritized subdirectory is determined by checking the `Choice().subdir`
        attribute of the provided `choice` argument:
        - If `None`, the reporter's default subdir is returned.
        - If not `None`, the Choice's subdir is returned as the prioritized subdirectory.

        Semantically, a subdir of '' indicates that report files should be saved
        in the root output directory, while any other string indicates a subdirectory
        within the output directory.

        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :return: The subdirectory for saving report files.
        :rtype: str
        """
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                f"Invalid choice argument: expected Choice instance, got {type(choice).__name__}",
                tag=ReporterErrorTag.GET_PRIORITIZED_SUBDIR_INVALID_CHOICE_ARG_TYPE)
        if choice.subdir is not None:
            return choice.subdir
        return self.subdir

    def get_prioritized_file_suffix(self: ReporterProtocol, choice: Choice) -> str:
        """Get the prioritized file suffix from the choice or reporter.

        This method retrieves the file suffix for the reporter by first checking
        the `choice` file_suffix, and if None is found falling back to the reporter's
        file_suffix.

        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :return: The file suffix for report files.
        :rtype: str
        """
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                f"Invalid choice argument: expected Choice instance, got {type(choice).__name__}",
                tag=ReporterErrorTag.GET_PRIORITIZED_FILE_SUFFIX_INVALID_CHOICE_ARG_TYPE)
        if choice.file_suffix is not None:
            return choice.file_suffix
        return self._file_suffix

    def get_prioritized_file_unique(self: ReporterProtocol, choice: Choice) -> bool:
        """Get the prioritized file unique flag from the choice or reporter.

        This method retrieves the file unique flag for the reporter by first checking
        the `choice` file_unique, and if None is found falling back to the reporter's
        file_unique.

        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :return: The file unique flag for report files.
        :rtype: bool
        """
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                f"Invalid choice argument: expected Choice instance, got {type(choice).__name__}",
                tag=ReporterErrorTag.GET_PRIORITIZED_FILE_UNIQUE_INVALID_CHOICE_ARG_TYPE)
        if choice.file_unique is not None:
            return choice.file_unique
        return self._file_unique

    def get_prioritized_file_append(self: ReporterProtocol, choice: Choice) -> bool:
        """Get the prioritized file append flag from the choice or reporter.

        This method retrieves the file append flag for the reporter by first checking
        the `choice` file_append, and if None is found falling back to the reporter's
        file_append.

        :param choice: The Choice instance specifying the report configuration.
        :type choice: Choice
        :return: The file append flag for report files.
        :rtype: bool
        """
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                f"Invalid choice argument: expected Choice instance, got {type(choice).__name__}",
                tag=ReporterErrorTag.GET_PRIORITIZED_FILE_APPEND_INVALID_CHOICE_ARG_TYPE)
        if choice.file_append is not None:
            return choice.file_append
        return self._file_append
