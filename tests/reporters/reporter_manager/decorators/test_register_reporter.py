"""Tests for the register_reporter decorator."""
from argparse import Namespace
from pathlib import Path
from typing import Any, ClassVar

import pytest

from simplebench.case import Case
from simplebench.enums import Section
from simplebench.reporters.choice import Choice
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.reporter_manager.decorators import (
    RegisterReporterErrorTag,
    clear_registered_reporters,
    get_registered_reporters,
    register_reporter,
)
from simplebench.session import Session

from ....factories import reporter_config_kwargs_factory, reporter_config_factory


class MockReporterOptions(ReporterOptions):
    """A mock ReporterOptions subclass for testing purposes."""


class MockReporter(Reporter):
    """A mock reporter subclass for testing purposes."""
    _OPTIONS_TYPE: ClassVar[type[MockReporterOptions]] = MockReporterOptions  # pylint: disable=line-too-long  # type: ignore[reportInvalidVariableOverride]  # noqa: E501
    """The ReporterOptions subclass type for the reporter: `MockReporterOptions`"""
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}
    """Keyword arguments for constructing a MockReporterOptions hardcoded default instance: `{}`"""

    def __init__(self, name: str = 'mock') -> None:
        config = reporter_config_factory(**reporter_config_kwargs_factory(name=name))
        super().__init__(config)

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None) -> None:
        """A mock run_report method.

        :param args: The command-line arguments.
        :type args: Namespace
        :param case: The benchmark case.
        :type case: Case
        :param choice: The reporter choice.
        :type choice: Choice
        :param path: The output path.
        :type path: Path | None
        :param session: The benchmark session.
        :type session: Session | None
        :param callback: The reporter callback.
        :type callback: ReporterCallback | None
        """
        self.render_by_section(  # pragma: no cover
            renderer=self.render,
            args=args,
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """A mock render method.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: A mock report.
        :rtype: str
        """
        return "Mock Report"  # pragma: no cover


def test_register_reporter() -> None:
    """Test the register_reporter decorator."""

    class TestReporterOptions(MockReporterOptions):
        """A mock ReporterOptions subclass for testing purposes."""

    @register_reporter
    class TestReporter(MockReporter):  # pylint: disable=unused-variable
        """A test reporter subclass for testing purposes."""

        _OPTIONS_TYPE: ClassVar[type[TestReporterOptions]] = TestReporterOptions  # pylint: disable=line-too-long  # type: ignore[reportInvalidVariableOverride]  # noqa: E501
        """The ReporterOptions subclass type for the reporter: `TestReporterOptions`"""
        _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}
        """Keyword arguments for constructing a TestReporterOptions hardcoded default instance: `{}`"""

        def run_report(self,
                       *,
                       args: Namespace,
                       case: Case,
                       choice: Choice,
                       path: Path | None = None,
                       session: Session | None = None,
                       callback: ReporterCallback | None = None) -> None:
            """A mock run_report method.

            :param args: The command-line arguments.
            :type args: Namespace
            :param case: The benchmark case.
            :type case: Case
            :param choice: The reporter choice.
            :type choice: Choice
            :param path: The output path.
            :type path: Path | None
            :param session: The benchmark session.
            :type session: Session | None
            :param callback: The reporter callback.
            :type callback: ReporterCallback | None
            """
            self.render_by_section(  # pragma: no cover
                renderer=self.render,
                args=args,
                case=case,
                choice=choice,
                path=path,
                session=session,
                callback=callback)

        def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
            """A mock render method.

            :param case: The benchmark case.
            :type case: Case
            :param section: The report section.
            :type section: Section
            :param options: The reporter options.
            :type options: ReporterOptions
            :return: A mock report.
            :rtype: str
            """
            return "Mock Report"  # pragma: no cover

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
