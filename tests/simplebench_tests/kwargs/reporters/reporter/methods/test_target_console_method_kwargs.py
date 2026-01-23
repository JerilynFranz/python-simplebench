"""Tests for TargetConsoleMethodKWArgs."""
import pytest

from simplebench.reporters.reporter import Reporter as _MODELED_CLASS

from .....kwargs import kwargs_class_matches_modeled_call
from .....testspec import Assert, TestAction, TestSpec, idspec
from .target_console_method_kwargs import TargetConsoleMethodKWArgs as _KWARGS_CLASS

_MODELED_CALL = _MODELED_CLASS.target_console


def target_console_method_kwargs_testspecs() -> list[TestSpec]:
    """Generates TestSpecs for testing TargetConsoleMethodKWArgs.

    :return: A list of TestSpec instances for testing TargetConsole  MethodKWArgs.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = [
        idspec("KWARGS_001", TestAction(
            name="Validate KWArgs subclass signature vs modeled call (no exception)",
            action=kwargs_class_matches_modeled_call,
            kwargs={
                'kwargs_class': _KWARGS_CLASS,
                'modeled_call': _MODELED_CALL,
            })),
        idspec("KWARGS_002", TestAction(
            name="Instantate KWArgs subclass default instance",
            action=_KWARGS_CLASS,
            assertion=Assert.ISINSTANCE,
            expected=_KWARGS_CLASS))
    ]

    return testspecs


@pytest.mark.parametrize("testspec", target_console_method_kwargs_testspecs())
def test_target_console_method_kwargs(testspec: TestSpec):
    """Tests for TargetConsoleMethodKWArgs."""
    testspec.run()
