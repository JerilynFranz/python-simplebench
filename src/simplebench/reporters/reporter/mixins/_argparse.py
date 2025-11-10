"""Mixin for argparse-related functionality for the Reporter class."""
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from typing import Iterable

from simplebench.enums import FlagType, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.choice.choice import Choice
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.utils import collect_arg_list
from simplebench.validators import validate_iterable_of_type, validate_type


class _ReporterArgparseMixin:
    """Mixin for argparse-related functionality for the Reporter class."""

    def select_targets_from_args(
        self: ReporterProtocol,
        *,
        args: Namespace,
        choice: Choice,
        default_targets: Iterable[Target],
    ) -> set[Target]:
        """Select the output targets based on command-line arguments and choice configuration.

        It checks the command-line arguments for any flags corresponding to the choice
        and collects the specified targets. It then cross-validates the specified targets
        against the supported targets for the choice. If no targets are specified in the
        command-line arguments, the default targets are used instead.

        An exception is raised if a target is specified in the arguments,
        or in the default targets, that are not supported by the choice.

        Args:
            args (Namespace): The parsed command-line arguments.
            choice (Choice): The Choice instance specifying the report configuration.
            default_targets (Iterable[Target]]): The default targets to use if no targets
                are specified in the command-line arguments.

        Returns:
            A set of Target enums representing the selected output targets.

        Raises:
            SimpleBenchTypeError: If args is not an argparse.Namespace instance.
            SimpleBenchValueError: If an unsupported target is specified in the arguments.
        """
        args = validate_type(args, Namespace, 'args',
                             ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_ARGS_ARG)
        choice = validate_type(choice, Choice, 'choice',
                               ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_CHOICE_ARG)
        default_targets = validate_iterable_of_type(
            default_targets, Target, 'default_targets',
            ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_DEFAULT_TARGETS_ARG,
            ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_DEFAULT_TARGETS_ARG,
            allow_empty=True)

        for target in default_targets:
            if target not in choice.targets:
                raise SimpleBenchValueError(
                    f"Default target {target} is not supported by the choice.",
                    tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_DEFAULT_TARGET_UNSUPPORTED)

        # Look for flags specified by choice, collect specified targets from command-line arguments
        # and cross-validate with supported targets for the choice. Add to selected_targets set.
        selected_targets: set[Target] = set()
        target_members = Target.__members__
        reverse_target_map = {v.value: v for k, v in target_members.items()}
        for flag in choice.flags:
            target_names = collect_arg_list(args=args, flag=flag)
            if not target_names:
                continue  # No targets specified for this flag, skip to next flag
            for name in target_names:
                target_enum = reverse_target_map.get(name, None)
                if target_enum is None:
                    raise SimpleBenchValueError(
                        f"Unknown output target {name} specified for {flag}.",
                        tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_UNKNOWN_TARGET_IN_ARGS)
                if target_enum in choice.targets:
                    selected_targets.add(target_enum)
                else:
                    raise SimpleBenchValueError(
                        f"Output target {name} is not supported by {flag}.",
                        tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_UNSUPPORTED_TARGET)

        return set(default_targets) if not selected_targets else selected_targets

    def add_flags_to_argparse(self: ReporterProtocol, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        This is an interface method for adding flags of different types to an ArgumentParser.

        Choices can define different types of flags, such as boolean flags or
        flags that accept multiple values (lists). This method allows adding
        flags of the specified type to the ArgumentParser.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                "parser arg must be an argparse.ArgumentParser instance",
                tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE,
            )
        for choice in self.choices.values():
            match choice.flag_type:
                case FlagType.BOOLEAN:
                    self.add_boolean_flags_to_argparse(parser=parser, choice=choice)
                case FlagType.TARGET_LIST:
                    self.add_list_of_targets_flags_to_argparse(parser=parser, choice=choice)
                case _:
                    raise SimpleBenchValueError(
                        f"Unsupported flag type: {choice.flag_type}",
                        tag=ReporterErrorTag.ADD_FLAGS_UNSUPPORTED_FLAG_TYPE,
                    )

    def add_list_of_targets_flags_to_argparse(
        self: ReporterProtocol, parser: ArgumentParser, choice: Choice
    ) -> None:
        """Add a Choice's command-line flags to an ArgumentParser.

        This is a default implementation of adding flags that accept multiple
        values for each Choice's flags to specify the output targets for the reporter.

        Example:
            For a Choice with flags ['--json'], this method will add an argument
            to the parser that accepts multiple target values, like so:

            --json                             # default target
            --json console filesystem callback # multiple targets
            --json filesystem                  # single target

        Subclasses can override this method if they need custom behavior such as adding
        arguments with different types or more complex logic.

        The added argument will use the 'append' action to allow multiple occurrences
        of the flag, each potentially specifying multiple targets, and uses the choices
        option to restrict the allowed target values to only those supported by the Choice.

        This will be enforced during argument parsing, so invalid target values will
        result in an error.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
            choice (Choice): The Choice instance for which to add the flags.

        Raises:
            SimpleBenchTypeError: If the parser arg is not an ArgumentParser instance.
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                "parser arg must be an argparse.ArgumentParser instance",
                tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE,
            )
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "choice arg must be a Choice instance",
                tag=ReporterErrorTag.ADD_LIST_OF_TARGETS_FLAGS_INVALID_CHOICE_ARG_TYPE,
            )
        targets = [target.value for target in choice.targets]
        for flag in choice.flags:
            # Add an argument that accepts multiple target values
            # for each occurrence of the flag, restricts the choices
            # to only those supported by the Choice. Zero or more
            # targets can be specified for each flag occurrence.
            # Zero is allowed so that the default targets can be used
            # when no targets are explicitly specified.
            parser.add_argument(
                flag, action='append', nargs='*', choices=targets, help=choice.description
            )

    def add_boolean_flags_to_argparse(
        self: ReporterProtocol, parser: ArgumentParser, choice: Choice
    ) -> None:
        """Adds a Choice's command-line flags to an ArgumentParser.

        This is a default implementation that adds boolean flags for each Choice's flags.
        Subclasses can override this method if they need custom behavior such as
        adding arguments with different types or more complex logic.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
            choice (Choice): The Choice instance for which to add the flags.
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                "parser arg must be an argparse.ArgumentParser instance",
                tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE,
            )
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "choice arg must be a Choice instance",
                tag=ReporterErrorTag.ADD_BOOLEAN_FLAGS_INVALID_CHOICE_ARG_TYPE,
            )
        for flag in choice.flags:
            parser.add_argument(flag, action='store_true', help=choice.description)
