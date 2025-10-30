"""simplebench.cases.Case KWArgs package for SimpleBench tests."""
from __future__ import annotations
import inspect
from typing import Any, TYPE_CHECKING

from tests.kwargs.helpers import NoDefaultValue

if TYPE_CHECKING:
    from simplebench.runners import SimpleRunner
    from simplebench.protocols import ActionRunner
    from simplebench.reporters.reporter.options import ReporterOptions
    from simplebench.reporters.protocols import ReporterCallback


class CaseKWArgs(dict):
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
            group: str | NoDefaultValue = NoDefaultValue(),
            title: str | NoDefaultValue = NoDefaultValue(),
            description: str | NoDefaultValue = NoDefaultValue(),
            action: ActionRunner | NoDefaultValue = NoDefaultValue(),
            iterations: int | NoDefaultValue = NoDefaultValue(),
            warmup_iterations: int | NoDefaultValue = NoDefaultValue(),
            rounds: int | NoDefaultValue = NoDefaultValue(),
            min_time: float | NoDefaultValue = NoDefaultValue(),
            max_time: float | NoDefaultValue = NoDefaultValue(),
            variation_cols: dict[str, str] | NoDefaultValue = NoDefaultValue(),
            kwargs_variations: dict[str, list[Any]] | NoDefaultValue = NoDefaultValue(),
            runner: type[SimpleRunner] | NoDefaultValue = NoDefaultValue(),
            callback: ReporterCallback | NoDefaultValue = NoDefaultValue(),
            options: list[ReporterOptions] | NoDefaultValue = NoDefaultValue()
    ) -> None:
        """Constructs a CaseKWArgs instance. This class is used to hold keyword arguments for
        initializing a Case instance in tests.

        Args:
            group (str): The benchmark reporting group to which the benchmark case belongs.
            title (str): The name of the benchmark case.
            description (str): A brief description of the benchmark case.
            action (ActionRunner): The function to perform the benchmark. This function must
                accept a `bench` parameter of type SimpleRunner and arbitrary keyword arguments ('**kwargs').
                It must return a Results object.
            iterations (int): The minimum number of iterations to run for the benchmark. (default: 20)
            warmup_iterations (int): The number of warmup iterations to run before the benchmark. (default: 10)
            rounds (int): The number of test rounds that will be run by the action on each iteration. (default: 1)
            min_time (float): The minimum time for the benchmark in seconds. (default: 5.0)
            max_time (float): The maximum time for the benchmark in seconds. (default: 20.0)
            variation_cols (dict[str, str]): kwargs to be used for cols to denote kwarg variations.
                Each key is a keyword argument name, and the value is the column label to use for that argument.

                .. code-block:: python
                    # example of variation_cols
                    variation_cols={
                        'search_depth': 'Search Depth',
                        'runtime_validation': 'Runtime Validation'
                    }
            kwargs_variations (dict[str, list[Any]]):
                Variations of keyword arguments for the benchmark.
                Each key is a keyword argument name, and the value is a list of possible values.

                .. code-block:: python
                    # example of kwargs_variations
                    kwargs_variations={
                        'search_depth': [1, 2, 3],
                        'runtime_validation': [True, False]
                    }
            runner (Optional[SimpleRunner]): A custom runner for the benchmark.
                If None, the default SimpleRunner is used. (default: None)

                The custom runner must be a subclass of SimpleRunner and must have a method
                named `run` that accepts the same parameters as SimpleRunner.run and returns a Results object.

                The action function will be called with a `bench` parameter that is an instance of the
                custom runner.

                It may also accept additional parameters to the run method as needed. If additional
                parameters are needed for the custom runner, they will need to be passed to the run
                method from the action function when using a directly defined Case.

                No support is provided for passing additional parameters to a custom runner from the @benchmark
                decorator.

            callback (ReporterCallback):
                A callback function for additional processing of the report. The function should accept
                four arguments: the Case instance, the Section, the Format, and the generated report data.
                Leave as None if no callback is needed. (default: None)

                The callback function will be called with the following arguments:
                    case (Case): The `Case` instance processed for the report.
                    section (Section): The `Section` of the report.
                    output_format (Format): The `Format` of the report.
                    output (Any): The generated report data. Note that the actual type of this data will
                        depend on the Format specified for the report and the type generated by the
                        reporter for that Format
            options (list[ReporterOptions]): A list of additional options for the benchmark case.

                Each option is an instance of ReporterOptions or a subclass of ReporterOptions.
                Reporter options can be used to customize the output of the benchmark reports for
                specific reporters. Reporters are responsible for extracting applicable ReporterOptionss
                from the list of options themselves.
        """
        kwargs_sig = inspect.signature(self.__init__)  # type: ignore[misc]
        params = set(kwargs_sig.parameters.keys()) - {'self'}
        kwargs: dict[str, Any] = {}
        for key in params:
            value = locals()[key]
            if not isinstance(value, NoDefaultValue):
                kwargs[key] = value
        super().__init__(**kwargs)
