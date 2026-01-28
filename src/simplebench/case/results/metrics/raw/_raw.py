"""Raw data metric implementation."""
from simplebench.metrics import Metric
from simplebench.report.versions import v1 as reports
from simplebench.simplebench_types import Values

from . import _validate

class Raw:
    """Generic container for raw data from a benchmark.

    :ivar Metric metric: The metric definition for the benchmark. (read only)
    :ivar int iterations: The total number of iterations represented by the data points. (read only)
    :ivar int rounds: The number of rounds each data point represents. (read only)
    :ivar Values data: Tuple of floating point data points. (read only)
    :itype data: simplebench.simplebench_types.Values
    :ivar timer: The timer used for the measurement. (read only)
    :itype timer: str | None
    """

    __slots__ = (
        '_metric',
        '_data',
        '_timer',
        '_rounds',
        '_raw_data_block',
    )

    def __init__(self, *, metric: Metric, data: Values, rounds: int, timer: str | None) -> None:
        """Initialize the Raw object.

        :param metric: The metric definition for the benchmark.
        :type metric: Metric
        :param data: Values tuple of data points.
        :type data: Values
        :param rounds: The number of rounds each data point represents.
        :type rounds: int
        :param timer: The timer used for the measurement.
        :type timer: str | None
        :raises SimpleBenchTypeError: If any of the arguments are of the wrong type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._metric: Metric = _validate.metric(metric)
        self._rounds: int = _validate.rounds(rounds)
        self._timer: str | None = _validate.timer(timer)
        self._data: Values = _validate.data(data)

    @property
    def metric(self) -> Metric:
        """The metric of the benchmark."""
        return self._metric

    # This takes advantage of the fact that Values is immutable
    # to allow us to keep references to it without copying.
    # So this has nearly zero overhead for memory or performance.
    @property
    def data(self) -> Values:
        """The data points of the benchmark."""
        return self._data

    @property
    def name(self) -> str:
        """The name of the metric."""
        return self.metric.title

    @property
    def semantic_type(self) -> str:
        """The semantic type of the metric"""
        return self.metric.metric_type.semantic_type

    @property
    def description(self) -> str:
        """"The description of the metric"""
        return self.metric.metric_type.description

    @property
    def unit(self) -> str:
        """The unit of the data."""
        return self.metric.metric_type.unit

    @property
    def scale(self) -> float:
        """The scale of the data."""
        return self.metric.metric_type.scale

    @property
    def rounds(self) -> int:
        """The number of rounds each data point represents.

        Each iteration represents a single measurement, which may represent multiple rounds.
        Multiple rounds are often used to reduce the impact of noise or timer precision and
        accuracy on individual measurements.

        The number of rounds is used to adjust the standard deviation calculation to estimate
        the true standard deviation of the underlying population.

        The number of rounds is typically set to a value that balances the trade-off between
        the number of measurements and the time required to perform the measurements.
        """
        return self._rounds

    @property
    def timer(self) -> str | None:
        """The timer used for the measurement.

        :return: The timer name or None if not specified.
        :rtype: str | None
        """
        return self._timer

    @property
    def iterations(self) -> int:
        """The total number of iterations represented by the data points.

        Each iteration represents a single measurement, which may represent multiple rounds.
        """
        return len(self.data)

    def raw_data_block(self) -> reports.RawDataBlock:
        """Returns a ``RawDataBlock`` for the statistics.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        This does not include raw data points, only the statistical data.

        The returned RawDataBlock is cached for efficiency.

        :returns: A RawDataBlock object representing the statistics.
        :rtype: reports.RawDataBlock
        """
        if self._raw_data_block is None:
             self._raw_data_block = reports.RawDataBlock(
                name=self.name,
                semantic_type=self.semantic_type,
                description=self.description,
                unit=self.unit,
                scale=self.scale,
                rounds=self.rounds,
                timer=self.timer,
                data=self.data
            )
        return self._raw_data_block

    def __eq__(self, other: object) -> bool:
        """Compare two Raw objects for equality.

        Compares all core attributes of the Raw objects to determine if they are equal.

        :param object other: The other object to compare against.
        :return: True if the objects are considered equal, False otherwise.
        :raises SimpleBenchValueError: If either Raw object has a scale of zero.
        """
        if not isinstance(other, Raw):
            return NotImplemented

        # Fast paths for common cases
        if (self.timer != other.timer
                or self.name != other.name
                or self.metric != other.metric
                or self.description != other.description
                or self.iterations != other.iterations
                or self.rounds != other.rounds):
            return False
        if self.data is other.data:
            return True
        if len(self.data) != len(other.data):
            return False

        # Check that the data is the same
        return tuple(self.data) == tuple(other.data)


    def __repr__(self) -> str:
        """The string representation of the Raw object.

        .. warning::
            This representation is intended for debugging purposes only
            and may change without notice in future releases. Do not
            rely on this format for programmatic access.

            The data points are not included in the representation
            to avoid excessive output.

        :returns: The string representation of the Raw object.
        :rtype: str

        """
        return (f"{self.__class__.__name__}("
                f"metric='{self.metric}', "
                f"rounds={self.rounds}, "
                f"timer={self.timer!r}"
                f"data=...)")
