"""Test simplebench/reporters/interfaces.py module"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Callable, Optional

import pytest

from simplebench.case import Case
from simplebench.enums import Section, Target, Format
from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchValueError, SimpleBenchTypeError, ErrorTag
from simplebench.reporters.choices import Choice, Choices
from simplebench.reporters.interfaces import Reporter
from simplebench.session import Session

from .testspec import TestAction, TestSetGet, TestSpec, idspec


class DummyReporter(Reporter):
    """A dummy Reporter subclass for testing purposes."""
    def __init__(self) -> None:
        super().__init__(
            name='dummy',
            description='A dummy reporter for testing.',
            sections={Section.OPS, Section.TIMING},
            targets={Target.CONSOLE, Target.FILESYSTEM},
            formats={Format.RICH_TEXT},
            choices=self._load_choices())

    def _load_choices(self) -> Choices:
        """Load the Choices instance for the reporter, including sections, output targets, and formats."""
        choices: Choices = Choices()
        choices.add(
            Choice(
                reporter=self,
                flags=['--dummy'],
                name='dummy',
                description='dummy choice',
                sections=[Section.OPS, Section.TIMING],
                targets=[Target.CONSOLE, Target.FILESYSTEM],
                formats=[Format.RICH_TEXT],
                extra=None)
        )
        return choices

    def run_report(self,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[Callable[[Case, Section, Format, Any], None]] = None) -> None:
        return super().run_report(case=case,
                                  choice=choice,
                                  path=path,
                                  session=session,
                                  callback=callback)


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_001', TestAction(
        name="abstract base class Reporter() cannot be instantiated directly",
        action=Reporter,
        exception=TypeError)),
    idspec('REPORTER_002', TestAction(
        name="configured subclass of Reporter() can be instantiated",
        action=DummyReporter,
        validate_result=lambda result: isinstance(result, DummyReporter))),
])
def test_reporter_class(testspec: TestSpec) -> None:
    """Test Reporter class"""
    testspec.run()
