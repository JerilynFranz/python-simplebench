"""Tests for StatsBlock() report for SimpleBench tests."""
import json
import pickle
from copy import copy, deepcopy
from typing import TypeAlias

import pytest
import simplejson
from jsonschema import validate
from testspec import Assert, PytestAction, TestSpec

from simplebench._log import _log
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _StatsBlockErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import (  # noqa: F401   # Used in type annotations and test assertions
    Values,
    is_immutable,
)
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

StatsBlock: TypeAlias = report.StatsBlock

@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.StatsBlock),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id and timer are optional)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs() - {'hash_id', 'timer'},  # Remove optional fields
        assertion=Assert.ISINSTANCE,
        expected=report.StatsBlock),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_HASH_ID_VALUE),
    PytestAction("INIT_005",
        name="Empty string for optional hash_id field",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(hash_id=''),
        assertion=Assert.ISINSTANCE,
        expected=report.StatsBlock),
    PytestAction("INIT_006",
        name="Missing required field (semantic_type)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs() - {'semantic_type'},
        exception=TypeError),
    PytestAction("INIT_007",
        name="Wrong type for field (semantic_type as int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(semantic_type=123),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_SEMANTIC_TYPE_TYPE),
    PytestAction("INIT_008",
        name="Invalid semantic_type value (not a valid namespaced identifier)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(semantic_type='invalid semantic type'),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_SEMANTIC_TYPE_VALUE),
    PytestAction("INIT_009",
        name="Wrong type for optional timer field (timer as int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(timer=123),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_TIMER_TYPE),
    PytestAction("INIT_011",
        name="Missing required field (unit)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs() - {'unit'},
        exception=TypeError),
    PytestAction("INIT_012",
        name="Wrong type for field (unit as int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(unit=123),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_UNIT_TYPE),
    PytestAction("INIT_013",
        name="Invalid unit value (empty string)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(unit=''),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_UNIT_VALUE),
    PytestAction("INIT_014",
        name="Missing required field (scale)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs() - {'scale'},
        exception=TypeError),
    PytestAction("INIT_015",
        name="Wrong type for field (scale as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(scale='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_SCALE_TYPE),
    PytestAction("INIT_016",
        name="Invalid scale value (negative float)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(scale=-1.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_SCALE_VALUE),
    PytestAction("INIT_017",
        name="Invalid scale value (zero)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(scale=0.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_SCALE_VALUE),
    PytestAction("INIT_018",
        name="Missing required field (name)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs() - {'name'},
        exception=TypeError),
    PytestAction("INIT_019",
        name="Wrong type for field (name as int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(name=123),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_NAME_TYPE),
    PytestAction("INIT_020",
        name="Invalid name value (empty string)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(name=''),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_NAME_VALUE),
    PytestAction("INIT_021",
        name="Wrong type for optional description field (description as int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(description=123),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_DESCRIPTION_TYPE),
    PytestAction("INIT_022",
        name="Missing required field (iterations)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs() - {'iterations'},
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE),
    PytestAction("INIT_023",
        name="Wrong type for field (iterations as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(iterations='not an int'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_ITERATIONS_TYPE),
    PytestAction("INIT_024",
        name="Invalid iterations value (zero)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(iterations=0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_ITERATIONS_VALUE),
    PytestAction("INIT_025",
        name="Invalid iterations value (negative int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(iterations=-1),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_ITERATIONS_VALUE),
    PytestAction("INIT_026",
        name="Missing required field (rounds)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs() - {'rounds'},
        exception=TypeError),
    PytestAction("INIT_027",
        name="Wrong type for field (rounds as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(rounds='not an int'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_ROUNDS_TYPE),
    PytestAction("INIT_028",
        name="Invalid rounds value (zero)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(rounds=0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_ROUNDS_VALUE),
    PytestAction("INIT_029",
        name="Invalid rounds value (negative int)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(rounds=-1),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_ROUNDS_VALUE),
    PytestAction("INIT_030",
        name="Wrong type for optional mean field (mean as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(mean='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_MEAN_TYPE),
    PytestAction("INIT_031",
        name="Wrong type for optional median field (median as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(median='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_MEDIAN_TYPE),
    PytestAction("INIT_032",
        name="Wrong type for optional minimum field (minimum as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(minimum='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_MINIMUM_TYPE),
    PytestAction("INIT_033",
        name="Wrong type for optional maximum field (maximum as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(maximum='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_MAXIMUM_TYPE),
    PytestAction("INIT_034",
        name="Wrong type for optional standard_deviation field (standard_deviation as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(stdev='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_TYPE),
    PytestAction("INIT_035",
        name="Invalid standard_deviation value (negative float)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(stdev=-1.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_VALUE),
    PytestAction("INIT_036",
        name=("Wrong type for optional relative_standard_deviation field "
              "(relative_standard_deviation as str)"),
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(relative_stdev='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_TYPE),
    PytestAction("INIT_037",
        name=("Invalid relative_standard_deviation value (negative float)"),
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(relative_stdev=-1.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_VALUE),
    PytestAction("INIT_038",
        name="Wrong type for optional percentiles field (percentiles as str)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(percentiles='not a list'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_PERCENTILES_TYPE),
    PytestAction("INIT_039",
        name="Invalid percentiles value (percentiles list not 101 items long)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(percentiles=[0.0, 50.0, 100.0]),  # Only 3 items instead of 101
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_PERCENTILES_LENGTH),
    PytestAction("INIT_040",
        name="Invalid percentiles value (percentiles list contains non-numeric value)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(
            percentiles=[float(i) for i in range(100)] + ['not a number']),  # Last item is invalid
        exception=SimpleBenchTypeError,
        exception_tag=_StatsBlockErrorTag.INVALID_PERCENTILES_TYPE),
    PytestAction("INIT_041",
        name="Invalid percentiles value (list is not sorted ascending)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs().replace(
            percentiles=list(reversed(report_factories.stats_block_data()['percentiles']))),  # Last item is invalid
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.INVALID_PERCENTILES_ORDER),
    PytestAction("INIT_042",
        name="Initialization with measurements instead of precomputed stats",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.StatsBlock),
    PytestAction("INIT_043",
        name="Initialization with measurements and missing optional hash_id (hash_id should be generated)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs() - {'hash_id'},
        assertion=Assert.ISINSTANCE,
        expected=report.StatsBlock),
    PytestAction("INIT_044",
        name="Initialization with measurements and median value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        #kwargs=report_factories.stats_block_kwargs(),
        kwargs=report_factories.stats_block_measurements_kwargs().replace(median=50.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.MEDIAN_AND_MEASUREMENTS_PROVIDED),
    PytestAction("INIT_045",
        name="Initialization with measurements and mean value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs().replace(mean=50.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.MEAN_AND_MEASUREMENTS_PROVIDED),
    PytestAction("INIT_046",
        name="Initialization with measurements and minimum value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs().replace(minimum=0.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.MINIMUM_AND_MEASUREMENTS_PROVIDED),
    PytestAction("INIT_047",
        name="Initialization with measurements and maximum value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs().replace(maximum=100.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.MAXIMUM_AND_MEASUREMENTS_PROVIDED),
    PytestAction("INIT_048",
        name="Initialization with measurements and stdev value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs().replace(stdev=10.0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.STDEV_AND_MEASUREMENTS_PROVIDED),
    PytestAction("INIT_049",
        name="Initialization with measurements and relative_stdev value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs().replace(relative_stdev=0.1),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.RELATIVE_STDEV_AND_MEASUREMENTS_PROVIDED),
    PytestAction("INIT_050",
        name="Initialization with measurements and percentiles value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs().replace(percentiles=[float(i) for i in range(101)]),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.PERCENTILES_AND_MEASUREMENTS_PROVIDED),
    PytestAction("INIT_051",
        name="Initialization with measurements and iterations value (should raise error due to conflicting data)",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs().replace(iterations=100),
        exception=SimpleBenchValueError,
        exception_tag=_StatsBlockErrorTag.ITERATIONS_AND_MEASUREMENTS_PROVIDED),
])
def test_init(testspec: TestSpec) -> None:
    _log.setLevel('DEBUG')
    testspec.run()
    _log.setLevel('INFO')



@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.stats_block_kwargs()['hash_id']),
    PytestAction("PROP_002",
        name="semantic_type property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='semantic_type',
        expected=report_factories.stats_block_kwargs()['semantic_type']),
    PytestAction("PROP_003",
        name="timer property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='timer',
        expected=report_factories.stats_block_kwargs()['timer']),
    PytestAction("PROP_004",
        name="unit property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='unit',
        expected=report_factories.stats_block_kwargs()['unit']),
    PytestAction("PROP_005",
        name="scale property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='scale',
        expected=report_factories.stats_block_kwargs()['scale']),
    PytestAction("PROP_006",
        name="iterations property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='iterations',
        expected=report_factories.stats_block_kwargs()['iterations']),
    PytestAction("PROP_007",
        name="rounds property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='rounds',
        expected=report_factories.stats_block_kwargs()['rounds']),
    PytestAction("PROP_008",
        name="mean property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='mean',
        expected=report_factories.stats_block_kwargs()['mean']),
    PytestAction("PROP_009",
        name="median property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='median',
        expected=report_factories.stats_block_kwargs()['median']),
    PytestAction("PROP_010",
        name="minimum property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='minimum',
        expected=report_factories.stats_block_kwargs()['minimum']),
    PytestAction("PROP_011",
        name="maximum property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='maximum',
        expected=report_factories.stats_block_kwargs()['maximum']),
    PytestAction("PROP_012",
        name="stdev property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='stdev',
        expected=report_factories.stats_block_kwargs()['stdev']),
    PytestAction("PROP_013",
        name="relative_stdev property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='relative_stdev',
        expected=report_factories.stats_block_kwargs()['relative_stdev']),
    PytestAction("PROP_014",
        name="percentiles property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_kwargs(),
        validate_attr='percentiles',
        expected=Values(report_factories.stats_block_kwargs()['percentiles'])),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("MEASUREMENTS_001",
        name="hash_id property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.stats_block_kwargs()['hash_id']),
    PytestAction("MEASUREMENTS_002",
        name="semantic_type property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='semantic_type',
        expected=report_factories.stats_block_kwargs()['semantic_type']),
    PytestAction("MEASUREMENTS_003",
        name="timer property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='timer',
        expected=report_factories.stats_block_kwargs()['timer']),
    PytestAction("MEASUREMENTS_004",
        name="unit property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='unit',
        expected=report_factories.stats_block_kwargs()['unit']),
    PytestAction("MEASUREMENTS_005",
        name="scale property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='scale',
        expected=report_factories.stats_block_kwargs()['scale']),
    PytestAction("MEASUREMENTS_006",
        name="iterations property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='iterations',
        expected=report_factories.stats_block_kwargs()['iterations']),
    PytestAction("MEASUREMENTS_007",
        name="rounds property set correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='rounds',
        expected=report_factories.stats_block_kwargs()['rounds']),
    PytestAction("MEASUREMENTS_008",
        name="mean property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='mean',
        expected=report_factories.stats_block_kwargs()['mean']),
    PytestAction("MEASUREMENTS_009",
        name="median property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='median',
        expected=report_factories.stats_block_kwargs()['median']),
    PytestAction("MEASUREMENTS_010",
        name="minimum property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='minimum',
        expected=report_factories.stats_block_kwargs()['minimum']),
    PytestAction("MEASUREMENTS_011",
        name="maximum property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='maximum',
        expected=report_factories.stats_block_kwargs()['maximum']),
    PytestAction("MEASUREMENTS_012",
        name="stdev property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='stdev',
        expected=report_factories.stats_block_kwargs()['stdev']),
    PytestAction("MEASUREMENTS_013",
        name="relative_stdev property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='relative_stdev',
        expected=report_factories.stats_block_kwargs()['relative_stdev']),
    PytestAction("MEASUREMENTS_014",
        name="percentiles property derived correctly",
        action=report.StatsBlock,
        kwargs=report_factories.stats_block_measurements_kwargs(),
        validate_attr='percentiles',
        expected=Values(report_factories.stats_block_kwargs()['percentiles'])),
])
def test_measurements(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.StatsBlock.from_dict,
            args=[report_factories.stats_block_data()],
            validate_attr="hash_id",
            expected=report_factories.stats_block_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.StatsBlock.from_dict,
            args=[report_factories.no_hash_id_stats_block_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.stats_block_kwargs()["hash_id"]),
])
def test_hash_id(testspec: TestSpec) -> None:
   """Test StatsBlock hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='StatsBlock to_dict returns a report.StatsBlockDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.stats_block().to_dict(), report.StatsBlockDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='StatsBlock to_dict returns a report.ImmutableStatsBlockDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.stats_block().to_dict(), report.ImmutableStatsBlockDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test StatsBlock to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='StatsBlock equality comparison with identical hash_id values',
        action=lambda: report.StatsBlock(**report_factories.stats_block_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.StatsBlock(**report_factories.stats_block_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='StatsBlock equality comparison with different hash_id values',
        action=lambda: report.StatsBlock(**report_factories.stats_block_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.StatsBlock(**report_factories.stats_block_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_003',
        name=('StatsBlock equality comparison with different timer value and '
            'calculated hash_id (hash_id not provided)'),
        action=lambda: report.StatsBlock(**report_factories.stats_block_kwargs() - {'hash_id'}),
        assertion=Assert.NOT_EQUAL,
        expected=report.StatsBlock(
            **report_factories.stats_block_kwargs().replace(timer='other') - {'hash_id'})
    ),
    PytestAction('EQUALITY_004',
        name='StatsBlock equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.StatsBlock(**report_factories.stats_block_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.StatsBlock(**report_factories.stats_block_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='StatsBlock equality comparison with different types (not a StatsBlock instance)',
        action=lambda: report.StatsBlock(**report_factories.stats_block_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a StatsBlock instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test StatsBlock equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test StatsBlock __repr__ method."""
    info = report_factories.stats_block()
    repr_str = repr(info)
    try:
        assert eval(repr_str) == info, (
            f"REPR_001 Evaluating __repr__ string did not produce the original object: {repr_str!r}")
    except Exception as e:
        raise AssertionError(
            f"REPR_001 Evaluating __repr__ string raised an exception: {e}\n"
            f"__repr__ string: {repr_str!r}"
        ) from e


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='StatsBlock instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.StatsBlock(**report_factories.stats_block_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.StatsBlock(**report_factories.stats_block_kwargs()))
    ),
    PytestAction('HASH_002',
        name='StatsBlock instances with different values have different hashes',
        action=hash,
        args=[report.StatsBlock(**report_factories.stats_block_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.StatsBlock(
            **report_factories.stats_block_kwargs().replace(timer='other')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test StatsBlock __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='StatsBlock instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.stats_block())),
        assertion=Assert.EQUAL,
        expected=report_factories.stats_block()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that StatsBlock instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='StatsBlock instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.stats_block(), 'timer', 'other'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='StatsBlock instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.stats_block()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that StatsBlock instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='StatsBlock JSON schema is valid and can validate to_dict() output',
        action=validate,
        kwargs={
            'instance': report_factories.stats_block().to_dict().thaw(),  # type: ignore
            'schema': report.StatsBlock.SCHEMA.as_dict()
        }
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for StatsBlock is valid and can be
    used to validate a StatsBlock instance's to_dict() output."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a StatsBlock instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.stats_block()],
        assertion=Assert.IS,
        expected=report_factories.stats_block()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a StatsBlock instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.stats_block()],
        assertion=Assert.IS,
        expected=report_factories.stats_block()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a StatsBlock instance returns the same instance (since it is immutable)."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of StatsBlock once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='StatsBlock can be serialized to JSON',
         action=report_factories.stats_block().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='StatsBlock can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.stats_block(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='StatsBlock.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.stats_block().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that StatsBlock can be serialized to JSON."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
