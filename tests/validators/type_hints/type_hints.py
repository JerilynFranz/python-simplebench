"""Tests for type hint validation functions."""
import sys
from pathlib import Path

import pytest

TEST_DIR = str(Path(__file__).parent.parent.parent.resolve())
sys.path.insert(0, TEST_DIR)

SRC_DIR = str(Path(__file__).parent.parent.parent.parent / 'src')
sys.path.insert(0, SRC_DIR)

from testspec import Assert, TestAction, TestGet, TestSpec, idspec

from simplebench.validators.type_hints.type_hints import (
    ImmutablePrimitiveTypes,
    ImmutablePrimitiveTypesTuple,
    TypedDictKeyInfo,
    is_immutable,
    is_instance_of_typehint,
)


@pytest.mark.parametrize('typespec', [
    idspec('IMMUTABLE_001', TestAction(
        name="Check immutable primitive types",
        action=is_immutable,
        args=[42, ImmutablePrimitiveTypes],
        assertion=Assert.EQUAL,
        expected=True)),
    idspec('IMMUTABLE_002', TestAction(
        name="Check mutable type (list)",
        action=is_immutable,
        args=[[1, 2, 3], list[int]],
        assertion=Assert.EQUAL,
        expected=False)),
])
def test_is_immutable(typespec: TestSpec) -> None:
    """Test is_immutable function."""
    typespec.run()

if __name__ == '__main__':
    pytest.main([__file__, "--log-cli-level=DEBUG"])
