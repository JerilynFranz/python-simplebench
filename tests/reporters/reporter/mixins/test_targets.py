"""Tests for the _ReporterTargetMixin in reporter mixins."""
import pytest
from rich.table import Table
from rich.text import Text

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.reporter.exceptions import _ReporterErrorTag
from simplebench.validators.exceptions import _ValidatorsErrorTag

from ....factories import reporter_factory
from ....factories.reporter.reporter_methods import (
    target_callback_kwargs_factory,
    target_console_kwargs_factory,
    target_filesystem_kwargs_factory,
)
from ....kwargs.reporters.reporter.methods import (
    TargetCallbackMethodKWArgs,
    TargetConsoleMethodKWArgs,
    TargetFilesystemMethodKWArgs,
)
from ....testspec import TestAction, TestSpec, idspec


def target_filesystem_params_testspecs() -> list[TestSpec]:
    """Test specifications for parameter validation of the target_filesystem method.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = [
        idspec("PARAMS_001", TestAction(
            name="Valid parameters for target_filesystem method (no exceptions raised)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory(),
        )),
        idspec("PARAMS_002", TestAction(
            name="Invalid path parameter type (not a Path instance)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                path="not_a_path_instance"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_PATH_ARG_TYPE,
        )),
        idspec("PARAMS_003", TestAction(
            name="Invalid subdir parameter type (not a string)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                subdir=123),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_TYPE,
        )),
        idspec("PARAMS_004", TestAction(
            name="Invalid filename parameter type (not a string)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                filename=456),
            exception=SimpleBenchTypeError,
            exception_tag=_ValidatorsErrorTag.VALIDATE_FILENAME_INVALID_FILENAME_ARG_TYPE,
        )),
        idspec("PARAMS_005", TestAction(
            name="Invalid append parameter type (not a bool)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                append="not_a_bool"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_APPEND_ARG_TYPE,
        )),
        idspec("PARAMS_006", TestAction(
            name="Invalid unique parameter type (not a bool)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                unique="not_a_bool"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_UNIQUE_ARG_TYPE,
        )),
        idspec("PARAMS_007", TestAction(
            name="Both append and unique parameters set to True (incompatible)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                append=True,
                unique=True,
            ),
            exception=SimpleBenchValueError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS,
        )),
        idspec("PARAMS_008", TestAction(
            name="Both append and unique parameters set to False (incompatible)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                append=False,
                unique=False,
            ),
            exception=SimpleBenchValueError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS,
        )),
        idspec("PARAMS_009", TestAction(
            name="append parameter is True, unique is False (valid)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                append=True,
                unique=False,
            ),
        )),
        idspec("PARAMS_010", TestAction(
            name="unique parameter is True, append is False (valid)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                append=False,
                unique=True,
            ),
        )),
        idspec("PARAMS_011", TestAction(
            name="Valid parameters with different str output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                output="This is a string output.",
            ),
        )),
        idspec("PARAMS_012", TestAction(
            name="Valid parameters with bytes output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                output=b"This is a bytes output.",
            ),
        )),
        idspec("PARAMS_013", TestAction(
            name="Valid parameters with Text output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                output=Text("This is a Rich Text output."),
            ),
        )),
        idspec("PARAMS_014", TestAction(
            name="Valid parameters with Table output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                output=Table(title="This is a Rich Table output."),
            ),
        )),
        idspec("PARAMS_015", TestAction(
            name="Invalid output parameter type (not str, bytes, Text, or Table)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(
                output=12345,
            ),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_OUTPUT_ARG_TYPE,
        )),
    ]

    return testspecs


@pytest.mark.parametrize("testspec", target_filesystem_params_testspecs())
def test_target_filesystem_params(testspec: TestSpec):
    """Tests for parameter validation of the target_filesystem method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
