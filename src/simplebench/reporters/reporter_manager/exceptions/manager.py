"""ErrorTags for reporter_manager module in simplebench.reporters."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class ReporterManagerErrorTag(ErrorTag):
    """ErrorTags for the ReporterManager class."""
    REGISTER_INVALID_REPORTER_ARG = "REGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the ReporterManager.register() method"""
    REGISTER_INVALID_CHOICES_RETURNED = "REGISTER_INVALID_CHOICES_RETURNED"
    """Something other than a Choices instance was returned from the reporter.choices property"""
    REGISTER_INVALID_CHOICES_CONTENT = "REGISTER_INVALID_CHOICES_CONTENT"
    """Something other than a Choice instance was found in the Choices instance returned
    from the reporter.choices property"""
    REGISTER_DUPLICATE_NAME = "REGISTER_DUPLICATE_NAME"
    """A Reporter with the same name already exists in the ReporterManager instance"""
    REGISTER_DUPLICATE_CLI_ARG = "REGISTER_DUPLICATE_CLI_ARG"
    """A Reporter with the same CLI argument already exists in the ReporterManager instance"""
    UNREGISTER_INVALID_REPORTER_ARG = "UNREGISTER_INVALID_REPORTER_ARG"
    """Something other than a Reporter instance was passed to the ReporterManager.unregister() method"""
    UNREGISTER_UNKNOWN_NAME = "UNREGISTER_UNKNOWN_NAME"
    """No Reporter with the given name is registered in the ReporterManager instance"""
    ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG = "ADD_REPORTERS_TO_ARGPARSE_INVALID_PARSER_ARG"
    """Something other than an ArgumentParser instance was passed to the
    ReporterManager.add_reporters_to_argparse() method"""
    ARGUMENT_ERROR_ADDING_FLAGS = "ARGUMENT_ERROR_ADDING_FLAGS"
    """An ArgumentError was raised when adding reporter flags to the ArgumentParser instance"""
