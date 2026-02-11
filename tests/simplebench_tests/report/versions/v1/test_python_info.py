"""Tests for PythonInfo() report for SimpleBench tests."""
import pickle
from typing import TypeAlias

import pytest
from jsonschema import validate
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _PythonInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import CoreDataMapping, is_immutable
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

PythonInfo: TypeAlias = report.PythonInfo

@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.PythonInfo),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id is optional)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'hash_id'},
        assertion=Assert.ISINSTANCE,
        expected=report.PythonInfo),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_PythonInfoErrorTag.INVALID_HASH_ID_VALUE),
    PytestAction("INIT_005",
        name="Missing required field (python_version)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'python_version'},
        exception=TypeError),
    PytestAction("INIT_006",
        name="Invalid type for field (python_version as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(python_version=312),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_PYTHON_VERSION_TYPE),
    PytestAction("INIT_007",
        name="Invalid value for field (python_version as empty string)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(python_version=''),
        exception=SimpleBenchValueError,
        exception_tag=_PythonInfoErrorTag.EMPTY_PYTHON_VERSION_VALUE),
    PytestAction("INIT_008",
        name="Missing required field (implementation)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'implementation'},
        exception=TypeError),
    PytestAction("INIT_009",
        name="Invalid type for field (implementation as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(implementation=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_IMPLEMENTATION_TYPE),
    PytestAction("INIT_010",
        name="Invalid value for field (implementation as empty string)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(implementation=''),
        exception=SimpleBenchValueError,
        exception_tag=_PythonInfoErrorTag.EMPTY_IMPLEMENTATION_VALUE),
    PytestAction("INIT_011",
        name="Missing required field (implementation_version)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'implementation_version'},
        exception=TypeError),
    PytestAction("INIT_012",
        name="Invalid type for field (implementation_version as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(implementation_version=312),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_IMPLEMENTATION_VERSION_TYPE),
    PytestAction("INIT_014",
        name="Missing required field (compiler)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'compiler'},
        exception=TypeError),
    PytestAction("INIT_015",
        name="Invalid type for field (compiler as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(compiler=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_COMPILER_TYPE),
    PytestAction("INIT_017",
        name="Missing required field (revision)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'revision'},
        exception=TypeError),
    PytestAction("INIT_018",
        name="Invalid type for field (revision as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(revision=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_REVISION),
    PytestAction("INIT_019",
        name="Missing required field (buildno)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'buildno'},
        exception=TypeError),
    PytestAction("INIT_020",
        name="Invalid type for field (buildno as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(buildno=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_BUILDNO_TYPE),
    PytestAction("INIT_021",
        name="Missing required field (builddate)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'builddate'},
        exception=TypeError),
    PytestAction("INIT_022",
        name="Invalid type for field (builddate as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(builddate=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_BUILDDATE),
    PytestAction("INIT_023",
        name="Missing required field (command_line_flags)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'command_line_flags'},
        exception=TypeError),
    PytestAction("INIT_024",
        name="Invalid type for field (command_line_flags as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(command_line_flags=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_COMMAND_LINE_FLAGS),
    PytestAction("INIT_025",
        name="Missing required field (environment_variables)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'environment_variables'},
        exception=TypeError),
    PytestAction("INIT_026",
        name="Invalid type for field (environment_variables as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(environment_variables=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_ENVIRONMENT_VARIABLES_TYPE),
    PytestAction("INIT_027",
        name="Invalid key type for field (environment_variables with non-string keys)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(
            environment_variables={1: 'VALUE'}),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_ENVIRONMENT_VARIABLES_ITEM_TYPE),
    PytestAction("INIT_028",
        name="Invalid value type for field (environment_variables with non-string values)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(
            environment_variables={'KEY': 1}),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_ENVIRONMENT_VARIABLES_ITEM_TYPE),
    PytestAction("INIT_029",
        name="Missing required field (gc_is_enabled)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'gc_is_enabled'},
        exception=TypeError),
    PytestAction("INIT_030",
        name="Invalid type for field (gc_is_enabled as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(gc_is_enabled=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_GC_IS_ENABLED_TYPE),
    PytestAction("INIT_031",
        name="Missing required field (gc_thresholds)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'gc_thresholds'},
        exception=TypeError),
    PytestAction("INIT_032",
        name="Invalid type for field (gc_thresholds as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(gc_thresholds=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_GC_THRESHOLDS_TYPE),
    PytestAction("INIT_033",
        name="Invalid number of items for field (gc_thresholds with 2 items)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(gc_thresholds=[700, 10]),
        exception=SimpleBenchValueError,
        exception_tag=_PythonInfoErrorTag.INVALID_NUMBER_OF_GC_THRESHOLDS),
    PytestAction("INIT_034",
        name="Invalid number of items for field (gc_thresholds with 4 items)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(gc_thresholds=[700, 10, 10, 5]),
        exception=SimpleBenchValueError,
        exception_tag=_PythonInfoErrorTag.INVALID_NUMBER_OF_GC_THRESHOLDS),
    PytestAction("INIT_035",
        name="Invalid item type for field (gc_thresholds with non-int item)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(gc_thresholds=[700, 'not_an_int', 10]),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_GC_THRESHOLD_ITEM_TYPE),
    PytestAction("INIT_036",
        name="Missing required field (thread_switch_interval)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'thread_switch_interval'},
        exception=TypeError),
    PytestAction("INIT_037",
        name="Invalid type for field (thread_switch_interval as str)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(thread_switch_interval='not_a_float'),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_THREAD_SWITCH_INTERVAL_TYPE),
    PytestAction("INIT_038",
        name="Missing required field (architecture_bits)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'architecture_bits'},
        exception=TypeError),
    PytestAction("INIT_039",
        name="Invalid type for field (architecture_bits as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(architecture_bits=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_ARCHITECTURE_BITS),
    PytestAction("INIT_040",
        name="Missing required field (architecture_linkage)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs() - {'architecture_linkage'},
        exception=TypeError),
    PytestAction("INIT_041",
        name="Invalid type for field (architecture_linkage as int)",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs().replace(architecture_linkage=123),
        exception=SimpleBenchTypeError,
        exception_tag=_PythonInfoErrorTag.INVALID_ARCHITECTURE_LINKAGE),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.report_python_info_kwargs()['hash_id']),
    PytestAction("PROP_002",
        name="python_version property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='python_version',
        expected=report_factories.report_python_info_kwargs()['python_version']),
    PytestAction("PROP_003",
        name="implementation property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='implementation',
        expected=report_factories.report_python_info_kwargs()['implementation']),
    PytestAction("PROP_004",
        name="implementation_version property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='implementation_version',
        expected=report_factories.report_python_info_kwargs()['implementation_version']),
    PytestAction("PROP_005",
        name="compiler property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='compiler',
        expected=report_factories.report_python_info_kwargs()['compiler']),
    PytestAction("PROP_006",
        name="revision property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='revision',
        expected=report_factories.report_python_info_kwargs()['revision']),
    PytestAction("PROP_007",
        name="buildno property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='buildno',
        expected=report_factories.report_python_info_kwargs()['buildno']),
    PytestAction("PROP_008",
        name="builddate property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='builddate',
        expected=report_factories.report_python_info_kwargs()['builddate']),
    PytestAction("PROP_009",
        name="command_line_flags property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='command_line_flags',
        expected=report_factories.report_python_info_kwargs()['command_line_flags']),
    PytestAction("PROP_010",
        name="environment_variables property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='environment_variables',
        expected=CoreDataMapping(report_factories.report_python_info_kwargs()['environment_variables'])),
    PytestAction("PROP_011",
        name="gc_is_enabled property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='gc_is_enabled',
        expected=report_factories.report_python_info_kwargs()['gc_is_enabled']),
    PytestAction("PROP_012",
        name="gc_thresholds property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='gc_thresholds',
        expected=report_factories.report_python_info_kwargs()['gc_thresholds']),
    PytestAction("PROP_013",
        name="thread_switch_interval property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='thread_switch_interval',
        expected=report_factories.report_python_info_kwargs()['thread_switch_interval']),
    PytestAction("PROP_014",
        name="architecture_bits property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='architecture_bits',
        expected=report_factories.report_python_info_kwargs()['architecture_bits']),
    PytestAction("PROP_015",
        name="architecture_linkage property set correctly",
        action=report.PythonInfo,
        kwargs=report_factories.report_python_info_kwargs(),
        validate_attr='architecture_linkage',
        expected=report_factories.report_python_info_kwargs()['architecture_linkage']),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.PythonInfo.from_dict,
            args=[report_factories.report_python_info_data()],
            validate_attr="hash_id",
            expected=report_factories.report_python_info_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.PythonInfo.from_dict,
            args=[report_factories.no_hash_id_report_python_info_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.report_python_info_kwargs()["hash_id"]),
      ])
def test_hash_id(testspec: TestSpec) -> None:
   """Test PythonInfo hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='PythonInfo to_dict returns a report.PythonInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.report_python_info().to_dict(), report.PythonInfoDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='PythonInfo to_dict returns a report.ImmutablePythonInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.report_python_info().to_dict(), report.ImmutablePythonInfoDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test PythonInfo to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='PythonInfo equality comparison with identical hash_id values',
        action=lambda: report.PythonInfo(**report_factories.report_python_info_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.PythonInfo(**report_factories.report_python_info_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='PythonInfo equality comparison with different hash_id values',
        action=lambda: report.PythonInfo(**report_factories.report_python_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.PythonInfo(**report_factories.report_python_info_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_003',
        name=('PythonInfo equality comparison with different python_version values and '
            'calculated hash_id (hash_id not provided)'),
        action=lambda: report.PythonInfo(**report_factories.report_python_info_kwargs() - {'hash_id'}),
        assertion=Assert.NOT_EQUAL,
        expected=report.PythonInfo(
            **report_factories.report_python_info_kwargs().replace(python_version='3.11.0') - {'hash_id'})
    ),
    PytestAction('EQUALITY_004',
        name='PythonInfo equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.PythonInfo(**report_factories.report_python_info_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.PythonInfo(**report_factories.report_python_info_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='PythonInfo equality comparison with different types (not a PythonInfo instance)',
        action=lambda: report.PythonInfo(**report_factories.report_python_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a PythonInfo instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test PythonInfo equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test PythonInfo __repr__ method."""
    info = report_factories.report_python_info()
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
        name='PythonInfo instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.PythonInfo(**report_factories.report_python_info_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.PythonInfo(**report_factories.report_python_info_kwargs()))
    ),
    PytestAction('HASH_002',
        name='PythonInfo instances with different values have different hashes',
        action=hash,
        args=[report.PythonInfo(**report_factories.report_python_info_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.PythonInfo(
            **report_factories.report_python_info_kwargs().replace(python_version='3.10.1a')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test PythonInfo __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='PythonInfo instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.report_python_info())),
        assertion=Assert.EQUAL,
        expected=report_factories.report_python_info()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that PythonInfo instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='PythonInfo instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.report_python_info(), 'python_version', '3.10.0'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='PythonInfo instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.report_python_info()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that PythonInfo instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='PythonInfo JSON schema is valid and can validate to_dict() output',
        action=validate,
        kwargs={
            'instance': report_factories.report_python_info().to_dict().thaw(),  # type: ignore
            'schema': report.PythonInfo.SCHEMA.as_dict()
        }
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for PythonInfo is valid and can be
    used to validate a PythonInfo instance's to_dict() output."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
