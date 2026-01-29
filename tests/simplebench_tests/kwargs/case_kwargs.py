"""simplebench.cases.Case KWArgs package for SimpleBench tests."""

from collections.abc import Callable, Iterable, Sequence

from simplebench_tests.kwargs.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

import simplebench.vcs as vcs
from simplebench.benchmark_runner import SimpleRunner
from simplebench.case import Case
from simplebench.case.function_runner import FunctionRunner
from simplebench.reporters.protocols import ReporterCallback
from simplebench.options.reporter.options import ReporterOptions
from simplebench.simplebench_types import ElementCollection


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
        self,
        *,
        benchmark_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
        vcs_info: vcs.VCSInfo | NoDefaultValue = NO_DEFAULT_VALUE,
        action: FunctionRunner | NoDefaultValue = NO_DEFAULT_VALUE,
        group: str | NoDefaultValue = NO_DEFAULT_VALUE,
        title: str | NoDefaultValue = NO_DEFAULT_VALUE,
        description: str | NoDefaultValue = NO_DEFAULT_VALUE,
        iterations: int | NoDefaultValue = NO_DEFAULT_VALUE,
        warmup_iterations: int | NoDefaultValue = NO_DEFAULT_VALUE,
        rounds: int | NoDefaultValue = NO_DEFAULT_VALUE,
        timer: Callable[[], int] | NoDefaultValue = NO_DEFAULT_VALUE,
        cpu_timer: Callable[[], int] | NoDefaultValue = NO_DEFAULT_VALUE,
        min_time: float | NoDefaultValue = NO_DEFAULT_VALUE,
        max_time: float | NoDefaultValue = NO_DEFAULT_VALUE,
        timeout: float | NoDefaultValue = NO_DEFAULT_VALUE,
        variation_cols: dict[str, str] | NoDefaultValue = NO_DEFAULT_VALUE,
        kwargs_variations: dict[str, ElementCollection] | NoDefaultValue = NO_DEFAULT_VALUE,
        runners: Sequence[type[SimpleRunner]] | NoDefaultValue = NO_DEFAULT_VALUE,
        callback: ReporterCallback | NoDefaultValue = NO_DEFAULT_VALUE,
        options: Iterable[ReporterOptions] | NoDefaultValue = NO_DEFAULT_VALUE,
        node: str | NoDefaultValue = NO_DEFAULT_VALUE,
    ) -> None:
        """Constructs a CaseKWArgs instance. This class is used to hold keyword arguments for
        initializing a Case instance in tests.

                :param benchmark_id: An optional unique identifier for the benchmark case.

            If None, a transient ID is assigned. This is meant to provide a stable identifier for the
            benchmark case across multiple runs for tracking purposes. If not provided,
            an attempt will be made to generate a stable ID based on the the action function
            name, signature, and group. If that is not possible, a transient ID based
            on the instance's id() will be used. If a transient ID is used, it will differ
            between runs and cannot be used to correlate results across multiple runs.

            Benchmark ids must be unique within a benchmarking session and stable across runs
            or they cannot be used for tracking benchmark results over time.
        :param vcs_info: An optional vcs.VCSInfo instance representing the state of the VCS repository.

            If not provided, the vcs.VCSInfo will be automatically retrieved from the current
            context of the caller if the code is part of a VCS repository.
        :param action: The function to perform the benchmark.

            This function must accept a `bench` instance of type BenchmarkRunner and
            arbitrary keyword arguments ('**kwargs'). See the ``FunctionRunner``
            protocol for the exact signature required. It must return a `Results` object.
        :param group: The benchmark reporting group to which the benchmark case belongs.

            Benchmarks with the same group can be selected for execution without running
            other benchmarks. If not specified, the default group 'default' is used.
        :param title: The title of the benchmark case.

            If None, the name of the action function will be used. Cannot be blank.
        :param description: A brief description of the benchmark case.

            If None, the docstring of the action function will be used, or
            '(no description)' if no docstring is available. Cannot be blank.
        :param iterations: The minimum number of iterations to run for the benchmark.
        :param warmup_iterations: The number of warmup iterations to run before the benchmark.
        :param rounds: The number of rounds to run for the benchmark.

            Rounds are multiple runs of calls to the action within an iteration to mitigate timer
            quantization, loop overhead, and other measurement effects for very fast actions. Setup and teardown
            functions are called only once per iteration (all rounds in the same iteration share the same
            setup/teardown context).

            If None, rounds will be auto-calibrated based on the precision and overhead of the timer function
            and the expected execution time of the action. If the action is very fast (e.g., under
            10 microseconds), rounds will be set to a higher value to improve measurement accuracy
            with the goal of reducing timer quantization errors. If the action is slower, rounds
            will be set lower values.

            If specified, it must be a positive integer.
        :param timer: The timer function to use for the benchmark. If None, the default timer
            from the Session() (if set) or from `simplebench.defaults.DEFAULT_TIMER` ({DEFAULT_TIMER})
            is used by benchmark runners that require a timer.

            The timer function should be a callable that returns a float or int representing the current time.
        :param cpu_timer: The CPU timer function to use for the benchmark. If None, the default CPU timer
            from the Session() (if set) or from `simplebench.defaults.DEFAULT_CPU_TIMER` ({DEFAULT_CPU_TIMER})
            is used by benchmark runners that require a CPU timer.

            The CPU timer function should be a callable that returns a float or int representing the current CPU time.
        :param min_time: The minimum time for the benchmark to run in seconds. Its reference depends on the timer used,
            but by default it is wall-clock time.
        :param max_time: The maximum time for the benchmark run in seconds. Its reference depends on the timer used,
            but by default it is wall-clock time.
        :param timeout: How long to wait before timing out a benchmark run (in seconds). It is
            measured as wall-clock time.

            If None, it waits the full duration of ``max_time`` plus the default timeout grace period
            ({DEFAULT_TIMEOUT_GRACE_PERIOD} seconds). It must be a positive float or int that is greater
            than ``max_time`` if provided. This is a safety mechanism to prevent runaway benchmarks.

            If the timeout is reached during a run, a :class:`~simplebench.exceptions.SimpleBenchTimeoutError``
            will be raised, and the benchmark case's state to TIMED_OUT.
        :param variation_cols: kwargs to be used for cols to denote kwarg variations.

            Each key is a keyword argument name, and the value is the column label to use for that
            argument. Only keywords that are also in `kwargs_variations` can be used here. These
            fields will be added to the output of reporters that support them as columns of data
            with the specified labels.

            If None, an empty dict is used.
        :param kwargs_variations: A map of keyword argument names to a list of possible values for that argument.

            Default is {}. When tests are run, the benchmark
            will be executed for each combination of the specified keyword argument variations. The action
            function will be called with a `bench` parameter that is an instance of the runner and the
            keyword arguments for the current variation.
            If None, an empty dict is used.

            kwargs_variation values can be of any type, including types that are not easily serializable.
            To handle this situation, the `Mark` class can be used to create standardized marks that
            can be used to represent these variations in results and reports.

            .. code-block:: python3
              :caption: Using Marks for Variation Representation

                from simplebench.case import Case, Mark, Results
                from simplebench.benchmark_runner import SimpleRunner


                def my_benchmark_action(_bench: SimpleRunner, mode: str) -> Results:
                    # Benchmark action implementation
                    pass


                case = Case(
                    action=my_benchmark_action, kwargs_variations={'mode': [Mark('ModeA', 1), Mark('ModeB', 2)]}
                )

        :param runners: A list of runners for the benchmark.

            Any runner classes must be a subclass of BenchmarkRunner and must have a method
            named `run` that accepts the same parameters as BenchmarkRunner.run and returns a Results object.
            The action function will be called with a `bench` parameter that is an instance of the
            custom runner.

            It may also accept additional parameters to the run method as needed. If additional
            parameters are needed for the custom runner, they will need to be passed to the run
            method as keyword arguments.

            No support is provided for passing additional parameters to a custom runner from the @benchmark
            decorator.

            If None, the default SimpleRunner will be used. If multiple runners are specified,
            the benchmark will be run for each runner, and the results will be combined.

        :param callback: A callback function for additional processing of the report.

            The function should must four arguments: the Case instance, the Metric,
            the Format, and the generated report data.

            - case (Case): The `Case` instance processed for the report.
            - metric (Metric): The `Metric` of the report.
            - output_format (Format): The `Format` of the report.
            - output (Any): The generated report data. Note that the actual type of this data will
                depend on the Format specified for the report and the type generated by the
                reporter for that Format

            Omit if no callback is needed by a reporter.
        :param options: A list of additional options for the benchmark case.

            Each option is an instance of ReporterOption or a subclass of ReporterOption.
            Reporter options can be used to customize the output of the benchmark reports for
            specific reporters. Reporters are responsible for extracting applicable ReporterOptions
            from the list of options themselves.
            If None, an empty list is used.
        :param node: An optional identifier for the node where the benchmark is run.
            This can be used in distributed benchmarking scenarios to identify
            the source of the benchmark data. If None, the actual node name
            from the environment will be used. Default is '' for privacy and
            security reasons.
        """
        super().__init__(call=Case.__init__, kwargs=locals())
