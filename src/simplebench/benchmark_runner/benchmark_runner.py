"""Base class for all benchmarkrunners"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.type_proxies import is_case, is_session

from ._error_tags import _RunnerErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.case.results import Results
    from simplebench.metrics import Metric
    from simplebench.session import Session


class BenchmarkRunner(ABC):
    """Base class for all benchmark runners"""

    @abstractmethod
    def __init__(self,
                 *,
                 case: Case,
                 kwargs: dict[str, Any],
                 session: Session | None = None,
                 runner: Callable[..., Any] | None = None) -> None:
        """Initialize the runner with the given case, kwargs, session, and additional arguments"""
        raise NotImplementedError("Subclasses must implement the __init__ method")

    @abstractmethod
    def run(self,
            *,
            n: int | float,
            action: Callable[..., Any],
            setup: Callable[..., Any] | None = None,
            teardown: Callable[..., Any] | None = None,
            kwargs: dict[str, Any] | None = None) -> Results:
        """Run the benchmark and return the results"""
        raise NotImplementedError("Subclasses must implement the run method")

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
            raise SimpleBenchTypeError(
                "case must be an instance of Case",
                tag=_RunnerErrorTag.NOT_A_CASE)
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
                "session must be an instance of Session or None",
                tag=_RunnerErrorTag.NOT_A_SESSION)
        self._session: Session | None = value

    @property
    def kwargs(self) -> dict[str, Any]:
        """Return the keyworded arguments for the benchmark.

        :return: The keyworded arguments for the benchmark.
        """
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value: dict[str, Any]) -> None:
        """Set the keyworded arguments for the benchmark.

        :param value: The new keyworded arguments for the benchmark.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                "kwargs must be a dictionary",
                tag=_RunnerErrorTag.KWARGS_NOT_A_DICT)
        self._kwargs: dict[str, Any] = value

    @property
    def variation_marks(self) -> dict[str, Any]:
        """Return the variation marks for the benchmark.

        The variation marks are defined by the :attr:`~.case.Case.variation_cols`
        and the current keyworded arguments to the function being benchmarked.

        The variation marks identify the specific variations being tested in a run
        from the kwargs values.

        :return: The variation marks for the benchmark.
        """
        return {key: self.kwargs.get(key, None) for key in self.case.variation_cols.keys()}

    @variation_marks.setter
    def variation_marks(self, value: dict[str, Any]) -> None:
        """Set the variation marks for the benchmark.

        :param value: The new variation marks for the benchmark.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                "variation_marks must be a dictionary",
                tag=_RunnerErrorTag.VARIATION_MARKS_NOT_A_DICT)
