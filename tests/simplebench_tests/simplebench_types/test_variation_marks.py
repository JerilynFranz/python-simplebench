"""Test for simplebench.types.values module."""
import autopypath  # noqa: F401 # autopypath adjusts sys.path on import when run as script
import pytest
from testspec import PytestAction, TestSpec

from simplebench.exceptions import (
    SimpleBenchKeyError,
    SimpleBenchTypeError,
    SimpleBenchValueError,
)
from simplebench.simplebench_types import Mark, VariationMarks
from simplebench.simplebench_types._variations._variation_marks import _VariationMarksErrorTag


@pytest.mark.parametrize(
    'testspec', [
        PytestAction('INIT_001',
            name='Create empty VariationMarks instance',
            action=VariationMarks, args=[{}],
            expected=VariationMarks({})),
        PytestAction('INIT_002',
            name='Create VariationMarks instance with data',
            action=VariationMarks, args=[{'mark1': Mark('ten', 10), 'mark2': Mark('twenty', 20)}],
            validate_result=lambda result: (
                result['mark1'] == Mark('ten', 10) and result['mark2'] == Mark('twenty', 20))),
        PytestAction('INIT_003',
            name='Fail to create VariationMarks with non-mapping',
            action=VariationMarks, args=[['not', 'a', 'mapping']],
            exception=SimpleBenchTypeError,
            exception_tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE),
        PytestAction('INIT_004',
            name='Fail to create VariationMarks with non-string keys',
            action=VariationMarks, args=[{1: Mark('one', 1), 'two': Mark('two', 2)}],
            exception=SimpleBenchTypeError,
            exception_tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_TYPE),
        PytestAction('INIT_005',
            name='Fail to create VariationMarks with invalid identifier keys',
            action=VariationMarks, args=[{'valid_key': Mark('valid', 0), 'invalid-key': Mark('invalid', 1)}],
            exception=SimpleBenchValueError,
            exception_tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_VALUE),
        PytestAction('INIT_006',
            name='Fail to create VariationMarks with non-Mark values',
            action=VariationMarks, args=[{'mark1': 'not_a_mark', 'mark2': Mark('two', 2)}],
            exception=SimpleBenchTypeError,
            exception_tag=_VariationMarksErrorTag.VARIATION_MARKS_INVALID_ARG_VALUE_TYPE),
    ]
)
def test_init(testspec: TestSpec) -> None:
    """Test initializing VariationMarks instances.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize(
    'testspec', [
        PytestAction('GETITEM_001',
            name='Test __getitem__ method of VariationMarks',
            action=lambda: VariationMarks({
                'mark1': Mark('one', 1),
                'mark2': Mark('two', 2),
            })['mark1'],
            expected=Mark('one', 1)),
        PytestAction('GETITEM_002',
            name='Test __getitem__ with non-existent key',
            action=lambda: VariationMarks({
                'mark1': Mark('one', 1),
            })['non_existent_mark'],
            exception=SimpleBenchKeyError,
            exception_tag=_VariationMarksErrorTag.VARIATION_MARKS_KEY_ERROR),
    ]
)
def test_getitem(testspec: TestSpec) -> None:
    """Test the __getitem__ method of VariationMarks.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SETITEM_001',
        name='Test that __setitem__ raises an AttributeError',
        action=lambda: VariationMarks({'mark1': Mark('one', 1)}).__setitem__('mark2', Mark('two', 2)),
        exception=SimpleBenchTypeError,
        exception_tag=_VariationMarksErrorTag.VARIATION_MARKS_IMMUTABLE),
])
def test_setitem_error(testspec: TestSpec) -> None:
    """Test that __setitem__ raises an AttributeError."""
    testspec.run()


@pytest.mark.parametrize(
    'testspec', [
        PytestAction('CONTAINS_001',
            name='Test __contains__ method of VariationMarks',
            action=lambda: 'mark1' in VariationMarks({
                'mark1': Mark('one', 1),
                'mark2': Mark('two', 2),
            }),
            expected=True),
        PytestAction('CONTAINS_002',
            name='Test __contains__ with non-existent key',
            action=lambda: 'non_existent_mark' in VariationMarks({
                'mark1': Mark('one', 1),
            }),
            expected=False),
    ]
)
def test_contains(testspec: TestSpec) -> None:
    """Test the __contains__ method of VariationMarks.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('LEN_001',
        name='Test the __len__ method of VariationMarks',
        action=lambda: len(VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
            'mark3': Mark('three', 3),
        })),
        expected=3),
    PytestAction('LEN_002',
        name='Test the __len__ method of empty VariationMarks',
        action=lambda: len(VariationMarks({})),
        expected=0),
])
def test_len(testspec: TestSpec) -> None:
    """Test the __len__ method of VariationMarks.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('ITER_001',
        name='Test the __iter__ method of VariationMarks',
        action=lambda: list(iter(VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
        }))),
        expected=['mark1', 'mark2']),
])
def test_iter(testspec: TestSpec) -> None:
    """Test the __iter__ method of VariationMarks.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()

def test_repr() -> None:
    """Test the __repr__ method of VariationMarks.

    This test ensures that the string representation of a VariationMarks
    instance can be used to recreate an equivalent instance using eval().

    .. note:: Using eval() can be dangerous if the input is not trusted.
    :raises AssertionError: If the recreated VariationMarks does not match the original.
    """
    variation_marks = VariationMarks({
        'mark1': Mark('one', 1),
        'mark2': Mark('two', 2),
    })
    found_repr = repr(variation_marks)
    recreated_variation_marks = eval(found_repr)
    assert recreated_variation_marks == variation_marks, (
        'REPR_001 - Recreated VariationMarks from repr '
        f'does not match original. Found: {found_repr}')


@pytest.mark.parametrize('testspec', [
    PytestAction('EQ_001',
        name='Test the __eq__ method of VariationMarks for equality',
        action=lambda: VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
        }) == VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
        }),
        expected=True),
    PytestAction('EQ_002',
        name='Test the __eq__ method of VariationMarks for inequality',
        action=lambda: VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
        }) == VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('three', 3),
        }),
        expected=False),
    PytestAction('EQ_003',
        name='Test the __eq__ method of VariationMarks with different type',
        action=lambda: VariationMarks({
            'mark1': Mark('one', 1),
        }) == {'mark1': Mark('one', 1)},
        expected=False),
])
def test_eq(testspec: TestSpec) -> None:
    """Test the __eq__ method of VariationMarks.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='Test that hashes of equal VariationMarks are equal',
        action=lambda: hash(VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
        })) == hash(VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
        })),
        expected=True),
    PytestAction('HASH_002',
        name='Test that hashes of different VariationMarks are not equal',
        action=lambda: hash(VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('two', 2),
        })) != hash(VariationMarks({
            'mark1': Mark('one', 1),
            'mark2': Mark('three', 3),
        })),
        expected=True),
])
def test_hash(testspec: TestSpec) -> None:
    """Test the __hash__ method of VariationMarks.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()

if __name__ == '__main__':
    pytest.main([__file__])
