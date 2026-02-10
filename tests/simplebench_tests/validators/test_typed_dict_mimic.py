"""Validation tests for TypedDict mimic functions."""
# ruff: noqa: F401,UP007,UP045
from collections.abc import Mapping, Sequence, Set
from typing import Optional, TypedDict, Union

import pytest
from testspec import Assert, PytestAction, TestSpec

from simplebench._log import _log
from simplebench.simplebench_types import (
    CoreDataMapping,
    CoreDataSequence,
    CoreDataSet,
    Never,
    NotRequired,
    Required,
)
from simplebench.validators import is_typed_dict_mimic


class SimpleTypedDict(TypedDict):
    name: str
    value: int


class SimpleTypedDictWithNestedTypedDict(TypedDict):
    name: str
    value: int
    nested: SimpleTypedDict


class TypedDictWithCollectionTypes(TypedDict):
    name: str
    values_list: list[int]
    values_set: set[int]
    values_mapping: dict[str, int]


class TypedDictWithCoreSetType(TypedDict):
    name: str
    values_set: CoreDataSet[int]


class TypedDictWithCoreSequenceType(TypedDict):
    name: str
    values_list: CoreDataSequence[int]


class TypedDictWithCoreMappingType(TypedDict):
    name: str
    values_mapping: CoreDataMapping[int]


class TypedDictWithModernUnionType(TypedDict):
    name: str
    value: int | str


class TypedDictWithOldUnionType(TypedDict):
    name: str
    value: Union[int, str]


class TypedDictWithOptionalField(TypedDict):
    name: str
    value: int
    optional_field: Optional[str]


class TypedDictWithSequenceOfInt(TypedDict):
    name: str
    values: Sequence[int]


class TypedDictWithNestedTypedDict(TypedDict):
    name: str
    nested_typed_dict: TypedDictWithSequenceOfInt


class TypedDictWithRequiredAndDefaultNotRequiredFields(TypedDict, total=False):
    name: str  # optional by default due to total=False
    value: int  # optional by default due to total=False
    optional_field: NotRequired[str]
    required_field: Required[int]


class TypedDictWithRequiredAndDefaultRequiredFields(TypedDict, total=True):
    name: str  # required by default due to total=True
    value: int  # required by default due to total=True
    optional_field: NotRequired[str]
    required_field: Required[int]


class TypedDictWithNeverField(TypedDict):
    name: Required[str]
    value: Required[int]
    never_field: NotRequired[Never]


@pytest.mark.parametrize('testspec', [
    PytestAction('MIMIC_001',
        name='dict conforming to SimpleTypedDict is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'value': 42}, SimpleTypedDict],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_002',
        name='dict with wrong type primitive value is NOT recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 2, 'value': 42}, SimpleTypedDict],
        assertion=Assert.FALSE
    ),
    PytestAction('MIMIC_003',
        name='dict conforming to TypedDictWithNestedTypedDict is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic, args=[
            {'name': 'test',
             'value': 42,
             'nested': {
                 'name': 'nested',
                 'value': 99}},
            SimpleTypedDictWithNestedTypedDict],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_004',
        name='dict with CoreDataSequence',
        action=is_typed_dict_mimic, args=[
            {'name': 'test',
             'values_list': CoreDataSequence([1, 2, 3])},
            TypedDictWithCoreSequenceType],
        assertion=Assert.TRUE
    ),
     PytestAction('MIMIC_005',
        name='dict with CoreDataSet',
        action=is_typed_dict_mimic, args=[
            {'name': 'test',
             'values_set': CoreDataSet({4, 5, 6})},
            TypedDictWithCoreSetType],
        assertion=Assert.TRUE
    ),
     PytestAction('MIMIC_006',
        name='dict with CoreDataMapping',
        action=is_typed_dict_mimic, args=[
            {'name': 'test',
             'values_mapping': CoreDataMapping({'a': 7, 'b': 8, 'c': 9})},
            TypedDictWithCoreMappingType],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_007',
        name='dict with CoreDataSequence with wrong element type is NOT recognized as a TypedDict mimic',
        action=is_typed_dict_mimic, args=[
            {'name': 'test',
             'values_list': CoreDataSequence([1, 2, 'a'])},
            TypedDictWithCoreSequenceType],
        assertion=Assert.FALSE
    ),
    PytestAction('MIMIC_008',
        name='dict with modern union type is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'value': 42}, TypedDictWithModernUnionType],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_009',
        name='dict with old union type is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'value': 42}, TypedDictWithOldUnionType],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_010',
        name='dict with Optional field set to None is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'value': 42, 'optional_field': None}, TypedDictWithOptionalField],
        assertion=Assert.TRUE
    ),
     PytestAction('MIMIC_011',
        name='dict with Optional field set to value is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'value': 42, 'optional_field': 'optional'}, TypedDictWithOptionalField],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_012',
        name='dict with missing default not-required fields is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'required_field': 42}, TypedDictWithRequiredAndDefaultNotRequiredFields],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_013',
        name='dict with missing default required fields is NOT recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'optional_field': 'optional', 'required_field': 42},
              TypedDictWithRequiredAndDefaultRequiredFields],
        assertion=Assert.FALSE
    ),
    PytestAction('MIMIC_014',
        name='dict with Never field set is NOT recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'value': 42, 'never_field': 'impossible'}, TypedDictWithNeverField],
        assertion=Assert.FALSE
    ),
    PytestAction('MIMIC_015',
        name='dict with Never field missing is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'value': 42}, TypedDictWithNeverField],
        assertion=Assert.TRUE
    ),
    PytestAction('MIMIC_016',
        name='dict with Sequence of int is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[{'name': 'test', 'values': [1, 2, 3]},
              TypedDictWithSequenceOfInt],
        assertion=Assert.TRUE
    ),
     PytestAction('MIMIC_017',
        name='dict with nested TypedDict with Sequence of int is recognized as a TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[
            {
                'name': 'test',
                'nested_typed_dict': {
                    'name': 'nested',
                    'values': [4, 5, 6]
                }
            },
            TypedDictWithNestedTypedDict],
        assertion=Assert.TRUE
    ),
])
def test_typed_dict_mimic(testspec: TestSpec) -> None:
    """Test that a valid TypedDict mimic is recognized as such."""
    testspec.run()


if __name__ == "__main__":
    _log.setLevel('DEBUG')
    pytest.main([__file__])
