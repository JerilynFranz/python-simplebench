"""Iteration class"""
from .defaults import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from .doc_utils import format_docstring
from .enums import Section
from .exceptions import IterationErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from .validators import (
    validate_int,
    validate_non_blank_string,
    validate_non_negative_float,
    validate_positive_float,
    validate_positive_int,
)


@format_docstring(DEFAULT_INTERVAL_UNIT=DEFAULT_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE=DEFAULT_INTERVAL_SCALE)
class Iteration:
    """Container for the results of a single benchmark iteration.

    An iteration represents a single run of a benchmarked action (a run may consist of multiple rounds
    and a full benchmark consists of multiple iterations).

    It holds the elapsed time, n weight, unit, scale, memory usage, and peak memory usage for
    that iteration.

    Elapsed time is the total time taken for the iteration in the specified unit (e.g., nanoseconds)
    and scale (e.g., 1e-9 to convert nanoseconds to seconds) divided by the number of rounds
    as measured in the unit and scale specified. It is the average time per round for the iteration.

    So if an iteration with a unit of 'ns' and a scale of 1e-9 had an `elapsed` time of 5000000
    (5 million nanoseconds) and 20 rounds, then the elapsed time would be equivalent to
    an average of (5000000 * 1e-9) / 20 = 0.00025 seconds per round.

    The n-weight represents the O(n) type complexity of the action being benchmarked.
    For example, if the action processes a list of size n, then the n-weight would be n.

    This allows data analysis tools to better understand the performance characteristics of the action
    being benchmarked when the benchmark data is exported, although it is not used directly in
    any calculations by SimpleBench itself currently.

    :ivar n: The complexity n-weight for the iteration. (read only)
    :vartype n: int
    :ivar rounds: The number of rounds in the iteration. (read only)
    :vartype rounds: int
    :ivar unit: The unit of measurement for the elapsed time.
        It gets its default value from `simplebench.defaults.DEFAULT_INTERVAL_UNIT`. (read only)
    :vartype unit: str
    :ivar scale: The scale factor for the elapsed time.
        It gets its default value from `simplebench.defaults.DEFAULT_INTERVAL_SCALE`. (read only)
    :vartype scale: float
    :ivar elapsed: The elapsed time for the iteration. (read only)
    :vartype elapsed: float
    :ivar ops_per_second: The number of operations per second. (read only)
    :vartype ops_per_second: float
    :ivar per_round_elapsed: The mean time for a single round scaled to the base unit. (read only)
    :vartype per_round_elapsed: float
    :ivar memory: The memory usage in bytes. (defaults to 0) (read only)
    :vartype memory: int
    :ivar peak_memory: The peak memory usage in bytes. (read only)
    :vartype peak_memory: int
    """

    __slots__ = ('_n', '_rounds', '_elapsed', '_unit', '_scale', '_memory', '_peak_memory')

    @format_docstring(DEFAULT_INTERVAL_UNIT=DEFAULT_INTERVAL_UNIT, DEFAULT_INTERVAL_SCALE=DEFAULT_INTERVAL_SCALE)
    def __init__(self,
                 *,
                 n: int = 1,
                 rounds: int = 1,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 elapsed: float = 0.0,
                 memory: int = 0,  # in bytes
                 peak_memory: int = 0,  # in bytes
                 ) -> None:
        """Initialize an Iteration instance.

        :param n: The complexity n-weight for the iteration. Must be a positive integer.
        :type n: int
        :param rounds: The number of rounds in the iteration. Must be a positive integer.
        :type rounds: int
        :param unit: The unit of measurement for the elapsed time.
            It gets its default value from `simplebench.defaults.DEFAULT_INTERVAL_UNIT`.
        :type unit: str
        :param scale: The scale factor for the elapsed time.
            It gets its default value from `simplebench.defaults.DEFAULT_INTERVAL_SCALE`.
        :type scale: float
        :param elapsed: The elapsed time for the iteration. Must be a non-negative float.
        :type elapsed: float
        :param memory: The memory usage in bytes. Must be an integer.
        :type memory: int
        :param peak_memory: The peak memory usage in bytes. Must be an integer.
        :type peak_memory: int
        :raises SimpleBenchTypeError: If any of the arguments are of the wrong type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._n = validate_positive_int(
            n, 'n',
            IterationErrorTag.N_ARG_TYPE,
            IterationErrorTag.N_ARG_VALUE)
        self._rounds = validate_positive_int(
            rounds, 'rounds',
            IterationErrorTag.ROUNDS_ARG_TYPE,
            IterationErrorTag.ROUNDS_ARG_VALUE)
        self._unit = validate_non_blank_string(
            unit, 'unit',
            IterationErrorTag.UNIT_ARG_TYPE,
            IterationErrorTag.UNIT_ARG_VALUE)
        self._scale = validate_positive_float(
            scale, 'scale',
            IterationErrorTag.SCALE_ARG_TYPE,
            IterationErrorTag.SCALE_ARG_VALUE)
        self._elapsed = validate_non_negative_float(
            elapsed, 'elapsed',
            IterationErrorTag.ELAPSED_ARG_TYPE,
            IterationErrorTag.ELAPSED_ARG_VALUE)
        self._memory = validate_int(
            memory, 'memory',
            IterationErrorTag.MEMORY_ARG_TYPE)
        self._peak_memory = validate_int(
            peak_memory, 'peak_memory',
            IterationErrorTag.PEAK_MEMORY_ARG_TYPE)

    def __eq__(self, other: object) -> bool:
        """Check equality between two Iteration instances.

        Two Iteration instances are considered equal if all their attributes are equal.
        """
        if not isinstance(other, Iteration):
            return False
        return (self.n == other.n and
                self.elapsed == other.elapsed and
                self.unit == other.unit and
                self.scale == other.scale and
                self.memory == other.memory and
                self.peak_memory == other.peak_memory)

    @property
    def n(self) -> int:
        """The n weight of the iteration"""
        return self._n

    @property
    def rounds(self) -> int:
        """The number of rounds in the iteration"""
        return self._rounds

    @property
    def unit(self) -> str:
        """The unit of measurement for the elapsed time."""
        return self._unit

    @property
    def scale(self) -> float:
        """The scale factor for the elapsed time."""
        return self._scale

    @property
    def elapsed(self) -> float:
        """The total elapsed time for the iteration in the specified unit."""
        return self._elapsed

    @property
    def memory(self) -> int:
        """The memory usage in bytes. This is the difference between the allocated
        memory before and after the action.

        The edge case of no memory allocated results in a returned value of 0
        """
        return self._memory

    @property
    def peak_memory(self) -> int:
        """The peak memory usage in bytes.

        This is the maximum memory allocated during the action.
        """
        return self._peak_memory

    @property
    def per_round_elapsed(self) -> float:
        """The mean time for a single round scaled to the base unit.
        If elapsed is 0, returns 0.0

        The per round computation is the elapsed time divided by the number
        of rounds in the iteration.

        The scaling to the base unit is done using the scale factor.
        This has the effect of converting the elapsed time into the base unit.
        For example, if the scale factor is 1e-9 then elapsed time in nanoseconds
        will be converted to seconds.

        :return: The mean time for a single round scaled to the base unit.
        :rtype: float
        """
        return self._elapsed * self._scale / self._rounds

    @property
    def ops_per_second(self) -> float:
        """The number of operations per second.

        This is calculated as the inverse of the elapsed time.

        The edge cases of 0 elapsed time results in a returned value of 0.0
        This would otherwise be an impossible value and so flags a measurement error.
        """
        if self._elapsed == 0.0:
            return 0.0
        return self._rounds / (self._elapsed * self._scale)

    def iteration_section(self, section: Section) -> int | float:
        """Returns the requested section of the benchmark results.

        :param section: The section of the results to return. Must be Section.OPS or Section.TIMING.
        :type section: Section
        :return: The requested section of the benchmark results.
        :rtype: Stats
        """
        if not isinstance(section, Section):
            raise SimpleBenchTypeError(
                f'Invalid section type: {type(section)}. Must be of type Section.',
                tag=IterationErrorTag.ITERATION_SECTION_INVALID_SECTION_ARG_TYPE
            )
        match section:
            case Section.OPS:
                return self.ops_per_second
            case Section.TIMING:
                return self.per_round_elapsed
            case Section.MEMORY:
                return self.memory
            case Section.PEAK_MEMORY:
                return self.peak_memory
            case _:  # needed for mypy
                raise SimpleBenchValueError(
                    f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                    tag=IterationErrorTag.ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
                )

    def __repr__(self) -> str:
        """Return a string representation of the Iteration instance."""
        unit = self.unit.replace("'", "\\'")
        return (f"Iteration(n={self.n}, elapsed={self.elapsed}, unit='{unit}', "
                f"scale={self.scale}, rounds={self.rounds}, memory={self.memory}, "
                f"peak_memory={self.peak_memory})")
