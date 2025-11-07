"""Tests for the register_reporter decorator."""
from argparse import Namespace

from pathlib import Path

import pytest

from tests.factories import reporter_kwargs_factory


from simplebench.case import Case
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.choice import ChoiceConf, Choice
from simplebench.session import Session

from simplebench.reporters.reporter_manager.decorators import (
    register_reporter, get_registered_reporters, clear_registered_reporters, RegisterReporterErrorTag)


class MockReporterOptions(ReporterOptions):
    """A mock ReporterOptions subclass for testing purposes."""


class MockReporter(Reporter):
    """A mock reporter subclass for testing purposes."""
    def __init__(self, name: str = 'mock') -> None:
        super().__init__(**reporter_kwargs_factory(cache_id=None))

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None) -> None:
        """A mock run_report method."""
        self.render_by_section(  # pragma: no cover
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """A mock render method."""
        return "Mock Report"  # pragma: no cover


def test_register_reporter():
    """Test the register_reporter decorator."""

    @register_reporter
    class TestReporter(MockReporter):  # pylint: disable=unused-variable
        """A test reporter subclass for testing purposes."""

    registered_reporters = get_registered_reporters()
    assert len(registered_reporters) == 1, (
        "REGISTER_001 - There should be exactly one registered reporter.")
    reporter = registered_reporters.pop()
    assert isinstance(reporter, TestReporter), (
        f"REGISTER_002 - The registered reporter should be an instance of TestReporter, got {reporter}.")

    clear_registered_reporters()
    assert len(get_registered_reporters()) == 0, (
        "REGISTER_003 - Registered reporters should have been cleared (they were not).")


def test_register_reporter_invalid_type():
    """Test that registering an invalid reporter type raises an error."""
    with pytest.raises(Exception) as exc_info:

        @register_reporter  # type: ignore
        class InvalidReporter:  # pylint: disable=unused-variable
            """An invalid reporter that does not inherit from Reporter."""

    assert exc_info.type.__name__ == "SimpleBenchTypeError", (
        f"REGISTER_004 - Expected SimpleBenchTypeError, got {exc_info.type.__name__}.")
    if hasattr(exc_info.value, 'tag_code'):
        error_tag = getattr(exc_info.value, 'tag_code')
        assert error_tag == RegisterReporterErrorTag.INVALID_REPORTER_TYPE_ARG, (
            f"REGISTER_005 - Expected tag INVALID_REPORTER_TYPE_ARG, got {error_tag}.")
    else:
        pytest.fail("REGISTER_006 - Exception does not have a 'tag_code' attribute.")
