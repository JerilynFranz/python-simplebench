"""simplebench.cases.Case KWArgs package for SimpleBench tests."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable

from simplebench.case import Case
from simplebench.vcs import GitInfo

from .kwargs import KWArgs, NoDefaultValue

if TYPE_CHECKING:
    from simplebench.protocols import ActionRunner
    from simplebench.reporters.protocols import ReporterCallback
    from simplebench.reporters.reporter.options import ReporterOptions
    from simplebench.runners import SimpleRunner


class CaseKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Case instance.

    This class is primarily used to facilitate testing of the Case class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Case class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self, *,
            benchmark_id: str | NoDefaultValue = NoDefaultValue(),
            git_info: GitInfo | NoDefaultValue = NoDefaultValue(),
            group: str | NoDefaultValue = NoDefaultValue(),
            title: str | NoDefaultValue = NoDefaultValue(),
            description: str | NoDefaultValue = NoDefaultValue(),
            action: ActionRunner | NoDefaultValue = NoDefaultValue(),
            iterations: int | NoDefaultValue = NoDefaultValue(),
            warmup_iterations: int | NoDefaultValue = NoDefaultValue(),
            rounds: int | NoDefaultValue = NoDefaultValue(),
            min_time: float | NoDefaultValue = NoDefaultValue(),
            max_time: float | NoDefaultValue = NoDefaultValue(),
            timeout: float | NoDefaultValue = NoDefaultValue(),
            variation_cols: dict[str, str] | NoDefaultValue = NoDefaultValue(),
            kwargs_variations: dict[str, list[Any]] | NoDefaultValue = NoDefaultValue(),
            runner: type[SimpleRunner] | NoDefaultValue = NoDefaultValue(),
            callback: ReporterCallback | NoDefaultValue = NoDefaultValue(),
            options: Iterable[ReporterOptions] | NoDefaultValue = NoDefaultValue()
    ) -> None:
        """Constructs a CaseKWArgs instance. This class is used to hold keyword arguments for
        initializing a Case instance in tests.

        :param benchmark_id: The unique identifier for the benchmark case.
        :type benchmark_id: str
        :param git_info: The GitInfo instance containing version control information.
                         If None, no git information is set.
        :type git_info: GitInfo | None
        :param group: The benchmark reporting group to which the benchmark case belongs.
        :type group: str
        :param title: The name of the benchmark case.
        :type title: str
        :param description: A brief description of the benchmark case.
        :type description: str
        :param action: The function to perform the benchmark. This function must
                       accept a `bench` parameter of type SimpleRunner and arbitrary keyword arguments ('**kwargs').
                       It must return a Results object.
        :type action: ActionRunner
        :param iterations: The minimum number of iterations to run for the benchmark. (default: 20)
        :type iterations: int
        :param warmup_iterations: The number of warmup iterations to run before the benchmark. (default: 10)
        :type warmup_iterations: int
        :param rounds: The number of test rounds that will be run by the action on each iteration. (default: 1)
        :type rounds: int
        :param min_time: The minimum time for the benchmark in seconds. (default: 5.0)
        :type min_time: float
        :param max_time: The maximum time for the benchmark in seconds. (default: 20.0)
        :type max_time: float
        :param timeout: The timeout interval in seconds for each benchmark. (default: None)
        :type timeout: float | None
        :param variation_cols: kwargs to be used for cols to denote kwarg variations.
                               Each key is a keyword argument name, and the value is the column label to use
                               for that argument.
        :type variation_cols: dict[str, str]
        :param kwargs_variations: Variations of keyword arguments for the benchmark.
                                  Each key is a keyword argument name, and the value is a list of possible values.
        :type kwargs_variations: dict[str, list[Any]]
        :param runner: A custom runner for the benchmark.
                       If None, the default SimpleRunner is used. (default: None)
        :type runner: type[SimpleRunner] | None
        :param callback: A callback function for additional processing of the report. The function should accept
                         four arguments: the Case instance, the Section, the Format, and the generated report data.
                         Leave as None if no callback is needed. (default: None)
        :type callback: ReporterCallback | None
        :param options: An iterable of additional options for the benchmark case.
        :type options: Iterable[ReporterOptions]
        """
        super().__init__(call=Case.__init__, kwargs=locals())
