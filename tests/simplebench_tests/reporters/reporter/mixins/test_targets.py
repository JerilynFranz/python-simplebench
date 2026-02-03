"""Tests for the _ReporterTargetMixin in reporter mixins."""
import autopypath  # noqa: F401
import pytest
from rich.table import Table
from rich.text import Text
from simplebench_tests.factories import reporter_factory
from simplebench_tests.factories.reporter.reporter_methods import (
    target_filesystem_kwargs_factory,
)

# from ....kwargs.reporters.reporter.methods import (
#      TargetCallbackMethodKWArgs,
#      TargetConsoleMethodKWArgs,
#      TargetFilesystemMethodKWArgs,
# )
from testspec import PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.reporter._error_tags import _ReporterErrorTag
from simplebench.validators._error_tags import _ValidatorsErrorTag


def target_filesystem_params_testspecs() -> list[TestSpec]:
    """Test specifications for parameter validation of the target_filesystem method.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = [
        PytestAction("PARAMS_001",
            name="Valid parameters for target_filesystem method (no exceptions raised)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory(),
        ),
        PytestAction("PARAMS_002",
            name="Invalid path parameter type (not a Path instance)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(path="not_a_path_instance"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_PATH_ARG_TYPE,
        ),
        PytestAction("PARAMS_003",
            name="Invalid subdir parameter type (not a string)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(subdir=123),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_TYPE,
        ),
        PytestAction("PARAMS_004",
            name="Invalid filename parameter type (not a string)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(filename=456),
            exception=SimpleBenchTypeError,
            exception_tag=_ValidatorsErrorTag.VALIDATE_FILENAME_INVALID_FILENAME_ARG_TYPE,
        ),
        PytestAction("PARAMS_005",
            name="Invalid append parameter type (not a bool)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(append="not_a_bool"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_APPEND_ARG_TYPE,
        ),
        PytestAction("PARAMS_006",
            name="Invalid unique parameter type (not a bool)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(unique="not_a_bool"),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_UNIQUE_ARG_TYPE,
        ),
        PytestAction("PARAMS_007",
            name="Both append and unique parameters set to True (incompatible)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(append=True, unique=True),
            exception=SimpleBenchValueError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS,
        ),
        PytestAction("PARAMS_008",
            name="Both append and unique parameters set to False (incompatible)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(append=False, unique=False),
            exception=SimpleBenchValueError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS,
        ),
        PytestAction("PARAMS_009",
            name="append parameter is True, unique is False (valid)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(append=True, unique=False),
        ),
        PytestAction("PARAMS_010",
            name="unique parameter is True, append is False (valid)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(append=False, unique=True),
        ),
        PytestAction("PARAMS_011",
            name="Valid parameters with different str output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(output="This is a string output."),
        ),
        PytestAction("PARAMS_012",
            name="Valid parameters with bytes output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(output=b"This is a bytes output."),
        ),
        PytestAction("PARAMS_013",
            name="Valid parameters with Text output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(output=Text("This is a Rich Text output.")),
        ),
        PytestAction("PARAMS_014",
            name="Valid parameters with Table output type",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(output=Table(title="This is a Rich Table output.")),
        ),
        PytestAction("PARAMS_015",
            name="Invalid output parameter type (not str, bytes, Text, or Table)",
            action=reporter_factory().target_filesystem,
            kwargs=target_filesystem_kwargs_factory().replace(output=12345),
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.TARGET_FILESYSTEM_INVALID_OUTPUT_ARG_TYPE,
        ),
    ]

    return testspecs


@pytest.mark.parametrize("testspec", target_filesystem_params_testspecs())
def test_target_filesystem_params(testspec: TestSpec) -> None:
    """Tests for parameter validation of the target_filesystem method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
