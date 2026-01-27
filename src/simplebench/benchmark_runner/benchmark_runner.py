"""Base class for all benchmarkrunners"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import VariationMarks
from simplebench.type_proxies import is_case, is_session

from ._error_tags import _RunnerErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case, Results
    from simplebench.session import Session


class BenchmarkRunner(ABC):
    """Base class for all benchmark runners"""

    @abstractmethod
    def __init__(
        self,
        *,
        case: Case,
        variation_marks: VariationMarks,
        session: Session | None = None,
        runner: Callable[..., Any] | None = None,
    ) -> None:
        """Initialize the runner with the given case, kwargs, session, and additional arguments"""
        raise NotImplementedError('Subclasses must implement the __init__ method')

    @abstractmethod
    def run(
        self,
        *,
        n: int | float,
        action: Callable[..., Any],
        setup: Callable[..., Any] | None = None,
        teardown: Callable[..., Any] | None = None,
        variation_marks: VariationMarks | None = None,
    ) -> Results:
        """Run the benchmark and return the results"""
        raise NotImplementedError('Subclasses must implement the run method')

    @property
    def case(self) -> Case:
        """Return the case for the benchmark.

        :return: The case for the benchmark.
        """
        return self._case

    @case.setter
    def case(self, value: Case) -> None:
        """Set the case for the benchmark.

        :param value: The new case for the benchmark.
        """
        if not is_case(value):
            raise SimpleBenchTypeError('case must be an instance of Case', tag=_RunnerErrorTag.NOT_A_CASE)
        self._case: Case = value

    @property
    def session(self) -> Session | None:
        """Return the session for the benchmark.

        :return: The session for the benchmark (if set).
        """
        return self._session

    @session.setter
    def session(self, value: Session | None) -> None:
        """Set the session for the benchmark.

        It is not necessary to set the session for a benchmark, but if it is set,
        it must be an instance of `Session`.

        :param value: The new session for the benchmark (if set).
        """
        if value is not None and not is_session(value):
            raise SimpleBenchValueError(
                'session must be an instance of Session or None', tag=_RunnerErrorTag.NOT_A_SESSION
            )
        self._session: Session | None = value

    @property
    def variation_marks(self) -> VariationMarks:
        """Return the keyworded arguments for the benchmark.

        :return: The keyworded arguments for the benchmark.
        """
        return self._variation_marks

    @variation_marks.setter
    def variation_marks(self, value: VariationMarks) -> None:
        """Set the keyworded arguments for the benchmark.

        :param value: The new keyworded arguments for the benchmark.
        """
        if not isinstance(value, VariationMarks):
            raise SimpleBenchTypeError(
                'varation_marks must be a VariationMarks instance',
                tag=_RunnerErrorTag.VARIATION_MARKS_NOT_A_VARIATION_MARKS,)
        self._variation_marks: VariationMarks = value if isinstance(
            value, VariationMarks) else VariationMarks(value)

